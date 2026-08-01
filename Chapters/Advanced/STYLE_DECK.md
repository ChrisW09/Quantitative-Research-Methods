# STYLE_DECK.md — How to author a lecture deck in this course's house style

This brief lets you write a Beamer deck that is indistinguishable from the existing
`Chapters/chapter_XX/chapter_XX.tex` decks (canonical short example: chapter 13,
1246 lines; canonical mid-size example: chapter 5, 1693 lines). Follow it exactly.

---

## 1. File layout and compilation

- One directory per deck: `chapter_XX/` containing `chapter_XX.tex`, an `images/`
  subdirectory, and (if the deck needs generated figures) a `make_figures.py`.
- Compile with **`pdflatex` run twice** (TOC + section navigation need the second pass):
  ```
  cd "<deck dir>" && pdflatex -interaction=nonstopmode chapter_XX.tex && pdflatex -interaction=nonstopmode chapter_XX.tex
  ```
- Document class is always `\documentclass[aspectratio=169,11pt]{beamer}`.
- Paths contain spaces — always quote them in shell commands.

## 2. The preamble — copy VERBATIM

This is the complete preamble of the canonical deck (chapter 13). Copy it unchanged,
editing only the chapter number/title in the comment header and in `\title`/`\subtitle`.

```latex
% ============================================================
% HSBI Beamer — ISLP Lecture Series — IMPROVED EDITION
% Chapter 13: Multiple Testing
% ============================================================
\documentclass[aspectratio=169,11pt]{beamer}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}\usepackage[english]{babel}
\usepackage{graphicx}\usepackage{booktabs}\usepackage{amsmath,amssymb,amsfonts}
\usepackage{mathtools}\usepackage{hyperref}\usepackage{xcolor}
\usepackage{verbatim}\usepackage{alltt}
\usepackage{tikz}\usetikzlibrary{calc,arrows.meta,positioning,shapes}
\usepackage{tcolorbox}\tcbuselibrary{skins}

\usetheme{Madrid}\usecolortheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}[frame number]
\setbeamertemplate{blocks}[rounded][shadow=false]
\setbeamertemplate{headline}{%
  \leavevmode\hbox{%
    \begin{beamercolorbox}[wd=\paperwidth,ht=2.2ex,dp=0.9ex]{section in head/foot}%
      {\fontsize{4.6}{5.2}\selectfont%
       \insertsectionnavigationhorizontal{\paperwidth}{}{\hskip0pt plus1filll}}%
    \end{beamercolorbox}}%
}
\setbeamerfont{section in head/foot}{size=\tiny}
\setbeamerfont{palette primary}{size=\tiny}
\setbeamerfont{palette tertiary}{size=\tiny}
\setbeamerfont{section in toc}{size=\footnotesize}

\usepackage{listings}
\definecolor{pyKw}{RGB}{0,0,180}\definecolor{pyStr}{RGB}{20,120,40}
\definecolor{pyCom}{RGB}{120,120,120}\definecolor{accent}{RGB}{38,70,140}
\lstdefinestyle{Pystyle}{language=Python,basicstyle=\ttfamily\footnotesize,
  keywordstyle=\color{pyKw}\bfseries,commentstyle=\color{pyCom}\itshape,
  stringstyle=\color{pyStr},showstringspaces=false,upquote=true,
  columns=fullflexible,breaklines=true,literate={~}{{$\sim$}}1}
\lstset{style=Pystyle}

\AtBeginSection[]{\begin{frame}{Outline}\footnotesize
  \tableofcontents[currentsection,sectionstyle=show/shaded,subsectionstyle=show/show/hide]
\end{frame}}

\newcommand{\islpsource}[1]{%
  \vfill\hfill{\tiny\itshape\color{gray}Source: #1 \textemdash{} ISLP, James et al.\ (2023).}\par
}

\newtcolorbox{takeaway}[1][Takeaway]{enhanced,colback=green!4,colframe=green!50!black,
  boxrule=0pt,leftrule=2.5pt,arc=2pt,fonttitle=\bfseries,title=#1,
  left=2mm,right=2mm,top=1mm,bottom=1mm}
\newtcolorbox{numexample}[1][Worked example]{enhanced,colback=orange!4,colframe=orange!70!black,
  boxrule=0pt,leftrule=2.5pt,arc=2pt,fonttitle=\bfseries,title=#1,
  left=2mm,right=2mm,top=1mm,bottom=1mm}
\newtcolorbox{readme}[1][How to read this]{enhanced,colback=blue!4,colframe=accent,
  boxrule=0pt,leftrule=2.5pt,arc=2pt,fonttitle=\bfseries,title=#1,
  left=2mm,right=2mm,top=1mm,bottom=1mm}

\title{Quantitative Research Methods}
\subtitle{Chapter 13: Multiple Testing}
\author{Prof.\ Dr.\ Christoph Weisser}\institute{HSBI}
\date{Summer Semester 2026}\graphicspath{{images/}}

\newtcolorbox{exercise}[1][Exercise]{enhanced, fontupper=\footnotesize, colback=purple!4, colframe=purple!55!black, boxrule=0pt, leftrule=2.5pt, arc=2pt, fonttitle=\bfseries, title=#1, left=2mm, right=2mm, top=1mm, bottom=1mm}
\newtcolorbox{solutionbox}[1][Solution]{enhanced, fontupper=\footnotesize, colback=teal!5, colframe=teal!55!black, boxrule=0pt, leftrule=2.5pt, arc=2pt, fonttitle=\bfseries, title=#1, left=2mm, right=2mm, top=1mm, bottom=1mm}
\newtcolorbox{longexercise}[1][Extended exercise (15 min)]{enhanced, fontupper=\footnotesize, colback=violet!6, colframe=violet!55!black, boxrule=0pt, leftrule=3pt, arc=2pt, fonttitle=\bfseries, title=#1, left=2mm, right=2mm, top=1mm, bottom=1mm}

% Reclaim ~2pt of body height (custom nav headline makes full slides tip over by ~1.83pt)
\addtobeamertemplate{frametitle}{}{\vspace{-2pt}}

\newtcolorbox{labnote}[1][Run this live in the lab notebook]{enhanced, fontupper=\footnotesize, colback=cyan!7, colframe=cyan!45!black, boxrule=0pt, leftrule=3pt, arc=2pt, fonttitle=\bfseries, title=#1, left=2mm, right=2mm, top=1mm, bottom=1mm}

% Industry application callout box --- slate grey, for real business/industry use
\definecolor{industryC}{RGB}{88,98,116}
\newtcolorbox{industry}[1][In industry]{enhanced, fontupper=\footnotesize, colback=industryC!7, colframe=industryC, boxrule=0pt, leftrule=3pt, arc=2pt, fonttitle=\bfseries, title={In industry --- #1}, left=2mm, right=2mm, top=1mm, bottom=1mm}

% Common-mistake callout --- crimson, for the error to pre-empt
\newtcolorbox{mistake}[1][Common mistake]{enhanced, fontupper=\footnotesize, colback=red!4, colframe=red!60!black, boxrule=0pt, leftrule=3pt, arc=2pt, fonttitle=\bfseries, title=#1, left=2mm, right=2mm, top=1mm, bottom=1mm}
```

Optional extras used by larger decks (chapter 5) — add only if you need them:

```latex
% Extra named colours for TikZ CV/bootstrap diagrams
\definecolor{cvtrain}{RGB}{38,70,140}\definecolor{cvtest}{RGB}{224,130,20}
\definecolor{cvgreen}{RGB}{46,125,50}\definecolor{cvred}{RGB}{198,40,40}

% Tighter TOC spacing (place AFTER \lstset, BEFORE \AtBeginSection)
\usepackage{etoolbox}
\makeatletter
\patchcmd{\beamer@sectionintoc}{\vskip1.5em}{\vskip.6em}{\typeout{TOCPATCH-OK}}{\typeout{TOCPATCH-FAIL}}
\makeatother
```

## 3. Front matter — the fixed opening sequence

Every deck opens with exactly this slide sequence, in this order:

1. `\begin{frame}[plain]\titlepage\end{frame}`
2. **"The course at a glance"** — `\footnotesize` centered 3-column tabular
   (` & \textbf{Lecture} & \textbf{Topic}`, `\midrule`, one row per lecture,
   `$\blacktriangleright$` in column 1 and bold text marking *today's* chapter), followed by
   `{\scriptsize Twelve sessions of 180 minutes. $\blacktriangleright$ marks today's chapter. Short exercises every $\sim$20 min; extended exercises every $\sim$45 min; each chapter has a companion lab notebook.}`
3. **"Contents"** — `\small\tableofcontents[hideallsubsections]`, then
   `\vfill {\tiny Optional and advanced material is collected in the \textbf{appendix} at the end of the deck.}`
4. **"Notation in this chapter"** — `\footnotesize` booktabs table with columns
   `\textbf{Symbol}` / `\textbf{Meaning}`, covering every symbol the chapter uses.
5. **"Sources and references"** — a `block` titled "Primary textbook" citing
   James, Witten, Hastie, Tibshirani \& Taylor (2023), *An Introduction to Statistical
   Learning, with Applications in Python*, Springer.
6. **"Learning objectives"** (chapter 5 titles it "Learning objectives for this chapter") —
   "By the end of this chapter you will be able to:" + itemize with a **bold verb**
   opening each item (Explain / Apply / Use / Avoid / …).
7. **"Roadmap of this chapter"** — a `takeaway` box (with a custom title) containing an
   enumerated 4–6 item plan of the chapter.
8. **"Where this chapter is used in industry"** — `\scriptsize` booktabs table with
   columns Sector / Concrete application / Which decision it drives (5–6 rows), often
   followed by one `industry` box drawing the common thread.
9. **"Industry case in depth: …"** — one full slide narrating a single realistic case,
   built from 2–3 boxes (`industry`, `readme`, `takeaway`).

Larger chapters (e.g. 5) insert a motivating section (`\section{Why this chapter matters}`
with 2–3 hook slides: the key question, why the naive answer fails, "Two big ideas in this
chapter" in `columns`) between front matter and the first content section.

## 4. Section skeleton and teaching rhythm

- Sections are marked with a banner comment:
  ```latex
  % ============================================================
  \section{Short Name}
  % ============================================================
  ```
  Section names are short (`The Problem`, `FWER`, `FDR`, `Practice`, `Python Lab`,
  `Summary`). `\AtBeginSection` auto-inserts an Outline slide before each — do not add one.
- Within a section the teaching flow is: **motivation → intuition → formal
  definition/algorithm → worked numeric example → picture → interpretation/decision
  guidance**, then exercises. Typical slide anatomy: 1–3 short body lines or a `block`
  with the formula/algorithm, then 1–3 tcolorboxes.
- Never leave a formula bare: a `block` titled "Rule"/"Algorithm" holds the boxed formula
  (`\boxed{...}` for the single most important rule), immediately followed by a `readme`
  box that decodes each symbol/step in plain words, and usually a `takeaway` stating the
  one-line consequence or guarantee.

### Which box goes where

| Box | Colour | Use |
|---|---|---|
| `takeaway` | green | the one thing to remember from the slide; also closes figure slides with the reading of the figure |
| `readme` (default title "How to read this") | blue | decode a formula, an algorithm's steps, a table, or definitions; also "Quick self-assessment" mini-checks |
| `numexample` | orange | small worked arithmetic on the slide (e.g. "Test 10 000 genes ⇒ ~500 false discoveries") |
| `mistake` | crimson | pre-empt one specific error; frequently placed *below* a solutionbox |
| `exercise` | purple | short in-lecture exercise (fits one slide) |
| `solutionbox` | teal | the full worked solution |
| `longexercise` | violet, default title "Extended exercise (15 min)" | multi-part integrative exercise |
| `labnote` | cyan, default title "Run this live in the lab notebook" | pointer to the companion notebook |
| `industry` | slate grey, title prints "In industry --- #1" (always pass a title) | real business application of the concept just taught |
| standard beamer `block` | theme blue | formal rule / algorithm / definition |
| standard `alertblock` | red, usually titled "Don't" | lists of prohibitions (p-hacking, pitfalls) |

Sprinkle `industry` boxes throughout content slides (roughly one every 3–5 slides), each
with a concrete sector title like `[Quantitative finance: backtest overfitting]`.

### Figures

- `\graphicspath{{images/}}` is set; include with
  `\includegraphics[width=0.92\textwidth,height=0.58\textheight,keepaspectratio]{ch13_fwer.png}`
  inside `\begin{center}...\end{center}` (widths 0.85–0.92, heights 0.52–0.58).
- Every figure slide ends with a `takeaway` box that tells the student what to see in
  the figure, with concrete numbers ("passes 50% by only m=14 tests").
- Figures reproduced from the textbook are PDFs named `13_5.pdf` etc. and are credited
  with `\islpsource{Figure 13.5}` after the takeaway.
- **Course-generated figures** are PNGs named `chXX_<slug>.png` produced by a
  `make_figures.py` in the deck directory (see §7). Extra figures added for exercises
  use an `x` infix: `ch05_x_bootstrap_alpha_hist.png`.
- Concept diagrams (CV fold layouts, decision tables, pipelines) are **native TikZ**,
  not images; slide titles sometimes note "(native diagram)". Style: `font=\small`,
  `minimum width/height` node styles, soft fills like `green!14`, `red!16`,
  `orange!14`, `accent!16`.

## 5. Exercises — the iron rules

- **Every exercise slide is immediately followed by its full solution slide(s).** No
  exceptions, no "solutions at the end".
- Numbering is per chapter: `Exercise 13.1`, `Exercise 13.2`, …; extended ones are
  `Extended Exercise 13.1`, … (their own counter).
- Slide title format: `Exercise 13.2 --- Bonferroni correction [Math]` — an em-dash
  (`---`), a short topic, then a **tag** in square brackets:
  `[Concept]` (verbal/definitional), `[Math]` (pencil-and-paper),
  `[Python]` (code), `[Integrative]` (design decisions spanning ideas).
- Solution slide titles: `Solution --- Exercise 13.2`. When a solution spans multiple
  slides, label each: `Solution --- Exercise 13.1 (1/2)`, `(2/2)` (extended exercises
  often run `(1/3)`–`(3/3)`). Multi-slide solutions may give each `solutionbox` a
  descriptive title: `\begin{solutionbox}[Solution --- code: setup and the BH rule]`.
- Solution content pattern: open with **`\textbf{Method.}`** (why this approach), then
  `\textbf{Part 1 --- ...}` / `\textbf{Step 1 --- ...}` paragraphs, small `array` tables
  for rank-by-rank comparisons, display math for the arithmetic, and a closing
  **Take-away/Comparison** line. Append a `mistake` box under the solutionbox (or an
  inline `\textit{Common mistake:}` paragraph inside it) naming the error students make.
- Short exercises appear roughly every 20 minutes of material (after each major concept);
  extended exercises every ~45 minutes (ends of major sections). Occasional
  "Mini-check" slides use a `readme`[Quick self-assessment] with numbered questions plus
  a `takeaway`[Answers] on the same slide.
- Code-bearing frames need `\begin{frame}[fragile]{...}` and use `lstlisting` (style is
  preset). Code lines carry short trailing `#` comments aligned in spirit, ~70 chars max;
  shrink to `basicstyle=\ttfamily\scriptsize` only when a listing would overflow.
- `[Python]` exercises get a `labnote` box on the exercise slide pointing to the exact
  notebook cell: "The worked solution sits in \texttt{chapter\_XX\_lab.ipynb} under
  \emph{Lecture exercises --- worked Python solutions}: the cell headed \emph{...}".

## 6. The Python Lab and Summary sections

- `\section{Python Lab}` opens with the slide **"Python lab --- run it live in the
  notebook"**: one `labnote` box titled `[Companion notebook: \texttt{chapter\_XX\_lab.ipynb}]`
  that says the code is meant to be **demonstrated live**, lists the notebook's numbered
  sections (§1, §2, …) as an itemize, and ends "Data loads via the \texttt{ISLP} package
  or the bundled CSV files; ... exercises ...".
- Then 2–4 `[fragile]` slides each showing one self-contained, runnable listing
  (imports included, seeded `rng`, `print` at the end), then the `[Python]` exercises.
- `\section{Summary}` closes the main deck with this fixed slide sequence (titles verbatim):
  1. **"Chapter X in one slide"** — `block`{What we accomplished} + itemize of topics.
  2. **"Key formulas at a glance"** — `\footnotesize description` list, one formula per item.
  3. **"Vocabulary checklist"** — `\footnotesize` booktabs table Term / Meaning.
  4. **"Decision rules of thumb"** — itemize of if-then guidance.
  5. **"Common pitfalls"** — `alertblock`{Don't} with an enumerate.
  6. Optional extras seen in the corpus: "Methods comparison" table, "Connections to
     the rest of the course", **"Self-check questions"**, "Five things to remember",
     "What's next" (or "Course-wide summary" + "Closing thoughts" in the final chapter).

## 7. Appendix pattern

```latex
% ============================================================
\appendix
\AtBeginSection[]{}
\section{Appendix: optional and advanced material}
% ============================================================
```

- The `\AtBeginSection[]{}` reset is mandatory (kills auto-Outline slides in the appendix).
- The appendix **opens with a signpost slide** titled "Appendix --- what is in here, and
  why", beginning verbatim: "Nothing in the appendix is needed to follow the chapter:
  each slide is a formal derivation, a longer worked exercise, or a side topic. Read it
  when you want the full story, or when a later chapter sends you back here." followed
  by a `block`{Contents of the appendix} whose bold-led items say what each piece is
  *and why it was moved out of the main deck*.
- Appendix content: derivations, drill exercises (still exercise → immediate solution),
  side topics, extra figures. Same box conventions as the main deck.

## 8. make_figures.py conventions (deck figures)

Model: `Chapters/chapter_00/make_figures.py`. Rules:

- **matplotlib only — seaborn is NOT installed on this machine.** `matplotlib.use("Agg")`
  before importing pyplot. numpy/pandas/scipy allowed.
- Module docstring states figures are computed from the bundled course datasets or
  clearly labelled simulations, and gives the run command.
- Paths resolved from the file location:
  ```python
  HERE = Path(__file__).parent
  ROOT = HERE.parents[1]
  DATA = ROOT / "ALL CSV FILES - 2nd Edition"
  OUT = HERE / "images"; OUT.mkdir(parents=True, exist_ok=True)
  ```
- House palette constants: `ACCENT = "#26468C"` (matches the deck's `accent` RGB 38,70,140),
  `ORANGE = "#C8641E"`, `GREY = "#7A7A7A"`, plus green `"#2E7D5B"` when needed.
  Seeded RNG: `RNG = np.random.default_rng(0)`.
- rcParams: `figure.dpi`/`savefig.dpi` 150, `font.size` 9, `axes.titlesize` 10,
  top/right spines off, `axes.grid True` with `grid.alpha 0.25`, `grid.linewidth 0.6`.
- One `def fig_<slug>():` per figure; a shared `save(fig, name)` helper doing
  `tight_layout`, `savefig(OUT / name, bbox_inches="tight")`, `close`, `print("wrote", name)`;
  an `if __name__ == "__main__":` block calling every figure function.
- Figure sizes ~(6.6–9.4, 2.5–4.0) inches — wide and short, sized for 16:9 slides.
  Output PNG named `chXX_<slug>.png`. Load CSVs with pandas (mind index columns:
  Advertising/Boston have `index_col=0`, Wage does not).

## 9. Tone and micro-style

- British-leaning academic prose ("regularisation", "visualising"), em-dashes written
  `---`, `\emph{}` for stress, `\textbf{}` for the load-bearing noun/verb.
- Frame titles are full sentences or claims, lowercase after the first word
  ("Why naive testing fails at scale", "Holm's step-down procedure (uniformly beats
  Bonferroni)").
- Numbers formatted with `$10\,000$` thin spaces; probabilities/percentages given
  concretely; `\checkmark` / `$\times$` in decision tables.
- Global font drops per slide (`\footnotesize`, `\scriptsize`) are the standard way to
  fit dense tables.
