"""Execute the lab notebooks and compare their output against what is stored.

    python3 .github/scripts/check_notebooks.py                 all 15 notebooks
    python3 .github/scripts/check_notebooks.py Chapters/chapter_03/chapter_03_lab.ipynb
    python3 .github/scripts/check_notebooks.py --no-compare    run only

Two different failures are reported, and either one exits 1:

* **error** — a cell raised. This is what a normal test run catches.
* **drift** — a cell ran fine but printed something other than what is stored
  in the notebook. Three silent numeric drifts were found by hand in one week;
  no exception was raised for any of them.

Only *text* output is compared: ``stream`` text and the ``text/plain`` part of
``execute_result``/``display_data``. Figures are ignored, because a PNG never
reproduces byte for byte across platforms and comparing them would make the
check useless. Three cosmetic diffs are normalised away and nothing else:
``statsmodels`` stamps ``Date:`` and ``Time:`` into every summary table, and
``lifelines`` stamps ``time fit was run``. See NORMALISERS.

Nothing is ever written back: the notebooks are executed on a copy in memory.

Requires nbclient and nbformat plus the course's own dependencies
(`pip install -r requirements.txt`), and a working `python3` kernel.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOKS = ROOT / "Chapters"
ADVANCED = ROOT / "Advanced"
PROJECTS = ROOT / "Projects"

try:
    import nbformat
    from nbclient import NotebookClient
except ImportError:  # pragma: no cover - guidance, not logic
    sys.exit(
        "nbclient and nbformat are needed to execute the notebooks.\n"
        "    pip install nbclient nbformat"
    )

# Every systematic difference in this course's output that says nothing about
# whether the numbers are right. Each pattern here is a place where real drift
# could hide, so each one is deliberately narrow, and each is proved
# load-bearing before it is added: clear NORMALISERS, and the cell it exists for
# must start failing.
NORMALISERS: list[tuple[re.Pattern[str], str]] = [
    # --- environment, not answers --------------------------------------------
    # The setup cell prints this exactly when the ISLP package is absent and the
    # bundled CSVs carry the notebook instead. Locally-refreshed outputs have
    # the line, the CI runners (which install ISLP) do not — same data either
    # way, so the line says nothing about the numbers.
    (re.compile(r"^ISLP not installed; using CSV / URL fallbacks\.\n?", re.M), ""),
    # advanced_02: the exact-Shapley cell reports its own wall time so students
    # see the 2^p cost on a real clock. Milliseconds differ per machine.
    (re.compile(r"wall time for one instance: \d+\.\d+s"),
     "wall time for one instance: <TIME>s"),
    # --- timestamps a library stamps into an otherwise deterministic table ---
    # statsmodels summary(): "Date:                Wed, 29 Jul 2026   Prob (F-...
    (re.compile(r"Date:\s+\w{3}, \d{2} \w{3} \d{4}"), "Date: <DATE>"),
    # statsmodels summary(): "Time:                        17:12:34   Log-Like...
    (re.compile(r"Time:\s+\d{2}:\d{2}:\d{2}"), "Time: <TIME>"),
    # lifelines fitter summaries: "  time fit was run = 2026-07-29 12:34:56 UTC"
    (re.compile(r"(time fit was run\s*=\s*).*"), r"\1<TIME>"),
    # --- where a warning came from -------------------------------------------
    # The setup cells silence only the spurious ".*encountered in matmul"
    # RuntimeWarnings, on purpose: chapter 7's prose tells students that pyGAM
    # prints a caveat, so genuine warnings are part of the teaching material and
    # must stay visible. Python prints them as
    #
    #     <file>:<lineno>: <Category>: <message>
    #       <the source line>
    #
    # and only the <file>:<lineno> part is environment-dependent. The category,
    # the message and the source line are all left alone — a changed message is
    # exactly the drift this check exists to catch.
    #
    # A warning raised inside the executing cell. The kernel writes each cell to
    # a scratch file whose directory carries the kernel's pid and whose name is
    # a fresh id per execution: /var/folders/.../T/ipykernel_65077/2384627512.py
    # on macOS, /tmp/ipykernel_1234/5678.py on a runner. The line number is kept
    # — it is the line *within the cell*, so it only moves if the cell's own
    # source moved, which is real drift.
    (re.compile(r"\S*/ipykernel_\d+/\d+\.py:(\d+):"), r"<cell>:\1:"),
    # A warning raised inside an installed package. The prefix up to
    # site-packages/ is pure machine layout ("/Users/x/Library/Python/3.9/lib/
    # python" here, "/opt/hostedtoolcache/Python/3.11.x/x64/lib/python3.11" on a
    # runner). The line number goes too: it moves on any patch release of the
    # package and carries no information the module path does not already give.
    # What survives is which module warned — sklearn/utils/validation.py.
    (re.compile(r"\S*/(?:site|dist)-packages/(\S+?\.pyx?):\d+:"), r"<site-packages>/\1:<line>:"),
]

# Cell execution is capped so a hung kernel fails the job instead of burning the
# runner's 6 hours. The whole suite takes about a minute.
CELL_TIMEOUT_S = 300


def normalise(text: str) -> str:
    for pattern, replacement in NORMALISERS:
        text = pattern.sub(replacement, text)
    return text


def text_of(outputs: list) -> str:
    """The text a cell printed, in order, with images and metadata dropped."""
    chunks = []
    for out in outputs:
        kind = out.get("output_type")
        if kind == "stream":
            chunks.append(out.get("text", ""))
        elif kind in ("execute_result", "display_data"):
            chunks.append(out.get("data", {}).get("text/plain", ""))
        elif kind == "error":
            chunks.append("\n".join(out.get("traceback", [])))
    return normalise("".join(chunks)).rstrip()


def errors_in(outputs: list) -> list[str]:
    return [
        f"{o.get('ename')}: {o.get('evalue')}"
        for o in outputs
        if o.get("output_type") == "error"
    ]


def code_cells(nb) -> list:
    return [c for c in nb.cells if c.cell_type == "code"]


def check(path: Path, compare: bool) -> tuple[int, int, list[str]]:
    """Run one notebook. Returns (error count, drift count, report lines)."""
    stored = nbformat.read(path, as_version=4)
    fresh = copy.deepcopy(stored)

    started = time.monotonic()
    # resources/metadata/path is the kernel's working directory: the notebooks
    # look for "../ALL CSV FILES - 2nd Edition", so they must run from their own
    # folder, exactly as a student runs them.
    #
    # allow_errors keeps the run going past the first exception so that one
    # report names every broken cell instead of only the first.
    client = NotebookClient(
        fresh,
        timeout=CELL_TIMEOUT_S,
        kernel_name="python3",
        allow_errors=True,
        resources={"metadata": {"path": str(path.parent)}},
    )
    client.execute()
    elapsed = time.monotonic() - started

    lines: list[str] = []
    n_errors = n_drift = 0
    for index, (old, new) in enumerate(zip(code_cells(stored), code_cells(fresh)), start=1):
        for message in errors_in(new.outputs):
            n_errors += 1
            lines.append(f"  error  cell {index}: {message}")
            lines += [f"         | {l}" for l in first_lines(new.get("source", ""), 3)]

        if not compare:
            continue
        # A cell with no execution_count was never run before it was committed,
        # so there is nothing to compare against. An empty *outputs* list is not
        # the same thing: several setup cells legitimately print nothing, and if
        # one starts printing (say "ISLP not installed; using CSV fallbacks")
        # that is exactly the drift worth catching.
        if old.get("execution_count") is None and not old.outputs:
            lines.append(f"  note   cell {index}: never run before it was committed")
            continue
        before, after = text_of(old.outputs), text_of(new.outputs)
        if before == after:
            continue
        n_drift += 1
        lines.append(f"  drift  cell {index}: output differs from the stored run")
        lines += [f"         {l}" for l in unified(before, after)]

    head = (
        f"{path.name}  {len(code_cells(fresh))} code cells, {elapsed:.1f}s"
        f"  —  {n_errors} error(s), {n_drift} drift(s)"
        if compare
        else f"{path.name}  {len(code_cells(fresh))} code cells, {elapsed:.1f}s"
        f"  —  {n_errors} error(s)"
    )
    return n_errors, n_drift, [head] + lines


def first_lines(text: str, limit: int) -> list[str]:
    out = [l for l in text.splitlines() if l.strip()][:limit]
    return out


def unified(before: str, after: str, context: int = 1, limit: int = 40) -> list[str]:
    diff = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile="stored",
            tofile="fresh",
            lineterm="",
            n=context,
        )
    )
    if len(diff) > limit:
        diff = diff[:limit] + [f"... ({len(diff) - limit} more diff lines)"]
    return diff


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("notebooks", nargs="*", type=Path, help="default: all of Chapters/")
    ap.add_argument(
        "--no-compare",
        action="store_true",
        help="only check that nothing raises; do not diff against stored output",
    )
    args = ap.parse_args()

    paths = args.notebooks or (
        sorted(NOTEBOOKS.glob("chapter_*/chapter_*_lab.ipynb"))
        + sorted(ADVANCED.glob("advanced_*/advanced_*_lab.ipynb"))
        # Project starters ship with stored outputs too: they are the scaffolding
        # students build on, so a starter that no longer runs is a broken project.
        + sorted(PROJECTS.glob("project_*/project_*_starter.ipynb"))
    )
    if not paths:
        print(f"no chapter_*_lab.ipynb under {NOTEBOOKS}")
        return 1

    # Deliberately no MPLBACKEND here. ipykernel installs the inline backend,
    # which is headless already and is what produced the stored outputs; forcing
    # Agg instead suppresses the "<Figure size ...>" line of every plotting cell
    # and reports the whole notebook as drifted.

    total_errors = total_drift = 0
    started = time.monotonic()
    for path in paths:
        n_errors, n_drift, lines = check(path, compare=not args.no_compare)
        total_errors += n_errors
        total_drift += n_drift
        print("\n".join(lines), flush=True)

    print(
        f"\n{len(paths)} notebooks in {time.monotonic() - started:.1f}s: "
        f"{total_errors} error(s), {total_drift} drifted cell(s)"
    )
    if total_drift and not total_errors:
        print(
            "Drift with no error is the case this check exists for: the notebook ran,\n"
            "and printed different numbers. Either the code changed and the stored\n"
            "outputs need refreshing, or a dependency changed the answer."
        )
    return 1 if (total_errors or total_drift) else 0


if __name__ == "__main__":
    sys.exit(main())
