#!/usr/bin/env python3
"""Recomputes every result of Mock Exam 1 independently (replaces verify.R).

The inputs (data, sums, coefficients, confusion matrix) are typed in here a
second time; every result is computed from them with NumPy / SciPy /
statsmodels and then looked up in the text of spec_qrm1.py (fields 'short' and
'result', and where useful 'q' or 'intro'). The three Python commands asked for
in the exam and the three lines of code students have to read are executed on
suitable data. Exit code 1 if anything disagrees.

    python3 verify.py
"""
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.formula.api as smf  # noqa: E402
from scipy import stats  # noqa: E402

import spec_qrm1  # noqa: E402
from templates import NORMAL_TABLE, T_TABLE  # noqa: E402

LETTERS = "abcdefghij"
SPEC = spec_qrm1.SPEC
ROWS, FAILS = [], []


def item(task, letter):
    return SPEC["tasks"][task - 1]["items"][LETTERS.index(letter)]


def check(task, letter, value, tokens, fields=("short", "result"), cond=True):
    """value: the recomputed result (printed); tokens: strings that must appear in
    every field listed; cond: an extra logical check of the recomputation."""
    it = item(task, letter)
    missing = [(f, t) for f in fields for t in tokens if t not in it[f]]
    ok = cond and not missing
    ROWS.append((task, letter, it["label"], value, "OK" if ok else "FAIL"))
    if not ok:
        FAILS.append("T%d %s): %s -- missing %s%s" % (task, letter, it["label"], missing,
                                                   "" if cond else " / logical check failed"))


def run_code(task, letter, **env):
    """Executes the line of code printed in a code-reading subtask (field 'code',
    LaTeX escapes removed) with the given variables."""
    code = item(task, letter)["code"]
    for old, new in (("\\{", "{"), ("\\}", "}"), ("\\ ", " "), ("\\_", "_")):
        code = code.replace(old, new)
    return eval(code, {}, env)


def check_text(where, text, tokens):
    missing = [t for t in tokens if t not in text]
    if missing:
        FAILS.append("%s: missing %s" % (where, missing))


def r4(x):
    return round(x + 0.0, 4)


# ============================================================================ Task 1
mu0, sigma, n, xbar, alpha = 80, 12, 36, 84.30, 0.05
se = sigma / math.sqrt(n)
z = (xbar - mu0) / se
z_crit_exact = stats.norm.ppf(1 - alpha / 2)
z_crit = round(z_crit_exact, 2)
phi_tab = r4(stats.norm.cdf(round(z, 2)))                 # table value Phi(2.15)
p_table = 2 * (1 - phi_tab)
p_exact = 2 * stats.norm.sf(abs(z))
ci = (xbar - z_crit * se, xbar + z_crit * se)
intro1 = SPEC["tasks"][0]["intro"]
check_text("T1 intro", intro1, ["$\\mu_0 = 80$", "$\\sigma = 12$", "$n = 36$", "$\\bar x = 84.30$",
                                "$\\alpha = 0.05$"])
check(1, "a", "H0: mu = %d vs H1: mu != %d" % (mu0, mu0), ["\\mu = %d" % mu0, "\\mu \\neq %d" % mu0])
check(1, "b", "SE = %g" % se, ["= %g$" % se], cond=se == 2)
check(1, "b", "SE (question)", ["$\\sigma = 12$", "$n = 36$"], fields=("q",))
check(1, "c", "Z_n = %.4f" % z, ["= %.2f$" % z], cond=abs(z - 2.15) < 1e-12)
q_crit = 1 - alpha / 2
z_code = run_code(1, "d", stats=stats, q=q_crit)          # the printed line with q = 0.975
check(1, "d", "stats.norm.ppf(%.3f) = %.6f -> %.2f" % (q_crit, z_code, z_crit),
      ["%.3f" % q_crit, "%.2f" % z_crit, "z_{0.975}"],
      cond=round(z_code, 2) == 1.96 and round(run_code(1, "d", stats=stats, q=0.95), 2) != 1.96)
check(1, "d", "ppf (question)", ["$\\alpha = 0.05$", "\\texttt{q}"], fields=("q",))
check(1, "d", "ppf (solution)", ["stats.norm.ppf(0.975)     # %.6f" % z_crit_exact], fields=("solution",))
check(1, "e", "|Z_n| = %.2f > %.2f -> reject" % (abs(z), z_crit), ["reject"], cond=abs(z) > z_crit)
check(1, "f", "Phi(2.15) = %.4f, p = %.4f (exact %.5f)" % (phi_tab, p_table, p_exact),
      ["%.4f" % phi_tab, "%.4f" % p_table], cond=round(p_exact, 4) == round(p_table, 4) and p_table < alpha)
check(1, "g", "CI = [%.2f; %.2f], e = %.2f" % (ci[0], ci[1], z_crit * se),
      ["%.2f" % ci[0], "%.2f" % ci[1], "%.2f" % (z_crit * se)], cond=not (ci[0] <= mu0 <= ci[1]))
check(1, "h", "CI interpretation for [%.2f; %.2f]" % ci, ["%.2f" % ci[0], "%.2f" % ci[1]],
      fields=("q", "short", "result"))
check(1, "i", "Type I error = reject true H0 (alpha = %.2f)" % alpha, ["although", "80"],
      fields=("short", "result"))
# j) run the command on simulated order values
rng = np.random.default_rng(1)
orders = rng.normal(xbar, sigma, n)
res = stats.ttest_1samp(orders, popmean=80)
res2 = stats.ttest_1samp(orders, popmean=80, alternative="two-sided")
check(1, "j", "ttest_1samp: df = %d, two-sided default = %s" % (res.df, res.pvalue == res2.pvalue),
      ["\\texttt{stats.ttest\\_1samp(orders, popmean=80)}"],
      cond=(res.df == n - 1 and res.pvalue == res2.pvalue))

# ============================================================================ Task 2
x = np.array([20, 22, 24, 26, 28], dtype=float)
y = np.array([46, 54, 62, 70, 68], dtype=float)
xb, yb = x.mean(), y.mean()
sxx = np.sum((x - xb) ** 2)
syy = np.sum((y - yb) ** 2)
sxy = np.sum((x - xb) * (y - yb))
b1 = sxy / sxx
b0 = yb - b1 * xb
yhat = b0 + b1 * x
u = y - yhat
rss = np.sum(u ** 2)
ess = np.sum((yhat - yb) ** 2)
tss = syy
r2 = 1 - rss / tss
rxy = np.corrcoef(x, y)[0, 1]
intro2 = SPEC["tasks"][1]["intro"]
check_text("T2 intro data", intro2, ["& 20 & 22 & 24 & 26 & 28", "& 46 & 54 & 62 & 70 & 68",
                                     "\\bar x = %g," % xb, "\\bar y = %g," % yb,
                                     "= %g,\\\\" % sxx, "= %g," % sxy, "= %g." % syy])
check(2, "a", "b1 = %g/%g = %g" % (sxy, sxx, b1), ["= %g$" % b1], cond=b1 == 3)
check(2, "a", "b1 (question)", ["S_{xy} = %g" % sxy, "S_{xx} = %g" % sxx], fields=("q",))
check(2, "b", "b0 = %g" % b0, ["= %g$" % b0], cond=b0 == -12)
check(2, "c", "slope interpretation: +1 degree -> +%g" % b1, ["$%g$ more" % b1])
y25 = b0 + b1 * 25
reg_d = smf.ols("sales ~ temp", data=pd.DataFrame({"temp": x, "sales": y})).fit()
pred25 = float(run_code(2, "d", reg=reg_d, pd=pd).iloc[0])   # the printed line
check(2, "d", "reg.predict(temp=25) = %.4f (25 inside [%g, %g])" % (pred25, x.min(), x.max()),
      ["%g" % y25], cond=abs(pred25 - y25) < 1e-9 and x.min() <= 25 <= x.max())
check(2, "d", "predict (question)", ["-12 + 3x"], fields=("q",))
check(2, "d", "predict (solution)", ['reg.predict(pd.DataFrame({"temp": [25]}))     # %.1f' % pred25],
      fields=("solution",))
check(2, "e", "yhat_5 = %g, u_5 = %g" % (yhat[4], u[4]), ["%g" % yhat[4], "%g$" % u[4]])
check(2, "f", "TSS = %g, ESS = %g, RSS = %g, R2 = %.4f" % (tss, ess, rss, r2), ["= %g$" % r2],
      cond=abs(ess + rss - tss) < 1e-9 and abs(r2 - 0.9) < 1e-12)
check(2, "f", "R2 (question)", ["\\text{TSS} = %g" % tss, "\\text{RSS} = %g" % rss], fields=("q",))
check(2, "g", "r_xy = %.4f (sign of b1 = %+g)" % (rxy, b1), ["%.4f" % rxy],
      cond=abs(rxy - math.copysign(math.sqrt(r2), b1)) < 1e-12)
cafe = pd.DataFrame({"temp": x, "sales": y})
reg = smf.ols("sales ~ temp", data=cafe).fit()
check(2, "h", "smf.ols -> Intercept %.4f, temp %.4f" % tuple(reg.params),
      ['\\texttt{smf.ols("sales \\textasciitilde{} temp", data=cafe).fit()}'],
      cond=np.allclose(reg.params.values, [b0, b1]))
# Part B: multiple regression on the 60 days
d60 = pd.read_csv(os.path.join(HERE, "data_qrm1_cafe60.csv"))
m = smf.ols("sales ~ temp + rain", data=d60).fit()
summary = m.summary().as_text().splitlines()
for line in spec_qrm1.CAFE_OUTPUT.splitlines():
    if line not in summary:
        FAILS.append("T2 output excerpt: line not in the statsmodels summary: %r" % line)
check(2, "i", "coef temp = %.4f (holding rain fixed)" % m.params["temp"], ["3.01", "rain"],
      cond=round(m.params["temp"], 4) == 3.0055 and len(d60) == 60)
check(2, "i", "coef temp (question)", ["%.4f" % m.params["temp"]], fields=("q",))
p_rain = m.pvalues["rain"]
check(2, "j", "coef rain = %.4f, p = %.3f > 0.05 -> not significant" % (m.params["rain"], p_rain),
      ["%.3f" % p_rain, "significant"], cond=p_rain > 0.05)
check(2, "j", "rain (question)", ["$%.4f$" % m.params["rain"], "$%.3f$" % p_rain], fields=("q",))
alone = smf.ols("sales ~ rain", data=d60).fit()
check(2, "j", "confounding: rain alone slope %.2f (p = %.1e)" % (alone.params["rain"], alone.pvalues["rain"]),
      ["%.2f" % alone.params["rain"]], fields=("solution",), cond=alone.pvalues["rain"] < 0.001)

# ============================================================================ Task 3
beta0, beta1 = -3.0, 0.5
TN, FP, FN, TP = 140, 20, 10, 30
N3 = TN + FP + FN + TP
intro3 = SPEC["tasks"][2]["intro"]
check_text("T3 intro", intro3, ["-3 + 0.5\\,x", "$\\mathrm{TN} = %d$" % TN, "$\\mathrm{FP} = %d$" % FP,
                                "$\\mathrm{FN} = %d$" % FN, "$\\mathrm{TP} = %d$" % TP,
                                "& $%d$\\\\" % (TN + FP), "& $%d$\\\\" % (FN + TP),
                                "Total & $%d$ & $%d$ & $%d$" % (TN + FN, FP + TP, N3)])
p_base = 0.2
odds = p_base / (1 - p_base)
check(3, "a", "odds = %.4f" % odds, ["%g$" % odds])


def p_of(xv):
    eta = beta0 + beta1 * xv
    return eta, math.exp(eta) / (1 + math.exp(eta))


eta2, p2 = p_of(2)
e2 = r4(math.exp(eta2))
p2_tab = e2 / (1 + e2)
check(3, "b", "eta(2) = %g, e^eta = %.4f, p = %.4f (exact %.6f)" % (eta2, e2, p2_tab, p2),
      ["%g" % eta2, "%.4f" % p2], cond=round(p2_tab, 4) == round(p2, 4))
check(3, "b", "e^-2 (question)", ["e^{-2} = %.4f" % e2], fields=("q",))
orr = math.exp(beta1)
check(3, "c", "odds ratio e^0.5 = %.4f (+%.0f %%)" % (orr, 100 * (orr - 1)),
      ["1.65", "%.0f" % (100 * (orr - 1))])
check(3, "c", "odds ratio (question)", ["%.4f" % orr], fields=("q",))
eta7, p7 = p_of(7)
check(3, "d", "eta(7) = %g, p = %.4f > 0.5 -> churn" % (eta7, p7), ["%.4f" % p7, "churn"],
      cond=p7 > 0.5 and round(math.exp(0.5) / (1 + math.exp(0.5)), 4) == round(r4(math.exp(0.5)) / (1 + r4(math.exp(0.5))), 4))
# e) the logit command on data simulated from the model; j) threshold effect on the same data
rng = np.random.default_rng(7)
calls = rng.integers(0, 15, 20000)
churn = (rng.random(20000) < 1 / (1 + np.exp(-(beta0 + beta1 * calls)))).astype(int)
df = pd.DataFrame({"churn": churn, "calls": calls})
g = smf.logit("churn ~ calls", data=df).fit(disp=0)
check(3, "e", "smf.logit on simulated data -> (%.3f, %.3f)" % tuple(g.params),
      ['\\texttt{smf.logit("churn \\textasciitilde{} calls", data=df).fit()}'],
      cond=np.allclose(g.params.values, [beta0, beta1], atol=0.15))
acc = (TP + TN) / N3
sens = TP / (TP + FN)
spec = TN / (TN + FP)
prec = TP / (TP + FP)
check(3, "f", "accuracy = %.4f" % acc, ["%g$" % acc])
# g) run the crosstab line on 200 customers with exactly these counts
test = pd.DataFrame({"churn": [0] * (TN + FP) + [1] * (FN + TP)})
phat = pd.Series([0.2] * TN + [0.7] * FP + [0.2] * FN + [0.7] * TP)
ct = run_code(3, "g", pd=pd, test=test, phat=phat)          # the printed line
check(3, "g", "crosstab row share [1, True] = %.4f = sensitivity %.4f" % (ct.loc[1, True], sens),
      ["%g$" % sens], cond=ct.loc[1, True] == sens and ct.loc[0, False] == spec)
check(3, "g", "crosstab printout (solution)",
      [l.rstrip() for l in ct.to_string().splitlines()], fields=("solution",))
check(3, "h", "specificity = %.4f" % spec, ["%g$" % spec])
check(3, "i", "precision = %.4f" % prec, ["%g$" % prec])
for L in "fghi":
    check(3, L, "counts in question", ["$\\mathrm{TN} = %d$" % TN, "$\\mathrm{FP} = %d$" % FP,
                                       "$\\mathrm{FN} = %d$" % FN, "$\\mathrm{TP} = %d$" % TP], fields=("q",))
ph = g.predict(df)
sens05 = ((ph > 0.5) & (df.churn == 1)).sum() / (df.churn == 1).sum()
sens03 = ((ph > 0.3) & (df.churn == 1)).sum() / (df.churn == 1).sum()
x_t5 = -beta0 / beta1
x_t3 = (math.log(0.3 / 0.7) - beta0) / beta1
check(3, "j", "sensitivity %.3f (t = 0.5) -> %.3f (t = 0.3): increases; flagged x > %.2f vs x > %.2f"
      % (sens05, sens03, x_t5, x_t3), ["increases"], cond=sens03 > sens05)
check(3, "j", "log-odds cut-off log(0.3/0.7) = %.3f" % math.log(0.3 / 0.7),
      ["%.3f" % math.log(0.3 / 0.7)], fields=("solution",))

# ============================================================================ tables
row21 = [l for l in NORMAL_TABLE.splitlines() if l.startswith("2.1 &")][0].split(" & ")
row19 = [l for l in NORMAL_TABLE.splitlines() if l.startswith("1.9 &")][0].split(" & ")
if row21[6] != "%.4f" % phi_tab or row19[7] != "0.9750":
    FAILS.append("normal table: Phi(2.15) or Phi(1.96) not as used in Task 1")
if "$1.960$" not in NORMAL_TABLE or "2.1314" not in T_TABLE:
    FAILS.append("table of quantiles incomplete")

# ============================================================================ report
print("%-4s %-3s %-44s %-62s %s" % ("Task", "", "Asked for", "Recomputed", ""))
print("-" * 120)
for t, l, lab, val, st in ROWS:
    for old, new in (("$", ""), ("\\,", " "), ("\\hat", ""), ("\\texttt", ""), ("^{\\circ}", "deg"),
                     ("\\", ""), ("{", ""), ("}", "")):
        lab = lab.replace(old, new)
    print("%-4d %-3s %-44.44s %-62.62s %s" % (t, l + ")", lab, val, st))
n_items = len({(t, l) for t, l, *_ in ROWS})
print("-" * 120)
if FAILS:
    print("PROBLEMS:")
    for f in FAILS:
        print("  - " + f)
    sys.exit(1)
print("All %d subtasks recomputed; every result agrees with spec_qrm1.py "
      "(%d checks incl. data, output excerpt and tables)." % (n_items, len(ROWS)))
