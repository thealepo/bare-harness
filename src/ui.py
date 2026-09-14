import json
from contextlib import contextmanager

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.spinner import Spinner
from rich.text import Text


MIDNIGHT = "#07111f"
SURFACE = "#0d1b2a"
BLUE = "#19b5fe"
BRIGHT_BLUE = "#63d7ff"
RED = "#ff4d67"
TEXT = "#d7e9f7"
MUTED = "#66829c"

MAX_TOOL_OUTPUT_LINES = 14


class UI:
    def __init__(self):
        self.console = Console(highlight=False)
        self._usage_totals = {}

    def banner(self):
        """Render a compact, atmospheric session header."""
        title = Text.assemble(
            ("NIGHTWING", f"bold {BRIGHT_BLUE}"),
            ("  //  CODING SYSTEM", f"bold {TEXT}"),
        )
        subtitle = Text("minimal harness  ·  online", style=MUTED)
        self.console.print()
        self.console.print(
            Panel(
                Group(title, subtitle),
                border_style=BLUE,
                style=f"on {MIDNIGHT}",
                padding=(0, 2),
            )
        )
        self.console.print(
            Rule(
                Text(" enter a directive  ·  ctrl-d to exit ", style=MUTED),
                style=f"dim {MUTED}",
            )
        )

    def ask(self):
        try:
            return self.console.input(f"[{BLUE}]  > [/]").strip()
        except (EOFError, KeyboardInterrupt):
            self.console.print()
            return ""

    def user(self, text):
        self.console.print(
            Panel(
                Text(text.strip(), style=TEXT),
                title=Text("YOU", style=f"bold {BRIGHT_BLUE}"),
                title_align="left",
                border_style=BLUE,
                style=f"on {SURFACE}",
                padding=(0, 1),
            )
        )

    def agent(self, text):
        self.console.print(
            Panel(
                Markdown(text.strip()),
                title=Text("AGENT", style=f"bold {BRIGHT_BLUE}"),
                title_align="left",
                border_style=MUTED,
                style=f"on {MIDNIGHT}",
                padding=(0, 1),
            )
        )

    def tool(self, name, args, result):
        """Show a tool invocation and a concise result preview."""
        argument_text = self._format_args(args)
        lines = str(result).strip().splitlines() or ["(no output)"]
        shown = lines[:MAX_TOOL_OUTPUT_LINES]
        body = Text("\n".join(shown), style=TEXT)
        hidden = len(lines) - len(shown)
        if hidden:
            body.append(f"\n... {hidden} more lines", style=f"italic {MUTED}")

        header = Text.assemble(
            (name, f"bold {BLUE}"),
            ("  ", MUTED),
            (argument_text, MUTED),
        )
        self.console.print(
            Panel(
                Group(header, Rule(style=f"dim {MUTED}"), body),
                title=Text("TOOL", style=f"bold {RED}"),
                title_align="left",
                border_style=MUTED,
                style=f"on {MIDNIGHT}",
                padding=(0, 1),
            )
        )

    def usage(self, stats):
        """Render per-request token usage and retain session totals."""
        if not stats:
            return

        values = []
        for key, value in stats.items():
            if value is None:
                continue
            self._usage_totals[key] = self._usage_totals.get(key, 0) + value
            label = key.replace("_tokens", "").replace("_", " ")
            values.append(f"{label} {value:,}")

        if not values:
            return

        total = sum(self._usage_totals.values())
        self.console.print(
            Panel(
                Text.assemble(
                    ("this turn  ", f"bold {MUTED}"),
                    ("  ·  ".join(values), TEXT),
                    ("\nall turns  ", f"bold {MUTED}"),
                    (f"{total:,} tokens", f"bold {BRIGHT_BLUE}"),
                ),
                title=Text("USAGE", style=f"bold {BLUE}"),
                title_align="left",
                border_style=f"dim {MUTED}",
                style=f"on {MIDNIGHT}",
                padding=(0, 1),
            )
        )

    @contextmanager
    def working(self, label="processing"):
        """Keep long model calls visually quiet and intentional."""
        with self.console.status(
            Spinner("dots", text=Text(f"  {label}", style=MUTED)),
            spinner_style=BLUE,
        ):
            yield

    @staticmethod
    def _format_args(args):
        if not args:
            return ""
        if len(args) == 1:
            value = next(iter(args.values()))
            return str(value)
        return json.dumps(args, ensure_ascii=False)


ui = UI()
