# =====================================================================
# Quantitative Research -- Part 3: Statistical Inference
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces the numbers shown on the slides of Part 3 (numpy, scipy,
# statsmodels). Run headless:  python3 Part_3_Statistical_Inference.py
# Sections follow the sections of the slide deck:
#   1  Confidence intervals   (milk, cream; known and unknown variance)
#   2  Hypothesis tests       (z- and t-test, reaction time)
#   3  The p-value
#   4  One-sided tests        (one-sided p-values and CIs, net weight)
#   5  Types of error         (beta and power)
#
# Note: a few slides work with table values rounded to 3-4 decimals
# (z_0.95 = 1.645, Phi(1.85) = 0.9678). Where Python's unrounded value
# changes the last printed digit, this is pointed out in a comment.
# =====================================================================

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
# 1 Confidence intervals
# =====================================================================
header("1 Confidence intervals")

# Slide "CI for milk (known variance)"
xbar_milk = milk.mean()
z = norm.ppf(1 - alpha / 2)
show("mean(milk)", xbar_milk)                                  # 1001
show("z_0.975", z)                                             # 1.96
show("milk 95% CI, sigma = 3", xbar_milk + np.array([-1, 1]) * z * 3 / np.sqrt(9),
     ".2f")                                                    # [999.04, 1002.96]

# Slide "Different confidence levels" (table 90 / 95 / 99 %)
for lev in (0.90, 0.95, 0.99):
    z_lev = norm.ppf(1 - (1 - lev) / 2)
    show(f"milk {lev:.0%} CI (z = {z_lev:.3f})",
         xbar_milk + np.array([-1, 1]) * z_lev * 3 / np.sqrt(9), ".2f")
# -> [999.36, 1002.64] for 90 %: the slide shows 1002.65 because it uses the
#    rounded z_0.95 = 1.645 (1001 + 1.645 = 1002.645); unrounded 1.644854
#    gives 1002.6449. 99 %: [998.42, 1003.58] as on the slide.

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

# Exercise / solution "CI for cream": known (sigma = 2) and unknown variance
xbar_cream = cream.mean()
show("mean(cream)", xbar_cream)                                # 248.9375
show("cream 95% CI, sigma = 2",
     xbar_cream + np.array([-1, 1]) * 1.96 * 2 / np.sqrt(16), ".2f")  # [247.96, 249.92]
show("var(cream)", cream.var(ddof=1))                          # 4.0625
s_cream = cream.std(ddof=1)
show("sd(cream)", s_cream)                                     # 2.0156
show("cream 95% CI, sigma unknown",
     xbar_cream + np.array([-1, 1]) * stats.t.ppf(0.975, 15) * s_cream / np.sqrt(16),
     ".2f")                                                    # [247.86, 250.01]

# =====================================================================
# 2 Hypothesis tests
# =====================================================================
header("2 Hypothesis tests")

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

# =====================================================================
# 3 The p-value (two-sided)
# =====================================================================
header("3 The p-value")

# Slides "p-value -- milk / cream (two variants)"
show("p milk, sigma known", 2 * norm.cdf(-abs(Zn_milk)))       # 0.3173
show("p milk, sigma unknown", 2 * stats.t.cdf(-abs(Tn_milk), df=8))   # 0.4497
show("p cream, sigma known", 2 * norm.cdf(-abs(Zn_cream)))     # 0.0336
show("p cream, sigma unknown", 2 * stats.t.cdf(-abs(Tn_cream), df=15))  # 0.0522

# Exercise "p-value from Z_n = 1.85"
show("Phi(1.85)", norm.cdf(1.85))                              # 0.9678
show("p = 2 (1 - Phi(1.85))", 2 * norm.sf(1.85))
# -> 0.0643; the slide shows 0.0644 = 2 * (1 - 0.9678) from the rounded table
#    value Phi(1.85) = 0.9678 (unrounded 0.967843).

# Slide "Significant != important -- the large-n trap" (xbar = 1000.2, sigma = 3)
for n in (9, 10_000):
    z_n = 0.2 / (3 / np.sqrt(n))
    print(f"large-n trap: n = {n:>6}, Z_n = {z_n:.2f}, p = {2 * norm.sf(z_n):.4g}")
# -> n = 9: Z_n = 0.20, p = 0.84;  n = 10000: Z_n = 6.67, p < 0.0001

# =====================================================================
# 4 One-sided tests
# =====================================================================
header("4 One-sided tests")

# Slides "Critical values" / t-table hint
show("z_0.95", norm.ppf(0.95))                                 # 1.6449 (slides: 1.645)
show("t_0.95;11", stats.t.ppf(0.95, 11))                       # 1.7959

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

# Exercise / solution "Substance K": known sigma = 90, n = 9, xbar = 1060,
# mu0 = 1000 (right-sided)
Z_K = (1060 - 1000) / (90 / np.sqrt(9))
show("Z_n substance K", Z_K, ".2f")                            # 2.00
show("p = 1 - Phi(2.00)", norm.sf(Z_K))                        # 0.0228

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

# Exercise / solution "One- vs. two-sided" (T_n = 1.80, df = 15)
show("right-sided p = 1 - F_t,15(1.80)", stats.t.sf(1.80, 15))  # 0.0460
show("two-sided p", 2 * stats.t.sf(1.80, 15))                  # 0.0920

# =====================================================================
# 5 Types of error: beta and power
# =====================================================================
header("5 Types of error")

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
