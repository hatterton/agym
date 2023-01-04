from typing import List

from agym.renderers import TextLabel
from timeprofiler import Stat, TimeProfiler, profile


class ProfileUpdater:
    def __init__(self, label: TextLabel, profiler: TimeProfiler) -> None:
        self._label = label
        self._profiler = profiler

    @profile("prof_update", "game_update")
    def update(self) -> None:
        stats = self._profiler.get_stats()
        stats = sorted(stats, key=lambda x: x.title)
        stats = sorted(
            stats, key=lambda x: x.parent_title if x.parent_title else ""
        )
        self._label.text = self._format_stats(stats)

    def _format_stats(self, stats: List[Stat]) -> str:
        title_len = 14
        title_pattern = f"{{:{title_len}}}"

        lines = []
        for stat in stats:
            cated_title = stat.title[:title_len]
            title = f"l:{title_pattern}".format(cated_title)

            num = f"n:{stat.n_cycles:4}"
            total = f"t:{stat.total:6.3f}s"
            relative = f"r:{stat.relative:6.1%}"

            cated_parent_title = (
                stat.parent_title[:title_len] if stat.parent_title else "None"
            )
            parent_title = f"l:{title_pattern}".format(cated_parent_title)

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
