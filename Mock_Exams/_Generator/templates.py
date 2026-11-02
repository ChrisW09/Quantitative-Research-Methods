# -*- coding: utf-8 -*-
"""LaTeX templates for the exam, the solutions and the slides of the
"Quantitative Research" mock exams (English port of the templates of the
course "Statistik fuer Oekonomen").

The two statistical tables are computed with SciPy, so every printed value
is the exact quantile / CDF value rounded to four decimals.
"""
from scipy import stats

HSBI_COLOURS = r"""
\definecolor{hsbiblau}{HTML}{3333B2}
\definecolor{hsbiblaudunkel}{HTML}{1C1C6E}
\definecolor{hsbiorange}{HTML}{E69F00}
\definecolor{hsbigrau}{HTML}{9A9A9A}
\definecolor{hsbirot}{HTML}{C0392B}
\definecolor{hsbigruen}{HTML}{2E8B57}
"""


# ---------------------------------------------------------------- statistical tables
def _normal_table():
    rows = []
    for i in range(35):                       # z = 0.0, 0.1, ..., 3.4
        z0 = i / 10
        vals = " & ".join("%.4f" % stats.norm.cdf(round(z0 + j / 100, 2)) for j in range(10))
        rows.append("%.1f & %s\\\\" % (z0, vals))
        if i in (9, 19, 29):
            rows.append(r"\addlinespace")
    head = " & ".join(r"\multicolumn{1}{c}{%.2f}" % (j / 100) for j in range(10))
    quant = " & ".join("$%.3f$" % stats.norm.ppf(p) for p in (0.90, 0.95, 0.975, 0.99, 0.995))
    return r"""
\begin{table}[H]
\centering
\caption{\label{tab:normal}Cumulative distribution function $\Phi(z)=P(Z\le z)$ of the standard normal distribution $N(0,1)$}
\begin{scriptsize}
\begin{tabular}{*{11}{r}}
\toprule
\multicolumn{1}{c}{$z$} & """ + head + r"""\\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{scriptsize}

\medskip
{\footnotesize Reading: row $=$ $z$ to one decimal, column $=$ second decimal, e.g.\ $\Phi(1.96)=0.9750$.
Negative $z$: $\Phi(-z)=1-\Phi(z)$. For $z\ge 3.5$: $\Phi(z)\approx 1$.\par}

\medskip
{\footnotesize\renewcommand{\arraystretch}{1.2}
\begin{tabular}{lccccc}
\toprule
\multicolumn{6}{l}{Selected quantiles $z_p$ with $\Phi(z_p)=p$}\\
\midrule
$p$ & $0.90$ & $0.95$ & $0.975$ & $0.99$ & $0.995$\\
$z_p$ & """ + quant + r"""\\
\bottomrule
\end{tabular}\par}
\end{table}
"""


T_PROBS = (0.80, 0.90, 0.95, 0.975, 0.99, 0.995)


def _dec(p):
    """0.8 -> '0.80', 0.975 -> '0.975' (at least two decimals)."""
    txt = "%g" % p
    return txt + "0" if len(txt.split(".")[1]) == 1 else txt
T_DFS = list(range(1, 31)) + [40, 60, 120]


def _t_table():
    rows = []
    for df in T_DFS:
        vals = " & ".join("%.4f" % stats.t.ppf(p, df) for p in T_PROBS)
        rows.append("%d & %s\\\\" % (df, vals))
        if df in (10, 20, 30):
            rows.append(r"\addlinespace")
    rows.append(r"$\infty$ & " + " & ".join("%.4f" % stats.norm.ppf(p) for p in T_PROBS) + r"\\")
    head = " & ".join("$%s$" % _dec(p) for p in T_PROBS)
    tail = " & ".join("$%s$" % _dec(round(1 - p, 3)) for p in T_PROBS)
    return r"""
\begin{table}[H]
\centering
\caption{\label{tab:t}Quantiles $t_{p;\,\mathrm{df}}$ of the $t$-distribution with $\mathrm{df}$ degrees of freedom}
\begin{footnotesize}
\renewcommand{\arraystretch}{1.02}
\begin{tabular}{r*{6}{c}}
\toprule
 & \multicolumn{6}{c}{probability $p$ (quantile $t_{p;\,\mathrm{df}}$)}\\
\cmidrule(l){2-7}
$\mathrm{df}$ & """ + head + r"""\\
\multicolumn{1}{r}{\scriptsize upper tail} & """ + tail + r"""\\
\midrule
""" + "\n".join(rows) + r"""
\bottomrule
\end{tabular}
\end{footnotesize}

\medskip
{\footnotesize Example: $t_{0.975;\,15}=2.1314$ (two-sided test, $\alpha=0.05$, $n=16$).
Symmetry: $t_{1-p;\,\mathrm{df}}=-t_{p;\,\mathrm{df}}$. The row $\infty$ is the standard normal distribution.\par}
\end{table}
"""


NORMAL_TABLE = _normal_table()
T_TABLE = _t_table()

TITLEPAGE_RULES = r"""
\small
\begin{description}[itemsep=2pt,topsep=4pt]
\item[First:] This exam consists of 3 tasks with 10 subtasks each. Please check that your copy is complete.
\item[Time allowed:] 120 minutes.
\item[Not allowed:] The staple of the exam must not be removed.
\item[Not allowed:] Copying other people's solutions and using aids that are not permitted.
\item[Allowed:] The only permitted aids are one of the calculators named in the lecture (Casio fx-85-MS, fx-85-MS-2, fx-82-MS or fx-82-MS-2) and a handwritten formula sheet of at most one A4 sheet.
\item[Points:] Each subtask is worth \textbf{2 points}; each task gives 20 points, the whole exam \textbf{60 points}.
\item[Independence:] \textbf{All subtasks can be solved independently of each other.} Every subtask states all the numbers needed to solve it. If you cannot solve a subtask, simply continue with the others -- you lose nothing else.
\item[Note 1:] Each subtask asks for exactly \emph{one} result. Write it in the answer box provided.
\item[Note 2:] Show your working on the pages with a correction margin after each task. A result without comprehensible working earns only half of the points.
\item[Note 3:] Round final results to four decimal places, or to two where this is sensible (e.g.\ amounts in euros).
\item[Tables:] The standard normal table (Table~1) and the $t$-table (Table~2) are at the end of the exam.
\end{description}
\normalsize
"""

# ---------------------------------------------------------------- exam
EXAM_PREAMBLE = r"""\NeedsTeXFormat{LaTeX2e}
\documentclass[a4paper]{article}
\usepackage[british]{babel}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,mathpazo,alltt,amssymb}
\renewcommand{\ttdefault}{lmtt}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{enumitem}
\usepackage{theorem}
\theoremstyle{break}
\theorembodyfont{\rmfamily}
\newtheorem{task}{Task}
\usepackage{float}
\floatstyle{plain}
\restylefloat{table}
\restylefloat{figure}
\usepackage{graphicx}
\usepackage[hidelinks,pdftitle={Quantitative Research -- Mock Exam @@NR@@},
  pdfauthor={Prof. Dr. Christoph Weisser}]{hyperref}
\renewcommand\textfraction{.1}
\renewcommand\floatpagefraction{.7}
\pagestyle{myheadings}
\markright{Mock Exam @@NR@@ -- Quantitative Research}
\sloppy
""" + HSBI_COLOURS + r"""
%% empty page with a vertical correction margin (for the working)
\def\correctionmargin{\vbox to 0pt{
    \hbox{\hskip\textwidth\hspace*{1pt}
        \vrule
        \vbox{\vskip\textheight}
}\vss}}

%% formulas such as $\hat\beta_1 = 3$ are not split across lines
\relpenalty=10000
\binoppenalty=10000
%% points flush right on the last line of the question (or on a line of their own)
\newcommand{\pts}{{\unskip\nobreak\hfil\penalty50\hskip1.5em\hbox{}\nobreak\hfil
  \mbox{\small(2 points)}\parfillskip=0pt\finalhyphendemerits=0\par}}
%% answer boxes
\usepackage{needspace}
\newcommand{\keepitem}[1]{\Needspace{#1\baselineskip}}
\newcommand{\answerbox}{\par\nopagebreak\vspace{2pt}%
  \noindent\hspace*{0.4em}{\footnotesize\textbf{Result:}}~%
  \fbox{\rule{0pt}{1.45em}\hspace{0.60\linewidth}}\par}
\newcommand{\answerboxsentence}{\par\nopagebreak\vspace{2pt}%
  \noindent\hspace*{0.4em}{\footnotesize\textbf{Result (one sentence):}}\par\nopagebreak\vspace{1pt}%
  \noindent\hspace*{0.4em}\fbox{\rule{0pt}{2.6em}\hspace{0.93\linewidth}}\par}
\newcommand{\answerboxsketch}{\par\nopagebreak\vspace{2pt}%
  \noindent\hspace*{0.4em}{\footnotesize\textbf{Result (sketch):}}\par\nopagebreak\vspace{1pt}%
  \noindent\hspace*{0.4em}\fbox{\rule{0pt}{5.2em}\hspace{0.93\linewidth}}\par}

\usepackage{tikz}
\definecolor{cloverdark}{RGB}{27,94,32}
\definecolor{cloverlight}{RGB}{102,187,106}
\newcommand{\clover}[1][1]{%
  \begin{tikzpicture}[scale=#1,line join=round]
    \draw[line width=1.4pt,cloverdark,line cap=round]
      (0,-0.05) .. controls (0.15,-0.9) and (0.62,-1.4) .. (0.42,-2.2);
    \foreach \a in {45,135,225,315}{
      \begin{scope}[rotate=\a]
        \shadedraw[draw=cloverdark,line width=0.8pt,top color=cloverlight,bottom color=cloverdark]
          (0,0) .. controls (0.98,0.52) and (0.96,1.72) .. (0,1.26)
                .. controls (-0.96,1.72) and (-0.98,0.52) .. (0,0) -- cycle;
      \end{scope}
    }
    \fill[cloverdark] (0,0) circle (0.07);
  \end{tikzpicture}}

\begin{document}
\begin{titlepage}
\begin{center}
{\huge Quantitative Research}\\[10pt]
{\LARGE\textbf{MOCK EXAM @@NR@@}}\\[8pt]
{\normalsize\itshape Practice exam for exam preparation -- not the actual module examination}\\[12pt]
{\large Prof.\ Dr.\ Christoph Weisser}
\end{center}

\vspace{0.6em}
@@RULES@@
\vfill
\begin{center}
{\clover[0.62]\par}
\vspace{6pt}
{\Large\itshape\color{cloverdark}Good luck!}
\end{center}
\vspace{1em}
\end{titlepage}
\setcounter{page}{2}
"""

# ---------------------------------------------------------------- solutions
SOL_PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[british]{babel}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb,mathpazo}
\renewcommand{\ttdefault}{lmtt}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{float}
\usepackage[justification=centering]{caption}% for \caption*
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage[a4paper,margin=2.2cm]{geometry}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{mdframed}
\usepackage{environ}
\usepackage{needspace}
\usepackage{listings}
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue!55!black,linktoc=all,
  pdftitle={Quantitative Research -- Mock Exam @@NR@@ -- Solutions},
  pdfauthor={Prof. Dr. Christoph Weisser}}
\sloppy
""" + HSBI_COLOURS + r"""
\pagestyle{fancy}
\fancyhf{}
\rhead{\small Quantitative Research}
\lhead{\small Mock Exam @@NR@@ -- Solutions and grading key}
\cfoot{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\headheight}{14pt}

\lstdefinestyle{Pystyle}{language=Python, basicstyle=\ttfamily\small,
  keywordstyle=\color{hsbiblau}, commentstyle=\color{hsbigrau!70!black}\itshape,
  stringstyle=\color{teal}, showstringspaces=false, upquote=true,
  columns=fixed, basewidth=0.5em, xleftmargin=1.2em, aboveskip=4pt, belowskip=4pt}
\lstdefinestyle{Pyout}{language={}, basicstyle=\ttfamily\footnotesize,
  keywordstyle={}, commentstyle={}, stringstyle={}, columns=fixed, keepspaces=true,
  basewidth=0.52em, showstringspaces=false, upquote=true, aboveskip=4pt, belowskip=4pt}
\lstset{style=Pystyle}

\newmdenv[linecolor=hsbiblau!70,backgroundcolor=hsbiblau!5,linewidth=0.8pt,
  innertopmargin=6pt,innerbottommargin=8pt,innerleftmargin=9pt,innerrightmargin=9pt,
  skipabove=4pt,skipbelow=8pt]{scenariobox}
\newmdenv[linecolor=hsbirot!70,backgroundcolor=hsbirot!5,linewidth=0.8pt,
  innertopmargin=5pt,innerbottommargin=6pt,innerleftmargin=9pt,innerrightmargin=9pt,
  skipabove=6pt,skipbelow=6pt]{mistakeboxframe}
%% the mistake box is never split: if it does not fit completely on the page,
%% it starts on the next one (no single line / heading at the bottom of a page)
\newsavebox{\mistakeboxmeasure}
\NewEnviron{mistakebox}{\par
  \sbox{\mistakeboxmeasure}{\begin{minipage}{\linewidth}%
    \begin{mistakeboxframe}\BODY\end{mistakeboxframe}\end{minipage}}%
  \Needspace{\dimexpr\ht\mistakeboxmeasure+\dp\mistakeboxmeasure+\baselineskip\relax}%
  \begin{mistakeboxframe}\BODY\end{mistakeboxframe}}
\newmdenv[linecolor=teal!55,backgroundcolor=teal!7,linewidth=0.8pt,
  innertopmargin=5pt,innerbottommargin=7pt,innerleftmargin=9pt,innerrightmargin=9pt,
  skipabove=4pt,skipbelow=8pt]{conceptbox}

%% highlighted final result
\newcommand{\result}[1]{\par\nopagebreak[4]\vspace{2pt}%
  \noindent\fcolorbox{hsbigruen}{hsbigruen!8}{\parbox{0.965\linewidth}{%
  \textbf{Result:}~#1}}\par\nopagebreak[4]\vspace{2pt}}
%% grading rubric of a subtask
\newcommand{\rubric}[1]{\par\nopagebreak[4]\vspace{1pt}%
  \noindent{\footnotesize\textcolor{black!62}{\textbf{Grading (2 P.):} #1}}\par\vspace{2pt}}
%% typical mistake of a subtask (optional)
\newcommand{\mistake}[1]{\par\nopagebreak[4]\noindent{\footnotesize\textcolor{hsbirot!85!black}{\textbf{Typical mistake:} #1}}\par\vspace{4pt}}
\newcommand{\lectureref}[1]{\noindent\textcolor{black!62}{\small$\hookrightarrow$\,\textit{Lecture reference:} #1}\par\vspace{4pt}}

\setlist[enumerate,1]{leftmargin=*}

\title{\vspace{-1.2cm}\textbf{Quantitative Research -- Mock Exam @@NR@@}\\[2pt]
\large Solutions, results overview and grading rubric}
\author{Prof.\ Dr.\ Christoph Weisser}
\date{}

\begin{document}
\maketitle
\thispagestyle{fancy}
\vspace{-0.7cm}

\noindent\small\textbf{Structure.} Section~\ref{sec:overview} lists all 30 final results
on one page (quick grading pass). Then, for every subtask, follow the worked solution, the
highlighted final result and a \emph{grading rubric} for the 2 points.\normalsize

\medskip
"""

# ---------------------------------------------------------------- slides
SLIDES_PREAMBLE = r"""%% ============================================================
%% Quantitative Research -- discussion of Mock Exam @@NR@@ (solutions)
%% Layout, colours and code styles as in common/preamble.tex of the lecture.
%% ============================================================
\documentclass[aspectratio=169,11pt]{beamer}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[british]{babel}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{mathtools}
\usepackage{xcolor}
\usepackage{colortbl}
\usepackage{array}
\usepackage{listings}
\usepackage{hyperref}
\hypersetup{pdftitle={Quantitative Research -- Mock Exam @@NR@@ -- Slides},
  pdfauthor={Prof. Dr. Christoph Weisser}}

%% sans-serif \mathrm and \mathbf (as in the lecture decks)
\renewcommand{\bfdefault}{bx}
\DeclareMathAlphabet{\mathrm}{T1}{cmss}{m}{n}
\DeclareMathAlphabet{\mathbf}{T1}{cmss}{bx}{n}
\SetMathAlphabet{\mathrm}{bold}{T1}{cmss}{bx}{n}
\SetMathAlphabet{\mathbf}{bold}{T1}{cmss}{bx}{n}
\SetSymbolFont{operators}{bold}{OT1}{cmss}{bx}{n}
\AtBeginDocument{\SetMathAlphabet{\mathrm}{normal}{T1}{cmss}{m}{n}%
                 \SetMathAlphabet{\mathrm}{bold}{T1}{cmss}{bx}{n}}
""" + HSBI_COLOURS + r"""
\usetheme{Madrid}
\usecolortheme{default}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{blocks}[rounded][shadow=false]
\setbeamerfont{section in head/foot}{size=\tiny}

\setbeamertemplate{headline}{%
  \leavevmode%
  \hbox{%
    \begin{beamercolorbox}[wd=\paperwidth,ht=2.5ex,dp=1.125ex]{section in head/foot}%
      \scriptsize\insertsectionnavigationhorizontal{\paperwidth}{}{\hskip0pt plus1filll}%
    \end{beamercolorbox}%
  }%
}
\newcommand{\footsection}{%
  \setbox0=\hbox{\insertsection}%
  \ifdim\wd0>0pt\ \textbar\ \insertsection\fi}
\setbeamertemplate{footline}{%
  \leavevmode%
  \hbox{%
  \begin{beamercolorbox}[wd=\paperwidth,ht=2.5ex,dp=1.125ex]{author in head/foot}%
    \hspace*{2em}Mock Exam~@@NR@@\footsection\hfill\insertframenumber{}/\inserttotalframenumber\hspace*{2em}%
  \end{beamercolorbox}%
  }%
}

\AtBeginSection[]{%
  \begin{frame}{Overview}
    \tableofcontents[currentsection,sectionstyle=show/shaded,subsectionstyle=show/show/hide]
  \end{frame}
}

\lstdefinestyle{Pystyle}{
  language=Python,
  basicstyle=\ttfamily\footnotesize,
  keywordstyle=\color{hsbiblau},
  commentstyle=\color{hsbigrau}\itshape,
  stringstyle=\color{teal},
  showstringspaces=false,
  literate={~}{{$\sim$}}1,
  upquote=true,
  columns=fixed, basewidth=0.5em
}
\lstdefinestyle{Pyout}{
  language={},
  basicstyle=\ttfamily\scriptsize,
  keywordstyle={}, commentstyle={}, stringstyle={},
  columns=fixed, keepspaces=true, basewidth=0.52em,
  showstringspaces=false,
  upquote=true
}
\lstset{style=Pystyle}

\renewcommand{\textasciitilde}{\ensuremath{\sim}}
\newcommand{\kernaussage}[1]{\begin{alertblock}{Key takeaway}#1\end{alertblock}}
\newcommand{\inworten}[1]{{\small\textbf{\textcolor{hsbiblaudunkel}{In words:}}~#1}}

\title{Quantitative Research -- Mock Exam @@NR@@}
\subtitle{Discussion of the solutions}
\author{Prof.\ Dr.\ Christoph Weisser}
\institute{}
\date{}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Contents}
  \tableofcontents[hideallsubsections]
\end{frame}
"""
