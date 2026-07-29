"""Check Teaching_Guide/runsheets/ against the compiled decks.

    python3 Teaching_Guide/check_runsheets.py             everything: failures,
                                                          heuristic warnings and
                                                          the page -> title
                                                          listing (make runsheets)
    python3 Teaching_Guide/check_runsheets.py --warnings   failures + warnings,
                                                          no page listing
    python3 Teaching_Guide/check_runsheets.py --quiet      failures only, plus one
                                                          summary line (make check)
    python3 Teaching_Guide/check_runsheets.py DIR          check a copy, for
                                                          testing the checker

A runsheet is a running order for one session, and every number in it is a page
number in that session's deck. Insert or delete a single frame and every later
number is silently wrong — the deck still compiles, `check_decks.py` still says
"ok", and the first person to notice is the lecturer standing in the room. This
script is the missing check. It verifies, per runsheet:

* the ``Slides`` column of the running order **partitions** the taught part of
  the deck: page 1 to the last page before the appendix, no gaps, no overlaps;
* the appendix range the file declares in prose is the deck's real appendix;
* the ``Min`` column adds up to the total the file states;
* every prose page reference (``p. 12``, ``pp. 12-17``, ``slide 68``,
  ``Slides 16-17``, ``Page 40``) points at a page that exists — and it prints
  each one as ``page -> frame title`` so a human can see whether it still means
  what it used to.

Hard failures (gap, overlap, minute mismatch, reference past the end of the
deck, appendix range that does not match the deck) exit 1.

Three further checks are heuristics and only ever warn, because all three
produce false positives. They are hidden at ``--quiet`` (which is what
``make check`` uses) and only counted, because 57 benign warnings on every run
train the reader to skip the output — and then the one real stale reference
scrolls past unread. ``make runsheets`` shows them in full.

* **gloss mismatch** — where the author wrote a parenthetical gloss right after
  a reference ("p. 58 (SD vs SE)"), that gloss is a claim about the page, so it
  is checked for a shared word against the frame title. See GLOSS_RE.
* **industry frame** — a reference landing on "Where this chapter is used in
  industry" or "Industry case in depth: …" from a note that never mentions
  industry. Those frames were inserted late, so their page numbers are the ones
  most likely to have absorbed a reference meant for whatever used to be there.
* **outside its own block** — a reference in a running-order note pointing at a
  page neither in that row's own Slides range nor in the appendix. Usually a
  deliberate forward or backward pointer; occasionally a number left behind.

Requires pypdf (`pip install -r Teaching_Guide/requirements.txt`) for the frame
titles, and the .toc files LaTeX writes for the appendix boundary — the same
inputs as make_index.py, whose helpers this reuses.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
RUNSHEETS = HERE / "runsheets"

# Run as a script, sys.path[0] is already Teaching_Guide/; be explicit anyway so
# that importing this module from elsewhere works too.
sys.path.insert(0, str(HERE))
from make_index import SLIDES, frame_titles, sections_from_toc  # noqa: E402

# ---------------------------------------------------------------- parsing rules

# The running order is the table under "## Running order"; the file also has an
# exercise table and a cut list with their own "Slides" column, and those are
# plans, not partitions — only this one has to tile the deck.
RUNNING_ORDER_HEADING = "## Running order"
RUNNING_ORDER_HEADER = "| Min | Slides | Block | What to do |"

# "*Total: 130 minutes of teaching — 15 minutes of slack, because ...*": the
# first number is the one the Min column has to reproduce.
TOTAL_RE = re.compile(r"\*Total:\s*(\d+)\s*minutes", re.I)

# "The deck ends with an appendix (pp. 72-77) that is **not** part of the timed
# plan above". Hyphen or en dash, "p." or "pp.". The wording is anchored on
# "ends with an appendix": the notes also say things like "3.L2, which now sits
# in the appendix (p. 147)", and matching that instead would move the boundary.
APPENDIX_RE = re.compile(
    r"ends with an appendix\s*\(pp?\.\s*(\d+)\s*[-–]\s*(\d+)\)", re.I
)

# The five reference forms the runsheets use. "p." and "pp." may be written
# without the space after the dot (lecture_03 does); \b keeps "app." out.
REF_RE = re.compile(
    r"\b(?:pp?\.\s*|(?:[Pp]ages?|[Ss]lides?)\s+)(\d+)(?:\s*[-–]\s*(\d+))?"
)
# "Slides 32-34 and 85-87", "pp. 69-71, 73-75": a second range hanging off the
# first. Only a *range* continues a reference — a bare "and 5" is far more often
# "and 5 minutes" than a second page.
CONT_RE = re.compile(r"\s*(?:,|and)\s*(\d+)\s*[-–]\s*(\d+)")

# A single slide spec in the Slides column: "40", "40-43", "27, 31", "28 and 34".
SPEC_RE = re.compile(r"(\d+)(?:\s*[-–]\s*(\d+))?")

# Frames added late in the deck's life, so the pages most likely to have
# absorbed a stale reference from whatever used to sit at that number.
INDUSTRY_RE = re.compile(r"used in industry|industry case in depth", re.I)

# A gloss: the parenthesis the author put straight after a reference to say what
# is on that page — "p. 58 (SD vs SE)", "p. 34 (the student paradox)". That is a
# claim about the page, so it can be checked against the frame title. Comparing
# the title against the *whole* sentence instead is useless: runsheet prose
# deliberately does not repeat slide titles, and the test then fires on roughly
# nine references in ten.
GLOSS_RE = re.compile(r"\s*\(([^()]{3,80})\)")

# Words too common to mean anything when matching a frame title against the
# gloss that cites it.
STOPWORDS = {
    "about", "after", "again", "against", "another", "back", "because", "been",
    "before", "being", "between", "both", "call", "called", "come", "does",
    "doing", "done", "down", "each", "else", "even", "every", "first", "from",
    "give", "gives", "goes", "have", "here", "into", "just", "keep", "less",
    "like", "long", "look", "made", "make", "makes", "many", "more", "most",
    "much", "must", "need", "next", "note", "once", "only", "onto", "other",
    "over", "part", "play", "point", "read", "real", "really", "right",
    "same", "says", "show", "shows", "side", "slide", "slides", "some", "stay",
    "still", "such", "take", "takes", "tell", "than", "that", "them", "then",
    "there", "these", "they", "thing", "things", "this", "those", "three",
    "through", "time", "true", "turn", "twice", "under", "used", "uses",
    "very", "want", "well", "were", "what", "when", "where", "which", "while",
    "will", "with", "without", "word", "work", "would", "your",
    # Words that appear in a gloss but say nothing about the topic of the page.
    "above", "alongside", "already", "appendix", "below", "board", "cell",
    "cells", "figure", "figures", "instead", "islp", "live", "minutes",
    "moment", "panel", "panels", "students", "verbatim",
}

# A gloss that only says where the answer is ("solution p. 18", "both in the
# appendix") makes no claim about the frame it hangs off, so it is not checked.
GLOSS_SKIP_RE = re.compile(r"^(?:solutions?|answers?|both|see|and)\b", re.I)
# Words are compared on their first few characters, so "regression" matches
# "regressions" and "spline" matches "splines" without a real stemmer.
STEM = 5


def words(text: str) -> set[str]:
    """Content-word stems of ``text``, for the gloss heuristic."""
    raw = re.findall(r"[A-Za-z][A-Za-z-]{3,}", text.lower())
    out = set()
    for w in raw:
        for piece in [w] + (w.split("-") if "-" in w else []):
            if len(piece) >= 4 and piece not in STOPWORDS:
                out.add(piece[:STEM])
    return out


def pages_in_spec(spec: str) -> list[int]:
    """Every page named by a Slides-column cell, in order, with repeats kept."""
    out: list[int] = []
    for m in SPEC_RE.finditer(spec):
        first = int(m.group(1))
        last = int(m.group(2)) if m.group(2) else first
        out.extend(range(first, last + 1) if last >= first else [first, last])
    return out


def cell_around(line: str, pos: int) -> str:
    """The table cell containing ``pos``, or the whole line if it is prose."""
    if not line.lstrip().startswith("|"):
        return line
    start = line.rfind("|", 0, pos) + 1
    end = line.find("|", pos)
    return line[start : end if end != -1 else len(line)]


# ------------------------------------------------------------------ the check


# How much to print. The three heuristics are benign until someone edits a deck,
# and 57 lines of benign warnings on every `make check` teach the reader to skip
# the output — which is exactly how the next real stale reference gets missed.
# So `make check` runs at QUIET and says only how many warnings it suppressed.
QUIET, WARNINGS, FULL = 0, 1, 2


class Report:
    """Collects lines to print, and whether anything hard went wrong.

    Four kinds of line, because they do not deserve the same volume:

    ``fail``  a wrong number. Always printed, and sets the exit status.
    ``note``  something about the *inputs* that limits what the run could check
              — a deck not recompiled since its .tex changed, a missing .toc, a
              runsheet with no total line. Always printed: "0 failures" measured
              against last week's PDF would be a trap. Rare by construction.
    ``warn``  one of the three heuristics. Counted always, printed from
              WARNINGS up.
    ``info``  the page -> frame title listing. FULL only.
    """

    def __init__(self, level: int) -> None:
        self.level = level
        self.lines: list[str] = []
        self.failures = 0
        self.warnings = 0
        self.notes = 0

    def head(self, text: str) -> None:
        self.lines.append(text)

    def info(self, text: str) -> None:
        if self.level >= FULL:
            self.lines.append(f"    {text}")

    def fail(self, text: str) -> None:
        self.failures += 1
        self.lines.append(f"  FAIL  {text}")

    def note(self, text: str) -> None:
        self.notes += 1
        self.lines.append(f"  note  {text}")

    def warn(self, text: str) -> None:
        self.warnings += 1
        if self.level >= WARNINGS:
            self.lines.append(f"  warn  {text}")


def running_order(text: str) -> list[tuple[int, int, str, str]]:
    """[(line number, minutes, slide spec, note), ...] from the running order."""
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == RUNNING_ORDER_HEADING)
    except StopIteration:
        return []
    rows = []
    seen_header = False
    for n, line in enumerate(lines[start:], start=start + 1):
        stripped = line.strip()
        if not seen_header:
            seen_header = stripped == RUNNING_ORDER_HEADER
            continue
        if not stripped.startswith("|"):
            if stripped.startswith("#") or (rows and not stripped):
                break  # end of the table
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 4 or not cells[0].lstrip("-").isdigit():
            continue  # the |--:|:--:| separator row
        rows.append((n, int(cells[0]), cells[1], cells[3]))
    return rows


class Ref:
    """One prose page reference, with everything needed to judge it."""

    __slots__ = ("line", "first", "last", "raw", "note", "gloss")

    def __init__(self, line: int, first: int, last: int, raw: str, note: str, gloss: str):
        self.line, self.first, self.last = line, first, last
        self.raw, self.note, self.gloss = raw, note, gloss

    @property
    def pages(self) -> range:
        return range(self.first, self.last + 1)


def references(text: str) -> list[Ref]:
    out = []
    for n, line in enumerate(text.splitlines(), start=1):
        for m in REF_RE.finditer(line):
            first = int(m.group(1))
            last = int(m.group(2)) if m.group(2) else first
            end = m.end()
            spans = [(first, last, m.group(0), end)]
            while True:  # "Slides 32-34 and 85-87"
                cont = CONT_RE.match(line, end)
                if not cont:
                    break
                end = cont.end()
                spans.append(
                    (int(cont.group(1)), int(cont.group(2)), cont.group(0).strip(), end)
                )
            note = cell_around(line, m.start())
            for a, b, raw, stop in spans:
                gloss = GLOSS_RE.match(line, stop)
                out.append(Ref(n, a, b, raw, note, gloss.group(1) if gloss else ""))
    return out


def check_runsheet(path: Path, rep: Report) -> None:
    text = path.read_text(errors="ignore")

    # The deck the file names in its own header, so a copied-and-renamed
    # runsheet pointing at the wrong deck is caught rather than assumed away.
    m = re.search(r"Lecture_Slides/(chapter_[\w]+)/", text)
    folder = m.group(1) if m else f"chapter_{path.stem.split('_', 1)[1]}"
    pdf = SLIDES / folder / f"{folder}.pdf"
    toc = SLIDES / folder / f"{folder}.toc"

    tex = SLIDES / folder / f"{folder}.tex"

    if not pdf.exists():
        rep.head(f"{path.name}  ->  {folder}")
        rep.fail(f"{folder}.pdf not compiled — run `make decks`")
        return

    try:
        titles = frame_titles(pdf)
    except Exception as exc:  # a half-written PDF: pdflatex is running right now
        rep.head(f"{path.name}  ->  {folder}")
        rep.fail(f"{folder}.pdf could not be read ({exc}) — is a build in progress?")
        return
    total = len(titles)
    # The .toc is a LaTeX by-product: git-ignored, and deleted by `make clean`.
    # Without one the deck's own appendix boundary is unknown, so the check
    # trusts the runsheet's declaration rather than inventing a failure.
    secs = sections_from_toc(toc)
    toc_appendix = next((p for t, p in secs if t.lower().startswith("appendix")), None)

    # --- the appendix boundary ------------------------------------------------
    declared = APPENDIX_RE.search(text)
    if declared:
        lo, hi = int(declared.group(1)), int(declared.group(2))
    else:
        lo, hi = (toc_appendix, total) if toc_appendix else (total + 1, total)

    rep.head(
        f"{path.name}  ->  {folder}.pdf, {total} pages, "
        + (f"appendix {lo}-{hi}" if lo <= total else "no appendix")
    )
    # Everything below is measured against the compiled PDF, so an edited but
    # unrecompiled deck means the numbers being checked are last week's.
    if tex.exists() and tex.stat().st_mtime > pdf.stat().st_mtime:
        rep.note(f"{folder}.tex is newer than {folder}.pdf — run `make decks` first")

    if not declared:
        rep.note(
            "no 'ends with an appendix (pp. X-Y)' sentence; "
            + (f"using the deck's own appendix at p. {toc_appendix}" if toc_appendix
               else "treating the whole deck as taught")
        )
    elif not secs:
        rep.note(f"no {folder}.toc, so the declared appendix pp. {lo}-{hi} is taken on trust "
                 f"(run `make -B decks` to check it)")
    else:
        if toc_appendix is None:
            rep.fail(f"declares an appendix at pp. {lo}-{hi} but the deck has no appendix section")
        elif lo != toc_appendix:
            rep.fail(f"appendix starts on p. {toc_appendix} in the deck, not p. {lo}")
        if hi != total:
            rep.fail(f"appendix declared to end on p. {hi}, but the deck has {total} pages")

    taught_end = min(lo, toc_appendix or lo) - 1

    # --- the running order partitions the taught pages ------------------------
    rows = running_order(text)
    if not rows:
        rep.fail("no running-order table found")
        return

    covered: dict[int, list[int]] = {}
    for line_no, _minutes, spec, _note in rows:
        for page in pages_in_spec(spec):
            covered.setdefault(page, []).append(line_no)

    gaps = [p for p in range(1, taught_end + 1) if p not in covered]
    overlaps = {p: ls for p, ls in covered.items() if len(ls) > 1}
    strays = sorted(p for p in covered if p > taught_end)

    if gaps:
        rep.fail(f"running order has gaps: {ranges(gaps)} in 1-{taught_end} covered by no row")
    if overlaps:
        detail = ", ".join(
            f"p. {p} (lines {', '.join(str(l) for l in ls)})"
            for p, ls in sorted(overlaps.items())[:6]
        )
        rep.fail(f"running order overlaps: {detail}")
    if strays:
        past = [p for p in strays if p > total]
        rep.fail(
            f"running order covers {ranges(strays)}, past the taught range 1-{taught_end}"
            + (f" (and past the end of the deck: {ranges(past)})" if past else "")
        )
    if not (gaps or overlaps or strays):
        rep.info(f"running order: {len(rows)} rows tile pp. 1-{taught_end} exactly")

    # --- the minutes add up ---------------------------------------------------
    minutes = sum(r[1] for r in rows)
    stated = TOTAL_RE.search(text)
    if not stated:
        rep.note("no '*Total: N minutes*' line to check the Min column against")
    elif int(stated.group(1)) != minutes:
        rep.fail(f"Min column sums to {minutes}, but the file states {stated.group(1)} minutes")
    else:
        rep.info(f"minutes: {len(rows)} rows sum to {minutes}, as stated")

    # --- every prose reference resolves to a real, plausible frame ------------
    # Which running-order row each line belongs to, for the locality warning.
    row_pages = {line_no: set(pages_in_spec(spec)) for line_no, _m, spec, _n in rows}

    refs = references(text)
    lines = text.splitlines()
    out_of_range = industry = mismatch = adrift = 0
    listing: list[str] = []
    for ref in refs:
        if ref.last > total:
            rep.fail(f"line {ref.line}: '{ref.raw}' is past the end of the deck ({total} pages)")
            out_of_range += 1
            continue

        own_row = row_pages.get(ref.line)
        if own_row and not (set(ref.pages) & own_row) and ref.first < lo:
            rep.warn(
                f"line {ref.line}: '{ref.raw}' points outside its own block "
                f"({ranges(sorted(own_row))}) and outside the appendix — deliberate "
                f"cross-reference, or a number left behind?"
            )
            adrift += 1

        for page in ref.pages:
            title = titles.get(page, "")
            listing.append(f"p. {page:>3} -> {title}")
            # The whole line, not just the cell: the Block column of the
            # running order is where "Where this chapter is used in industry"
            # is named, and a reference from that row is obviously intentional.
            context = lines[ref.line - 1]
            if INDUSTRY_RE.search(title) and not re.search(r"industry|business|case", context, re.I):
                rep.warn(
                    f"line {ref.line}: '{ref.raw}' lands on the industry frame "
                    f"p. {page} “{title}”, in a note that never mentions industry: "
                    f"{snippet(ref.note)}"
                )
                industry += 1
            elif ref.gloss and gloss_mismatch(title, ref.gloss):
                rep.warn(
                    f"line {ref.line}: '{ref.raw} ({ref.gloss})' -> p. {page} “{title}” "
                    f"— gloss and frame title share no word"
                )
                mismatch += 1

    rep.info(
        f"references: {len(refs)} found, {out_of_range} out of range, "
        f"{industry} on industry frames, {mismatch} gloss mismatch, "
        f"{adrift} outside their own block"
    )
    for entry in listing:
        rep.info(f"  {entry}")


def gloss_mismatch(title: str, gloss: str) -> bool:
    """True if the author's parenthetical gloss shares no word with the frame title."""
    if GLOSS_SKIP_RE.match(gloss.strip()):
        return False
    t, g = words(title), words(gloss)
    return bool(t and g and not (t & g))


def snippet(note: str, width: int = 70) -> str:
    flat = " ".join(note.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def ranges(pages: list[int]) -> str:
    """[1,2,3,7] -> '1-3, 7'."""
    out = []
    for page in sorted(pages):
        if out and page == out[-1][1] + 1:
            out[-1][1] = page
        else:
            out.append([page, page])
    return ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in out)


def main(argv: list[str]) -> int:
    if "--quiet" in argv or "-q" in argv:
        level = QUIET
    elif "--warnings" in argv or "-w" in argv:
        level = WARNINGS
    else:
        level = FULL
    # An explicit directory is only for testing the checker itself against a
    # deliberately broken copy; the default is the real runsheets.
    rest = [a for a in argv if not a.startswith("-")]
    where = Path(rest[0]) if rest else RUNSHEETS

    if not where.is_dir():
        print(f"{where}/ not present (git-ignored) — nothing to check")
        return 0

    files = sorted(where.glob("lecture_*.md"))
    if not files:
        print(f"no lecture_*.md under {where}/")
        return 0

    rep = Report(level)
    for path in files:
        before = len(rep.lines)
        check_runsheet(path, rep)
        if len(rep.lines) == before + 1:
            rep.lines.pop()  # only the header: nothing to say about this file

    if rep.lines:
        print("\n".join(rep.lines))
        print()
    tail = (
        f" ({rep.warnings} heuristic warnings, run `make runsheets` to see them)"
        if rep.warnings and level == QUIET
        else f", {rep.warnings} heuristic warning(s)" if rep.warnings else ""
    )
    print(f"{len(files)} runsheets: {rep.failures} failure(s)" + tail)
    if rep.warnings and level >= WARNINGS:
        print(
            "Warnings are heuristics and do produce false positives: a gloss often\n"
            "describes a page in words its title does not use, and a note may point\n"
            "somewhere else on purpose. They do not fail the build."
        )
    return 1 if rep.failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
