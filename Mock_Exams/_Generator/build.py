# -*- coding: utf-8 -*-
"""Builds exam, solutions and slides of a mock exam from one specification.

    python3 build.py              # all mock exams (spec_qrm*.py), .tex + PDFs
    python3 build.py 1            # only Mock Exam 1
    python3 build.py 1 --tex-only # write the .tex files and run the checks, no PDFs

The automatic checks (audit) stop the build with exit code 1 if a subtask asks
for more than one result or refers back to another subtask.
"""
import glob
import importlib
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from templates import (NORMAL_TABLE, T_TABLE, TITLEPAGE_RULES, EXAM_PREAMBLE,  # noqa: E402
                       SOL_PREAMBLE, SLIDES_PREAMBLE)

LETTERS = "abcdefghij"
REQUIRED = ("label", "q", "short", "result", "rubric", "solution")


# ------------------------------------------------------------------ quality checks
# Phrases that ask for a second result in the same subtask (checked per sentence).
MULTI_PATTERNS = [
    (r"\band (also )?(give|state|name|write down|list|report)\b",
     "two requests ('... and give ...')"),
    (r"\band (also )?(justify|explain|interpret|describe|comment on|discuss|argue|reason)\b",
     "result + justification/explanation as two requests"),
    (r"\band (also )?(compute|calculate|determine|derive|find|test|decide|classify|draw|sketch|plot)\b",
     "two tasks in one sentence ('... and compute ...')"),
    (r"\bas well as\b", "two requests ('... as well as ...')"),
    (r"\b(then|afterwards)\b", "chained requests ('... then ...')"),
    (r"\bcommands\b", "several Python commands requested"),
    (r"\bcritical values\b", "several critical values requested"),
    (r"\b(all|both) (measures|values|results|rates|probabilities)\b", "several results requested"),
]
# two calculation verbs in the same sentence = two calculations
CALC_VERBS = r"\b(compute|calculate|determine|derive|find)\b"
# references to other subtasks (the brief: every subtask is self-contained)
BACKREF_PATTERNS = [
    r"\b(from|in|of|see) (sub)?(task|part) [a-j]\)", r"\b(sub)?task [a-j]\)", r"\bfrom [a-j]\)",
    r"\b(previous|preceding|earlier|last) (sub)?(task|part|result)",
    r"\b(computed|calculated|obtained|determined|derived|found|shown) (above|earlier|before)\b",
    r"\byour (result|answer|value|solution)", r"\bresult of (sub)?task", r"\b(from|see) above\b",
]


def sentences(text):
    """Split a question into sentences (decimal points such as 84.30 are kept)."""
    return [s for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\\$])", text) if s.strip()]


def audit(spec):
    """Checks: 3 tasks x 10 subtasks, exactly one requested result, no back-references,
    at most 3 one-sentence answers, at most one Python-command subtask (python=True) and
    at most one Python code-reading subtask (pycode=True) per task."""
    warn = []
    if len(spec["tasks"]) != 3:
        warn.append("the exam has %d instead of 3 tasks" % len(spec["tasks"]))
    for a in spec["tasks"]:
        if len(a["items"]) != 10:
            warn.append("Task %d has %d instead of 10 subtasks" % (a["nr"], len(a["items"])))
        n_satz = sum(1 for it in a["items"] if it.get("kind") == "satz")
        n_py = sum(1 for it in a["items"] if it.get("python"))
        n_code = sum(1 for it in a["items"] if it.get("pycode"))
        if n_satz > 3:
            warn.append("Task %d has %d one-sentence answers (at most 3)" % (a["nr"], n_satz))
        if n_py > 1:
            warn.append("Task %d has %d Python-command subtasks (at most 1)" % (a["nr"], n_py))
        if n_code > 1:
            warn.append("Task %d has %d Python code-reading subtasks (at most 1)" % (a["nr"], n_code))
        for i, it in enumerate(a["items"]):
            tag = "T%d %s)" % (a["nr"], LETTERS[i])
            for key in REQUIRED:
                if not it.get(key):
                    warn.append("%s: field '%s' missing" % (tag, key))
            q = it["q"]
            for s in sentences(q):
                for rx, why in MULTI_PATTERNS:
                    if re.search(rx, s, re.IGNORECASE):
                        warn.append("%s: %s -- %s" % (tag, why, it["label"]))
                if len(re.findall(CALC_VERBS, s, re.IGNORECASE)) > 1:
                    warn.append("%s: two calculation requests in one sentence -- %s" % (tag, it["label"]))
            for rx in BACKREF_PATTERNS:
                if re.search(rx, q, re.IGNORECASE):
                    warn.append("%s: back-reference to another subtask -- %s" % (tag, it["label"]))
            if it.get("python") and not re.search(r"\bcommand\b", q):
                warn.append("%s: Python subtask must ask for exactly one 'command'" % tag)
            if it.get("pycode") and not it.get("code"):
                warn.append("%s: Python code-reading subtask needs the field 'code'" % tag)
            if not q.rstrip().endswith((".", "?")):
                warn.append("%s: question does not end with '.' or '?'" % tag)
    return warn


# ------------------------------------------------------------------ exam
def question(it):
    """Question text; for code-reading subtasks the line of code follows on its own,
    indented line (upright typewriter, also inside the italic question of the solutions)."""
    q = it["q"].strip()
    if it.get("code"):
        q += r"\\*[3pt]\hspace*{1.5em}\texttt{\upshape %s}" % it["code"].strip()
    return q


def build_exam(spec):
    nr = str(spec["nr"])
    out = [EXAM_PREAMBLE.replace("@@NR@@", nr).replace("@@RULES@@", TITLEPAGE_RULES)]
    for a in spec["tasks"]:
        out.append("\n%" + "=" * 68 + "\n")
        out.append(r"\begin{task} [20 points -- 10 subtasks worth 2 points each]" + "\n")
        out.append(a["intro"].strip() + "\n\n")
        out.append(r"\begin{enumerate}[label=\textbf{\alph*)},leftmargin=1.9em,"
                   r"itemsep=10pt,topsep=4pt]" + "\n")
        for it in a["items"]:
            # no answer boxes: working and result go on the correction-margin pages
            out.append(r"\keepitem{5}\item %s \pts" % question(it) + "\n")
        out.append(r"\end{enumerate}" + "\n")
        out.append(r"\end{task}" + "\n")
        out.append(r"\pagebreak" + "\n" + r"\correctionmargin" + "\n" +
                   r"\pagebreak" + "\n" + r"\correctionmargin" + "\n" +
                   r"\pagebreak" + "\n")
    out.append("\n%" + "=" * 68 + "\n")
    out.append("% ===================== STATISTICAL TABLES =========================\n")
    out.append(NORMAL_TABLE)
    out.append(r"\pagebreak" + "\n")
    out.append(T_TABLE)
    out.append("\n" + r"\end{document}" + "\n")
    return "".join(out)


# ------------------------------------------------------------------ solutions
def overview_table(spec):
    """Results overview: all 30 final results on one page."""
    rows = []
    for a in spec["tasks"]:
        rows.append(r"\midrule" + "\n" +
                    r"\multicolumn{4}{l}{\textbf{Task %d -- %s}\hfill\textnormal{20 points}}\\"
                    % (a["nr"], a["topic"]) + "\n" + r"\midrule" + "\n")
        for i, it in enumerate(a["items"]):
            rows.append(r"\textbf{%s)} & %s & %s & 2\\" % (LETTERS[i], it["label"], it["short"]) + "\n")
    body = "".join(rows)
    return (r"""
\vspace{-0.4cm}
\section{Results overview -- all final results at a glance}\label{sec:overview}

\begin{mistakebox}
\small\textbf{Grading note.} Each subtask asks for exactly \emph{one} result: a correct result
with comprehensible working earns 2 points (split for partial answers: see the rubric of the
subtask). A result without working, or correct working with a mere slip (transposed digits,
rounding), counts 1 point. All subtasks are independent -- there are no follow-on errors.
\end{mistakebox}

\begin{footnotesize}
\renewcommand{\arraystretch}{1.0}
\noindent\begin{longtable}{@{}p{0.8cm}>{\raggedright\arraybackslash}p{5.3cm}>{\raggedright\arraybackslash}p{8.4cm}c@{}}
\toprule
\textbf{Part} & \textbf{Asked for} & \textbf{Result} & \textbf{P.}\\
""" + body + r"""\midrule
\multicolumn{3}{r}{\textbf{Total}} & \textbf{60}\\
\bottomrule
\end{longtable}
\end{footnotesize}

\clearpage
""")


def build_solutions(spec):
    out = [SOL_PREAMBLE.replace("@@NR@@", str(spec["nr"]))]
    out.append(overview_table(spec))
    for a in spec["tasks"]:
        out.append("\n%" + "=" * 68 + "\n")
        out.append(r"\section[Task %d -- %s]{Task %d -- %s \hfill\mbox{\normalsize(20 points)}}"
                   % (a["nr"], a["topic"], a["nr"], a["topic"]) + "\n\n")
        out.append(r"\begin{scenariobox}" + "\n")
        out.append(r"\textbf{Scenario.} " + a["scenario"].strip() + "\n")
        out.append(r"\end{scenariobox}" + "\n")
        out.append(r"\lectureref{%s}" % a["lecture_ref"].strip() + "\n\n")
        out.append(r"\begin{conceptbox}" + "\n")
        out.append(r"\textbf{The concepts behind this task}" + "\n")
        out.append(r"\begin{itemize}[leftmargin=1.3em,itemsep=1.5pt,topsep=3pt]" + "\n")
        for k in a["concepts"]:
            out.append(r"\item " + k.strip() + "\n")
        out.append(r"\end{itemize}" + "\n" + r"\end{conceptbox}" + "\n\n")

        for i, it in enumerate(a["items"]):
            # keep heading + question together with the start of the solution
            out.append(r"\Needspace{7\baselineskip}" + "\n")
            out.append(r"\subsection*{%s)\quad %s}" % (LETTERS[i], it["label"]) + "\n")
            # question never split, and never separated from the first solution line
            out.append(r"{\interlinepenalty=10000\noindent\textit{%s}\par}\nopagebreak[4]"
                       % question(it) + (r"\medskip" if it.get("code") else "") + "\n\n")
            out.append(it["solution"].strip() + "\n")
            out.append(r"\result{%s}" % it["result"].strip() + "\n")
            out.append(r"\rubric{%s}" % it["rubric"].strip() + "\n")
            if it.get("mistake"):
                out.append(r"\mistake{%s}" % it["mistake"].strip() + "\n")
            out.append("\n")

        for fig in a.get("figs_sol", []):
            out.append(r"\begin{figure}[H]\centering" + "\n")
            out.append(r"\includegraphics[width=%s\textwidth]{%s}" % (fig[1], fig[0]) + "\n")
            out.append(r"\caption*{\small %s}" % fig[2] + "\n")
            out.append(r"\end{figure}" + "\n\n")

        out.append(r"\begin{mistakebox}" + "\n")
        out.append(r"\textbf{Typical mistakes in Task %d}" % a["nr"] + "\n")
        out.append(r"\begin{itemize}[leftmargin=1.3em,itemsep=1.5pt,topsep=3pt]" + "\n")
        for f in a["mistakes"]:
            out.append(r"\item " + f.strip() + "\n")
        out.append(r"\end{itemize}" + "\n" + r"\end{mistakebox}" + "\n")
        out.append(r"\clearpage" + "\n")
    out.append(r"\end{document}" + "\n")
    return "".join(out)


# ------------------------------------------------------------------ slides
def build_slides(spec):
    out = [SLIDES_PREAMBLE.replace("@@NR@@", str(spec["nr"]))]
    rows = "".join(r"    %d & %s & %s & 20\\" % (a["nr"], a["topic"], a["short_scenario"]) + "\n"
                   for a in spec["tasks"])
    out.append(r"""
\begin{frame}{The mock exam at a glance}
  \begin{center}\small
  \renewcommand{\arraystretch}{1.2}
  \begin{tabular}{@{}c>{\raggedright\arraybackslash}p{5.6cm}>{\raggedright\arraybackslash}p{4.8cm}c@{}}
    \toprule
    Task & Topic & Scenario & Points\\
    \midrule
""" + rows + r"""    \midrule
    \multicolumn{3}{@{}l}{\textbf{Total} \hfill 3 $\times$ 10 subtasks worth 2 points each} & \textbf{60}\\
    \bottomrule
  \end{tabular}
  \end{center}
  \medskip
  \begin{block}{How the exam is built}
    Every subtask can be solved \textbf{independently} and asks for exactly \textbf{one} result.
    No intermediate result is needed in a later subtask -- all values required are stated in
    the subtask itself.
  \end{block}
\end{frame}
""")
    for a in spec["tasks"]:
        out.append("\n%" + "=" * 68 + "\n")
        out.append(r"\section[Task %d]{Task %d: %s}" % (a["nr"], a["nr"], a["topic"]) + "\n\n")
        out.append(r"\begin{frame}{Task %d -- scenario}" % a["nr"] + "\n")
        out.append(a["slide_scenario"].strip() + "\n")
        out.append(r"\end{frame}" + "\n\n")

        out.append(r"\begin{frame}{Task %d -- the concepts you need}" % a["nr"] + "\n")
        out.append(r"  \begin{itemize}\setlength{\itemsep}{3pt}" + "\n")
        for k in a["concepts"]:
            out.append(r"    \item " + k.strip() + "\n")
        out.append(r"  \end{itemize}" + "\n" + r"\end{frame}" + "\n\n")

        for det in a.get("slides_detail", []):
            title, body = det[0], det[1]
            opt = "[fragile]" if len(det) > 2 and det[2] else ""
            out.append(r"\begin{frame}%s{%s}" % (opt, title) + "\n")
            out.append(body.strip("\n") + "\n")
            out.append(r"\end{frame}" + "\n\n")

        for half in (0, 1):
            part = a["items"][half * 5:(half + 1) * 5]
            rng = "%s)--%s)" % (LETTERS[half * 5], LETTERS[half * 5 + len(part) - 1])
            out.append(r"\begin{frame}{Task %d -- results %s}" % (a["nr"], rng) + "\n")
            out.append(r"  \begin{center}\small" + "\n")
            out.append(r"  \renewcommand{\arraystretch}{1.35}" + "\n")
            # ragged right instead of justified: no stretched spaces, no hyphenation
            out.append(r"  \begin{tabular}{@{}c>{\raggedright\arraybackslash}p{4.9cm}"
                       r">{\raggedright\arraybackslash}p{8.4cm}@{}}" + "\n")
            out.append(r"    \toprule Part & Asked for & Result\\ \midrule" + "\n")
            for j, it in enumerate(part):
                out.append(r"    \textbf{%s)} & %s & %s\\" %
                           (LETTERS[half * 5 + j], it["label"], it["short"]) + "\n")
            out.append(r"    \bottomrule" + "\n  \\end{tabular}" + "\n  \\end{center}" + "\n")
            out.append(r"\end{frame}" + "\n\n")

        for fig in a.get("figs_slides", []):
            out.append(r"\begin{frame}{%s}" % fig[2] + "\n")
            out.append(r"  \begin{center}" + "\n")
            out.append(r"    \includegraphics[width=\textwidth,height=%s\textheight,"
                       r"keepaspectratio]{%s}" % (fig[1], fig[0]) + "\n")
            out.append(r"  \end{center}" + "\n")
            out.append(r"\end{frame}" + "\n\n")

        out.append(r"\begin{frame}{Task %d -- typical mistakes}" % a["nr"] + "\n")
        out.append(r"  \begin{itemize}\setlength{\itemsep}{4pt}" + "\n")
        for f in a["mistakes"]:
            out.append(r"    \item " + f.strip() + "\n")
        out.append(r"  \end{itemize}" + "\n" + r"\end{frame}" + "\n\n")

    out.append(r"""
\section*{Wrap-up}
\begin{frame}{Points and exam strategy}
  \begin{block}{Structure}
    3~tasks $\times$ 10~subtasks $\times$ 2~points = 60~points in 120~minutes
    -- about 4~minutes per subtask.
  \end{block}
  \begin{itemize}\setlength{\itemsep}{4pt}
    \item All subtasks are \textbf{independent}: skip whatever is stuck and come back to it at
      the end -- you lose no further points.
    \item Each subtask asks for \textbf{one} result -- mark it clearly on your working pages.
    \item Still write down your working: a result without working earns only half the points.
    \item Do not forget units, signs and rounding.
  \end{itemize}
\end{frame}

\end{document}
""")
    return "".join(out)


# ------------------------------------------------------------------ compilation
def compile_pdf(outdir, texname, pdfname):
    """Compile texname in outdir (aux files in a temporary sub-folder) and save the PDF
    under its final name. Returns a list of problems found in the log."""
    build = os.path.join(outdir, "_build")
    os.makedirs(build, exist_ok=True)
    base = os.path.splitext(texname)[0]
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
           "-outdir=_build", texname]
    r = subprocess.run(cmd, cwd=outdir, capture_output=True, text=True)
    problems = []
    logfile = os.path.join(build, base + ".log")
    log = open(logfile, encoding="latin-1").read() if os.path.exists(logfile) else ""
    if r.returncode != 0 or not os.path.exists(os.path.join(build, base + ".pdf")):
        problems.append("LaTeX error (see %s)" % logfile)
        err = [l for l in log.splitlines() if l.startswith("!")]
        problems.extend("   " + e for e in err[:5])
        return problems
    for m in re.finditer(r"Overfull \\[hv]box \((\d+\.\d+)pt too \w+\)[^\n]*", log):
        if float(m.group(1)) > 1.0:
            problems.append(m.group(0))
    for m in re.finditer(r"LaTeX Warning: (Reference|Citation)[^\n]*", log):
        problems.append(m.group(0))
    shutil.copyfile(os.path.join(build, base + ".pdf"), os.path.join(outdir, pdfname))
    pages = re.search(r"Output written on .*?\((\d+) pages?", log.replace("\n", ""))
    print("   pdf: %s (%s pages)" % (pdfname, pages.group(1) if pages else "?"))
    return problems


# ------------------------------------------------------------------ main
def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tex_only = "--tex-only" in sys.argv
    if not args:
        args = sorted(re.findall(r"spec_qrm(\d+)\.py", " ".join(
            os.path.basename(p) for p in glob.glob(os.path.join(HERE, "spec_qrm*.py")))), key=int)
    failed = []
    for nr in args:
        spec = importlib.import_module("spec_qrm%s" % nr).SPEC
        d = spec["outdir"]
        os.makedirs(d, exist_ok=True)
        files = [("Mock_Exam_%s.tex" % nr, build_exam(spec),
                  "Quantitative Research Mock Exam %s.pdf" % nr),
                 ("Mock_Exam_%s_Solutions.tex" % nr, build_solutions(spec),
                  "Quantitative Research Mock Exam %s Solutions.pdf" % nr),
                 ("Mock_Exam_%s_Slides.tex" % nr, build_slides(spec),
                  "Quantitative Research Mock Exam %s Slides.pdf" % nr)]
        for name, content, _ in files:
            with open(os.path.join(d, name), "w", encoding="utf-8") as fh:
                fh.write(content)
            print("written:", os.path.join(d, name))
        problems = audit(spec)
        if problems:
            print("  !! Mock Exam %s:" % nr)
            for w in problems:
                print("     - " + w)
            failed.append(nr)
            continue
        print("  Check OK: 3 x 10 subtasks, one requested result each, no back-references")
        if tex_only:
            continue
        latex_problems = []
        for name, _, pdf in files:
            latex_problems += ["%s: %s" % (name, p) for p in compile_pdf(d, name, pdf)]
        if latex_problems:
            print("  !! LaTeX problems in Mock Exam %s:" % nr)
            for p in latex_problems:
                print("     - " + p)
            failed.append(nr)
        else:
            shutil.rmtree(os.path.join(d, "_build"), ignore_errors=True)
            print("  LaTeX OK: 3 PDFs, 0 errors, no overfull boxes > 1pt")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
