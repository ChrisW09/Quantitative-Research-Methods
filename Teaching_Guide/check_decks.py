"""Health check for the lecture decks: page counts and slides that overflow.

    python3 Teaching_Guide/check_decks.py      (or: make check)

Reads the .log files LaTeX already writes, so it costs nothing and needs no
extra packages. An "overfull vbox" means content ran past the bottom of a
slide — usually the projector shows it, but it is worth a look.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SLIDES = ROOT / "Lecture_Slides"

# Anything above this is worth fixing; below it the eye cannot see the overflow.
TOLERANCE_PT = 12.0


def main() -> None:
    rows = []
    for folder in sorted(SLIDES.glob("chapter_*")):
        log = folder / f"{folder.name}.log"
        pdf = folder / f"{folder.name}.pdf"
        if not log.exists():
            rows.append((folder.name, None, None, None, "not compiled"))
            continue
        text = log.read_text(errors="ignore")

        pages = None
        m = re.search(r"Output written on .*\((\d+) pages", text)
        if m:
            pages = int(m.group(1))

        # Match only the message itself. Looking the page up in a *separate*
        # search keeps finditer from consuming the following lines — an earlier
        # version captured 200 dotall characters here and silently swallowed
        # any overfull box reported inside that window.
        overfull = []
        for m in re.finditer(r"Overfull \\vbox \(([\d.]+)pt too high\)", text):
            page = re.search(r"\[(\d+)", text[m.end() : m.end() + 400])
            overfull.append((float(m.group(1)), page.group(1) if page else "?"))

        bad = [o for o in overfull if o[0] >= TOLERANCE_PT]
        note = "ok" if not bad else "review: p. " + ", ".join(p for _, p in sorted(bad, reverse=True)[:5])
        rows.append((folder.name, pages, len(overfull), max((o[0] for o in overfull), default=0.0), note))

    if not rows:
        print(f"no chapter_* folders under {SLIDES}")
        return

    width = max(len(r[0]) for r in rows)
    print(f"{'deck'.ljust(width)}  pages  overfull  worst    status")
    print("-" * (width + 36))
    total = 0
    for name, pages, n_over, worst, note in rows:
        total += pages or 0
        # worst is None for a deck that was never compiled — do not format it as a float.
        worst_col = f"{worst:5.1f}pt" if worst is not None else "     —  "
        print(
            f"{name.ljust(width)}  {str(pages or '—').rjust(5)}  "
            f"{str(n_over if n_over is not None else '—').rjust(8)}  "
            f"{worst_col}  {note}"
        )
    print("-" * (width + 36))
    print(f"{'total'.ljust(width)}  {str(total).rjust(5)}")
    print(f"\n(overfull boxes below {TOLERANCE_PT:.0f}pt are ignored — they are invisible in the room)")


if __name__ == "__main__":
    main()
