# =====================================================================
# Quantitative Research -- Part 4: Regression
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 4. Run it from the
# folder Part_4_Regression (the data sets are read from ../data):
#     python3 Part_4_Regression.py
# Plots are drawn headless (Agg backend) and closed again -- nothing is
# written to disk; all numbers are printed.
# Sections follow the sections of the slide deck:
#   1  Correlation              (lamp example)
#   2  Simple regression        (least squares, leverage)
#   3  Goodness of fit          (variance decomposition, R^2)
#   4  Residual analysis        (residual plot, QQ-plot), body heights
#   5  Inference                (SE, t-test, CI, p-value, prediction)
#   6  Multiple regression      (Advertising, Credit)
#   Appendix                    (interactions, diagnostics, collinearity / VIF)
# =====================================================================
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                       # headless: no window opens
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

DATA = Path(__file__).resolve().parent.parent / "data"
pd.set_option("display.width", 120)
# summary() runs normality tests that warn for small n (n = 6, 9, 15) -- silence them
warnings.filterwarnings("ignore", category=UserWarning)


def header(title):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70)


def fit_line(m):
    """Short summary line: R^2, adjusted R^2, F, p(F), sigma-hat."""
    print(f"R^2 = {m.rsquared:.4f}, adj. R^2 = {m.rsquared_adj:.4f}, "
          f"F = {m.fvalue:.1f} (p = {m.f_pvalue:.3g}), "
          f"sigma = {np.sqrt(m.scale):.4f}, df = {m.df_resid:.0f}")


# ---------------------------------------------------------------------
# SETUP: lamp example (price in Euro, sales quantity) -- running story
# ---------------------------------------------------------------------
price = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120])
quantity = np.array([20, 17, 15, 9, 11, 8, 4, 4, 2])
df = pd.DataFrame({"price": price, "quantity": quantity})
n = len(df)

# =====================================================================
# 1 Correlation
# =====================================================================
header("1 Correlation -- slide 'Covariance and correlation with Python'")
fig, ax = plt.subplots()
ax.scatter(df["price"], df["quantity"])
ax.set(xlabel="Price (Euro)", ylabel="Sales quantity", title="Scatter plot")
plt.close(fig)
print("cov  :", df["price"].cov(df["quantity"]))            # -83.75
print("corr :", round(df["price"].corr(df["quantity"]), 4))  # -0.9732
print("sd   :", round(df["price"].std(), 4), round(df["quantity"].std(), 4))  # 13.6931, 6.2849

# Exercise "covariance and correlation by hand"
xa = pd.Series([2, 4, 5, 6, 8]); ya = pd.Series([10, 14, 17, 16, 23])
print("Exercise cov/sd/sd/corr:", xa.cov(ya), round(xa.std(), 4),
      round(ya.std(), 4), round(xa.corr(ya), 4))   # 10.25, 2.2361, 4.7434, 0.9664

# =====================================================================
# 2 Simple linear regression
# =====================================================================
header("2 Simple regression -- slide 'Linear regression with Python'")
beta1 = df["price"].cov(df["quantity"]) / df["price"].var()
beta0 = df["quantity"].mean() - beta1 * df["price"].mean()
print("beta1 =", round(beta1, 4), " beta0 =", round(beta0, 4))   # -0.4467, 54.6667
print("beta1 * s_x / s_y =", round(beta1 * df["price"].std() / df["quantity"].std(), 4))

reg = smf.ols("quantity ~ price", data=df).fit()
print(reg.params.round(4))                                      # 54.6667 -0.4467
fig, ax = plt.subplots()
ax.scatter(df["price"], df["quantity"])
xs = np.array([0, 125])
ax.plot(xs, reg.params["Intercept"] + reg.params["price"] * xs, color="red")
ax.set(xlim=(0, 125), ylim=(0, 60))
plt.close(fig)

# Sums of squares used on the slides
xc = price - price.mean(); yc = quantity - quantity.mean()
Sxx, Sxy, Syy = (xc**2).sum(), (xc * yc).sum(), (yc**2).sum()
print("Sxx, Sxy, Syy:", Sxx, Sxy, Syy)                          # 1500 -670 316

# Slide 'Leverage values -- lamp example': h_i = 1/n + (x_i - xbar)^2 / Sxx
h = reg.get_influence().hat_matrix_diag
print("leverages:", h.round(3))                    # 0.378 (ends) ... 0.111 (centre)
print("rules of thumb 4/n, 6/n:", round(4 / n, 3), round(6 / n, 3))   # 0.444, 0.667

# Exercise "least squares by hand"
ex = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [3, 4, 2, 5, 6]})
print("Exercise least squares:", smf.ols("y ~ x", data=ex).fit().params.round(4).tolist())  # 1.9, 0.7

# =====================================================================
# 3 Goodness of fit
# =====================================================================
header("3 Goodness of fit -- slide 'Coefficient of determination in Python'")
TSS = ((quantity - quantity.mean())**2).sum()               # 316
RSS = (reg.resid**2).sum()                                  # 16.7333
ESS = ((reg.fittedvalues - quantity.mean())**2).sum()       # 299.2667
print("TSS, RSS, ESS:", TSS, round(RSS, 4), round(ESS, 4))
print("R^2 = 1 - RSS/TSS =", round(1 - RSS / TSS, 4))      # 0.9470
print("reg.rsquared      =", round(reg.rsquared, 4))
print("corr^2            =", round(df["price"].corr(df["quantity"])**2, 4))

# =====================================================================
# 4 Residual analysis
# =====================================================================
header("4 Residual analysis -- residual plot and QQ-plots")
# Slide 'Creating a residual plot with Python'
fig, ax = plt.subplots()
ax.scatter(reg.fittedvalues, reg.resid)
ax.axhline(0, linestyle="--")
ax.set(xlabel="fitted values", ylabel="residuals", title="Residual plot")
plt.close(fig)

# Slide 'Creating a QQ-plot with Python': two empirical distributions
fig, ax = plt.subplots()
qx, qy = np.sort(df["price"]), np.sort(df["quantity"])
ax.scatter(qx, qy)
q1x, q3x = np.percentile(qx, [25, 75]); q1y, q3y = np.percentile(qy, [25, 75])
slope = (q3y - q1y) / (q3x - q1x)
ax.axline((q1x, q1y), slope=slope, linestyle="--")
plt.close(fig)
print("two-sample QQ line through quartiles: slope", round(slope, 4))

# Slide 'QQ-plot of the residuals ... in Python' (positions (i-0.5)/n: a=0.5)
fig = sm.qqplot(reg.resid, line="q", a=0.5)
plt.close(fig)
# table on the slide 'Inspecting the residuals with the QQ-plot -- example'
u = np.sort(reg.resid.to_numpy()); p = (np.arange(1, n + 1) - 0.5) / n
print(pd.DataFrame({"resid": reg.resid.round(4), "u_sorted": u.round(4),
                    "p": p.round(4), "z": stats.norm.ppf(p).round(4)}))

# Exercise body heights (k) -- shoe sizes (s)
header("4 Exercise body heights -- shoe sizes")
ks = pd.DataFrame({
    "k": [164, 162, 168, 198, 166, 166, 192, 160, 151, 175, 180, 160, 168, 175, 168],
    "s": [39, 38, 39, 46, 40, 39, 45, 37, 36, 42, 43, 38, 41, 40, 39]})
print("cov, corr:", round(ks["k"].cov(ks["s"]), 4), round(ks["k"].corr(ks["s"]), 4))  # 33.6857, 0.9684
reg_ks = smf.ols("s ~ k", data=ks).fit()
print(reg_ks.params.round(4).tolist(), " R^2 =", round(reg_ks.rsquared, 4))  # 2.3147, 0.2222; 0.9379
fig, ax = plt.subplots(); ax.scatter(reg_ks.fittedvalues, reg_ks.resid)
ax.axhline(0, linestyle="--"); plt.close(fig)
fig = sm.qqplot(reg_ks.resid, line="q", a=0.5); plt.close(fig)

# =====================================================================
# 5 Inference in simple regression
# =====================================================================
header("5 Inference -- slide 'Reading the regression output in Python'")
print(reg.summary().tables[1])
fit_line(reg)                                   # R^2 0.947, F 125.2, sigma 1.5461
sigma_hat = np.sqrt(RSS / (n - 2))              # = np.sqrt(reg.scale) = 1.5461
se_b1 = sigma_hat / np.sqrt(Sxx)                # 0.03992
se_b0 = sigma_hat * np.sqrt(1 / n + price.mean()**2 / Sxx)   # 4.0252
print("sigma_hat, SE(b1), SE(b0):", round(sigma_hat, 4), round(se_b1, 5), round(se_b0, 4))
print("statsmodels bse:", reg.bse.round(5).tolist())

# t-test H0: beta1 = 0
T = reg.params["price"] / reg.bse["price"]                  # -11.19
print("T =", round(T, 2), " = reg.tvalues:", round(reg.tvalues["price"], 2))
print("t_0.975;7 =", round(stats.t.ppf(0.975, df=n - 2), 4))           # 2.3646
print("two-sided p =", f"{2 * stats.t.cdf(-abs(T), df=n - 2):.3g}")    # 1.02e-05
# one-sided H1: beta1 < 0
print("t_0.95;7 =", round(stats.t.ppf(0.95, df=n - 2), 4))             # 1.8946
print("left-sided p =", f"{stats.t.cdf(T, df=n - 2):.3g}")             # 5.1e-06
# H0: beta1 = -0.5  (slide 'Inference in simple regression with Python (1/2)')
T2 = (reg.params["price"] - (-0.5)) / reg.bse["price"]                 # 1.336
print("T2 =", round(T2, 3), " p =", round(2 * stats.t.sf(abs(T2), df=n - 2), 3))  # 0.223

# confidence intervals
print(reg.conf_int(alpha=0.05).round(4))       # beta1: [-0.5411, -0.3523], beta0: [45.15, 64.18]
print("by hand:", (beta1 + np.array([-1, 1]) * stats.t.ppf(0.975, n - 2) * se_b1).round(4))

# F-statistic = T^2 in simple regression
print("T^2 =", round(T**2, 1), " F =", round(reg.fvalue, 1))           # 125.2

# prediction: confidence vs. prediction interval (slide '... with Python (2/2)')
new = pd.DataFrame({"price": [100, 110, 125]})
pred = reg.get_prediction(new).summary_frame(alpha=0.05)
print(pred.round(2))               # 110: CI [3.99, 7.07], PI [1.57, 9.50]; 125: -1.17

# Exercise: inference for the shoe-size regression
header("5 Exercise -- inference for the shoe-size regression")
print(reg_ks.summary().tables[1])
fit_line(reg_ks)
print(reg_ks.conf_int().round(4))                                      # [0.1879, 0.2565]
print("t_0.975;13 =", round(stats.t.ppf(0.975, df=13), 4))             # 2.1604
T3 = (reg_ks.params["k"] - 0.25) / reg_ks.bse["k"]                     # -1.75
print("T3 =", round(T3, 2), " p =", round(2 * stats.t.sf(abs(T3), df=13), 3))   # 0.103
print(reg_ks.get_prediction(pd.DataFrame({"k": [180]}))
      .summary_frame(alpha=0.05).round(2))

# Exercise used cars from A to Z
header("5 Exercise -- used cars from A to Z")
cars = pd.DataFrame({"age": range(1, 7), "value": [19, 18, 17, 15, 12, 9]})
car = smf.ols("value ~ age", data=cars).fit()
print(car.summary().tables[1])
fit_line(car)
print(car.conf_int().round(4))                                         # [-2.66, -1.34]
print("t_0.975;4 =", round(stats.t.ppf(0.975, df=4), 3))               # 2.776
print(car.get_prediction(pd.DataFrame({"age": [7]}))
      .summary_frame(alpha=0.05).round(2))                             # PI [4.21, 11.79]

# =====================================================================
# 6 Multiple linear regression
# =====================================================================
header("6 Multiple regression -- Advertising data")
ad = pd.read_csv(DATA / "Advertising.csv", index_col=0)
m_tv = smf.ols("sales ~ TV", data=ad).fit()
print(m_tv.summary().tables[1]); fit_line(m_tv)                        # slide 'Significant != important'
print(m_tv.conf_int().round(4))                                        # [0.0422, 0.0528]
print(smf.ols("sales ~ radio", data=ad).fit().summary().tables[1])
print(smf.ols("sales ~ newspaper", data=ad).fit().summary().tables[1])

# Slide 'Multiple regression with Python'
m3 = smf.ols("sales ~ TV + radio + newspaper", data=ad).fit()
print(m3.summary().tables[1])
fit_line(m3)                                   # R^2 0.897, F 570.3, sigma 1.686
print(m3.conf_int().round(4))
print("t_0.975;196 =", round(stats.t.ppf(0.975, df=196), 3))           # 1.972
print(ad.corr().round(4))                      # corr(radio, newspaper) = 0.354

# F-test by hand
TSS_ad = ((ad["sales"] - ad["sales"].mean())**2).sum()               # 5417.15
RSS_ad = (m3.resid**2).sum()                                         # 556.83
print("TSS, RSS:", round(TSS_ad, 2), round(RSS_ad, 2))
print("F =", round(((TSS_ad - RSS_ad) / 3) / (RSS_ad / (200 - 3 - 1)), 1))   # 570.3
print("F_0.95;3,196 =", round(stats.f.ppf(0.95, 3, 196), 2))         # 2.65

# dropping newspaper (slide 'Model choice -- dropping newspaper')
m2 = smf.ols("sales ~ TV + radio", data=ad).fit()
print(m2.summary().tables[1])
for name, m in [("TV+radio+newspaper", m3), ("TV+radio", m2)]:
    print(f"{name:20s} R^2 = {m.rsquared:.5f}  adj = {m.rsquared_adj:.5f}  "
          f"sigma = {np.sqrt(m.scale):.4f}")
print(sm.stats.anova_lm(m2, m3))                 # partial F = 0.031, p = 0.86
pred_ad = m2.get_prediction(pd.DataFrame({"TV": [100], "radio": [20]}))
print(pred_ad.summary_frame(alpha=0.05).round(2))  # 11.26, CI [10.99, 11.53], PI [7.93, 14.58]

# qualitative predictors (Credit data)
header("6 Multiple regression -- Credit data")
cr = pd.read_csv(DATA / "Credit.csv")
# Exercise "reading a multiple regression output" (Credit data)
mc = smf.ols("Balance ~ Income + Limit + Student", data=cr).fit()
print(mc.summary().tables[1])
fit_line(mc)                                     # R^2 0.9488, adj 0.9484, F 2447, sigma 104.4
print(mc.conf_int().round(3))                    # Income: [-8.380, -7.424]
print("t_0.975;396 =", round(stats.t.ppf(0.975, 396), 3))            # 1.966
print("alone:", smf.ols("Balance ~ Income", data=cr).fit().params.round(2).tolist())  # +6.05
print("corr(Income, Limit) =", round(cr["Income"].corr(cr["Limit"]), 2))  # 0.79
new_cr = pd.DataFrame({"Income": 50, "Limit": 5000, "Student": ["No", "Yes"]})
print(mc.get_prediction(new_cr).summary_frame(alpha=0.05).round(1))  # 510.3 [304.7, 715.8]; 937.3

print(smf.ols("Balance ~ Student", data=cr).fit().summary().tables[1])          # 480.37, 396.46
print(smf.ols("Balance ~ Income + Student", data=cr).fit().summary().tables[1]) # 211.1, 5.98, 382.7
print(smf.ols("Balance ~ Region", data=cr).fit().summary().tables[1])           # baseline East

# =====================================================================
# Appendix A.2: Interactions
# =====================================================================
header("Appendix A.2 -- interaction sales ~ TV * radio")
mi = smf.ols("sales ~ TV * radio", data=ad).fit()       # TV + radio + TV:radio
print(mi.summary().tables[1])
fit_line(mi)                                             # R^2 0.968, T(TV:radio) 20.7
print("TV effect at radio = 0, 50:",
      round(mi.params["TV"], 4), round(mi.params["TV"] + 50 * mi.params["TV:radio"], 4))

# =====================================================================
# Appendix A.3: Diagnostics in multiple regression
# =====================================================================
header("Appendix A.3 -- diagnostics, collinearity, VIF")
for m in (m2, mi):                                       # curvature / pattern gone
    fig, ax = plt.subplots(); ax.scatter(m.fittedvalues, m.resid)
    ax.axhline(0, linestyle="--"); plt.close(fig)

# collinearity: Limit and Rating
print("corr(Limit, Rating) =", round(cr["Limit"].corr(cr["Rating"]), 3))   # 0.997
m_alr = smf.ols("Balance ~ Age + Limit + Rating", data=cr).fit()
m_al = smf.ols("Balance ~ Age + Limit", data=cr).fit()
print(m_alr.summary().tables[1]); print(m_al.summary().tables[1])
print("SE ratio:", round(m_alr.bse["Limit"] / m_al.bse["Limit"], 1))      # 12.6

# VIF_j = 1 / (1 - R^2_j), R^2_j from regressing x_j on the other predictors
for x, others in [("Age", "Limit + Rating"), ("Limit", "Age + Rating"),
                  ("Rating", "Age + Limit")]:
    r2 = smf.ols(f"{x} ~ {others}", data=cr).fit().rsquared
    print(f"VIF({x}) = {1 / (1 - r2):.2f}")              # 1.01, 160.6, 160.7
X = sm.add_constant(cr[["Age", "Limit", "Rating"]])
print("variance_inflation_factor:",
      [round(variance_inflation_factor(X.values, j), 2) for j in (1, 2, 3)])

# leverage rule in multiple regression: h_ii > 2(p+1)/n
h2 = m2.get_influence().hat_matrix_diag
print("points with h > 2(p+1)/n:", int((h2 > 2 * (2 + 1) / 200).sum()))
