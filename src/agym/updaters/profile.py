from typing import List

from agym.utils import TimeProfiler, Stat, profile
from agym.gui import TextLabel


class ProfileUpdater:
    def __init__(self, label: TextLabel, profiler: TimeProfiler) -> None:
        self.label = label
        self.profiler = profiler

        # self.profiler.set_default_parent("game_iter")

    @profile("prof_update", "game_update")
    def update(self) -> None:
        stats = self.profiler.get_stats()
        stats = sorted(stats, key=lambda x: x.title)
        # stats = sorted(stats, key=lambda x: x.parent_relative if x.parent_relative else 0., reverse=True)
        stats = sorted(stats, key=lambda x: x.parent_title if x.parent_title else "")
        self.label.text = self._format_stats(stats)

    def _format_stats(self, stats: List[Stat]) -> str:
        title_len = 10

        lines = []
        for stat in stats:
            title = f"l:{stat.title[:10]:10}"
            num = f"n:{stat.n_cycles:4}"
            total = f"t:{stat.total:6.3f}s"
            relative = f"r:{stat.relative:6.1%}"
            parent_title = "pl:{:10}".format(
                stat.parent_title[:10] if stat.parent_title else "None"
            )
            parent_relative = "pr:{:6.1%}".format(
                stat.parent_relative if stat.parent_relative else 0
            )

            msg = "| ".join(
                [
                    title,
                    parent_title,
                    relative,
                    parent_relative,
                    total,
                    num,
                ]
            )
            lines.append(msg)

        text = "\n".join(lines)

        return text
