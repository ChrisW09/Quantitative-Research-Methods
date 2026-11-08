# =====================================================================
# Quantitative Research -- Part 4: Regression
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 4. Run it from the
# folder Part_4_Regression (the data sets are read from ../data):
#     python3 Part_4_Regression.py
# Plots are drawn headless (Agg backend) and closed again -- nothing is
# written to disk; all numbers are printed. The inline (pgfplots) figures
# of Sections 1-4 use the coordinates printed here.
# Sections follow the sections of the slide deck:
#   1  Correlation              (lamp example; running exercise "online
#                                shop" (1)-(2): covariance, correlation)
#   2  Simple regression        (twelve stores: the best line, least squares;
#                                lamp; online shop (3)-(6): residuals of two
#                                lines, squares, OLS line, second shop;
#                                exercises: furniture store, price-demand)
#   3  Goodness of fit          (variance decomposition, R^2, three sums;
#                                online shop (7)-(8); exercises: heating
#                                costs, study hours -- statsmodels output)
#   3  (end)                    exercise body heights and shoe sizes, tasks 1-2
#   4  Inference                (regression model, SE, t-test, CI, p-value,
#                                prediction; online shop (9)-(10))
#   5  Multiple regression      (Advertising, Credit)
#   A.3-A.5 (appendix)          residual analysis, leverage, QQ-plots (saturation
#                                example; online shop (B)-(C); exercises:
#                                maintenance costs, body heights residual plot
#                                and QQ-plot). This block stays before Section 4
#                                in the script because later sections reuse its
#                                body-height data.
#   Appendix                    (derivation of OLS with exercise online
#                                shop (A), minimum property of OLS,
#                                interactions, diagnostics, collinearity / VIF)
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
# summary() runs normality tests that warn for small n (n = 6, 9, 12, 15) -- silence them
warnings.filterwarnings("ignore", category=UserWarning)


def header(title):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70)


def fit_line(m):
    """Short summary line: R^2, adjusted R^2, F, p(F), sigma-hat."""
    print(f"R^2 = {m.rsquared:.4f}, adj. R^2 = {m.rsquared_adj:.4f}, "
          f"F = {m.fvalue:.1f} (p = {m.f_pvalue:.3g}), "
          f"sigma = {np.sqrt(m.scale):.4f}, df = {m.df_resid:.0f}")


def sums(x, y):
    """Means and the three basic sums S_xx, S_yy, S_xy (Section 3)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xc, yc = x - x.mean(), y - y.mean()
    return x.mean(), y.mean(), (xc**2).sum(), (yc**2).sum(), (xc * yc).sum()


def ols_by_hand(x, y, label):
    """Recipe of the slide 'Step by step to the regression line'."""
    xbar, ybar, Sxx_, Syy_, Sxy_ = sums(x, y)
    n_ = len(x)
    b1 = Sxy_ / Sxx_; b0 = ybar - b1 * xbar
    print(f"{label}: n = {n_}, xbar = {xbar:.4f}, ybar = {ybar:.4f}, "
          f"S_xx = {Sxx_:.4f}, S_yy = {Syy_:.4f}, S_xy = {Sxy_:.4f}")
    print(f"   s_xy = {Sxy_ / (n_ - 1):.4f}, s_x^2 = {Sxx_ / (n_ - 1):.4f}, "
          f"b1 = {b1:.4f}, b0 = {b0:.4f}, r = {Sxy_ / np.sqrt(Sxx_ * Syy_):.4f}, "
          f"R^2 = {Sxy_**2 / (Sxx_ * Syy_):.4f}")
    return b0, b1


def rss_of_line(x, y, b0, b1):
    u = np.asarray(y, float) - (b0 + b1 * np.asarray(x, float))
    return u, (u**2).sum()


# ---------------------------------------------------------------------
# SETUP: lamp example (price in euros, sales quantity) -- running story
# ---------------------------------------------------------------------
price = np.array([80, 85, 90, 95, 100, 105, 110, 115, 120])
quantity = np.array([20, 17, 15, 9, 11, 8, 4, 4, 2])
df = pd.DataFrame({"price": price, "quantity": quantity})
n = len(df)

# twelve stores: advertising and revenue (both in 1000 EUR) -- Sections 2-4
x12 = np.array([1, 3, 4, 5, 6, 8, 8, 9, 10, 11, 12, 13])
y12 = np.array([33, 30, 37, 33, 38, 41, 39, 43, 45, 40, 42, 47])
stores = pd.DataFrame({"adv": x12, "revenue": y12})

# =====================================================================
# 1 Correlation
# =====================================================================
header("1 Correlation -- slide 'Covariance and correlation with Python'")
fig, ax = plt.subplots()
ax.scatter(df["price"], df["quantity"])
ax.set(xlabel="Price (EUR)", ylabel="Sales quantity", title="Scatter plot")
plt.close(fig)
print("cov  :", df["price"].cov(df["quantity"]))            # -83.75
print("corr :", round(df["price"].corr(df["quantity"]), 4))  # -0.9732
print("sd   :", round(df["price"].std(), 4), round(df["quantity"].std(), 4))  # 13.6931, 6.2849

print("lamp: S_xy, S_xx, S_yy:", ((price - 100) * (quantity - 10)).sum(),
      ((price - 100)**2).sum(), ((quantity - 10)**2).sum())     # -670 1500 316
print("var: s_x^2 = 1500/8 =", 1500 / 8, " s_y^2 = 316/8 =", 316 / 8)   # 187.5, 39.5

# Running exercise "online shop" (advertising and revenue, both in 1000 EUR)
shop = pd.DataFrame({"adv": [1, 2, 3, 4, 5], "revenue": [21, 26, 24, 30, 29]})
xs_, ys_ = shop["adv"].to_numpy(), shop["revenue"].to_numpy()
header("1 Exercise -- online shop (1): scatter plot and covariance")
print("means:", xs_.mean(), ys_.mean())                                   # 3, 26
print("deviations x:", (xs_ - 3).tolist(), " y:", (ys_ - 26).tolist())    # -2..2; -5 0 -2 4 3
print("products:", ((xs_ - 3) * (ys_ - 26)).tolist(),
      " S_xy =", ((xs_ - 3) * (ys_ - 26)).sum(), " s_xy =", shop["adv"].cov(shop["revenue"]))  # 20, 5
header("1 Exercise -- online shop (2): correlation coefficient")
print("S_xx =", ((xs_ - 3)**2).sum(), " S_yy =", ((ys_ - 26)**2).sum())   # 10, 54
print("s_x, s_y =", round(shop["adv"].std(), 4), round(shop["revenue"].std(), 4))   # 1.5811, 3.6742
print("r =", round(shop["adv"].corr(shop["revenue"]), 4),
      " = S_xy/sqrt(S_xx S_yy) =", round(20 / np.sqrt(10 * 54), 4))       # 0.8607

# =====================================================================
# 2 Simple linear regression
# =====================================================================
header("2 Simple regression -- twelve stores: which line is best?")
print("r_xy (twelve stores) =", round(stores["adv"].corr(stores["revenue"]), 4))   # 0.8803
# candidate lines of the slides 'Which line describes the data best?' ff.
lines = {"A": (24, 2), "B": (34.5, 0.6), "C": (35, 1.2), "D": (30, 1.2)}
for name, (a, b) in lines.items():
    u, rss = rss_of_line(x12, y12, a, b)
    print(f"line {name:2s} y = {a} + {b} x: residuals {u.round(2).tolist()}, "
          f"sum = {u.sum():.1f}, sum of squares S = {rss:.1f}")
# A: sum 0, S = 164.0; B: 0, 120.6; C: -60, 364.8; D: 0, 64.8
print("store 9: yhat =", 30 + 1.2 * 10, " residual =", 45 - (30 + 1.2 * 10))   # 42, 3
u_D, _ = rss_of_line(x12, y12, 30, 1.2)
print("squared residuals of D:", (u_D**2).round(2).tolist())

header("2 Exercise -- online shop (3) and (4): residuals of two lines, squared")
for name, (a, b) in {"line 1": (23, 1), "line 2": (20, 2)}.items():
    u, rss = rss_of_line(xs_, ys_, a, b)
    print(f"{name} y = {a} + {b} x: fitted {(a + b * xs_).tolist()}, residuals {u.tolist()}, "
          f"sum {u.sum():.0f}, squares {(u**2).tolist()}, S = {rss:.0f}")   # 0, 24 / 0, 14

header("2 Simple regression -- least squares (twelve stores)")
b0_12, b1_12 = ols_by_hand(x12, y12, "twelve stores")    # S_xy 186, S_xx 155, b1 1.2, b0 30
print("s_xy = 186/11 =", round(186 / 11, 2), " s_x^2 = 155/11 =", round(155 / 11, 2))  # 16.91, 14.09
reg12 = smf.ols("revenue ~ adv", data=stores).fit()
print("smf.ols:", reg12.params.round(4).tolist())          # 30.0, 1.2: line D is the OLS line
# first-order conditions: sum u = 0 and sum x u = 0
print("sum u =", round(reg12.resid.sum(), 10), " sum x*u =", round((x12 * reg12.resid).sum(), 10))
print("fitted values:", reg12.fittedvalues.round(2).tolist())
# slide 'How do we interpret the slope?': advertising 5 -> 10
print("yhat(5), yhat(10):", 30 + 1.2 * 5, 30 + 1.2 * 10)   # 36, 42
# slide 'Intercept, OLS line and the answer': answer to the starting question
print("yhat(7) =", round(30 + 1.2 * 7, 4))                 # 38.4
# slide 'Interpretation at a glance -- and predictions'
print("yhat(9.5), yhat(25):", round(30 + 1.2 * 9.5, 4), round(30 + 1.2 * 25, 4), " 1.2 * 5 =", 1.2 * 5)  # 41.4, 60, 6

header("2 Exercise -- online shop (5): the OLS line of the online shop")
print("b1 = s_xy/s_x^2 = 5/2.5 =", 5 / 2.5, " = S_xy/S_xx = 20/10 =", 20 / 10,
      " b0 = 26 - 2*3 =", 26 - 2 * 3, " centroid check:", 20 + 2 * 3)   # 2, 2, 20, 26
# slide 'Solution -- online shop (5)', block 'Check with Python'
x5, y5 = pd.Series([1, 2, 3, 4, 5]), pd.Series([21, 26, 24, 30, 29])
print("sum of squares: OLS line", ((y5 - (20 + 2 * x5))**2).sum(),
      " line 1", ((y5 - (23 + x5))**2).sum())                          # 14, 24

header("Appendix A.1 -- exercise online shop (A): solving the normal equations")
n_s, Sx, Sy, Sxx_raw, Sxy_raw = 5, xs_.sum(), ys_.sum(), (xs_**2).sum(), (xs_ * ys_).sum()
print("sums:", n_s, Sx, Sy, Sxx_raw, Sxy_raw, " products:", (xs_ * ys_).tolist())  # 5 15 130 55 410
b1_ne, b0_ne = np.linalg.solve([[n_s, Sx], [Sx, Sxx_raw]], [Sy, Sxy_raw])[::-1]
print("I: 130 = 5 b0 + 15 b1, II: 410 = 15 b0 + 55 b1  ->  b1 =", round(b1_ne, 4), " b0 =", round(b0_ne, 4))  # 2, 20
print("np.linalg.solve(A, [130, 410]) =", np.linalg.solve([[5, 15], [15, 55]], [130, 410]))  # [20. 2.]
print("15 * 26 =", 15 * 26, " 55 - 45 =", 55 - 45)          # 390, 10

header("2 Simple regression -- lamp example, slide 'Linear regression with Python'")
beta1 = df["price"].cov(df["quantity"]) / df["price"].var()
beta0 = df["quantity"].mean() - beta1 * df["price"].mean()
print("beta1 =", round(beta1, 4), " beta0 =", round(beta0, 4))   # -0.4467, 54.6667
print("s_xy = -670/8 =", -670 / 8, " s_x^2 = 1500/8 =", 1500 / 8)  # -83.75, 187.5

reg = smf.ols("quantity ~ price", data=df).fit()
print(reg.params.round(4))                                      # 54.6667 -0.4467
print("reg.resid.sum() =", f"{reg.resid.sum():.1e}")            # practically 0
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

header("2 Exercise -- online shop (6): the OLS line for a second shop")
shopB = pd.DataFrame({"adv": [2, 4, 5, 6, 8], "revenue": [12, 20, 19, 23, 31]})
xB, yB = shopB["adv"].to_numpy(), shopB["revenue"].to_numpy()
print("deviations x:", (xB - xB.mean()).tolist(), " y:", (yB - yB.mean()).tolist())  # -3 -1 0 1 3; -9 -1 -2 2 10
print("products:", ((xB - 5) * (yB - 21)).tolist(), " squares:", ((xB - 5)**2).tolist())
b0_B, b1_B = ols_by_hand(xB, yB, "second shop")          # xbar 5, ybar 21, S_xy 60, S_xx 20; b1 3, b0 6
print("fitted:", (b0_B + b1_B * xB).tolist(), " residuals:", (yB - (b0_B + b1_B * xB)).tolist())  # 0 2 -2 -1 1
# first shop for comparison (and for the later exercises)
b0_s, b1_s = ols_by_hand(xs_, ys_, "first shop")         # S_xy 20, S_xx 10; b1 2, b0 20
u_shop, rss_shop = rss_of_line(xs_, ys_, 20, 2)
print("first shop residuals:", u_shop.tolist(), " sum =", u_shop.sum(), " RSS =", rss_shop)   # -1 2 -2 2 -1; 14

header("2 Exercise -- interpreting coefficients and making predictions (furniture)")
fs = pd.DataFrame({"adv": [2, 4, 6, 8, 10, 12], "revenue": [44, 49, 58, 62, 61, 71]})
reg_fs = smf.ols("revenue ~ adv", data=fs).fit()
print(reg_fs.params.round(4).tolist())                                      # 40.0  2.5
print(reg_fs.predict(pd.DataFrame({"adv": [5, 30]})).round(4).tolist())     # 52.5  115.0
print("yhat at 4, 6, 10, 12:", reg_fs.predict(pd.DataFrame({"adv": [4, 6, 10, 12]})).round(4).tolist())
print("residuals:", reg_fs.resid.round(4).tolist())                         # max |u| = 4
print(smf.ols("revenue ~ I(1000 * adv)", data=fs).fit().params.round(4).tolist())   # 40.0  0.0025
fs_euro = pd.DataFrame({"adv": 1000 * fs["adv"], "revenue": 1000 * fs["revenue"]})
print("both in euros:", smf.ols("revenue ~ adv", data=fs_euro).fit().params.round(4).tolist())  # 40000, 2.5

header("2 Exercise -- a falling price-demand line (mock exam 4, task 2)")
dem = pd.DataFrame({"price": [10, 12, 14, 16, 18], "units": [64, 50, 46, 42, 38]})
b0_d, b1_d = ols_by_hand(dem["price"], dem["units"], "price-demand")    # S_xy -120, S_xx 40; -3, 90
reg_dem = smf.ols("units ~ price", data=dem).fit()
print(reg_dem.predict(pd.DataFrame({"price": [15, 42]})).round(4).tolist())   # 45, -36
print("residual week 1:", 64 - (b0_d + b1_d * 10))                            # +4

# =====================================================================
# 3 Goodness of fit
# =====================================================================
header("3 Goodness of fit -- twelve stores: variance decomposition")
yb = y12.mean()
print("TSS terms :", ((y12 - yb)**2).tolist(), "sum", ((y12 - yb)**2).sum())                 # 288
print("ESS terms :", ((reg12.fittedvalues - yb)**2).round(2).tolist(),
      "sum", round(((reg12.fittedvalues - yb)**2).sum(), 4))                                 # 223.2
print("RSS terms :", (reg12.resid**2).round(2).tolist(), "sum", round((reg12.resid**2).sum(), 4))  # 64.8
print("store 12: total", 47 - 39, " explained", round(45.6 - 39, 1), " residual", round(47 - 45.6, 1))
print("R^2 = 223.2/288 =", round(223.2 / 288, 4), " reg12.rsquared =", round(reg12.rsquared, 4))  # 0.775
print("ESS = b1^2 S_xx = 1.2^2 * 155 =", round(1.2**2 * 155, 4))                            # 223.2
ess_A = ((24 + 2 * x12 - yb)**2).sum()
print("line A: ESS_A =", ess_A, " + RSS_A = 164 ->", ess_A + 164, "!= 288")                 # 620
# extreme cases (schematic data of the slide)
xe = np.arange(1, 9)
print("R^2 = 1 example:", round(smf.ols("y ~ x", data=pd.DataFrame({"x": xe, "y": 2 + 1.5 * xe})).fit().rsquared, 4))
r0 = smf.ols("y ~ x", data=pd.DataFrame({"x": xe, "y": [5, 7, 4, 6, 6, 4, 7, 5]})).fit()
print("R^2 = 0 example: b =", r0.params.round(4).tolist(), " R^2 =", round(r0.rsquared, 4))   # 5.5, 0, 0

header("3 Goodness of fit -- lamp example, slide 'Coefficient of determination in Python'")
TSS = ((quantity - quantity.mean())**2).sum()               # 316
RSS = (reg.resid**2).sum()                                  # 16.7333
ESS = ((reg.fittedvalues - quantity.mean())**2).sum()       # 299.2667
print("TSS, RSS, ESS:", TSS, round(RSS, 4), round(ESS, 4))
print("ESS = b1^2 S_xx =", round((Sxy / Sxx)**2 * Sxx, 2))  # 299.27
print("R^2 = 1 - RSS/TSS =", round(1 - RSS / TSS, 4))      # 0.9470
print("reg.rsquared      =", round(reg.rsquared, 4))
print("corr^2            =", round(df["price"].corr(df["quantity"])**2, 4))

header("3 Useful transformations -- three sums, shift theorem, standardised slope")
print("twelve stores: r =", round(186 / np.sqrt(155 * 288), 4), " R^2 =", 186**2, "/", 155 * 288,
      "=", round(186**2 / (155 * 288), 4), " ESS = b1*S_xy =", round(1.2 * 186, 4),
      " RSS =", round(288 - 1.2 * 186, 4))
print("online shop: sum xy =", (xs_ * ys_).sum(), " sum x^2 =", (xs_**2).sum(),
      " sum y^2 =", (ys_**2).sum())                                     # 410, 55, 3434
print("   S_xy =", (xs_ * ys_).sum() - 5 * 3 * 26, " S_xx =", (xs_**2).sum() - 5 * 9,
      " S_yy =", (ys_**2).sum() - 5 * 26**2)                            # 20, 10, 54
print("s_x/s_y (stores) =", round(np.sqrt(155 / 288), 4), " r = 1.2 * s_x/s_y =",
      round(1.2 * np.sqrt(155 / 288), 4))                               # 0.7336, 0.8803
print("lamp: r * s_y / s_x =", round(df["price"].corr(df["quantity"]) * df["quantity"].std()
                                      / df["price"].std(), 4))           # -0.4467
# slide 'Three sums with Python' (twelve stores)
xs12, ys12 = stores["adv"], stores["revenue"]
print("shift theorem (stores): sum xy - n xbar ybar =", (xs12 * ys12).sum(), "-",
      len(xs12) * xs12.mean() * ys12.mean(), "=",
      (xs12 * ys12).sum() - len(xs12) * xs12.mean() * ys12.mean())      # 3696 - 3510 = 186
print("reg.centered_tss, reg.ess, reg.ssr, reg.rsquared:", reg12.centered_tss,
      round(reg12.ess, 4), round(reg12.ssr, 4), round(reg12.rsquared, 4))  # 288 223.2 64.8 0.775

header("3 Exercise -- online shop (7): the sum-of-squares decomposition")
reg_shop = smf.ols("revenue ~ adv", data=shop).fit()
yhat_s = reg_shop.fittedvalues.to_numpy()
print("(y-ybar)^2:", ((ys_ - 26)**2).tolist(), " TSS =", ((ys_ - 26)**2).sum())          # 25 0 4 16 9; 54
print("yhat-ybar:", (yhat_s - 26).round(4).tolist(), " (yhat-ybar)^2:", ((yhat_s - 26)**2).round(4).tolist(),
      " ESS =", round(((yhat_s - 26)**2).sum(), 4))                                      # 16 4 0 4 16; 40
print("u^2:", (u_shop**2).tolist(), " RSS =", rss_shop, " ESS = 2^2*10 =", 4 * 10)      # 1 4 4 4 1; 14
header("3 Exercise -- online shop (8): computing and assessing R^2")
print("R^2 = 40/54 =", round(40 / 54, 4), " = 1 - 14/54 =", round(1 - 14 / 54, 4),
      " r^2 = 0.8607^2 =", round(0.8607**2, 4))                         # 0.7407, 0.7408
print("reg.ssr, reg.centered_tss, reg.rsquared:", round(reg_shop.ssr, 4),
      reg_shop.centered_tss, round(reg_shop.rsquared, 4))               # 14.0 54.0 0.7407

header("3 Exercise -- from sums of squares to the correlation coefficient (heating)")
hc = pd.DataFrame({"temp": [0, 3, 6, 9, 12], "cost": [82, 65, 63, 41, 49]})
reg_hc = smf.ols("cost ~ temp", data=hc).fit()
print(reg_hc.params.round(4).tolist())                                 # 78, -3
print("TSS =", reg_hc.centered_tss, " RSS =", round(reg_hc.ssr, 4), " ESS =", round(reg_hc.ess, 4))  # 1000 190 810
print("R^2 =", round(reg_hc.rsquared, 4), " r =", round(hc["temp"].corr(hc["cost"]), 4))  # 0.81, -0.9
print("S_xx =", ((hc["temp"] - 6)**2).sum(), " ESS = (-3)^2 * 90 =", 9 * 90,
      " y - ybar:", (hc["cost"] - hc["cost"].mean()).tolist())          # 90, 810; 22 5 3 -19 -11

header("3 Exercise -- reading a simple regression output (study hours; mock exam 1, task 2)")
# data constructed to match the exam: n = 12, x in [5, 24], xbar = 14, S_xx = 360,
# TSS = 2500, b0 = 28, b1 = 2.5, R^2 = 0.9 (exactly)
st = pd.DataFrame({"hours": [5, 7, 8, 10, 12, 14, 16, 17, 17, 18, 20, 24],
                   "points": [36, 50, 47, 51, 63, 71, 62, 65, 75, 69, 76, 91]})
reg_st = smf.ols("points ~ hours", data=st).fit()
print(reg_st.summary())                                 # output (excerpt) shown on the slide
print("xbar =", st["hours"].mean(), " S_xx =", ((st["hours"] - 14)**2).sum(),
      " TSS =", reg_st.centered_tss)                    # 14, 360, 2500
print("predictions 16, 30:", reg_st.predict(pd.DataFrame({"hours": [16, 30]})).round(4).tolist())  # 68, 103
print("r = sqrt(R^2) =", round(np.sqrt(reg_st.rsquared), 4), " corr =",
      round(st["hours"].corr(st["points"]), 4))         # 0.9487
print("ESS =", round(reg_st.ess, 4), " RSS =", round(reg_st.ssr, 4),
      " b1^2 * S_xx =", 2.5**2 * 360)                   # 2250, 250, 2250

# =====================================================================
# Appendix A.3-A.5: residual analysis, leverage, QQ-plots
# =====================================================================
header("Appendix A.3-A.5 -- residual analysis -- saturation example (ten regions)")
sat = pd.DataFrame({"adv": np.arange(1, 11), "revenue": [25, 32, 37, 41, 44, 46, 47, 48, 48, 47]})
reg_sat = smf.ols("revenue ~ adv", data=sat).fit()
print(reg_sat.params.round(4).tolist(), " R^2 =", round(reg_sat.rsquared, 4))   # 28.6667 2.3333; 0.81
print("fitted/residual pairs:", list(zip(reg_sat.fittedvalues.round(4), reg_sat.resid.round(4))))

header("Appendix A.3-A.5 -- residual analysis -- residual plots (twelve stores, lamp)")
print("twelve stores (fitted, residual):", list(zip(reg12.fittedvalues.round(2), reg12.resid.round(2))))
print("largest |residual| =", round(np.abs(reg12.resid).max(), 2))               # 3.6 (store 2)
fig, ax = plt.subplots()                         # slide 'Creating a residual plot with Python'
ax.scatter(reg.fittedvalues, reg.resid)
ax.axhline(0, linestyle="--")
ax.set(xlabel="fitted values", ylabel="residuals", title="Residual plot")
plt.close(fig)
print("lamp (fitted, residual):", list(zip(reg.fittedvalues.round(4), reg.resid.round(4))))

header("Appendix A.3-A.5 -- residual analysis -- leverage values (lamp)")
# Slide 'Leverage values -- lamp example': h_i = 1/n + (x_i - xbar)^2 / Sxx
h = reg.get_influence().hat_matrix_diag
print("leverages:", h.round(3))                    # 0.378 (ends) ... 0.111 (centre)
print("rules of thumb 4/n, 6/n:", round(4 / n, 3), round(6 / n, 3))   # 0.444, 0.667
# slide 'Leverage values with Python'
print("(h > 4/n).sum() =", (h > 4 / n).sum(), " by hand equal:",
      np.allclose(h, 1 / n + (price - price.mean())**2 / Sxx))       # 0, True
for p_out in (95, 80):                             # fit without one store
    b_wo = smf.ols("quantity ~ price", data=df[df["price"] != p_out]).fit().params["price"]
    print(f"slope without the store at {p_out} EUR: {b_wo:.4f}")       # -0.4590, -0.4238

header("Appendix A.3-A.5 -- residual analysis -- QQ-plots")
# two empirical distributions (slide 'QQ-plot: prices against quantities')
fig, ax = plt.subplots()
qx, qy = np.sort(df["price"]), np.sort(df["quantity"])
ax.scatter(qx, qy)
q1x, q3x = np.percentile(qx, [25, 75]); q1y, q3y = np.percentile(qy, [25, 75])
slope = (q3y - q1y) / (q3x - q1x)
ax.axline((q1x, q1y), slope=slope, linestyle="--")
plt.close(fig)
print("two-sample QQ: quartiles", q1x, q3x, q1y, q3y, " line: y =",
      round(q1y - slope * q1x, 4), "+", round(slope, 4), "x")           # -45.5 + 0.55 x
# theoretical quantiles for n = 5 (slide 'Residuals against the normal distribution')
print("strip boundaries Phi^-1(0.2..0.8):", stats.norm.ppf([0.2, 0.4, 0.6, 0.8]).round(4))
print("z_i for n = 5:", stats.norm.ppf((np.arange(1, 6) - 0.5) / 5).round(4))
# residuals against the normal distribution (positions (i-0.5)/n: a=0.5)
fig = sm.qqplot(reg.resid, line="q", a=0.5)
plt.close(fig)
u = np.sort(reg.resid.to_numpy()); p = (np.arange(1, n + 1) - 0.5) / n
order = np.argsort(reg.resid.to_numpy(), kind="stable")
print(pd.DataFrame({"u_sorted": u.round(4), "price": price[order],
                    "p": p.round(4), "z": stats.norm.ppf(p).round(4)}))


def qq_reference_line(resid):
    """Line through the quartiles of the residuals and of N(0,1) (line='q')."""
    q1, q3 = np.percentile(resid, [25, 75]); z1, z3 = stats.norm.ppf([0.25, 0.75])
    b = (q3 - q1) / (z3 - z1)
    return q1 - b * z1, b


print("lamp QQ reference line: intercept, slope =",
      [round(float(v), 4) for v in qq_reference_line(reg.resid)])               # 0.5833, 0.5189

header("Appendix A.3 -- exercise online shop (B): draw the residual plot")
print("fitted:", (20 + 2 * xs_).tolist(), " residuals:", u_shop.tolist())   # 22..30; -1 2 -2 2 -1

header("Appendix A.4 -- exercise online shop (C): a month with a big campaign (leverage)")
x8 = np.array([1, 2, 3, 4, 5, 6, 7, 20])
Sxx8 = ((x8 - x8.mean())**2).sum()
h8 = 1 / len(x8) + (x8 - x8.mean())**2 / Sxx8
print("xbar =", x8.mean(), " deviations:", (x8 - x8.mean()).tolist(), " S_xx =", Sxx8)   # 6, 252
print("h_1, h_6, h_8 =", h8[0].round(4), h8[5].round(4), h8[7].round(4),
      " (25/252, 196/252 =", round(25 / 252, 4), round(196 / 252, 4), ")")              # 0.2242 0.125 0.9028
print("all h:", h8.round(4).tolist(), " sum =", round(h8.sum(), 4),
      " 4/n, 6/n =", 4 / len(x8), 6 / len(x8))                                           # sum 2; 0.5, 0.75

header("Appendix A.5 -- exercise: a QQ-plot by hand (maintenance costs; mock exam 2, task 2)")
mc5 = pd.DataFrame({"age": [1, 2, 3, 4, 5], "cost": [17, 21, 25, 29, 43]})
b0_m, b1_m = ols_by_hand(mc5["age"], mc5["cost"], "maintenance")      # S_xy 60, S_xx 10; 6, 9
reg_mc5 = smf.ols("cost ~ age", data=mc5).fit()
print("fitted:", reg_mc5.fittedvalues.round(4).tolist(), " residuals:", reg_mc5.resid.round(4).tolist())
p5 = (np.arange(1, 6) - 0.5) / 5
print("sorted:", np.sort(reg_mc5.resid).round(4).tolist(), " p:", p5.tolist(),
      " z:", stats.norm.ppf(p5).round(2).tolist())
print("QQ reference line:", [round(float(v), 4) for v in qq_reference_line(reg_mc5.resid)])   # 0, 2.9652
fig = sm.qqplot(reg_mc5.resid, line="q", a=0.5); plt.close(fig)

# Exercise body heights (k) -- shoe sizes (s)
header("3 Exercise -- body heights and shoe sizes (tasks 1-2; residual plot and QQ-plot: Appendix A.5)")
ks = pd.DataFrame({
    "k": [164, 162, 168, 198, 166, 166, 192, 160, 151, 175, 180, 160, 168, 175, 168],
    "s": [39, 38, 39, 46, 40, 39, 45, 37, 36, 42, 43, 38, 41, 40, 39]})
k_, s_ = ks["k"].to_numpy(), ks["s"].to_numpy()
print("auxiliary sums:", k_.sum(), s_.sum(), (k_ * s_).sum(), (k_**2).sum(), (s_**2).sum())
S_ks = (k_ * s_).sum() - k_.sum() * s_.sum() / 15                       # shift theorem
S_kk = (k_**2).sum() - k_.sum()**2 / 15
S_ss = (s_**2).sum() - s_.sum()**2 / 15
print("S_ks, S_kk, S_ss:", round(S_ks, 4), round(S_kk, 4), round(S_ss, 4))   # 471.6 2122.4 111.7333
print("cov, var_k, var_s:", round(S_ks / 14, 4), round(S_kk / 14, 4), round(S_ss / 14, 4))
print("cov, corr:", round(ks["k"].cov(ks["s"]), 4), round(ks["k"].corr(ks["s"]), 4))  # 33.6857, 0.9684
print("s_k, s_s:", round(ks["k"].std(), 4), round(ks["s"].std(), 4))                  # 12.3126, 2.8251
reg_ks = smf.ols("s ~ k", data=ks).fit()
print(reg_ks.params.round(4).tolist(), " R^2 =", round(reg_ks.rsquared, 4))  # 2.3147, 0.2222; 0.9379
print("ESS = b1 * S_ks =", round(reg_ks.params["k"] * S_ks, 2),
      " RSS =", round(S_ss - reg_ks.params["k"] * S_ks, 2))                 # 104.79, 6.94
print("(fitted, residual):", list(zip(reg_ks.fittedvalues.round(4), reg_ks.resid.round(4))))
fig, ax = plt.subplots(); ax.scatter(reg_ks.fittedvalues, reg_ks.resid)
ax.axhline(0, linestyle="--"); plt.close(fig)
fig = sm.qqplot(reg_ks.resid, line="q", a=0.5); plt.close(fig)
p15 = (np.arange(1, 16) - 0.5) / 15
order15 = np.argsort(reg_ks.resid.to_numpy(), kind="stable")
print(pd.DataFrame({"u_sorted": np.sort(reg_ks.resid.to_numpy()).round(4),
                    "person": order15 + 1, "p": p15.round(4),
                    "z": stats.norm.ppf(p15).round(4)}))
print("QQ reference line:", [round(float(v), 4) for v in qq_reference_line(reg_ks.resid)])  # -0.0056, 0.7002

# =====================================================================
# 4 Inference in simple regression
# =====================================================================
header("4 Inference -- slide 'Reading the regression output in Python'")
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

header("4 Exercise -- online shop (9) and (10): standard error and t-test")
sig_s = np.sqrt(rss_shop / (5 - 2)); se_s = sig_s / np.sqrt(10); T_s = 2 / se_s
print("sigma_hat =", round(sig_s, 4), " SE(b1) =", round(se_s, 4), " sqrt(10) =", round(np.sqrt(10), 4),
      " T =", round(T_s, 4))                                         # 2.1602 0.6831 3.1623 2.9277
print("t_0.975;3 =", round(stats.t.ppf(0.975, 3), 4), " p =", round(2 * stats.t.sf(T_s, 3), 4))   # 3.1824, 0.0611
print("statsmodels:", reg_shop.bse.round(4).tolist(), reg_shop.tvalues.round(4).tolist(),
      reg_shop.pvalues.round(4).tolist())

# confidence intervals (lamp)
print(reg.conf_int(alpha=0.05).round(4))       # beta1: [-0.5411, -0.3523], beta0: [45.15, 64.18]
print("by hand:", (beta1 + np.array([-1, 1]) * stats.t.ppf(0.975, n - 2) * se_b1).round(4))

# F-statistic = T^2 in simple regression
print("T^2 =", round(T**2, 1), " F =", round(reg.fvalue, 1))           # 125.2

# prediction: confidence vs. prediction interval (slide '... with Python (2/2)')
new = pd.DataFrame({"price": [100, 110, 125]})
pred = reg.get_prediction(new).summary_frame(alpha=0.05)
print(pred.round(2))               # 110: CI [3.99, 7.07], PI [1.57, 9.50]; 125: -1.17

# Exercise: inference for the shoe-size regression
header("4 Exercise -- inference for the shoe-size regression")
print(reg_ks.summary().tables[1])
fit_line(reg_ks)
print(reg_ks.conf_int().round(4))                                      # [0.1879, 0.2565]
print("t_0.975;13 =", round(stats.t.ppf(0.975, df=13), 4))             # 2.1604
T3 = (reg_ks.params["k"] - 0.25) / reg_ks.bse["k"]                     # -1.75
print("T3 =", round(T3, 2), " p =", round(2 * stats.t.sf(abs(T3), df=13), 3))   # 0.103
print(reg_ks.get_prediction(pd.DataFrame({"k": [180]}))
      .summary_frame(alpha=0.05).round(2))

# Exercise used cars from A to Z
header("4 Exercise -- used cars from A to Z")
cars = pd.DataFrame({"age": range(1, 7), "value": [19, 18, 17, 15, 12, 9]})
car = smf.ols("value ~ age", data=cars).fit()
print(car.summary().tables[1])
fit_line(car)
print(car.conf_int().round(4))                                         # [-2.66, -1.34]
print("t_0.975;4 =", round(stats.t.ppf(0.975, df=4), 3))               # 2.776
print(car.get_prediction(pd.DataFrame({"age": [7]}))
      .summary_frame(alpha=0.05).round(2))                             # PI [4.21, 11.79]

# =====================================================================
# 5 Multiple linear regression
# =====================================================================
header("5 Multiple regression -- Advertising data")
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
F_ad = ((TSS_ad - RSS_ad) / 3) / (RSS_ad / (200 - 3 - 1))
print("F =", round(F_ad, 1))                                         # 570.3
print("F_0.95;3,196 =", round(stats.f.ppf(0.95, 3, 196), 2))         # 2.65
# slide 'The F-test with Python'
print("m3.fvalue, m3.f_pvalue:", round(m3.fvalue, 1), f"{m3.f_pvalue:.3g}",
      " stats.f.sf(F):", f"{stats.f.sf(F_ad, 3, 196):.3g}")          # 570.3 1.58e-96 1.58e-96

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
header("5 Multiple regression -- Credit data")
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
# slide 'Dummy variables with Python'
for f in ("Balance ~ Student", "Balance ~ Income + Student", "Balance ~ Region"):
    print(f"{f:28s} params:", smf.ols(f, data=cr).fit().params.round(2).to_dict())
print("group means:", cr.groupby("Student")["Balance"].mean().round(3).to_dict())   # 480.369, 876.825

# =====================================================================
# Appendix A.2: Why no other line beats the OLS line
# =====================================================================
header("Appendix A.2 -- S(b0, b1) = RSS + n (a + b xbar)^2 + b^2 S_xx")
rss12 = (reg12.resid**2).sum()
for name in ("A", "B", "C"):
    a0, a1_ = lines[name]
    a, b = a0 - b0_12, a1_ - b1_12
    S_formula = rss12 + 12 * (a + b * x12.mean())**2 + b**2 * 155
    print(f"line {name}: a = {a:.1f}, b = {b:.1f}, a + b*xbar = {a + b * x12.mean():.1f}, "
          f"S = {S_formula:.1f} (direct: {rss_of_line(x12, y12, a0, a1_)[1]:.1f})")
# A: 164.0, B: 120.6, C: 364.8

# =====================================================================
# Appendix A.6: Interactions
# =====================================================================
header("Appendix A.6 -- interaction sales ~ TV * radio")
mi = smf.ols("sales ~ TV * radio", data=ad).fit()       # TV + radio + TV:radio
print(mi.summary().tables[1])
fit_line(mi)                                             # R^2 0.968, T(TV:radio) 20.7
print("TV effect at radio = 0, 50:",
      round(mi.params["TV"], 4), round(mi.params["TV"] + 50 * mi.params["TV:radio"], 4))

# =====================================================================
# Appendix A.7: Diagnostics in multiple regression
# =====================================================================
header("Appendix A.7 -- diagnostics, collinearity, VIF")
for m in (m2, mi):                                       # curvature / pattern gone
    fig, ax = plt.subplots(); ax.scatter(m.fittedvalues, m.resid)
    ax.axhline(0, linestyle="--"); plt.close(fig)

# collinearity: Limit and Rating
print("corr(Limit, Rating) =", round(cr["Limit"].corr(cr["Rating"]), 3))   # 0.997
m_alr = smf.ols("Balance ~ Age + Limit + Rating", data=cr).fit()
m_al = smf.ols("Balance ~ Age + Limit", data=cr).fit()
print(m_alr.summary().tables[1]); print(m_al.summary().tables[1])
print("SE ratio:", round(m_alr.bse["Limit"] / m_al.bse["Limit"], 2))     # 12.53 (0.06296 / 0.00503)

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
