"""Health check for the lecture decks: page counts and slides that overflow.

    python3 Teaching_Guide/check_decks.py      (or: make check)

Reads the .log files LaTeX already writes, so it costs nothing and needs no
extra packages. An "overfull vbox" means content ran past the bottom of a
slide — usually the projector shows it, but it is worth a look.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SLIDES = ROOT / "Chapters"

# Anything above this is worth fixing; below it the eye cannot see the overflow.
TOLERANCE_PT = 12.0


def main() -> int:
    rows = []
    for folder in sorted(SLIDES.glob("chapter_*")) + sorted((SLIDES / "Advanced").glob("advanced_*")):
        log = folder / f"{folder.name}.log"
        pdf = folder / f"{folder.name}.pdf"
        # A folder with no .tex holds no deck at all, so there is nothing that
        # could have failed to compile: say that rather than reporting a build
        # that was never meant to run. (Every chapter carries a deck today.)
        if not (folder / f"{folder.name}.tex").exists():
            rows.append((folder.name, None, None, None, "no deck (no .tex)"))
            continue
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

        # No "Output written on" means pdflatex never reached the end: the log is
        # from a failed compile. Reporting that as "ok" is how a deck that does not
        # build at all used to pass this check.
        if pages is None:
            rows.append((folder.name, None, len(overfull), None, "COMPILE FAILED (no 'Output written on')"))
            continue

        bad = [o for o in overfull if o[0] >= TOLERANCE_PT]
        note = "ok" if not bad else "review: p. " + ", ".join(p for _, p in sorted(bad, reverse=True)[:5])
        rows.append((folder.name, pages, len(overfull), max((o[0] for o in overfull), default=0.0), note))

    if not rows:
        print(f"no chapter_* folders under {SLIDES}")
        return 1

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

    # A deck that has never been compiled is not a failure: the .log files are
    # build artefacts and git-ignored, so a fresh clone legitimately has none.
    # A log that exists but records a failed compile, or a slide that overruns
    # its frame, is one — and the exit code has to say so, or `make check` is
    # green no matter what it just printed.
    uncompiled = [n for n, _, _, _, note in rows if note in ("not compiled", "no deck (no .tex)")]
    failed = [(n, note) for n, _, _, _, note in rows if note not in ("ok", "not compiled", "no deck (no .tex)")]
    if uncompiled:
        print(f"\n{len(uncompiled)} deck(s) not compiled yet — run `make decks advanced` to check them")
    if failed:
        print(f"\n{len(failed)} deck(s) need attention:")
        for name, note in failed:
            print(f"  {name}: {note}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
