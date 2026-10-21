# =====================================================================
# Quantitative Research -- Part 3: Statistical Inference
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces the numbers shown on the slides of Part 3. Base R only.
# Sections follow the sections of the slide deck:
#   1  Confidence intervals   (milk, cream; known and unknown variance)
#   2  Hypothesis tests       (z- and t-test, reaction time)
#   3  The p-value
#   4  One-sided tests        (one-sided p-values and CIs, net weight)
#   5  Types of error         (beta and power)
# =====================================================================

# ---------------------------------------------------------------------
# SETUP: the two running examples
# ---------------------------------------------------------------------
milk  <- c(1005, 1001, 997, 1000, 1001, 998, 999, 999, 1009)   # ml, sigma = 3
cream <- c(251, 248, 248, 249, 250, 251, 247, 246, 252,
           251, 248, 247, 246, 249, 248, 252)                   # g, sigma^2 = 4
alpha <- 0.05

# =====================================================================
# 1 Confidence intervals
# =====================================================================
# milk, known variance
mean(milk)                                           # 1001
z <- qnorm(1 - alpha / 2)                            # 1.96
mean(milk) + c(-1, 1) * z * 3 / sqrt(9)              # [999.04, 1002.96]
# different confidence levels
for (lev in c(0.90, 0.95, 0.99))
  print(mean(milk) + c(-1, 1) * qnorm(1 - (1 - lev) / 2) * 3 / sqrt(9))  # slides use z rounded to 3 decimals

# milk, unknown variance
sd(milk)                                             # 3.7749
qt(1 - alpha / 2, df = 8)                            # 2.3060
mean(milk) + c(-1, 1) * qt(0.975, 8) * sd(milk) / sqrt(9)   # [998.10, 1003.90]

# cream exercise: known (sigma = 2) and unknown variance
mean(cream)                                          # 248.9375
mean(cream) + c(-1, 1) * 1.96 * 2 / sqrt(16)         # [247.96, 249.92]
var(cream); sd(cream)                                # 4.0625, 2.0156
mean(cream) + c(-1, 1) * qt(0.975, 15) * sd(cream) / sqrt(16)  # [247.86, 250.01]

# =====================================================================
# 2 Hypothesis tests
# =====================================================================
(Zn_milk  <- (mean(milk) - 1000) / (3 / sqrt(9)))             # 1.000
(Tn_milk  <- (mean(milk) - 1000) / (sd(milk) / sqrt(9)))      # 0.7947
(Zn_cream <- (mean(cream) - 250) / (2 / sqrt(16)))            # -2.125
(Tn_cream <- (mean(cream) - 250) / (sd(cream) / sqrt(16)))    # -2.1086
t.test(milk, mu = 1000)                     # two-sided t-test with CI

# reaction time exercise (n = 50, xbar = 242, s = 30, mu0 = 250)
(T_rt <- (242 - 250) / (30 / sqrt(50)))                       # -1.8856
qt(0.975, 49)                                                 # 2.0096
2 * pt(-abs(T_rt), 49)                                        # 0.0653

# =====================================================================
# 3 The p-value (two-sided)
# =====================================================================
2 * pnorm(-abs(Zn_milk))                    # 0.3173
2 * pt(-abs(Tn_milk), df = 8)               # 0.4497
2 * pnorm(-abs(Zn_cream))                   # 0.0336
2 * pt(-abs(Tn_cream), df = 15)             # 0.0522
2 * (1 - pnorm(1.85))                       # exercise: 0.0643 (slide: 0.0644 from the table value 0.9678)

# large-n trap: xbar = 1000.2, sigma = 3
for (n in c(9, 10000)) {
  z_n <- 0.2 / (3 / sqrt(n)); print(c(n = n, z = z_n, p = 2 * pnorm(-z_n)))
}

# =====================================================================
# 4 One-sided tests
# =====================================================================
qnorm(0.95); qt(0.95, 11)                   # 1.645, 1.7959
t.test(milk,  mu = 1000, alternative = "less")      # p = 0.7751
t.test(milk,  mu = 1000, alternative = "greater")   # p = 0.2249
t.test(cream, mu = 250,  alternative = "less")      # p = 0.0261, CI (-Inf, 249.82]

# substance K: known sigma = 90, n = 9, xbar = 1060, mu0 = 1000 (right-sided)
(Z_K <- (1060 - 1000) / (90 / sqrt(9)))     # 2.00
1 - pnorm(Z_K)                              # 0.0228

# one-sided CIs with known variance
1001 + qnorm(0.95) * 3 / sqrt(9)            # milk, upper bound 1002.645
1001 - qnorm(0.95) * 3 / sqrt(9)            # milk, lower bound  999.355

# net weight exercise (n = 12, xbar = 496, s = 6, mu0 = 500, left-sided)
(T_nw <- (496 - 500) / (6 / sqrt(12)))      # -2.3094
pt(T_nw, df = 11)                           # 0.0207

# one- vs. two-sided (T = 1.80, df = 15)
1 - pt(1.80, 15); 2 * (1 - pt(1.80, 15))    # 0.0460, 0.0920

# =====================================================================
# 5 Types of error: beta and power
# =====================================================================
# milk: H0 mu = 1000, sigma = 3, n = 9 (SE = 1), true mu1 = 1002
se <- 3 / sqrt(9)
lo <- 1000 - 1.96 * se; hi <- 1000 + 1.96 * se
(beta <- pnorm((hi - 1002) / se) - pnorm((lo - 1002) / se))   # 0.484
1 - beta                                                      # power 0.516
se36 <- 3 / sqrt(36)                                          # n = 36
1 - (pnorm((1000 + 1.96 * se36 - 1002) / se36) -
     pnorm((1000 - 1.96 * se36 - 1002) / se36))               # 0.979

# exercise: sigma = 10, n = 25, mu0 = 100, mu1 = 105
se <- 10 / sqrt(25)
(beta2 <- pnorm((100 + 1.96 * se - 105) / se) -
          pnorm((100 - 1.96 * se - 105) / se))                # 0.2946
1 - beta2                                                     # 0.7054
1 - pnorm((100 + qnorm(0.95) * se - 105) / se)                # right-sided: 0.8037
