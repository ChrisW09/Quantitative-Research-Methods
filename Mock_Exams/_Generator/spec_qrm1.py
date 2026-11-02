# -*- coding: utf-8 -*-
"""Content of Mock Exam 1 (Quantitative Research).

Task 1 -- Part 3 (Statistical Inference), Task 2 -- Part 4 (Regression),
Task 3 -- Part 5 (Classification). Every subtask asks for exactly one result and
states all the numbers it needs. All results are recomputed by verify.py.
"""
import os

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Mock_Exam_1")

# ======================================================================== Task 1
T1 = dict(
    nr=1, topic=r"Statistical inference: \texorpdfstring{$z$}{z}-test and confidence interval",
    short_scenario="Order values of an online shop",
    intro=r"""An online shop for sports equipment plans with a mean order value of
$\mu_0 = 80$~EUR. From many years of experience, the standard deviation of the order
values is known: $\sigma = 12$~EUR. After a redesign of the website, a random sample of
$n = 36$ orders gives a mean order value of $\bar x = 84.30$~EUR.
The significance level is $\alpha = 0.05$. Because $\sigma$ is known, the test and the
confidence interval are based on the standard normal distribution (Table~1).

\medskip
\noindent\textit{All subtasks can be solved independently of each other.}
""",
    scenario=r"""Two-sided $z$-test ($\sigma$ known) of the mean order value of an online shop:
$\mu_0 = 80$~EUR, $\sigma = 12$~EUR, $n = 36$, $\bar x = 84.30$~EUR, $\alpha = 0.05$.
Asked for are the test in its steps, the $p$-value, the $95\,\%$ confidence interval, two
interpretations and the Python command for the $t$-test.""",
    slide_scenario=r"""
  \begin{block}{Order values after the website redesign}
    Planning figure $\mu_0 = 80$~EUR, \quad known $\sigma = 12$~EUR\\[2pt]
    Random sample: $n = 36$ orders, \quad $\bar x = 84.30$~EUR, \quad $\alpha = 0.05$
  \end{block}
  \begin{itemize}\setlength{\itemsep}{3pt}
    \item Question: has the mean order value \emph{changed} (in either direction)?
          $\Rightarrow$ \textbf{two-sided} test.
    \item $\sigma$ known $\Rightarrow$ $Z_n$ and the $\Phi$-table; \ $\sqrt{36} = 6$ keeps the numbers clean.
  \end{itemize}""",
    lecture_ref=r"""Part~3, sections \emph{Confidence Intervals} (known variance),
\emph{Hypothesis Tests}, \emph{The $p$-Value} and \emph{Types of Error}; Python: slide
``Hypothesis test with Python -- \texttt{ttest\_1samp}'' and Summary~6.""",
    concepts=[
        r"\textbf{Standard error} ($\sigma$ known): $\mathrm{SE} = \sigma/\sqrt{n}$ -- how strongly $\bar X$ fluctuates around $\mu$.",
        r"\textbf{Test statistic:} $Z_n = \dfrac{\bar X-\mu_0}{\sigma/\sqrt{n}} \sim N(0,1)$ under $H_0$; two-sided: reject $H_0$ if $|Z_n| > z_{1-\alpha/2}$.",
        r"\textbf{$p$-value} (two-sided): $p = 2\,\Phi(-|Z_n|)$; reject $H_0$ if $p < \alpha$.",
        r"\textbf{Confidence interval:} $\text{CI}_{1-\alpha} = \bigl[\bar X \pm z_{1-\alpha/2}\,\sigma/\sqrt{n}\bigr]$; $\mu_0$ outside the CI $\Leftrightarrow$ reject $H_0$ (duality).",
        r"\textbf{Type~I error:} reject $H_0$ although $H_0$ is true (false alarm); its probability is $\alpha$.",
    ],
    items=[
        dict(label=r"Hypothesis pair",
             q=r"The management wants to find out whether the mean order value after the redesign \emph{differs} from the planning figure of $80$~EUR (in either direction). State the hypothesis pair.",
             short=r"$H_0\colon \mu = 80$ vs.\ $H_1\colon \mu \neq 80$",
             result=r"$H_0\colon \mu = 80$ \ vs.\ \ $H_1\colon \mu \neq 80$ \ (two-sided)",
             rubric=r"1 P. $H_1\colon \mu \neq 80$ (two-sided alternative), 1 P. matching $H_0\colon \mu = 80$.",
             mistake=r"hypotheses written with $\bar x$ instead of $\mu$, or a one-sided $H_1$ although both directions matter.",
             solution=r"""The statement the management wants to find evidence for -- the mean order value
\emph{differs} from the plan -- goes into $H_1$. Because a deviation in either direction
counts, the test is two-sided:
\[ H_0\colon \mu = 80 \qquad\text{vs.}\qquad H_1\colon \mu \neq 80 . \]
Here $\mu$ is the unknown mean order value of \emph{all} orders after the redesign.
Hypotheses are always statements about the population parameter, never about $\bar x$."""),
        dict(label=r"Standard error",
             q=r"Compute the standard error $\sigma/\sqrt{n}$ of the sample mean for $\sigma = 12$~EUR and $n = 36$.",
             short=r"$\sigma/\sqrt{n} = 12/6 = 2$~EUR",
             result=r"$\dfrac{\sigma}{\sqrt{n}} = \dfrac{12}{\sqrt{36}} = \dfrac{12}{6} = 2$~EUR",
             rubric=r"1 P. formula with $\sqrt{36} = 6$, 1 P. result $2$.",
             mistake=r"dividing by $n$ ($0.33$) or by $\sqrt{n-1}$ instead of $\sqrt{n}$.",
             solution=r"""\[ \mathrm{SE} = \frac{\sigma}{\sqrt{n}} = \frac{12}{\sqrt{36}} = \frac{12}{6} = 2 \text{ EUR}. \]
The mean of $36$ orders fluctuates much less than a single order value: its standard
deviation is only one sixth of $\sigma$."""),
        dict(label=r"Test statistic $Z_n$",
             q=r"Compute the test statistic $Z_n$ for $\bar x = 84.30$~EUR, $\mu_0 = 80$~EUR, $\sigma = 12$~EUR and $n = 36$.",
             short=r"$Z_n = 4.30/2 = 2.15$",
             result=r"$Z_n = \dfrac{84.30-80}{12/\sqrt{36}} = \dfrac{4.30}{2} = 2.15$",
             rubric=r"1 P. formula with correct substitution, 1 P. result $2.15$.",
             solution=r"""\[ Z_n = \frac{\bar x-\mu_0}{\sigma/\sqrt{n}} = \frac{84.30-80}{12/\sqrt{36}}
   = \frac{4.30}{2} = 2.15 . \]
The sample mean lies $2.15$ standard errors \emph{above} the hypothesised value
$\mu_0 = 80$~EUR."""),
        dict(label=r"Critical value",
             q=r"State the critical value of the two-sided test at the significance level $\alpha = 0.05$ ($\sigma$ known; use Table~1).",
             short=r"$z_{1-\alpha/2} = z_{0.975} = 1.96$",
             result=r"$z_{1-\alpha/2} = z_{0.975} = 1.96$ \ (reject $H_0$ if $|Z_n| > 1.96$)",
             rubric=r"1 P. two-sided quantile $z_{1-\alpha/2} = z_{0.975}$ ($\alpha$ split), 1 P. value $1.96$ from the table (also accepted: $\pm 1.96$).",
             mistake=r"using the one-sided quantile $z_{0.95} = 1.645$.",
             solution=r"""Two-sided test: $\alpha$ is split into two tails of $\alpha/2 = 0.025$ each, so the
$1-\alpha/2 = 0.975$ quantile is needed. Search $0.9750$ \emph{inside} Table~1: row $1.9$,
column $0.06$, hence
\[ z_{1-\alpha/2} = z_{0.975} = 1.96 . \]
$H_0$ is rejected if $|Z_n| > 1.96$, i.e.\ if $Z_n < -1.96$ or $Z_n > 1.96$."""),
        dict(label=r"Test decision",
             q=r"The test statistic is $Z_n = 2.15$ and the critical value is $z_{0.975} = 1.96$. Make the test decision for $H_0\colon \mu = 80$ vs.\ $H_1\colon \mu \neq 80$ at $\alpha = 0.05$.",
             short=r"$|Z_n| = 2.15 > 1.96$ $\Rightarrow$ reject $H_0$",
             result=r"Since $|Z_n| = 2.15 > 1.96 = z_{0.975}$, $H_0$ is \textbf{rejected}: the mean order value differs significantly from $80$~EUR.",
             rubric=r"1 P. comparison $|Z_n| = 2.15 > 1.96$, 1 P. decision ``reject $H_0$''.",
             solution=r"""Rejection region of the two-sided test: $|Z_n| > z_{0.975}$. Here
\[ |Z_n| = 2.15 \;>\; 1.96 = z_{0.975} , \]
so the test statistic lies in the rejection region and $H_0\colon \mu = 80$ is rejected at
the $5\,\%$ level. The data provide evidence that the mean order value after the redesign
differs from $80$~EUR -- the sample points to a \emph{higher} value ($\bar x = 84.30$)."""),
        dict(label=r"$p$-value",
             q=r"Compute the two-sided $p$-value for the test statistic $Z_n = 2.15$ (use Table~1).",
             short=r"$p = 2\,(1-0.9842) = 0.0316$",
             result=r"$p = 2\,\Phi(-|Z_n|) = 2\,\bigl(1-\Phi(2.15)\bigr) = 2\,(1-0.9842) = 0.0316$",
             rubric=r"1 P. $\Phi(2.15) = 0.9842$ from the table, 1 P. doubling and result $0.0316$.",
             mistake=r"forgetting the factor $2$ ($0.0158$) or reporting $\Phi(2.15) = 0.9842$ itself.",
             solution=r"""For $H_1\colon \mu \neq \mu_0$ both tails count:
\[ p = 2\,\Phi(-|Z_n|) = 2\,\bigl(1-\Phi(2.15)\bigr). \]
Table~1, row $2.1$, column $0.05$: $\Phi(2.15) = 0.9842$. Hence
\[ p = 2\,(1-0.9842) = 2\cdot 0.0158 = 0.0316 . \]
Because $p = 0.0316 < 0.05 = \alpha$, the $p$-value leads to the same decision as the
critical value: reject $H_0$. (Python: \texttt{2 * stats.norm.sf(2.15)} gives $0.0316$.)"""),
        dict(label=r"$95\,\%$ confidence interval",
             q=r"Compute the $95\,\%$ confidence interval for $\mu$ with $\bar x = 84.30$~EUR, $\sigma/\sqrt{n} = 2$~EUR and $z_{0.975} = 1.96$.",
             short=r"$84.30 \pm 3.92 = [80.38;\ 88.22]$~EUR",
             result=r"$84.30 \pm 1.96\cdot 2 = 84.30 \pm 3.92$, \ $\text{CI}_{0.95} = [80.38;\ 88.22]$~EUR",
             rubric=r"1 P. formula $\bar x \pm z_{0.975}\,\sigma/\sqrt{n}$ (margin of error $3.92$), 1 P. both bounds correct.",
             solution=r"""\[ \text{CI}_{0.95} = \Bigl[\bar x - z_{0.975}\frac{\sigma}{\sqrt n};\ \bar x + z_{0.975}\frac{\sigma}{\sqrt n}\Bigr],
   \qquad e = 1.96\cdot 2 = 3.92 \]
\[ \text{CI}_{0.95} = [84.30-3.92;\ 84.30+3.92] = [80.38;\ 88.22] \text{ EUR}. \]
\emph{Duality:} the planning figure $\mu_0 = 80$ lies \emph{outside} the interval -- this
agrees with the rejection of $H_0\colon \mu = 80$ by the two-sided test at $\alpha = 0.05$."""),
        dict(label=r"Interpretation of the CI", kind="satz",
             q=r"For the mean order value $\mu$, the $95\,\%$ confidence interval $[80.38;\ 88.22]$~EUR was computed. Interpret this interval in one sentence.",
             short=r"with $95\,\%$ confidence, the mean $\mu$ of \emph{all} orders lies in $[80.38;\ 88.22]$~EUR",
             result=r"With $95\,\%$ confidence, the true mean order value $\mu$ of \emph{all} orders after the redesign lies between $80.38$ and $88.22$~EUR -- intervals constructed in this way contain the true $\mu$ in $95\,\%$ of all samples.",
             rubric=r"1 P. statement about the true mean $\mu$ of all orders (not about single orders or $\bar x$), 1 P. correct reading of the $95\,\%$ (confidence in the procedure / values compatible with the data).",
             mistake=r"``$95\,\%$ of all orders have a value between $80.38$ and $88.22$~EUR'' (0 P.).",
             solution=r"""The lecture gives three correct readings: \emph{coverage} (the procedure yields
intervals that contain the fixed true $\mu$ in $95\,\%$ of all samples), \emph{compatibility}
(the interval holds the values of $\mu$ that are consistent with the data) and
\emph{duality} (it holds exactly the $\mu_0$ a two-sided test at $\alpha = 0.05$ would not reject).

\smallskip
\noindent\emph{Model answer:} ``With $95\,\%$ confidence, the mean order value of all orders
after the redesign lies between $80.38$ and $88.22$~EUR.''

\smallskip
\noindent Not correct: ``$95\,\%$ of the orders lie in the interval'' (the CI is about the
\emph{mean}, not about single orders). Strictly speaking also wrong: ``$\mu$ lies in
\emph{this} interval with probability $95\,\%$'' ($\mu$ is fixed; the bounds are random)
-- 1~P."""),
        dict(label=r"Type I error in context", kind="satz",
             q=r"Describe in one sentence what a Type~I error would mean in this situation.",
             short=r"rejecting $H_0$ (``mean changed'') although $\mu = 80$~EUR still holds",
             result=r"A Type~I error means that the shop concludes that the mean order value has changed (rejects $H_0\colon \mu = 80$) although it is in fact still $80$~EUR -- a false alarm, whose probability is $\alpha = 0.05$.",
             rubric=r"1 P. ``reject $H_0$ / conclude a change'', 1 P. ``although $H_0$ is true ($\mu = 80$~EUR)'' -- in the context of the order value.",
             mistake=r"describing the Type~II error (keeping $H_0$ although the mean has changed).",
             solution=r"""Type~I error $=$ reject $H_0$ although $H_0$ is true (false alarm):
\[ P(\text{reject } H_0 \mid H_0 \text{ true}) = \alpha = 0.05 . \]
In this situation: the shop concludes that the redesign has changed the mean order value,
although the mean of all orders is in fact still $80$~EUR. Because $H_0$ was rejected here,
a Type~I error is the only error the test can have made. (A Type~II error would be:
keeping $H_0$ although the mean has changed.)"""),
        dict(label=r"Python command ($t$-test)", python=True,
             q=r"In practice $\sigma$ is often unknown. Suppose the 36 order values are stored in a NumPy array \texttt{orders} and $\sigma$ is estimated from the data. Give the \texttt{scipy.stats} command that carries out the two-sided one-sample $t$-test of $H_0\colon \mu = 80$.",
             short=r"\texttt{stats.ttest\_1samp(orders, popmean=80)}",
             result=r"\texttt{stats.ttest\_1samp(orders, popmean=80)}",
             rubric=r'1 P. function \texttt{stats.ttest\_1samp}, 1 P. arguments \texttt{orders} and \texttt{popmean=80} (also accepted: \texttt{stats.ttest\_1samp(orders, 80)}, the prefix \texttt{scipy.stats.}, with or without \texttt{alternative="two-sided"}).',
             solution=r"""\begin{lstlisting}
from scipy import stats
res = stats.ttest_1samp(orders, popmean=80)   # two-sided by default
res.statistic, res.df, res.pvalue             # T_n, n - 1 = 35, p-value
\end{lstlisting}
\texttt{ttest\_1samp} estimates $\sigma$ by $s$ and compares $T_n$ with the
$t$-distribution with $n-1 = 35$ degrees of freedom. The default
\texttt{alternative="two-sided"} matches $H_1\colon \mu \neq 80$; one-sided tests would
need \texttt{alternative="less"} or \texttt{"greater"}."""),
    ],
    figs_sol=[
        ("qrm1_t1_ztest.pdf", "0.62", r"Standard normal distribution under $H_0$: rejection region $|Z_n| > 1.96$ (orange, $\alpha/2 = 0.025$ per tail) and the observed $Z_n = 2.15$."),
        ("qrm1_t1_ci.pdf", "0.70", r"$95\,\%$ confidence interval $[80.38;\ 88.22]$: the planning figure $\mu_0 = 80$ lies outside $\Rightarrow$ reject $H_0$."),
    ],
    figs_slides=[
        ("qrm1_t1_ztest.pdf", "0.78", r"Task 1 -- rejection region and test statistic"),
        ("qrm1_t1_ci.pdf", "0.62", r"Task 1 -- confidence interval and duality"),
    ],
    slides_detail=[
        (r"Task 1 -- the test step by step", r"""
  \begin{center}\small
  \renewcommand{\arraystretch}{1.3}
  \begin{tabular}{@{}llll@{}}
    \toprule
    Step & Formula & Numbers & Value\\
    \midrule
    Hypotheses & $H_0\colon\mu = \mu_0$ vs.\ $H_1\colon\mu \neq \mu_0$ & $\mu_0 = 80$ & two-sided\\
    Standard error & $\sigma/\sqrt{n}$ & $12/\sqrt{36}$ & $2$\\
    Test statistic & $Z_n = (\bar x-\mu_0)/(\sigma/\sqrt{n})$ & $(84.30-80)/2$ & $2.15$\\
    Critical value & $z_{1-\alpha/2}$ & $z_{0.975}$ & $1.96$\\
    Decision & $|Z_n| > z_{1-\alpha/2}$\,? & $2.15 > 1.96$ & reject $H_0$\\
    $p$-value & $2\,\Phi(-|Z_n|)$ & $2\,(1-0.9842)$ & $0.0316$\\
    $95\,\%$ CI & $\bar x \pm z_{0.975}\,\sigma/\sqrt{n}$ & $84.30 \pm 3.92$ & $[80.38;\ 88.22]$\\
    \bottomrule
  \end{tabular}
  \end{center}"""),
        (r"Task 1 -- three routes, one verdict", r"""
  \begin{columns}[T]
    \column{0.31\textwidth}
    \begin{block}{Critical value}
      $|Z_n| = 2.15$\\ $z_{0.975} = 1.96$\\[2pt]
      $2.15 > 1.96$\\ $\Rightarrow$ \textbf{reject} $H_0$
    \end{block}
    \column{0.31\textwidth}
    \begin{block}{$p$-value}
      $p = 2\,(1-\Phi(2.15))$\\ $\phantom{p} = 0.0316$\\[2pt]
      $0.0316 < 0.05$\\ $\Rightarrow$ \textbf{reject} $H_0$
    \end{block}
    \column{0.31\textwidth}
    \begin{block}{Confidence interval}
      $[80.38;\ 88.22]$\\ $\mu_0 = 80$ outside\\[2pt]
      \phantom{x}\\ $\Rightarrow$ \textbf{reject} $H_0$
    \end{block}
  \end{columns}
  \medskip
  \begin{itemize}\setlength{\itemsep}{2pt}
    \item Type~I error here: ``the mean changed'' although it is still $80$~EUR -- probability $\alpha = 0.05$.
    \item $\sigma$ unknown in practice: \texttt{stats.ttest\_1samp(orders, popmean=80)} (two-sided by default, $t_{35}$).
  \end{itemize}
  \kernaussage{Critical value, $p$-value and CI are three views of the same test -- they always agree.}"""),
    ],
    mistakes=[
        r"Using the one-sided quantile $z_{0.95} = 1.645$ for the two-sided test.",
        r"Forgetting the factor $2$ in the two-sided $p$-value ($0.0158$ instead of $0.0316$).",
        r"Standard error with $n$ or $n-1$ instead of $\sqrt{n}$.",
        r"Reading the CI as the range of single order values, or as ``$95\,\%$ probability for \emph{this} interval''.",
        r"Mixing up the Type~I error (false alarm: reject a true $H_0$) and the Type~II error (miss).",
    ],
)

# ======================================================================== Task 2
CAFE_OUTPUT = r"""Dep. Variable:                  sales   R-squared:                       0.947
Model:                            OLS   Adj. R-squared:                  0.945
Method:                 Least Squares   F-statistic:                     512.4
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept    -12.2152      3.783     -3.229      0.002     -19.790      -4.641
temp           3.0055      0.131     22.863      0.000       2.742       3.269
rain          -0.4313      0.374     -1.154      0.253      -1.180       0.317"""

T2 = dict(
    nr=2, topic=r"Simple and multiple linear regression",
    short_scenario="Temperature and iced-coffee sales of a caf\\'e",
    intro=r"""\textbf{Part A (subtasks a--h).} A caf\'e records on five summer days the daily
maximum temperature $x$ (in $^{\circ}$C) and the number $y$ of iced coffees sold:

\medskip
\begin{center}
\begin{tabular}{lccccc}
\toprule
Day $i$ & 1 & 2 & 3 & 4 & 5\\
\midrule
Maximum temperature $x_i$ ($^{\circ}$C) & 20 & 22 & 24 & 26 & 28\\
Iced coffees sold $y_i$ & 46 & 54 & 62 & 70 & 68\\
\bottomrule
\end{tabular}
\end{center}

\medskip
\noindent Model: $y_i = \beta_0 + \beta_1 x_i + u_i$. Auxiliary values:
\begin{gather*}
\bar x = 24, \qquad \bar y = 60, \qquad S_{xx} = \sum (x_i-\bar x)^2 = 40,\\
S_{xy} = \sum (x_i-\bar x)(y_i-\bar y) = 120, \qquad S_{yy} = \sum (y_i-\bar y)^2 = 400.
\end{gather*}

\medskip
\noindent\textbf{Part B (subtasks i--j).} For a larger sample of $n = 60$ summer days the
caf\'e also records the rainfall \texttt{rain} (in mm) and estimates a multiple linear
regression of \texttt{sales} (iced coffees sold) on \texttt{temp} (maximum temperature in
$^{\circ}$C) and \texttt{rain}. Excerpt of the \texttt{statsmodels} output:
\begin{footnotesize}
\begin{verbatim}
""" + CAFE_OUTPUT + r"""
\end{verbatim}
\end{footnotesize}

\noindent\textit{All subtasks can be solved independently of each other.}
""",
    scenario=r"""Part~A: simple regression of the number of iced coffees sold ($y$) on the daily
maximum temperature ($x$, in $^{\circ}$C), $n = 5$; $\bar x = 24$, $\bar y = 60$,
$S_{xx} = 40$, $S_{xy} = 120$, $S_{yy} = 400$. Part~B: \texttt{statsmodels} output of the
multiple regression \texttt{sales \textasciitilde{} temp + rain} for $n = 60$ days.""",
    slide_scenario=r"""
  \begin{columns}[T]
    \column{0.47\textwidth}
    \begin{block}{Part A: five summer days}
      \begin{center}\small
      \begin{tabular}{lccccc}
        \toprule
        $x_i$ ($^{\circ}$C) & 20 & 22 & 24 & 26 & 28\\
        $y_i$ & 46 & 54 & 62 & 70 & 68\\
        \bottomrule
      \end{tabular}
      \end{center}
      \small $\bar x = 24$, $\bar y = 60$\\
      $S_{xx} = 40$, $S_{xy} = 120$, $S_{yy} = 400$
    \end{block}
    \column{0.49\textwidth}
    \begin{block}{Part B: 60 days, two explanatory variables}
      \small \texttt{sales \textasciitilde{} temp + rain}\\[3pt]
      \begin{tabular}{lrr}
        \toprule
        & coef & \texttt{P>|t|}\\
        \midrule
        \texttt{temp} & $3.0055$ & $0.000$\\
        \texttt{rain} & $-0.4313$ & $0.253$\\
        \bottomrule
      \end{tabular}
    \end{block}
  \end{columns}""",
    lecture_ref=r"""Part~4, sections \emph{Simple Linear Regression} (least squares,
interpretation), \emph{Goodness of Fit: the Coefficient of Determination} and
\emph{Multiple Linear Regression} (ceteris paribus, $t$-test of a coefficient); Python:
Summary~5.""",
    concepts=[
        r"\textbf{OLS estimators:} $\hat\beta_1 = S_{xy}/S_{xx}$, \ $\hat\beta_0 = \bar y - \hat\beta_1\bar x$; \ line $\hat y = \hat\beta_0 + \hat\beta_1 x$.",
        r"\textbf{Residual:} $\hat u_i = y_i - \hat y_i$ -- positive: point above the line, negative: below.",
        r"\textbf{Sum-of-squares decomposition:} $\text{TSS} = \text{ESS} + \text{RSS}$, \ $R^2 = \text{ESS}/\text{TSS} = 1 - \text{RSS}/\text{TSS}$.",
        r"\textbf{Correlation} (simple regression): $R^2 = r_{xy}^2$, so $r_{xy} = \pm\sqrt{R^2}$ with the sign of $\hat\beta_1$.",
        r"\textbf{Multiple regression:} $\hat\beta_j$ = change of $y$ per unit of $x_j$ \emph{holding the other variables fixed}; $H_0\colon \beta_j = 0$ is rejected if $p < \alpha$.",
    ],
    items=[
        dict(label=r"Slope $\hat\beta_1$",
             q=r"Compute the slope $\hat\beta_1$ from $S_{xy} = 120$ and $S_{xx} = 40$.",
             short=r"$\hat\beta_1 = 120/40 = 3$",
             result=r"$\hat\beta_1 = \dfrac{S_{xy}}{S_{xx}} = \dfrac{120}{40} = 3$ (iced coffees per $^{\circ}$C)",
             rubric=r"1 P. formula $S_{xy}/S_{xx}$, 1 P. result $3$.",
             mistake=r"inverted ratio $S_{xx}/S_{xy} = 0.33$.",
             solution=r"""\[ \hat\beta_1 = \frac{S_{xy}}{S_{xx}} = \frac{120}{40} = 3 . \]
The slope has the sign of $S_{xy}$: the cloud of points rises."""),
        dict(label=r"Intercept $\hat\beta_0$",
             q=r"Compute the intercept $\hat\beta_0$ from $\hat\beta_1 = 3$, $\bar x = 24$ and $\bar y = 60$.",
             short=r"$\hat\beta_0 = 60 - 3\cdot 24 = -12$",
             result=r"$\hat\beta_0 = \bar y - \hat\beta_1\bar x = 60 - 3\cdot 24 = -12$",
             rubric=r"1 P. formula $\bar y - \hat\beta_1\bar x$, 1 P. result $-12$ (with sign).",
             solution=r"""\[ \hat\beta_0 = \bar y - \hat\beta_1\,\bar x = 60 - 3\cdot 24 = 60 - 72 = -12 . \]
Estimated line: $\hat y = -12 + 3x$; it passes through the centroid $(\bar x,\bar y) = (24;\ 60)$.
The intercept has no sensible meaning of its own: $x = 0$\,$^{\circ}$C lies far outside the
observed range $20$--$28$\,$^{\circ}$C (extrapolation)."""),
        dict(label=r"Interpretation of the slope", kind="satz",
             q=r"Interpret the slope $\hat\beta_1 = 3$ in one sentence in the context of the caf\'e.",
             short=r"$1$\,$^{\circ}$C warmer $\Rightarrow$ on average about $3$ more iced coffees sold",
             result=r"On a day that is $1$\,$^{\circ}$C warmer, the caf\'e sells on average about $3$ more iced coffees.",
             rubric=r"1 P. ``per additional $1$\,$^{\circ}$C'', 1 P. ``on average $3$ more iced coffees''.",
             mistake=r"no units, or a causal claim (``the heat causes exactly 3 additional sales'').",
             solution=r"""$\hat\beta_1$ is the change of $\hat y$ when $x$ increases by one unit. Here: one degree
Celsius more goes along with, on average, $3$ more iced coffees sold per day. The line
describes an association within the observed range ($20$--$28$\,$^{\circ}$C); it does not
prove a causal effect, and it should not be extended far beyond the data."""),
        dict(label=r"Prediction at $x = 25$\,$^{\circ}$C",
             q=r"Use the estimated regression line $\hat y = -12 + 3x$ to predict the number of iced coffees sold on a day with a maximum temperature of $x = 25$\,$^{\circ}$C.",
             short=r"$\hat y(25) = -12 + 75 = 63$ iced coffees",
             result=r"$\hat y(25) = -12 + 3\cdot 25 = 63$ iced coffees",
             rubric=r"1 P. substitution of $x = 25$, 1 P. result $63$.",
             solution=r"""\[ \hat y(25) = -12 + 3\cdot 25 = -12 + 75 = 63 . \]
$x = 25$ lies within the observed range $[20;\ 28]$, so this is an interpolation -- no
extrapolation problem."""),
        dict(label=r"Residual of day 5",
             q=r"Compute the residual $\hat u_5$ of day~5 with $(x_5;\ y_5) = (28;\ 68)$, using the estimated regression line $\hat y = -12 + 3x$.",
             short=r"$\hat u_5 = 68 - 72 = -4$",
             result=r"$\hat y_5 = -12 + 3\cdot 28 = 72$, \ $\hat u_5 = y_5 - \hat y_5 = 68 - 72 = -4$",
             rubric=r"1 P. fitted value $\hat y_5 = 72$, 1 P. residual $-4$ with the correct sign.",
             mistake=r"residual with the wrong sign ($\hat y_5 - y_5 = +4$).",
             solution=r"""\[ \hat y_5 = -12 + 3\cdot 28 = 72, \qquad \hat u_5 = y_5 - \hat y_5 = 68 - 72 = -4 . \]
On day~5 the caf\'e sold $4$ iced coffees fewer than the line predicts; the point lies
\emph{below} the line. (All residuals: $-2,\ 0,\ +2,\ +4,\ -4$; they add up to $0$.)"""),
        dict(label=r"Coefficient of determination $R^2$",
             q=r"For the five days, the total sum of squares is $\text{TSS} = 400$ and the residual sum of squares is $\text{RSS} = 40$. Compute the coefficient of determination $R^2$.",
             short=r"$R^2 = 1 - 40/400 = 0.9$",
             result=r"$R^2 = 1 - \dfrac{\text{RSS}}{\text{TSS}} = 1 - \dfrac{40}{400} = 0.9$",
             rubric=r"1 P. formula $1 - \text{RSS}/\text{TSS}$ (or $\text{ESS}/\text{TSS}$ with $\text{ESS} = 360$), 1 P. result $0.9$.",
             mistake=r"$R^2 = \text{RSS}/\text{TSS} = 0.1$ (share of the \emph{unexplained} variation).",
             solution=r"""\[ R^2 = 1 - \frac{\text{RSS}}{\text{TSS}} = 1 - \frac{40}{400} = 0.9
   \qquad\bigl(= \tfrac{\text{ESS}}{\text{TSS}} = \tfrac{360}{400}\ \text{with } \text{ESS} = \text{TSS} - \text{RSS} = 360\bigr). \]
$90\,\%$ of the variation in the daily iced-coffee sales is explained (linearly) by the
temperature; by the rule of thumb of the lecture ($R^2 \ge 0.8$) the fit is good.
Check: $\text{ESS} = \hat\beta_1^2\,S_{xx} = 9\cdot 40 = 360$ \checkmark"""),
        dict(label=r"Correlation coefficient $r_{xy}$",
             q=r"Determine the correlation coefficient $r_{xy}$ from $R^2 = 0.9$ and the slope $\hat\beta_1 = 3$.",
             short=r"$r_{xy} = +\sqrt{0.9} = 0.9487$",
             result=r"$r_{xy} = +\sqrt{0.9} = 0.9487$ (positive, because $\hat\beta_1 > 0$)",
             rubric=r"1 P. $|r_{xy}| = \sqrt{R^2}$, 1 P. value $0.9487$ with positive sign.",
             mistake=r"$r_{xy} = R^2 = 0.9$, or the sign ignored.",
             solution=r"""In simple regression $R^2 = r_{xy}^2$, hence
\[ |r_{xy}| = \sqrt{0.9} = 0.9487 , \qquad r_{xy} = +0.9487 \]
-- positive, because the slope $\hat\beta_1 = 3$ is positive. Check with the sums:
$r_{xy} = S_{xy}/\sqrt{S_{xx}S_{yy}} = 120/\sqrt{40\cdot 400} = 120/126.49 = 0.9487$ \checkmark"""),
        dict(label=r"Python command (OLS)", python=True,
             q=r"The five days are stored in a pandas DataFrame \texttt{cafe} with the columns \texttt{temp} and \texttt{sales}. Give the \texttt{statsmodels} command that estimates the simple linear regression of \texttt{sales} on \texttt{temp}.",
             short=r'\texttt{smf.ols("sales \textasciitilde{} temp", data=cafe).fit()}',
             result=r'\texttt{smf.ols("sales \textasciitilde{} temp", data=cafe).fit()}',
             rubric=r'1 P. \texttt{smf.ols(...).fit()}, 1 P. formula \texttt{"sales \textasciitilde{} temp"} (dependent variable on the left) with \texttt{data=cafe} (also accepted: the array form \texttt{sm.OLS(cafe["sales"], sm.add\_constant(cafe["temp"])).fit()}).',
             mistake=r'formula the wrong way round (\texttt{"temp \textasciitilde{} sales"}) or \texttt{.fit()} forgotten.',
             solution=r"""\begin{lstlisting}
import statsmodels.formula.api as smf
reg = smf.ols("sales ~ temp", data=cafe).fit()
reg.params             # Intercept -12.0, temp 3.0
\end{lstlisting}
The dependent variable stands to the \emph{left} of \texttt{\textasciitilde}, the explanatory
variable to the right; \texttt{.fit()} carries out the least-squares estimation."""),
        dict(label=r"Ceteris-paribus interpretation", kind="satz",
             q=r"In the multiple regression of Part~B, the coefficient of \texttt{temp} is $\hat\beta_1 = 3.0055$. Interpret this coefficient in one sentence.",
             short=r"holding rain fixed: $+1$\,$^{\circ}$C $\Rightarrow$ on average $3.01$ more iced coffees",
             result=r"Holding the rainfall fixed, a $1$\,$^{\circ}$C higher maximum temperature goes along with on average about $3.01$ more iced coffees sold per day.",
             rubric=r"1 P. ``$+1$\,$^{\circ}$C $\Rightarrow$ on average about $3.01$ (or $3$) more iced coffees'', 1 P. ceteris-paribus clause ``holding the rainfall fixed''.",
             mistake=r"the clause ``holding rain fixed'' is missing -- then the sentence describes the simple, not the multiple regression.",
             solution=r"""In a multiple regression each coefficient is a \emph{partial} effect: it compares
days that differ in temperature but have the \emph{same} rainfall.
\begin{lstlisting}[style=Pyout]
""" + CAFE_OUTPUT + r"""
\end{lstlisting}
\emph{Model answer:} ``Holding the rainfall fixed, one degree Celsius more goes along with,
on average, about $3.01$ more iced coffees sold per day.'' The $p$-value $0.000$ shows that
this effect is highly significant."""),
        dict(label=r"Significance of \texttt{rain}",
             q=r"In the multiple regression of Part~B, the coefficient of \texttt{rain} is $-0.4313$ with the $p$-value $0.253$ (column \texttt{P>|t|}). Decide at $\alpha = 0.05$ whether rainfall has a significant effect on sales when the temperature is held fixed.",
             short=r"$p = 0.253 > 0.05$ $\Rightarrow$ not significant (keep $H_0\colon \beta_2 = 0$)",
             result=r"$p = 0.253 > 0.05 = \alpha$ $\Rightarrow$ $H_0\colon \beta_2 = 0$ is kept: given the temperature, rainfall has \textbf{no significant} effect on sales.",
             rubric=r"1 P. comparison $p = 0.253 > 0.05$, 1 P. conclusion ``not significant / keep $H_0$''.",
             mistake=r"``$p > 0.05$, so rain has no effect at all'' -- not significant only means: no evidence found.",
             solution=r"""$t$-test of a single coefficient: $H_0\colon \beta_2 = 0$ vs.\ $H_1\colon \beta_2 \neq 0$.
Decision rule: reject $H_0$ if $p < \alpha$. Here
\[ p = 0.253 \;>\; 0.05 = \alpha \quad\Rightarrow\quad \text{keep } H_0 . \]
Equivalently, $|t| = 1.154 < t_{0.975;\,57} \approx 2.00$, and the $95\,\%$ CI
$[-1.180;\ 0.317]$ contains $0$. Once the temperature is in the model, the rainfall adds no
significant explanation. This is \emph{confounding}: alone, \texttt{sales \textasciitilde{} rain}
gives a clearly negative slope ($-6.19$), because rainy days are also cooler days.
``Not significant'' does not prove ``no effect'': effects of about $-1$ iced coffee per mm are
still compatible with the data."""),
    ],
    figs_sol=[
        ("qrm1_t2_scatter.pdf", "0.62", r"Scatter plot of the five days with the OLS line $\hat y = -12 + 3x$ and the residuals (dashed); the line passes through $(\bar x,\bar y) = (24;\ 60)$."),
    ],
    figs_slides=[
        ("qrm1_t2_scatter.pdf", "0.78", r"Task 2 -- scatter plot, OLS line and residuals"),
    ],
    slides_detail=[
        (r"Task 2 -- line, fitted values and residuals", r"""
  \[ \hat\beta_1 = \frac{S_{xy}}{S_{xx}} = \frac{120}{40} = 3, \qquad
     \hat\beta_0 = \bar y - \hat\beta_1\bar x = 60 - 3\cdot 24 = -12
     \qquad\Rightarrow\qquad \hat y = -12 + 3x \]
  \begin{center}\small
  \renewcommand{\arraystretch}{1.2}
  \begin{tabular}{lccccc|c}
    \toprule
    $x_i$ & 20 & 22 & 24 & 26 & 28 & $\sum$\\
    $y_i$ & 46 & 54 & 62 & 70 & 68 & 300\\
    $\hat y_i$ & 48 & 54 & 60 & 66 & 72 & 300\\
    $\hat u_i = y_i - \hat y_i$ & $-2$ & $0$ & $+2$ & $+4$ & $-4$ & $0$\\
    $\hat u_i^{\,2}$ & 4 & 0 & 4 & 16 & 16 & $40 = \text{RSS}$\\
    \bottomrule
  \end{tabular}
  \end{center}
  \begin{itemize}\setlength{\itemsep}{2pt}
    \item Prediction at $x = 25$ (inside the data range): $\hat y = -12 + 75 = 63$.
    \item Slope: $1$\,$^{\circ}$C warmer $\Rightarrow$ on average $3$ more iced coffees; the intercept $-12$ is pure extrapolation.
  \end{itemize}"""),
        (r"Task 2 -- sums of squares, $R^2$ and $r_{xy}$", r"""
  \[ \underbrace{\text{TSS}}_{S_{yy} = 400} \;=\; \underbrace{\text{ESS}}_{\hat\beta_1^2 S_{xx} = 9\cdot 40 = 360}
     \;+\; \underbrace{\text{RSS}}_{\sum\hat u_i^2 = 40} \]
  \[ R^2 = \frac{\text{ESS}}{\text{TSS}} = 1 - \frac{\text{RSS}}{\text{TSS}} = 1 - \frac{40}{400} = 0.9,
     \qquad r_{xy} = +\sqrt{0.9} = 0.9487 \]
  \begin{itemize}\setlength{\itemsep}{3pt}
    \item $90\,\%$ of the variation in sales is explained (linearly) by the temperature.
    \item The sign of $r_{xy}$ comes from $\hat\beta_1 > 0$; check: $120/\sqrt{40\cdot 400} = 0.9487$.
  \end{itemize}
  \kernaussage{$R^2 = r_{xy}^2$ holds in \emph{simple} regression only -- take the root and add the sign of the slope.}"""),
        (r"Task 2 -- reading the multiple regression output", r"""
\begin{lstlisting}[style=Pyout]
""" + CAFE_OUTPUT + r"""
\end{lstlisting}
  \begin{itemize}\setlength{\itemsep}{2pt}\small
    \item \texttt{temp}: holding \texttt{rain} fixed, $+1$\,$^{\circ}$C $\Rightarrow$ on average $+3.01$ iced coffees ($p = 0.000$).
    \item \texttt{rain}: $p = 0.253 > 0.05$ $\Rightarrow$ keep $H_0\colon \beta_2 = 0$ -- not significant \emph{given the temperature}.
    \item Confounding: alone, \texttt{sales \textasciitilde{} rain} has slope $-6.19$ -- rainy days are also cooler days.
  \end{itemize}""", True),
    ],
    mistakes=[
        r"$\hat\beta_1 = S_{xx}/S_{xy}$ instead of $S_{xy}/S_{xx}$.",
        r"Residual with the wrong sign ($\hat y_i - y_i$ instead of $y_i - \hat y_i$).",
        r"$r_{xy} = R^2$, or the sign of $r_{xy}$ ignored.",
        r"Slope interpreted without units or as a proven causal effect.",
        r"Multiple regression: the clause ``holding the other variables fixed'' forgotten; ``not significant'' read as ``no effect''.",
    ],
)

# ======================================================================== Task 3
T3 = dict(
    nr=3, topic=r"Classification: logistic regression and evaluation",
    short_scenario="Churn prediction of a mobile-phone provider",
    intro=r"""A mobile-phone provider wants to predict whether a customer cancels the contract
in the next quarter ($Y = 1$: churn, $Y = 0$: no churn). The explanatory variable $x$ is the
number of calls to the service hotline in the last six months. A logistic regression gives
the estimated linear predictor (log-odds)
\[ \hat\eta(x) = \hat\beta_0 + \hat\beta_1 x = -3 + 0.5\,x
   \qquad\text{and}\qquad \hat p(x) = \frac{e^{\hat\eta(x)}}{1+e^{\hat\eta(x)}} . \]
The provider then classifies $n = 200$ test customers with the threshold $t = 0.5$
(predicted churn if $\hat p(x) > 0.5$):

\medskip
\begin{center}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{l|cc|c}
& Pred.\ No & Pred.\ Yes & Total\\
\hline
Actual No & $\mathrm{TN} = 140$ & $\mathrm{FP} = 20$ & $160$\\
Actual Yes & $\mathrm{FN} = 10$ & $\mathrm{TP} = 30$ & $40$\\
\hline
Total & $150$ & $50$ & $200$\\
\end{tabular}
\end{center}

\medskip
\noindent\textit{All subtasks can be solved independently of each other.}
""",
    scenario=r"""Churn of mobile-phone customers ($Y = 1$) explained by the number $x$ of hotline
calls: $\hat\eta(x) = -3 + 0.5\,x$. Confusion matrix of $n = 200$ test customers at $t = 0.5$:
$\mathrm{TN} = 140$, $\mathrm{FP} = 20$, $\mathrm{FN} = 10$, $\mathrm{TP} = 30$.""",
    slide_scenario=r"""
  \begin{columns}[T]
    \column{0.50\textwidth}
    \begin{block}{Logistic regression}
      $Y = 1$: customer cancels (churn)\\
      $x$: hotline calls in the last six months\\[4pt]
      $\hat\eta(x) = -3 + 0.5\,x$\\[3pt]
      $\hat p(x) = \dfrac{e^{\hat\eta}}{1+e^{\hat\eta}}$
    \end{block}
    \column{0.46\textwidth}
    \begin{block}{Test data, $t = 0.5$}
      \begin{center}\small
      \begin{tabular}{l|cc|c}
        & Pred.\ No & Pred.\ Yes & \\
        \hline
        Act.\ No & 140 & 20 & 160\\
        Act.\ Yes & 10 & 30 & 40\\
        \hline
        & 150 & 50 & 200
      \end{tabular}
      \end{center}
    \end{block}
  \end{columns}""",
    lecture_ref=r"""Part~5, sections \emph{Logistic Regression} (odds, log-odds, the model, odds
ratio), \emph{From Probabilities to Decisions} (classification rule) and \emph{Evaluating a
Classifier} (confusion matrix, threshold trade-off); Python: Summary~4.""",
    concepts=[
        r"\textbf{Odds:} $\text{odds} = \dfrac{p}{1-p}$; back: $p = \dfrac{\text{odds}}{1+\text{odds}}$.",
        r"\textbf{Logistic model:} linear predictor $\eta = \beta_0 + \beta_1 x$ (log-odds), \ $p(x) = \dfrac{e^{\eta}}{1+e^{\eta}}$.",
        r"\textbf{Odds ratio} $e^{\beta_1}$: factor by which the \emph{odds} change per additional unit of $x$.",
        r"\textbf{Classification rule:} $\hat y = 1$ if $\hat p(x) > t$; \ $t = 0.5 \Leftrightarrow \hat\eta(x) > 0$.",
        r"\textbf{Confusion matrix:} accuracy $= (\mathrm{TP}+\mathrm{TN})/n$, sensitivity $= \mathrm{TP}/(\mathrm{TP}+\mathrm{FN})$, specificity $= \mathrm{TN}/(\mathrm{TN}+\mathrm{FP})$, precision $= \mathrm{TP}/(\mathrm{TP}+\mathrm{FP})$.",
    ],
    items=[
        dict(label=r"Odds of churn",
             q=r"Last year, $20\,\%$ of all customers churned, i.e.\ $p = 0.2$. Compute the odds of churn.",
             short=r"odds $= 0.2/0.8 = 0.25$",
             result=r"$\text{odds} = \dfrac{p}{1-p} = \dfrac{0.2}{0.8} = 0.25$",
             rubric=r"1 P. formula $p/(1-p)$, 1 P. result $0.25$.",
             mistake=r"odds confused with the probability ($0.2$) or computed as $(1-p)/p = 4$.",
             solution=r"""\[ \text{odds} = \frac{p}{1-p} = \frac{0.2}{0.8} = 0.25 . \]
Odds of $0.25$ mean ``$1$ to $4$'': for every customer who churns, four customers stay."""),
        dict(label=r"Churn probability at $x = 2$",
             q=r"Compute the predicted churn probability $\hat p(x)$ of a customer with $x = 2$ hotline calls, using $\hat\eta(x) = -3 + 0.5\,x$ and $e^{-2} = 0.1353$.",
             short=r"$\hat\eta = -2$, \ $\hat p = 0.1353/1.1353 = 0.1192$",
             result=r"$\hat\eta(2) = -3 + 0.5\cdot 2 = -2$, \ $\hat p(2) = \dfrac{e^{-2}}{1+e^{-2}} = \dfrac{0.1353}{1.1353} = 0.1192$",
             rubric=r"1 P. linear predictor $\hat\eta = -2$, 1 P. probability $0.1192$.",
             mistake=r"reporting the log-odds $-2$ or the odds $0.1353$ as the probability.",
             solution=r"""Pipeline $x \to \hat\eta \to \text{odds} \to \hat p$:
\[ \hat\eta(2) = -3 + 0.5\cdot 2 = -2, \qquad \text{odds} = e^{-2} = 0.1353, \qquad
   \hat p(2) = \frac{0.1353}{1 + 0.1353} = \frac{0.1353}{1.1353} = 0.1192 . \]
A customer with two hotline calls churns with an estimated probability of about $12\,\%$."""),
        dict(label=r"Interpretation of the odds ratio", kind="satz",
             q=r"The odds ratio of the hotline calls is $e^{\hat\beta_1} = e^{0.5} = 1.6487$. Interpret it in one sentence.",
             short=r"each extra call multiplies the \emph{odds} of churn by $1.65$ ($+65\,\%$)",
             result=r"Each additional hotline call multiplies the \emph{odds} of churn by about $1.65$, i.e.\ the odds of churn rise by about $65\,\%$ per call.",
             rubric=r"1 P. ``per additional hotline call'', 1 P. ``\emph{odds} multiplied by $1.65$ / $+65\,\%$'' (``probability $+65\,\%$'': 0 P. for this part).",
             mistake=r"``the probability of churn rises by $65\,\%$'' -- the factor applies to the odds, not to the probability.",
             solution=r"""On the log-odds scale one call more adds $\hat\beta_1 = 0.5$; on the odds scale it
\emph{multiplies} the odds by $e^{0.5} = 1.6487$ -- independent of the starting value of $x$:
\[ \frac{\text{odds}(x+1)}{\text{odds}(x)} = e^{\hat\beta_1} = 1.6487 . \]
\emph{Model answer:} ``Each additional hotline call multiplies the odds of churn by about
$1.65$ (the odds rise by about $65\,\%$).'' The change in the \emph{probability} is not
constant -- it depends on where on the S-curve the customer is."""),
        dict(label=r"Classification at $x = 7$",
             q=r"A customer has $x = 7$ hotline calls. Classify this customer with the threshold $t = 0.5$, using $\hat\eta(x) = -3 + 0.5\,x$ (you may use $e^{0.5} = 1.6487$).",
             short=r"$\hat\eta = 0.5 > 0$, $\hat p = 0.6225 > 0.5$ $\Rightarrow$ $\hat y = 1$ (churn)",
             result=r"$\hat\eta(7) = 0.5 > 0$, \ $\hat p(7) = \dfrac{1.6487}{2.6487} = 0.6225 > 0.5$ \ $\Rightarrow$ \ $\hat y = 1$: predicted to \textbf{churn}",
             rubric=r"1 P. $\hat\eta = 0.5$ or $\hat p = 0.6225$, 1 P. classification $\hat y = 1$ (churn).",
             solution=r"""\[ \hat\eta(7) = -3 + 0.5\cdot 7 = 0.5, \qquad
   \hat p(7) = \frac{e^{0.5}}{1+e^{0.5}} = \frac{1.6487}{2.6487} = 0.6225 . \]
Since $\hat p(7) = 0.6225 > 0.5 = t$, the customer is classified as \textbf{churner}
($\hat y = 1$). Shortcut: $t = 0.5$ corresponds to $\hat\eta > 0$, and $\hat\eta(7) = 0.5 > 0$.
The decision boundary lies at $\hat\eta = 0 \Leftrightarrow x = 6$: customers with at least
$7$ calls are flagged."""),
        dict(label=r"Python command (logit)", python=True,
             q=r"The customer data are stored in a pandas DataFrame \texttt{df} with the columns \texttt{churn} (coded $0/1$) and \texttt{calls}. Give the \texttt{statsmodels} command that estimates the logistic regression of \texttt{churn} on \texttt{calls}.",
             short=r'\texttt{smf.logit("churn \textasciitilde{} calls", data=df).fit()}',
             result=r'\texttt{smf.logit("churn \textasciitilde{} calls", data=df).fit()}',
             rubric=r'1 P. \texttt{smf.logit(...).fit()} (not \texttt{smf.ols}), 1 P. formula \texttt{"churn \textasciitilde{} calls"} with \texttt{data=df} (also accepted: the array form \texttt{sm.Logit(df["churn"], sm.add\_constant(df["calls"])).fit()}).',
             mistake=r"\texttt{smf.ols} instead of \texttt{smf.logit} (a linear probability model).",
             solution=r"""\begin{lstlisting}
import numpy as np
import statsmodels.formula.api as smf
g = smf.logit("churn ~ calls", data=df).fit()
print(g.summary())     # z-tests of the coefficients
np.exp(g.params)       # odds ratios
\end{lstlisting}
\texttt{smf.logit} estimates the coefficients by maximum likelihood; the response must be
coded $0/1$."""),
        dict(label=r"Accuracy",
             q=r"Compute the accuracy of the classifier from the confusion matrix with $\mathrm{TN} = 140$, $\mathrm{FP} = 20$, $\mathrm{FN} = 10$ and $\mathrm{TP} = 30$.",
             short=r"$(30 + 140)/200 = 0.85$",
             result=r"$\text{accuracy} = \dfrac{\mathrm{TP}+\mathrm{TN}}{n} = \dfrac{30 + 140}{200} = 0.85$",
             rubric=r"1 P. formula $(\mathrm{TP}+\mathrm{TN})/n$, 1 P. result $0.85$.",
             solution=r"""\[ \text{accuracy} = \frac{\mathrm{TP}+\mathrm{TN}}{n} = \frac{30 + 140}{200} = \frac{170}{200} = 0.85 . \]
$85\,\%$ of all test customers are classified correctly (error rate $0.15$). Note: the trivial
rule ``nobody churns'' would already reach $160/200 = 0.80$ -- accuracy alone is not enough."""),
        dict(label=r"Sensitivity",
             q=r"Compute the sensitivity of the classifier from the confusion matrix with $\mathrm{TN} = 140$, $\mathrm{FP} = 20$, $\mathrm{FN} = 10$ and $\mathrm{TP} = 30$.",
             short=r"$30/(30 + 10) = 0.75$",
             result=r"$\text{sensitivity} = \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}} = \dfrac{30}{40} = 0.75$",
             rubric=r"1 P. formula $\mathrm{TP}/(\mathrm{TP}+\mathrm{FN})$ (row ``Actual Yes''), 1 P. result $0.75$.",
             mistake=r"dividing by the column total ``Pred.\ Yes'' ($30/50$ is the precision).",
             solution=r"""Condition on the row ``Actual Yes'' ($40$ actual churners):
\[ \text{sensitivity} = P(\hat y = 1 \mid y = 1) = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}} = \frac{30}{30+10} = 0.75 . \]
The rule catches $75\,\%$ of the customers who actually churn."""),
        dict(label=r"Specificity",
             q=r"Compute the specificity of the classifier from the confusion matrix with $\mathrm{TN} = 140$, $\mathrm{FP} = 20$, $\mathrm{FN} = 10$ and $\mathrm{TP} = 30$.",
             short=r"$140/(140 + 20) = 0.875$",
             result=r"$\text{specificity} = \dfrac{\mathrm{TN}}{\mathrm{TN}+\mathrm{FP}} = \dfrac{140}{160} = 0.875$",
             rubric=r"1 P. formula $\mathrm{TN}/(\mathrm{TN}+\mathrm{FP})$ (row ``Actual No''), 1 P. result $0.875$.",
             mistake=r"$\mathrm{TN}/(\mathrm{TN}+\mathrm{FN}) = 140/150$ (column instead of row).",
             solution=r"""Condition on the row ``Actual No'' ($160$ customers who stay):
\[ \text{specificity} = P(\hat y = 0 \mid y = 0) = \frac{\mathrm{TN}}{\mathrm{TN}+\mathrm{FP}} = \frac{140}{140+20} = 0.875 . \]
$87.5\,\%$ of the loyal customers are correctly left alone."""),
        dict(label=r"Precision",
             q=r"Compute the precision of the classifier from the confusion matrix with $\mathrm{TN} = 140$, $\mathrm{FP} = 20$, $\mathrm{FN} = 10$ and $\mathrm{TP} = 30$.",
             short=r"$30/(30 + 20) = 0.6$",
             result=r"$\text{precision} = \dfrac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}} = \dfrac{30}{50} = 0.6$",
             rubric=r"1 P. formula $\mathrm{TP}/(\mathrm{TP}+\mathrm{FP})$ (column ``Pred.\ Yes''), 1 P. result $0.6$.",
             mistake=r"confusing precision with sensitivity ($30/40$).",
             solution=r"""Condition on the column ``Pred.\ Yes'' ($50$ flagged customers):
\[ \text{precision} = P(y = 1 \mid \hat y = 1) = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FP}} = \frac{30}{30+20} = 0.6 . \]
$60\,\%$ of the customers flagged as churners really churn -- $4$ of $10$ alarms are false
alarms. Sensitivity and precision both have TP on top but divide by different totals."""),
        dict(label=r"Lower threshold $t = 0.3$",
             q=r"To catch more churners, the provider lowers the threshold from $t = 0.5$ to $t = 0.3$. Does the sensitivity increase or decrease?",
             short=r"sensitivity \textbf{increases} (more churners caught)",
             result=r"The sensitivity \textbf{increases} (it cannot decrease): with $t = 0.3$ more customers are classified as churners, so more of the actual churners are caught ($\mathrm{TP}\uparrow$, $\mathrm{FN}\downarrow$).",
             rubric=r"1 P. ``increases'', 1 P. reason: more customers predicted as churners $\Rightarrow$ more actual churners caught.",
             mistake=r"``decreases'' -- confusing sensitivity with specificity, which falls when the threshold is lowered.",
             solution=r"""Lowering $t$ flags every customer with $\hat p(x) > 0.3$ instead of $\hat p(x) > 0.5$:
on the log-odds scale $\hat\eta(x) > \log(0.3/0.7) = -0.847$, i.e.\ $x \ge 5$ calls instead of
$x \ge 7$. Every customer flagged before is still flagged, plus some more. Hence
$\mathrm{TP}$ can only rise and $\mathrm{FN}$ only fall:
\[ \text{sensitivity} = \frac{\mathrm{TP}}{\mathrm{TP}+\mathrm{FN}} \ \uparrow \quad(\text{denominator fixed at } 40). \]
The price: more false alarms ($\mathrm{FP}\uparrow$), so the specificity falls. Which threshold
is best is a business decision (cost of a lost customer vs.\ cost of a retention offer)."""),
    ],
    figs_sol=[
        ("qrm1_t3_logistic.pdf", "0.62", r"Estimated churn probability $\hat p(x)$ with $\hat\eta(x) = -3 + 0.5\,x$: customers with $x = 2$ ($\hat p = 0.1192$) and $x = 7$ ($\hat p = 0.6225$); thresholds $t = 0.5$ (boundary $x = 6$) and $t = 0.3$."),
    ],
    figs_slides=[
        ("qrm1_t3_logistic.pdf", "0.78", r"Task 3 -- the S-curve and the two thresholds"),
    ],
    slides_detail=[
        (r"Task 3 -- from hotline calls to a decision", r"""
  \begin{center}\small
  \renewcommand{\arraystretch}{1.25}
  \begin{tabular}{cccccc}
    \toprule
    calls $x$ & $\hat\eta = -3 + 0.5x$ & odds $= e^{\hat\eta}$ & $\hat p = \frac{\text{odds}}{1+\text{odds}}$ & $\hat y$ ($t = 0.5$) & $\hat y$ ($t = 0.3$)\\
    \midrule
    2 & $-2.0$ & $0.1353$ & $0.1192$ & 0 & 0\\
    4 & $-1.0$ & $0.3679$ & $0.2689$ & 0 & 0\\
    5 & $-0.5$ & $0.6065$ & $0.3775$ & 0 & \textbf{1}\\
    6 & $\phantom{-}0.0$ & $1.0000$ & $0.5000$ & 0 & \textbf{1}\\
    7 & $\phantom{-}0.5$ & $1.6487$ & $0.6225$ & \textbf{1} & \textbf{1}\\
    \bottomrule
  \end{tabular}
  \end{center}
  \begin{itemize}\setlength{\itemsep}{2pt}
    \item Odds of churn overall: $0.2/0.8 = 0.25$.
    \item One call more: odds $\times\, e^{0.5} = 1.6487$ -- the \emph{odds} rise by $65\,\%$, not the probability.
    \item $t = 0.5 \Leftrightarrow \hat\eta > 0 \Leftrightarrow x \ge 7$; \quad $t = 0.3 \Leftrightarrow \hat\eta > -0.847 \Leftrightarrow x \ge 5$.
  \end{itemize}"""),
        (r"Task 3 -- the confusion matrix and its four measures", r"""
  \begin{columns}[c]
    \column{0.42\textwidth}
    \begin{center}\small
    \renewcommand{\arraystretch}{1.3}
    \begin{tabular}{l|cc|c}
      & Pred.\ No & Pred.\ Yes & \\
      \hline
      Act.\ No & \cellcolor{hsbigruen!18}TN $= 140$ & \cellcolor{hsbirot!15}FP $= 20$ & 160\\
      Act.\ Yes & \cellcolor{hsbirot!15}FN $= 10$ & \cellcolor{hsbigruen!18}TP $= 30$ & 40\\
      \hline
      & 150 & 50 & 200
    \end{tabular}
    \end{center}
    \column{0.54\textwidth}
    \begin{block}{Measures (which total do we divide by?)}
      \renewcommand{\arraystretch}{1.3}
      \begin{tabular}{@{}lll@{}}
        Accuracy & $(30+140)/200$ & $= 0.85$\\
        Sensitivity & $30/40$ \ (row Act.\ Yes) & $= 0.75$\\
        Specificity & $140/160$ \ (row Act.\ No) & $= 0.875$\\
        Precision & $30/50$ \ (column Pred.\ Yes) & $= 0.6$
      \end{tabular}
    \end{block}
  \end{columns}
  \medskip
  \kernaussage{Lower threshold $\Rightarrow$ more customers flagged $\Rightarrow$ sensitivity $\uparrow$, specificity $\downarrow$.}"""),
    ],
    mistakes=[
        r"Reading the log-odds $\hat\eta$ (or the odds $e^{\hat\eta}$) as a probability.",
        r"``The odds ratio is $1.65$, so the \emph{probability} rises by $65\,\%$.''",
        r"Mixing up sensitivity (divide by \emph{actual} Yes) and precision (divide by \emph{predicted} Yes).",
        r"Rows and columns of the confusion matrix confused (specificity $\neq$ $\mathrm{TN}/(\mathrm{TN}+\mathrm{FN})$).",
        r"Believing that a lower threshold catches \emph{fewer} churners.",
    ],
)

SPEC = dict(nr=1, outdir=BASE, tasks=[T1, T2, T3])
