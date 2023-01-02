import sys
import time
from collections import defaultdict
from contextlib import contextmanager
from copy import copy
from dataclasses import dataclass
from functools import wraps
from statistics import mean
from typing import Generator, List, Optional, Tuple

from custom_queue import Queue

Text = str
Time = float

EPS = 1e-4


@dataclass
class Event:
    text: Text
    time: Time


@dataclass
class Signup:
    start_event: str
    finish_event: str
    title: str
    parent_title: Optional[str] = None


@dataclass
class Stat:
    title: str
    n_cycles: int
    total: Time
    average: Time
    relative: float
    parent_title: Optional[str] = None
    parent_relative: Optional[float] = None


class TimeProfiler:
    def __init__(self, window_size: int = 10000, log_self: bool = True) -> None:
        self._window_size = window_size
        self._log_self: bool = log_self

        self._default_parent: Optional[str] = None

        self._events: Queue[Event]
        self._signups: List[Signup]

        self.reset()
        register_profiler(self)

    def set_default_parent(self, defaut_parent: Optional[str] = None) -> None:
        for signup in self._signups:
            if signup.parent_title == self._default_parent:
                signup.parent_title = defaut_parent

        self._default_parent = defaut_parent

    @contextmanager
    def profiling(self, start_event: str, finish_event: str):
        try:
            self.add_event(start_event)
            yield

        finally:
            self.add_event(finish_event)

    @contextmanager
    def _profiling(
        self, start_event: str, finish_event: str
    ) -> Generator[None, None, None]:
        try:
            if self._log_self:
                self._add_event(start_event)
            yield

        finally:
            if self._log_self:
                self._add_event(finish_event)

    def reset(self) -> None:
        self._events = Queue()
        self._signups = []

        if self._log_self:
            self.add_signup(
                Signup(
                    start_event="start_add_event",
                    finish_event="finish_add_event",
                    title="add_event",
                    parent_title=self._default_parent,
                )
            )
            self.add_signup(
                Signup(
                    start_event="start_get_stats",
                    finish_event="finish_get_stats",
                    title="get_stats",
                    parent_title=self._default_parent,
                )
            )

    def add_signup(self, signup: Signup) -> None:
        self._signups.append(signup)

    def add_event(self, text: str) -> None:
        with self._profiling("start_add_event", "finish_add_event"):
            self._add_event(text)

    def _add_event(self, text: str) -> None:
        event = Event(text=text, time=self._clock())
        self._events.push(event)

        if len(self._events) > self._window_size:
            self._events.pop()

    def get_stats(self) -> List[Stat]:
        with self._profiling("start_get_stats", "finish_get_stats"):
            stats = self._get_stats()

        return stats

    def _get_stats(self) -> List[Stat]:
        start_event2ids = defaultdict(list)
        finish_event2ids = defaultdict(list)
        for idx, signup in enumerate(self._signups):
            start_event2ids[signup.start_event].append(idx)
            finish_event2ids[signup.finish_event].append(idx)

        accumulated_durations: List[List[float]] = [
            [] for _ in range(len(self._signups))
        ]
        is_opened = [False for _ in range(len(self._signups))]
        opening_times = [0.0 for _ in range(len(self._signups))]

        for event in self._events:
            for idx in start_event2ids[event.text]:
                opening_times[idx] = event.time
                is_opened[idx] = True

            for idx in finish_event2ids[event.text]:
                if not is_opened[idx]:
                    continue

                duration = event.time - opening_times[idx]
                accumulated_durations[idx].append(duration)

                is_opened[idx] = False

        stats = [
            Stat(
                title=signup.title,
                n_cycles=0,
                total=EPS,
                average=EPS,
                relative=EPS,
                parent_title=signup.parent_title,
            )
            for signup in self._signups
        ]

        if len(self._events) < 2:
            return stats

        window_start_time, window_finish_time = self._get_current_timewindow()
        window_duration = window_finish_time - window_start_time

        for idx, opening_time in enumerate(opening_times):
            if is_opened[idx]:
                duration = window_finish_time - opening_times[idx]
                accumulated_durations[idx].append(duration)

        for idx, durations in enumerate(accumulated_durations):
            if len(durations) == 0:
                continue

            total = sum(durations)
            n_cycles = len(durations)
            avg = total / n_cycles
            relative = total / window_duration

            stat = stats[idx]
            stat.total = total
            stat.n_cycles = n_cycles
            stat.average = avg
            stat.relative = relative

        title2idx = {stat.title: idx for idx, stat in enumerate(stats)}
        for stat in stats:
            if stat.parent_title not in title2idx:
                continue

            parent_stat = stats[title2idx[stat.parent_title]]
            stat.parent_relative = stat.total / parent_stat.total

        return stats

    def _clock(self) -> Time:
        return time.time()

    def _get_current_timewindow(self) -> Tuple[Time, Time]:
        return (self._events.back.time, self._events.front.time)


class ProfilingManager:
    def __init__(self) -> None:
        self._signups: List[Signup] = []
        self._registered_profilers: List[TimeProfiler] = []

    def add_signup(self, signup: Signup) -> None:
        self._signups.append(copy(signup))

    def add_event(self, text: str) -> None:
        for profiler in self._registered_profilers:
            profiler.add_event(text)

    def register(self, profiler: TimeProfiler) -> None:
        for signup in self._signups:
            profiler.add_signup(signup)

        self._registered_profilers.append(profiler)


profiling_manager = ProfilingManager()


@contextmanager
def profiling(
    self,
    title: str,
    start_suffix: str = "_start",
    finish_suffix: str = "_finish",
) -> Generator[None, None, None]:

    start_event = title + start_suffix
    finish_event = title + finish_suffix

    try:
        profiling_manager.add_event(start_event)

        yield

    finally:
        profiling_manager.add_event(finish_event)


def profile(
    title: Optional[str] = None,
    parent_title: Optional[str] = None,
    start_suffix: str = "_start",
    finish_suffix: str = "_finish",
    signup_suffix: str = "",
):
    def decorator(func):
        if title is None:
            prefix = func.__name__
        else:
            prefix = title

        start_event = prefix + start_suffix
        finish_event = prefix + finish_suffix
        signup_title = prefix + signup_suffix

        signup = Signup(
            start_event=start_event,
            finish_event=finish_event,
            title=signup_title,
            parent_title=parent_title,
        )
        profiling_manager.add_signup(signup)

        @wraps(func)
        def derivated(*args, **kwargs):
            profiling_manager.add_event(start_event)
            result = func(*args, **kwargs)
            profiling_manager.add_event(finish_event)

            return result

        return derivated

    return decorator


def register_profiler(profiler) -> None:
    profiling_manager.register(profiler)


def format_stats(stats: List[Stat]) -> str:
    lines = []
    for stat in stats:
        msg = "l:{:20}| n:{:4}| t:{:6.3f}s| a:{:6.3f}s| r:{:5.1%}| pl:{:20}| pr:{:4.1%}".format(
            stat.title[:20],
            stat.n_cycles,
            stat.total,
            stat.average,
            stat.relative,
            stat.parent_title[:20] if stat.parent_title else "",
            stat.parent_relative if stat.parent_relative else 0.0,
        )
        lines.append(msg)

    text = "\n".join(lines)

    return text
