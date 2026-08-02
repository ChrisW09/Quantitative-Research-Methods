"""Generate Teaching_Guide/slide_index.md from the compiled decks.

For every deck this writes: the section structure with page ranges, a
proportional time budget for the session, and the page number of every
exercise, solution and "switch to the notebook" cue — the things you actually
need to find while standing in front of a room.

Run it after rebuilding any deck:

    python3 Teaching_Guide/make_index.py

Requires pypdf (`pip install -r Teaching_Guide/requirements.txt`). Everything
else comes from the .toc files LaTeX already writes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SLIDES = ROOT / "Chapters"
OUT = Path(__file__).parent / "slide_index.md"

try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - guidance, not logic
    sys.exit(
        "pypdf is needed to read the frame titles.\n"
        "    pip install -r Teaching_Guide/requirements.txt"
    )

# Deck -> (display name, how many 180-minute sessions it is taught over).
DECKS = {
    "chapter_00":  ("Precourse (a) — Statistics Refresher", 1),
    "chapter_00b": ("Precourse (b) — Toolkit", 1),
    "chapter_01":  ("Ch. 1 — Introduction", 0.5),
    "chapter_02":  ("Ch. 2 — Statistical Learning", 1.5),
    "chapter_03":  ("Ch. 3 — Linear Regression", 2),
    "chapter_04":  ("Ch. 4 — Classification", 2),
    "chapter_05":  ("Ch. 5 — Resampling Methods", 1),
    "chapter_06":  ("Ch. 6 — Model Selection & Regularisation", 1),
    "chapter_07":  ("Ch. 7 — Moving Beyond Linearity", 1),
    "chapter_08":  ("Ch. 8 — Tree-Based Methods", 1),
    "chapter_10":  ("Ch. 10 — Deep Learning", 1),
    "chapter_12":  ("Ch. 12 — Unsupervised Learning", 1),
}

SESSION_MINUTES = 180
# Minutes lost to arriving, settling, breaks and questions in a 180-min session.
OVERHEAD_MINUTES = 35


def sections_from_toc(toc: Path) -> list[tuple[str, int]]:
    """[(section title, first page), ...] in document order."""
    if not toc.exists():
        return []
    pat = re.compile(r"\\beamer@sectionintoc\s*\{\d+\}\{(.+?)\}\{(\d+)\}")
    out = []
    for m in pat.finditer(toc.read_text(errors="ignore")):
        title = re.sub(r"\\[a-zA-Z]+\s?|[{}$]", "", m.group(1)).strip()
        out.append((title, int(m.group(2))))
    return out


def frame_titles(pdf: Path) -> dict[int, str]:
    """{page number: frame title}. The title is the first line after the nav bar."""
    reader = PdfReader(str(pdf))
    titles = {}
    for i, page in enumerate(reader.pages, start=1):
        lines = [l.strip() for l in page.extract_text().split("\n") if l.strip()]
        titles[i] = lines[1] if len(lines) > 1 else ""
    return titles


def classify(title: str) -> str | None:
    t = title.lower()
    if t.startswith("extended exercise"):
        return "extended"
    if t.startswith("exercise"):
        return "short"
    if t.startswith("solution"):
        return "solution"
    return None


def deck_block(folder: str, name: str, sessions: float) -> list[str]:
    pdf = SLIDES / folder / f"{folder}.pdf"
    toc = SLIDES / folder / f"{folder}.toc"
    tex = SLIDES / folder / f"{folder}.tex"
    if not pdf.exists():
        return [f"### {name}\n", f"*Not compiled — run `pdflatex` in `Chapters/{folder}/`.*\n"]

    titles = frame_titles(pdf)
    total = len(titles)
    secs = sections_from_toc(toc)
    teaching_minutes = int(sessions * (SESSION_MINUTES - OVERHEAD_MINUTES))

    # The appendix holds optional material, so it is outside the time budget.
    appendix_start = next((p for ti, p in secs if ti.lower().startswith("appendix")), None)
    taught = appendix_start - 1 if appendix_start else total
    if taught <= 0:
        # A deck that opens with its appendix (or an empty PDF) has nothing to
        # budget; say so rather than dividing by zero.
        return [
            f"### {name}",
            "",
            f"`{folder}.pdf` — **{total} slides**, none of them in a main flow.",
            "",
        ]

    lines = [
        f"### {name}",
        "",
        f"`{folder}.pdf` — **{taught} slides** in the main flow"
        + (f" plus **{total - taught}** in the appendix" if appendix_start else "")
        + f", planned for **{sessions:g} × 180 min** "
        f"(≈ {teaching_minutes} min of actual teaching, "
        f"≈ {teaching_minutes / taught:.1f} min per slide).",
        "",
        "| Section | Pages | Slides | Time budget |",
        "|---|:--:|:--:|:--:|",
    ]

    # Minutes are apportioned cumulatively, so the rows add up to
    # teaching_minutes exactly. Rounding each row on its own drifts by a minute
    # or two against the session total quoted just above the table.
    spent = {"slides": 0, "minutes": 0}

    def budget(span: int) -> str:
        spent["slides"] += span
        upto = round(teaching_minutes * spent["slides"] / taught)
        minutes, spent["minutes"] = upto - spent["minutes"], upto
        return f"{minutes} min"

    bounds = [(t, p) for t, p in secs] + [("", total + 1)]
    front = secs[0][1] - 1 if secs else total
    if front > 0:
        lines.append(f"| *front matter* | 1–{front} | {front} | {budget(front)} |")
    for (title, start), (_, nxt) in zip(bounds, bounds[1:]):
        span = nxt - start
        cell = "optional" if appendix_start and start >= appendix_start else budget(span)
        lines.append(f"| {title} | {start}–{nxt - 1} | {span} | {cell} |")
    lines.append("")

    # Exercises, with their solutions folded in.
    ex_rows = []
    for page in sorted(titles):
        kind = classify(titles[page])
        if kind in ("short", "extended"):
            sol = next(
                (p for p in range(page + 1, min(page + 6, total + 1))
                 if classify(titles[p]) == "solution"),
                None,
            )
            tag = re.search(r"\[(Concept|Math|Python|Integrative)\]", titles[page])
            ex_rows.append(
                (titles[page].split("---")[0].split("—")[0].strip(),
                 "extended" if kind == "extended" else "short",
                 tag.group(1) if tag else "—",
                 page, sol or "—")
            )
    if ex_rows:
        lines += [
            "| Exercise | Type | Tag | Prompt | Solution |",
            "|---|:--:|:--:|:--:|:--:|",
        ]
        for label, kind, tag, page, sol in ex_rows:
            lines.append(f"| {label} | {kind} | {tag} | p. {page} | p. {sol} |")
        lines.append("")

    # Cue points: where the deck tells you to switch to the notebook.
    if tex.exists():
        body = tex.read_text(errors="ignore")
        n_lab = body.count("\\begin{labnote}")
        if n_lab:
            cues = [p for p, t in titles.items()
                    if "notebook" in t.lower() or "lab" in t.lower()]
            hint = f" (near pp. {', '.join(str(c) for c in cues[:4])})" if cues else ""
            lines.append(f"**Notebook cues:** {n_lab} in this deck{hint}.")
            lines.append("")

    return lines


def main() -> None:
    # The .toc files are LaTeX build artefacts: git-ignored, and deleted by
    # `make clean`. Without one, every section table collapses to a single
    # "front matter" row spanning the whole deck — so refuse to overwrite the
    # tracked index with a gutted version, and say what to run instead.
    stale = [
        f for f in DECKS
        if (SLIDES / f / f"{f}.pdf").exists() and not (SLIDES / f / f"{f}.toc").exists()
    ]
    if stale:
        sys.exit(
            "no .toc file for: " + ", ".join(stale) + "\n"
            "Section structure comes from the .toc files LaTeX writes, and they are\n"
            "not in git (a fresh clone has none, and `make clean` deletes them). A\n"
            "deck whose .pdf is already current will not recompile on its own, so\n"
            "force it:\n"
            "    make -B decks"
        )

    doc = [
        "# Slide index",
        "",
        "*Generated by `Teaching_Guide/make_index.py` — do not edit by hand.*",
        "",
        "Page numbers are the printed slide numbers in each deck's PDF. Time budgets "
        "are proportional to slide count after allowing "
        f"{OVERHEAD_MINUTES} min per session for arrival, breaks and questions; treat "
        "them as a starting point, not a rule.",
        "",
    ]
    for folder, (name, sessions) in DECKS.items():
        doc += deck_block(folder, name, sessions)
    OUT.write_text("\n".join(doc).rstrip() + "\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(doc)} lines)")


if __name__ == "__main__":
    main()
