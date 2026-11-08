# =====================================================================
# Quantitative Research -- Part 3: Statistical Inference
# Author:  Prof. Dr. Christoph Weisser
#
# Reproduces the numbers shown on the slides of Part 3 (numpy, scipy,
# statsmodels). Run headless:  python3 Part_3_Statistical_Inference.py
# Sections follow the sections of the slide deck:
#   1  Foundations            (expected value/variance, warranty claims,
#                              normal distribution, standard-normal table,
#                              central limit theorem incl. simulation)
#   2  Confidence intervals   (standard error, milk, cream; known and unknown
#                              variance; sample-size planning)
#   3  Hypothesis tests       (CI duality, z- and t-test, reaction time,
#                              delivery time)
#   4  The p-value            (incl. t-table bracketing, coffee roastery)
#   5  One-sided tests        (critical-value tables, test direction, discount
#                              campaign, one-sided p-values and CIs, net
#                              weight, muesli, delivery time revisited)
# Blocks appear in the order of the slides; exercises sit right after the
# slides they practise.
#   6  Types of error         (beta and power)
#   A  Appendix               (estimator properties, why n-1, law of
#                              large numbers)
#
# Note: a few slides work with table values rounded to 3-4 decimals
# (z_0.95 = 1.645, Phi(1.85) = 0.9678). Where Python's unrounded value
# changes the last printed digit, this is pointed out in a comment.
# =====================================================================

import math
import numpy as np
from scipy import stats
from statsmodels.stats.power import NormalIndPower

# ---------------------------------------------------------------------
# SETUP: the two running examples
# ---------------------------------------------------------------------
milk = np.array([1005, 1001, 997, 1000, 1001, 998, 999, 999, 1009])  # ml, sigma = 3
cream = np.array([251, 248, 248, 249, 250, 251, 247, 246, 252,
                  251, 248, 247, 246, 249, 248, 252])               # g, sigma^2 = 4
alpha = 0.05
norm = stats.norm


def show(label, value, fmt=".4f"):
    """Print a label and a number (or a sequence of numbers)."""
    if np.ndim(value) == 0:
        print(f"{label:<44} {value:{fmt}}")
    else:
        print(f"{label:<44} [" + ", ".join(f"{v:{fmt}}" for v in value) + "]")


def header(title):
    print("\n" + "=" * 70 + f"\n{title}\n" + "=" * 70)


# =====================================================================
# 1 Foundations
# =====================================================================
header("1 Foundations")

# Slide "Random variables, expected value and variance": complaints per day
x_c = np.array([0, 1, 2, 3]); p_c = np.array([0.1, 0.3, 0.4, 0.2])
E_c = np.sum(x_c * p_c)
Var_c = np.sum((x_c - E_c) ** 2 * p_c)
show("E(X) complaints per day", E_c, ".2f")                     # 1.70
show("E(X^2)", np.sum(x_c ** 2 * p_c), ".2f")                  # 3.70
show("Var(X) = E(X^2) - E(X)^2", Var_c, ".2f")                  # 0.81
show("sd(X)", np.sqrt(Var_c), ".2f")                           # 0.90

# Exercise "Expected value and variance: warranty claims" (claims per week,
# P = 0.2, 0.4, 0.3, 0.1; costs K = 100 + 150 X; n = 9 independent weeks)
x_w = np.array([0, 1, 2, 3]); p_w = np.array([0.2, 0.4, 0.3, 0.1])
E_w = np.sum(x_w * p_w)
EX2_w = np.sum(x_w ** 2 * p_w)
Var_w = EX2_w - E_w ** 2
show("a) E(X) warranty claims", E_w, ".2f")                      # 1.30
show("a) E(X^2)", EX2_w, ".2f")                                 # 2.50
show("a) Var(X) = 2.5 - 1.3^2", Var_w, ".2f")                   # 0.81
show("a) sd(X)", np.sqrt(Var_w), ".2f")                         # 0.90
show("b) E(K) = 100 + 150 * 1.3", 100 + 150 * E_w, ".2f")       # 295.00
show("b) Var(K) = 150^2 * 0.81", 150 ** 2 * Var_w, ".2f")       # 18225.00
show("b) sd(K) = 150 * 0.9", 150 * np.sqrt(Var_w), ".2f")       # 135.00
show("c) E(S), Var(S), sd(S) for S = X1+...+X9",
     (9 * E_w, 9 * Var_w, np.sqrt(9 * Var_w)), ".2f")           # 11.70, 7.29, 2.70
show("c) wrong: adding sds 9 * 0.9", 9 * np.sqrt(Var_w), ".2f")  # 8.10
show("c) E(Xbar), Var(Xbar), sd(Xbar), n = 9",
     (E_w, Var_w / 9, np.sqrt(Var_w / 9)), ".2f")               # 1.30, 0.09, 0.30
# Python code shown on the slide (same rounding, the two print lines)
print("slide output a):", round(E_w, 2), round(Var_w, 2))                      # 1.3 0.81
print("slide output c):", round(np.sqrt(9 * Var_w), 2), round(np.sqrt(Var_w / 9), 2))  # 2.7 0.3

# Slide "Standardisation": milk bottle, X ~ N(1000, 3^2), P(X <= 997)
show("P(X <= 997) = Phi((997-1000)/3) = Phi(-1)", norm.cdf(997, loc=1000, scale=3))  # 0.1587

# Slide "Probabilities as areas -- the four basic cases"
show("Phi(0.75)", norm.cdf(0.75))                              # 0.7734
show("P(Z > 0.75) = 1 - Phi(0.75)", norm.sf(0.75))             # 0.2266
show("P(Z <= -0.75)", norm.cdf(-0.75))                         # 0.2266
show("P(-0.5 <= Z <= 1) = Phi(1) - Phi(-0.5)", norm.cdf(1) - norm.cdf(-0.5))  # 0.5328

# Slides "Standard normal table (1/2), (2/2)": Phi(z) for z = 0.00 ... 2.99
print("\nStandard normal table Phi(z) (rows: z to one decimal, columns: 2nd decimal)")
print("  z   " + " ".join(f"  .0{j}" for j in range(10)))
for i in range(30):
    z0 = i / 10
    print(f"{z0:4.1f} " + " ".join(f"{norm.cdf(z0 + j / 100):.4f}" for j in range(10)))
print()

# Slide "Reading the table -- forwards and backwards"
show("Phi(1.64), Phi(1.65)", (norm.cdf(1.64), norm.cdf(1.65)))  # 0.9495, 0.9505
show("z_0.95 = norm.ppf(0.95)", norm.ppf(0.95))                 # 1.6449 -> 1.645
show("Phi(1.96)", norm.cdf(1.96))                               # 0.9750
show("z_0.975 = norm.ppf(0.975)", norm.ppf(0.975))              # 1.9600

# Exercise "Normal distribution: fill volume", X ~ N(1000, 10^2), minimum 985 ml
show("a) P(X < 985) = Phi(-1.5)", norm.cdf(985, 1000, 10))      # 0.0668
show("   table: 1 - Phi(1.5) = 1 - 0.9332", 1 - 0.9332)
show("b) P(990 <= X <= 1015) = Phi(1.5) - Phi(-1)",
     norm.cdf(1015, 1000, 10) - norm.cdf(990, 1000, 10))       # 0.7745
show("   table: 0.9332 - (1 - 0.8413)", 0.9332 - (1 - 0.8413))  # 0.7745
show("c) 95% quantile, exact", norm.ppf(0.95, 1000, 10), ".2f")  # 1016.45
show("c) table: 1000 + 1.645 * 10", 1000 + 1.645 * 10, ".2f")  # 1016.45
show("d) Phi(2.33) (table look-up for 0.99)", norm.cdf(2.33))  # 0.9901
show("d) setpoint mu = 985 + 2.33 * 10 (table)", 985 + 2.33 * 10, ".1f")   # 1008.3
show("d) setpoint, exact z_0.99 = 2.3263", 985 - norm.ppf(0.01) * 10, ".2f")  # 1008.26

# Slides "The central limit theorem" (simulation figure): right-skewed
# processing times, gamma(shape 4, scale 3) => mu = 12, sigma = 6 minutes
g = stats.gamma(a=4, scale=3)
show("gamma(4, 3): mean, sd", (g.mean(), g.std()), ".1f")       # 12.0, 6.0
rng = np.random.default_rng(42)                                 # same seed as make_figures.py
for n_ in (1, 4, 9, 36):
    m_ = rng.gamma(4, 3, size=(20_000, n_)).mean(axis=1)
    print(f"  n = {n_:>2}: mean of 20000 sample means = {m_.mean():.3f}, "
          f"sd = {m_.std():.3f} (theory SE = {6 / np.sqrt(n_):.3f})")

# Slide "The central limit theorem with Python" (own seed 42, n = 36 only)
rng = np.random.default_rng(42)
times = rng.gamma(shape=4, scale=3, size=(20_000, 36))
means = times.mean(axis=1)
show("single values: mean, sd", (times.mean(), times.std()), ".1f")        # 12.0, 6.0
show("shift means: mean, sd", (means.mean(), means.std()), ".3f")          # 12.003, 0.990 -> 0.99
show("skewness single values, means",
     (stats.skew(times.ravel()), stats.skew(means)), ".2f")                 # 1.00, 0.15
show("share of shift means > 13.5 (simulation)", np.mean(means > 13.5))    # 0.0698
show("CLT: P(Xbar > 13.5) = 1 - Phi(1.5)", norm.sf(13.5, loc=12, scale=6 / np.sqrt(36)))  # 0.0668

# Exercise "Central limit theorem: processing times" (mu = 12, sigma = 6, n = 36)
show("a) SE = 6/sqrt(36)", 6 / np.sqrt(36), ".1f")              # 1.0
show("b) P(Xbar > 13.5) = 1 - Phi(1.5)", norm.sf(13.5, 12, 1))  # 0.0668
show("c) P(X > 13.5) IF X were normal = 1 - Phi(0.25)", norm.sf(13.5, 12, 6))  # 0.4013
show("   table: 1 - Phi(0.25) = 1 - 0.5987", 1 - 0.5987)
# for comparison: exact values under the right-skewed gamma model of the figure
show("   gamma model: P(X > 13.5) exact", g.sf(13.5))           # 0.342
show("   gamma model: P(Xbar_36 > 13.5) exact",
     stats.gamma(a=4 * 36, scale=3 / 36).sf(13.5))              # 0.071 (CLT: 0.067)
show("d) n >= (6/0.5)^2", (6 / 0.5) ** 2, ".0f")                # 144

# =====================================================================
# 2 Confidence intervals
# =====================================================================
header("2 Confidence intervals")

# Slide "Why divide by the standard error?" (xbar = 8, mu0 = 10)
for sig_, n_ in ((6, 9), (4, 100)):
    se_ = sig_ / np.sqrt(n_)
    print(f"sigma = {sig_}, n = {n_:>3}: SE = {se_:.1f}, z = (8 - 10)/SE = {(8 - 10) / se_:.1f}")
# -> SE = 2.0, z = -1.0;  SE = 0.4, z = -5.0

# Exercise "Standard error: packing flour" (sigma = 8 g, xbar = 497, mu0 = 500)
for n_ in (16, 64):
    se_ = 8 / np.sqrt(n_)
    show(f"a)/b) n = {n_}: SE, z = (497 - 500)/SE", (se_, (497 - 500) / se_), ".1f")
# -> n = 16: SE = 2, z = -1.5;  n = 64: SE = 1, z = -3.0
show("n = 16: P(|Z| >= 1.5) = 2 (1 - Phi(1.5)) exact", 2 * norm.sf(1.5))  # 0.1336
show("        table: 1 - 0.9332, 2 * (1 - 0.9332)",
     (1 - 0.9332, 2 * (1 - 0.9332)))                                  # 0.0668, 0.1336

# Slide "CI for milk (known variance)"
xbar_milk = milk.mean()
z = norm.ppf(1 - alpha / 2)
show("mean(milk)", xbar_milk)                                  # 1001
show("z_0.975", z)                                             # 1.96
show("milk 95% CI, sigma = 3", xbar_milk + np.array([-1, 1]) * z * 3 / np.sqrt(9),
     ".2f")                                                    # [999.04, 1002.96]

# Exercises "Filling cream (known variance)" and "Filling cream (unknown
# variance)": CI with sigma = 2 and with s
xbar_cream = cream.mean()
show("sum(cream)", cream.sum(), ".0f")                         # 3983
show("mean(cream) = 3983/16", xbar_cream)                      # 248.9375
show("sum of squared deviations (cream)",
     np.sum((cream - xbar_cream) ** 2))                        # 60.9375
show("margin of error, unknown variance 2.1314 * s/4",
     stats.t.ppf(0.975, 15) * cream.std(ddof=1) / 4)           # 1.0740
show("cream 95% CI, sigma = 2",
     xbar_cream + np.array([-1, 1]) * 1.96 * 2 / np.sqrt(16), ".2f")  # [247.96, 249.92]
show("var(cream)", cream.var(ddof=1))                          # 4.0625
s_cream = cream.std(ddof=1)
show("sd(cream)", s_cream)                                     # 2.0156
show("cream 95% CI, sigma unknown",
     xbar_cream + np.array([-1, 1]) * stats.t.ppf(0.975, 15) * s_cream / np.sqrt(16),
     ".2f")                                                    # [247.86, 250.01]

# Exercise "Reading a confidence interval correctly" (cream, sigma = 2, n = 16)
show("2) fluctuation interval of single cups xbar +- 1.96*2",
     xbar_cream + np.array([-1, 1]) * 1.96 * 2, ".2f")         # [245.02, 252.86]
show("5) margin of error at 99 %: 2.576 * 2/4", 2.576 * 2 / 4, ".3f")  # 1.288
show("5) 99 % CI cream (sigma known)",
     xbar_cream + np.array([-1, 1]) * 2.576 * 2 / 4, ".2f")    # [247.65, 250.23]

# Slide "Different confidence levels" (table 90 / 95 / 99 %)
for lev in (0.90, 0.95, 0.99):
    z_lev = norm.ppf(1 - (1 - lev) / 2)
    show(f"milk {lev:.0%} CI (z = {z_lev:.3f})",
         xbar_milk + np.array([-1, 1]) * z_lev * 3 / np.sqrt(9), ".2f")
# -> [999.36, 1002.64] for 90 % (unrounded z_0.95 = 1.644854; the rounded
#    1.645 would give 1002.645 -> 1002.65), [998.42, 1003.58] for 99 %.

# Slide "Planning the sample size" and exercise "How many bottles?"
# (milk, sigma = 3 known): margin of error e = z * sigma / sqrt(n)
show("a) margin of error with n = 9", 1.96 * 3 / np.sqrt(9), ".2f")            # 1.96
for lab, zq, e in [("b) 95 %, e = 1", 1.96, 1.0), ("c) 99 %, e = 1", 2.576, 1.0),
                   ("d) 95 %, e = 0.5", 1.96, 0.5)]:
    n_req = (zq * 3 / e) ** 2
    print(f"{lab}: (z*sigma/e)^2 = ({zq}*3/{e})^2 = {n_req:.2f} -> n = {math.ceil(n_req)}")
# -> 34.57 -> 35, 59.72 -> 60, 138.30 -> 139; with unrounded quantiles:
print("   unrounded quantiles:",
      [math.ceil((norm.ppf(q) * 3 / e) ** 2) for q, e in [(0.975, 1), (0.995, 1), (0.975, 0.5)]])
# -> [35, 60, 139] -- identical

# Slide "CI for milk (unknown variance)"
s_milk = milk.std(ddof=1)
t_8 = stats.t.ppf(1 - alpha / 2, df=8)
show("sd(milk)", s_milk)                                       # 3.7749
show("t_0.975;8", t_8)                                         # 2.3060
show("milk 95% CI, sigma unknown",
     xbar_milk + np.array([-1, 1]) * t_8 * s_milk / np.sqrt(9), ".2f")  # [998.10, 1003.90]
# same via scipy (the slide "Hypothesis test with Python"):
ci = stats.ttest_1samp(milk, 1000).confidence_interval(0.95)
show("  ... via ttest_1samp().confidence_interval", (ci.low, ci.high), ".2f")

# Slide "Confidence intervals with Python" (stats.norm.interval / stats.t.interval)
show("xbar, s (milk)", (xbar_milk, s_milk))                     # 1001.0000, 3.7749
show("z_0.975, t_0.975;8", (norm.ppf(0.975), t_8))              # 1.9600, 2.3060
show("by formula xbar +- 1.96 * 3/sqrt(9)",
     xbar_milk + np.array([-1, 1]) * 1.96 * 3 / np.sqrt(9), ".2f")   # [999.04, 1002.96]
for conf in (0.90, 0.95, 0.99):
    lo_, hi_ = stats.norm.interval(conf, loc=xbar_milk, scale=3 / np.sqrt(9))
    print(f"z, {conf:.0%}: [{lo_:.2f}, {hi_:.2f}]")
lo_, hi_ = stats.t.interval(0.95, df=8, loc=xbar_milk, scale=s_milk / np.sqrt(9))
print(f"t, 95%: [{lo_:.2f}, {hi_:.2f}]")
# -> z, 90%: [999.36, 1002.64]  z, 95%: [999.04, 1002.96]  z, 99%: [998.42, 1003.58]
#    t, 95%: [998.10, 1003.90]

# =====================================================================
# 3 Hypothesis tests
# =====================================================================
header("3 Hypothesis tests")

# Exercise "Hypotheses and deciding with the CI" (bank: mu0 = 30 min,
# sigma = 6 known, n = 36, xbar = 32.8, two-sided, alpha = 0.05)
se_b = 6 / np.sqrt(36)
ci_b = 32.8 + np.array([-1, 1]) * 1.96 * se_b
show("SE bank, margin of error 1.96 * SE", (se_b, 1.96 * se_b), ".2f")   # 1.00, 1.96
show("95% CI bank", ci_b, ".2f")                                         # [30.84, 34.76]
show("cross-check |Z_n| = |32.8 - 30| / 1", abs(32.8 - 30) / se_b, ".2f")  # 2.80
for mu0_ in (30, 31, 33, 35):
    print(f"  mu0 = {mu0_}: inside CI? {ci_b[0] <= mu0_ <= ci_b[1]}  "
          f"(|Z_n| = {abs(32.8 - mu0_) / se_b:.2f})")
# -> 30: False (reject), 31: True, 33: True (keep), 35: False (reject)

# Slides "Test statistic -- milk / cream" (known and unknown variance)
Zn_milk = (xbar_milk - 1000) / (3 / np.sqrt(9))
Tn_milk = (xbar_milk - 1000) / (s_milk / np.sqrt(9))
Zn_cream = (xbar_cream - 250) / (2 / np.sqrt(16))
Tn_cream = (xbar_cream - 250) / (s_cream / np.sqrt(16))
show("Z_n milk", Zn_milk)                                      # 1.000
show("T_n milk", Tn_milk)                                      # 0.7947
show("Z_n cream", Zn_cream)                                    # -2.125
show("T_n cream", Tn_cream)                                    # -2.1086
show("t_0.975;15 (critical value cream)", stats.t.ppf(0.975, 15), ".3f")  # 2.131

# Slide "Hypothesis test with Python -- ttest_1samp" (two-sided, unknown var.)
res = stats.ttest_1samp(milk, popmean=1000)
ci = res.confidence_interval(confidence_level=0.95)
print(f"ttest_1samp(milk, 1000):  t = {res.statistic:.4f}, df = {res.df}, "
      f"p = {res.pvalue:.4f}, 95% CI: [{ci.low:.2f}, {ci.high:.2f}]")
# -> t = 0.7947, df = 8, p = 0.4497, 95% CI: [998.10, 1003.90]

# Exercise / solution "Reaction time" (n = 50, xbar = 242, s = 30, mu0 = 250)
T_rt = (242 - 250) / (30 / np.sqrt(50))
show("T_n reaction time", T_rt)                                # -1.8856
show("t_0.975;49", stats.t.ppf(0.975, 49))                     # 2.0096
show("p two-sided reaction time", 2 * stats.t.cdf(-abs(T_rt), 49))  # 0.0653

# Exercise "Delivery time (complete t-test by hand)"
delivery = np.array([51, 39, 49, 41, 47, 43, 45, 45])         # hours, mu0 = 48
show("mean, sd (delivery)", (delivery.mean(), delivery.std(ddof=1)), ".4f")  # 45, 4
show("sum of squared deviations", np.sum((delivery - delivery.mean()) ** 2), ".0f")  # 112
se_d = delivery.std(ddof=1) / np.sqrt(8)
show("standard error s/sqrt(8)", se_d)                          # 1.4142
T_d = (delivery.mean() - 48) / se_d
show("T_n delivery", T_d)                                       # -2.1213
show("t_0.975;7", stats.t.ppf(0.975, 7))                        # 2.3646
show("margin of error 2.3646 * 1.4142", stats.t.ppf(0.975, 7) * se_d)  # 3.3441
res = stats.ttest_1samp(delivery, popmean=48)
ci = res.confidence_interval(confidence_level=0.95)
print(f"ttest_1samp(delivery, 48):  t = {res.statistic:.4f}, df = {res.df}, "
      f"p = {res.pvalue:.4f}, 95% CI: [{ci.low:.2f}, {ci.high:.2f}]")
# -> t = -2.1213, df = 7, p = 0.0716, 95% CI: [41.66, 48.34]

# =====================================================================
# 4 The p-value (two-sided)
# =====================================================================
header("4 The p-value")

# Exercise "p-value from Z_n = 1.85"
show("Phi(1.85)", norm.cdf(1.85))                              # 0.9678
show("p = 2 (1 - Phi(1.85))", 2 * norm.sf(1.85))
# -> 0.0643 exactly; with the table value Phi(1.85) = 0.9678 one gets
#    2 * 0.0322 = 0.0644 (the slide shows both).
show("   table: 1 - 0.9678, 2 * (1 - 0.9678)",
     (1 - 0.9678, 2 * (1 - 0.9678)))                            # 0.0322, 0.0644
show("   critical values z_0.975, z_0.95 (two-sided 5 %, 10 %)",
     (norm.ppf(0.975), norm.ppf(0.95)), ".3f")                  # 1.960, 1.645

# Slides "p-value -- milk / cream (two variants)"
show("p milk, sigma known", 2 * norm.cdf(-abs(Zn_milk)))       # 0.3173
show("p milk, sigma unknown", 2 * stats.t.cdf(-abs(Tn_milk), df=8))   # 0.4497
show("p cream, sigma known", 2 * norm.cdf(-abs(Zn_cream)))     # 0.0336
show("p cream, sigma unknown", 2 * stats.t.cdf(-abs(Tn_cream), df=15))  # 0.0522
# "Exact vs. table" notes on the same slides (printed Phi table: 4 decimals)
show("milk, Phi table: 2 * (1 - 0.8413)", 2 * (1 - round(norm.cdf(1.00), 4)))   # 0.3174
show("milk, t-table df = 8: t_0.90;8 (0.7947 below it -> p > 0.20)",
     stats.t.ppf(0.90, 8), ".3f")                                                # 1.397
show("cream, Phi(2.12), Phi(2.13) from the table",
     (round(norm.cdf(2.12), 4), round(norm.cdf(2.13), 4)))                       # 0.9830, 0.9834
show("cream, Phi-table bracket for p",
     (2 * (1 - round(norm.cdf(2.13), 4)), 2 * (1 - round(norm.cdf(2.12), 4))))   # 0.0332, 0.0340
show("cream, t-table df = 15: t_0.95;15, t_0.975;15 (-> 0.05 < p < 0.10)",
     (stats.t.ppf(0.95, 15), stats.t.ppf(0.975, 15)), ".3f")                    # 1.753, 2.131

# Slide "p-values with Python" (loop over milk and cream, sigma known / estimated)
for x_, mu0_, sig_ in [(milk, 1000, 3), (cream, 250, 2)]:
    n_ = len(x_)
    z_ = (x_.mean() - mu0_) / (sig_ / np.sqrt(n_))
    t_ = (x_.mean() - mu0_) / (x_.std(ddof=1) / np.sqrt(n_))
    print(f"z = {z_:.4f}, p = {2 * norm.sf(abs(z_)):.4f} | "
          f"t = {t_:.4f}, p = {2 * stats.t.sf(abs(t_), df=n_ - 1):.4f}")
# -> z = 1.0000, p = 0.3173 | t = 0.7947, p = 0.4497
#    z = -2.1250, p = 0.0336 | t = -2.1086, p = 0.0522

# Slide "Significant != important -- the large-n trap" (xbar = 1000.2, sigma = 3)
for n in (9, 10_000):
    z_n = 0.2 / (3 / np.sqrt(n))
    print(f"large-n trap: n = {n:>6}, Z_n = {z_n:.2f}, p = {2 * norm.sf(z_n):.4g}")
# -> n = 9: Z_n = 0.20, p = 0.84;  n = 10000: Z_n = 6.67, p < 0.0001

# Exercise "Bracketing the p-value with the t-table" (delivery time, df = 7)
print("t-table row df = 7 (upper-tail 0.10, 0.05, 0.025, 0.01, 0.005):",
      [round(float(stats.t.isf(a, 7)), 3) for a in (0.10, 0.05, 0.025, 0.01, 0.005)])
# -> [1.415, 1.895, 2.365, 2.998, 3.499]; 1.895 < 2.121 < 2.365
show("P(T > 2.1213), df = 7", stats.t.sf(abs(T_d), 7))          # 0.0358 (in (0.025, 0.05))
show("two-sided p = 2 * F_t,7(-2.1213)", 2 * stats.t.cdf(-abs(T_d), 7))  # 0.0716

# Exam-style exercise "Coffee roastery" (Gauss test): mu0 = 1000 g,
# sigma = 40 g known, n = 64, xbar = 1012 g, alpha = 0.05, two-sided
se_k = 40 / np.sqrt(64)
z_k = (1012 - 1000) / se_k
show("SE coffee", se_k, ".1f")                                  # 5.0
show("z coffee", z_k, ".2f")                                    # 2.40
show("Phi(2.40)", norm.cdf(2.40))                               # 0.9918
show("p = 2 * (1 - Phi(2.4)) exact", 2 * norm.sf(z_k))         # 0.0164
show("p from table 2 * (1 - 0.9918)", 2 * (1 - 0.9918))         # 0.0164
show("95% CI coffee (sigma known)", 1012 + np.array([-1, 1]) * 1.96 * se_k, ".1f")  # [1002.2, 1021.8]
show("t_0.975;24", stats.t.ppf(0.975, 24))                      # 2.0639
show("95% CI 2nd sample (n = 25, s = 40)",
     1012 + np.array([-1, 1]) * stats.t.ppf(0.975, 24) * 40 / np.sqrt(25), ".2f")  # [995.49, 1028.51]
show("  margin of error 2.0639 * 8", stats.t.ppf(0.975, 24) * 8, ".2f")          # 16.51

# =====================================================================
# 5 One-sided tests
# =====================================================================
header("Appendix A.3-A.7 -- one-sided tests (moved to the appendix)")

# Slides "Critical values" / t-table hint
show("z_0.95", norm.ppf(0.95))                                 # 1.6449 (slides: 1.645)
show("t_0.95;11", stats.t.ppf(0.95, 11))                       # 1.7959
show("t_0.975;11 (slide '3 steps': 2.20)", stats.t.ppf(0.975, 11))  # 2.2010

# Slides "Critical values of the standard normal" and "... of the t-distribution"
print("N(0,1): alpha, one-sided z_(1-alpha), two-sided z_(1-alpha/2)")
for a_ in (0.10, 0.05, 0.02, 0.01, 0.001):
    print(f"  {a_:<6} {norm.ppf(1 - a_):.3f}  {norm.ppf(1 - a_ / 2):.3f}")
print("t-table, upper-tail probability 0.10 0.05 0.025 0.01 0.005")
for df_ in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 60):
    print(f"  df = {df_:>2}: " + "  ".join(f"{stats.t.isf(a_, df_):6.3f}"
                                      for a_ in (0.10, 0.05, 0.025, 0.01, 0.005)))
print("  df = oo: " + "  ".join(f"{norm.isf(a_):6.3f}" for a_ in (0.10, 0.05, 0.025, 0.01, 0.005)))

# Exercise "Test direction and critical value" (table values, 3 decimals)
show("1) left-sided,  t_0.95;15  (n = 16, alpha = 0.05)", stats.t.ppf(0.95, 15), ".3f")   # 1.753
show("2) right-sided, z_0.99     (sigma known, alpha = 0.01)", norm.ppf(0.99), ".3f")     # 2.326
show("3) two-sided,   t_0.995;9  (n = 10, alpha = 0.01)", stats.t.ppf(0.995, 9), ".3f")   # 3.250
show("4) right-sided, t_0.90;20  (n = 21, alpha = 0.10)", stats.t.ppf(0.90, 20), ".3f")   # 1.325

# Exercise / solution "Substance K": known sigma = 90, n = 9, xbar = 1060,
# mu0 = 1000 (right-sided)
Z_K = (1060 - 1000) / (90 / np.sqrt(9))
show("Z_n substance K", Z_K, ".2f")                            # 2.00
show("p = 1 - Phi(2.00)", norm.sf(Z_K))                        # 0.0228

# Exercise "Discount campaign (right-sided t-test)": mu0 = 48 EUR, n = 25,
# xbar = 51.20 EUR, s = 8 EUR, alpha = 0.05
se_dc = 8 / np.sqrt(25)
T_dc = (51.20 - 48) / se_dc
show("SE discount campaign = 8/5", se_dc, ".1f")                # 1.6
show("T_n discount campaign = 3.2/1.6", T_dc, ".2f")            # 2.00
show("t_0.95;24", stats.t.ppf(0.95, 24))                        # 1.7109
show("critical mean 48 + 1.7109 * 1.6 (table value)", 48 + 1.7109 * se_dc, ".2f")       # 50.74
show("  ... with the unrounded quantile", 48 + stats.t.ppf(0.95, 24) * se_dc, ".2f")   # 50.74

# Slides "One-sided p-value -- milk" and "One-sided test with Python"
p_less = stats.ttest_1samp(milk, 1000, alternative="less").pvalue
p_greater = stats.ttest_1samp(milk, 1000, alternative="greater").pvalue
show("milk left-sided p  (F_t,8(0.7947))", p_less)             # 0.7751
show("milk right-sided p (1 - 0.7751)", p_greater)             # 0.2249

# Slides "One-sided p-value -- cream" and "One-sided test with Python"
res = stats.ttest_1samp(cream, 250, alternative="less")
ci = res.confidence_interval(0.95)                              # one-sided CI
print(f"ttest_1samp(cream, 250, 'less'):  t = {res.statistic:.4f}, "
      f"df = {res.df}, p = {res.pvalue:.4f}, 95% CI: [{ci.low}, {ci.high:.2f}]")
# -> t = -2.1086, df = 15, p = 0.0261, 95% CI: [-inf, 249.82]

# Exercise / solution "One- vs. two-sided" (T_n = 1.80, df = 15)
show("right-sided p = 1 - F_t,15(1.80)", stats.t.sf(1.80, 15))  # 0.0460
show("two-sided p", 2 * stats.t.sf(1.80, 15))                  # 0.0920
show("check: t_0.95;15, t_0.975;15", (stats.t.ppf(0.95, 15), stats.t.ppf(0.975, 15)), ".3f")  # 1.753, 2.131

# Slide "One-sided CIs -- milk and cream (known)"
# The slide uses z_0.95 = 1.645; the unrounded 1.644854 changes only the
# 4th decimal (1002.6449 vs. 1002.645, 249.7599 vs. 249.760, ...).
z95 = norm.ppf(0.95)
show("milk upper bound (left-sided test)", xbar_milk + z95 * 3 / np.sqrt(9))       # 1002.645
show("cream upper bound (left-sided test)", xbar_cream + z95 * 2 / np.sqrt(16))    # 249.760
show("milk lower bound (right-sided test)", xbar_milk - z95 * 3 / np.sqrt(9))      # 999.355
show("cream lower bound (right-sided test)", xbar_cream - z95 * 2 / np.sqrt(16))   # 248.115

# Exercise / solution "Net weight" (n = 12, xbar = 496, s = 6, mu0 = 500, left-sided)
T_nw = (496 - 500) / (6 / np.sqrt(12))
show("T_n net weight", T_nw)                                   # -2.3094
show("p = F_t,11(T_n)", stats.t.cdf(T_nw, df=11))              # 0.0207

# Exam-style exercise "Muesli filling" (right-sided t-test): mu0 = 250 g,
# n = 25, xbar = 252.6 g, s = 5.0 g, alpha = 0.05
t_m = (252.6 - 250) / (5.0 / np.sqrt(25))
show("t muesli", t_m, ".2f")                                    # 2.60
show("t_0.95;24, t_0.99;24, t_0.995;24",
     (stats.t.ppf(0.95, 24), stats.t.ppf(0.99, 24), stats.t.ppf(0.995, 24)))  # 1.7109 2.4922 2.7969
show("exact one-sided p = 1 - F_t,24(2.6)", stats.t.sf(t_m, 24))  # 0.0079 (in (0.005, 0.01))
show("normal approximation 1 - Phi(2.60)", norm.sf(2.60))        # 0.0047
show("table 1 - 0.9953", 1 - 0.9953)
show("95% CI muesli (two-sided)",
     252.6 + np.array([-1, 1]) * stats.t.ppf(0.975, 24) * 1.0, ".2f")  # [250.54, 254.66]
show("one-sided 95% CI (right-sided test): lower bound 252.6 - 1.7109 * 1.0",
     252.6 - stats.t.ppf(0.95, 24) * 1.0, ".2f")               # 250.89

# Exam-style exercise "Delivery time revisited" (left-sided t-test):
# claim "mean delivery time below 48 h", n = 16, xbar = 46.4, s = 3.2
t_l = (46.4 - 48) / (3.2 / np.sqrt(16))
show("t delivery revisited", t_l, ".2f")                        # -2.00
show("-t_0.95;15", -stats.t.ppf(0.95, 15))                      # -1.7531
show("p = F_t,15(-2.0)", stats.t.cdf(t_l, 15))                  # 0.0320
show("two-sided 95% CI",
     46.4 + np.array([-1, 1]) * stats.t.ppf(0.975, 15) * 0.8, ".2f")  # [44.69, 48.11]
show("  margin of error 2.1314 * 0.8 (table value)", 2.1314 * 0.8)    # 1.7051
show("  ... with the unrounded quantile", stats.t.ppf(0.975, 15) * 0.8)  # 1.7052
show("one-sided 95% CI: upper bound 46.4 + 1.7531 * 0.8",
     46.4 + stats.t.ppf(0.95, 15) * 0.8, ".2f")                 # 47.80
show("two-sided p (for comparison)", 2 * stats.t.cdf(t_l, 15))  # 0.0639

# =====================================================================
# 5 Types of error (beta and power: Appendix A.8)
# =====================================================================
header("5 Types of error (power: Appendix A.8)")

# Slide "Computing beta concretely -- milk":
# H0 mu = 1000, sigma = 3, n = 9 (SE = 1), true mu1 = 1002
se = 3 / np.sqrt(9)
lo, hi = 1000 - 1.96 * se, 1000 + 1.96 * se
show("acceptance region for xbar", (lo, hi), ".2f")            # [998.04, 1001.96]
beta = norm.cdf((hi - 1002) / se) - norm.cdf((lo - 1002) / se)
show("beta (milk, n = 9)", beta, ".3f")                        # 0.484
show("power (milk, n = 9)", 1 - beta, ".3f")                   # 0.516
# cross-check with statsmodels (one-sample z-test: ratio=0, effect size d = 2/3)
show("  ... via statsmodels NormalIndPower",
     NormalIndPower().power(effect_size=2 / 3, nobs1=9, alpha=0.05, ratio=0), ".3f")

# Slide "Four levers for more power": same situation with n = 36
se36 = 3 / np.sqrt(36)
beta36 = (norm.cdf((1000 + 1.96 * se36 - 1002) / se36)
          - norm.cdf((1000 - 1.96 * se36 - 1002) / se36))
show("beta (milk, n = 36)", beta36, ".3f")                     # 0.021
show("power (milk, n = 36)", 1 - beta36, ".3f")                # 0.979

# Slide "beta and power with Python" (milk, n = 9 and 36; statsmodels)
for n_ in (9, 36):
    se_ = 3 / np.sqrt(n_)
    lo_, hi_ = 1000 - 1.96 * se_, 1000 + 1.96 * se_
    b_ = norm.cdf(hi_, 1002, se_) - norm.cdf(lo_, 1002, se_)
    print(f"n = {n_}: beta = {b_:.3f}, power = {1 - b_:.3f}")
# -> n = 9: beta = 0.484, power = 0.516;  n = 36: beta = 0.021, power = 0.979
pw_ = NormalIndPower()
show("statsmodels power (d = 2/3, n = 9)",
     pw_.power(effect_size=2 / 3, nobs1=9, alpha=0.05, ratio=0), ".3f")          # 0.516
n80 = pw_.solve_power(effect_size=2 / 3, power=0.80, alpha=0.05, ratio=0)
show("statsmodels solve_power: n for 80 % power", n80, ".2f")                    # 17.66
print("   -> round up: n =", math.ceil(n80))                                     # 18

# Exercise / solution "beta and power (two-sided)":
# sigma = 10, n = 25, mu0 = 100, mu1 = 105
se = 10 / np.sqrt(25)
show("acceptance region for xbar", (100 - 1.96 * se, 100 + 1.96 * se), ".2f")  # [96.08, 103.92]
beta2 = (norm.cdf((100 + 1.96 * se - 105) / se)
         - norm.cdf((100 - 1.96 * se - 105) / se))
show("beta (exercise)", beta2)                                 # 0.2946
show("power (exercise)", 1 - beta2)                            # 0.7054

# Exercise / solution "Power of a one-sided test" (right-sided, H1: mu > 100)
x_crit = 100 + norm.ppf(0.95) * se
show("critical mean", x_crit, ".2f")                           # 103.29
show("power (right-sided)", norm.sf((x_crit - 105) / se))      # 0.8038
# -> the slide shows 0.8037: it uses the rounded z_0.95 = 1.645, i.e.
#    1 - Phi(-0.855) = 0.80373; the unrounded quantile gives 0.80376.
show("power (right-sided, z = 1.645 as on slide)", norm.sf((100 + 1.645 * se - 105) / se))


# =====================================================================
# A Appendix: estimators and the law of large numbers
# =====================================================================
header("A Appendix")

# Exercise "Properties of estimators: egg weight" (n = 4, mu = 50, sigma^2 = 25)
weights = {"A": [1/4, 1/4, 1/4, 1/4], "B": [1/2, 0, 0, 1/2],
           "C": [1/5, 2/5, 1/5, 1/5], "D": [1/4, 1/4, 1/4, 0]}
for k, w in weights.items():
    w = np.array(w)
    print(f"estimator {k}: E = {50 * w.sum():.1f}, bias = {50 * w.sum() - 50:+.1f}, "
          f"Var = {25 * np.sum(w ** 2):.4f}")
# -> A: 50, 6.25; B: 50, 12.5; C: 50, 7; D: 37.5 (bias -12.5), 4.6875

# Simulation shown on the slide (10 000 samples of 4 eggs)
rng = np.random.default_rng(1)
m = rng.normal(50, 5, size=(10_000, 4))
A = m.mean(axis=1)
B = (m[:, 0] + m[:, 3]) / 2
C = (m[:, 0] + 2 * m[:, 1] + m[:, 2] + m[:, 3]) / 5
D = (m[:, 0] + m[:, 1] + m[:, 2]) / 4
print("means:    ", np.round([A.mean(), B.mean(), C.mean(), D.mean()], 2))
print("variances:", np.round([A.var(ddof=1), B.var(ddof=1), C.var(ddof=1), D.var(ddof=1)], 2))

# Slide "Why divide by n - 1?": average of s^2 over many samples of size 4
rng = np.random.default_rng(5)
samples = rng.normal(50, 5, size=(100_000, 4))
show("mean of s^2 with n-1 (sigma^2 = 25)", samples.var(axis=1, ddof=1).mean(), ".2f")  # ~ 25
show("mean of s^2 with n   ((n-1)/n * 25 = 18.75)", samples.var(axis=1, ddof=0).mean(), ".2f")

# Slide "Law of large numbers": fair die, E(X) = 3.5, sd = sqrt(35/12)
show("die: E(X), sd(X)", (3.5, np.sqrt(35 / 12)), ".3f")        # 3.5, 1.708
for n_ in (10, 100, 1000):
    print(f"  n = {n_:>4}: 95% of running means within 3.5 +- {1.96 * np.sqrt(35 / 12) / np.sqrt(n_):.2f}")  # 1.06, 0.33, 0.11
