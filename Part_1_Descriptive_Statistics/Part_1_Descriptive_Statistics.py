# =====================================================================
# Python code for: Part_1_Descriptive_Statistics.tex
# Title:  Quantitative Research - Part 1: Descriptive Statistics
# Author: Prof. Dr. Christoph Weisser
#
# Reproduces every number shown on the slides of Part 1 -- including all
# exercises and the exam-style exercise. The script is organised like the
# deck (sections / slide titles in the comments) and prints all results.
# Run it with:   python3 Part_1_Descriptive_Statistics.py
#
# Packages: numpy, pandas, scipy, matplotlib
# (Anaconda: already included; otherwise: pip install numpy pandas scipy matplotlib)
# =====================================================================

import math

import matplotlib
matplotlib.use("Agg")            # headless: figures are created, not shown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

pd.set_option("display.precision", 4)


def header(title):
    print("\n" + "=" * 70 + "\n" + title + "\n" + "=" * 70)


def course_quantile(x, p):
    """Course definition: x_(ceil(n*p)) of the sorted data
    (identical to np.quantile(x, p, method="inverted_cdf"))."""
    return np.quantile(x, p, method="inverted_cdf")


# =====================================================================
# SETUP - Data (slide "The Data -- an Example (2)")
# Shoe sizes of the 11 players of a soccer team
# =====================================================================
data = pd.Series([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39])
n = len(data)

# =====================================================================
# SECTION "Fundamentals" > SUBSECTION "Levels of Measurement"
# Slide "Levels of Measurement with Python"
# =====================================================================
header('Slide "Levels of Measurement with Python"')
# Nominal: categories without an order -> data type "category"
colour = pd.Series(["black", "white", "blue", "black"], dtype="category")
print((colour == "black").tolist())    # [True, False, False, True]   (=, != only)
# Ordinal: categories WITH an order (clothing sizes S < M < L < XL)
size = pd.Series(pd.Categorical(["M", "S", "XL", "M"],
                 categories=["S", "M", "L", "XL"], ordered=True))
print(size.max(), (size > "S").sum())  # XL 3                         (additionally <, >)
# Metric: numbers -> differences (and means) are meaningful
price = pd.Series([19.90, 24.90, 29.90, 19.90])   # euros
print(round(price.max() - price.min(), 2), round(price.mean(), 2))   # 10.0 23.65

# =====================================================================
# SECTION "Descriptive Statistics" > SUBSECTION "Frequencies"
# =====================================================================

# ---------------------------------------------------------------------
# Slide "Frequency Table"  /  Slide "Frequencies with Python"
# ---------------------------------------------------------------------
header('Slides "Frequency Table" / "Frequencies with Python"')
abs_freq = data.value_counts().sort_index()                # h_j
rel_freq = data.value_counts(normalize=True).sort_index()  # f_j
cum_freq = rel_freq.cumsum()                               # F(x)

table = pd.DataFrame({
    "absolute": abs_freq,
    "relative": rel_freq.round(4),
    "relative in %": (100 * rel_freq).round(1),
    "fraction": [f"{h}/{n}" for h in abs_freq],
    "cumulative": cum_freq.round(4),
    "cum. fraction": [f"{h}/{n}" for h in abs_freq.cumsum()],
})
print(table.T)
print("Total absolute frequency:", abs_freq.sum())         # 11
print("Total relative frequency:", rel_freq.sum())         # 1.0
print("Cumulative absolute frequency H_j:",
      abs_freq.cumsum().tolist())                          # [1, 3, 7, 9, 10, 11]

# ---------------------------------------------------------------------
# Slide "Comparing Relative Frequencies: Percent vs. Percentage Points"
# share of 5-star ratings rises from 40 % to 50 %
# ---------------------------------------------------------------------
header('Slide "Comparing Relative Frequencies: Percent vs. Percentage Points"')
old_share, new_share = 0.40, 0.50
print("Absolute difference:", round(100 * (new_share - old_share), 2),
      "percentage points")                                 # 10.0
print("Relative change:    ", round((new_share - old_share) / old_share, 4))  # 0.25
# Line exactly as on slide "Frequencies with Python"
print(50 - 40, round((50 - 40) / 40, 4))     # 10 0.25

# ---------------------------------------------------------------------
# Slides "Exercise -- Frequencies of a Nominal Variable" /
#        "Solution (1/2), (2/2)"  (payment methods of n = 10 orders)
# ---------------------------------------------------------------------
header('Exercise "Frequencies of a Nominal Variable" (payment methods)')
pay = pd.Series(["P", "C", "I", "P", "P", "C", "P", "I", "C", "P"])
h_pay = pay.value_counts()[["I", "P", "C"]]              # invoice, PayPal, card
f_pay = h_pay / len(pay)
print(pd.DataFrame({"h_j": h_pay,
                    "f_j (fraction)": [f"{h}/{len(pay)}" for h in h_pay],
                    "f_j": f_pay.round(2),
                    "in %": (100 * f_pay).round(0)}).T)
# h_j: 2 5 3 | f_j: 0.20 0.50 0.30 | 20 % 50 % 30 %
print("Checks:", h_pay.sum(), round(f_pay.sum(), 4))                  # 10 1.0
print("b) not by invoice:", round(f_pay["P"] + f_pay["C"], 2),        # 0.8
      "= 1 - f_invoice =", round(1 - f_pay["I"], 2),                  # 0.8
      "|", (pay != "I").sum(), "orders")                              # 8
print("c) change of the invoice share (25 % -> 20 %):",
      round(100 * (f_pay["I"] - 0.25), 2), "percentage points |",     # -5.0
      round((f_pay["I"] - 0.25) / 0.25, 4))                           # -0.2 = -20 %
print("d) 'cumulative up to PayPal' depends on the column order:",
      "I, P, C ->", round(f_pay["I"] + f_pay["P"], 2),                # 0.7
      "| C, P, I ->", round(f_pay["C"] + f_pay["P"], 2))              # 0.8

# ---------------------------------------------------------------------
# Slides "Column Chart", "Bar Chart", "Pie Chart",
#        "Empirical Distribution Function"
# (the slides only show the images; this is the corresponding code)
# ---------------------------------------------------------------------
header('Slides "Column Chart" / "Bar Chart" / "Pie Chart" / "Empirical '
       'Distribution Function"')
fig, ax = plt.subplots()
ax.bar(abs_freq.index.astype(str), abs_freq.values)
ax.set(title="Column chart - Shoe sizes", xlabel="Shoe size",
       ylabel="Absolute frequency")
plt.close(fig)

fig, ax = plt.subplots()
ax.barh(abs_freq.index.astype(str), abs_freq.values)
ax.set(title="Bar chart - Shoe sizes", xlabel="Absolute frequency",
       ylabel="Shoe size")
plt.close(fig)

fig, ax = plt.subplots()
ax.pie(abs_freq.values, labels=abs_freq.index)
ax.set(title="Pie chart - Shoe sizes")
plt.close(fig)

fig, ax = plt.subplots()
ax.ecdf(data)                                   # step function F(x)
ax.set(title="Empirical distribution function - Shoe sizes",
       xlabel="Shoe size", ylabel="F(x)")
plt.close(fig)

print("F(39) =", round((data <= 39).mean(), 4))   # 0.6364 = 7/11

# Slide "Charts with Python" -- the same four charts with the plt commands of
# the slide (plt.show() is replaced by plt.close() in this headless script)
counts = data.value_counts().sort_index()        # h_j: 37:1, 38:2, 39:4, 40:2, 41:1, 46:1
print("counts:", dict(zip(counts.index.tolist(), counts.tolist())))
plt.bar(counts.index, counts.values)             # column chart (numeric axis: gap 41-46)
plt.xlabel("Shoe size"); plt.ylabel("Absolute frequency")
plt.close()
plt.barh(counts.index, counts.values)            # bar chart (horizontal bars)
plt.close()
plt.pie(counts.values, labels=counts.index)      # pie chart: slice = share f_j
plt.close()
plt.ecdf(data)                                   # empirical distribution function F(x)
plt.close()
print("Figures created (not shown, headless mode).")

# =====================================================================
# SUBSECTION "Exercises" (Frequencies)
# Slides "Exercise -- Frequency Table" / "Solution (1/2), (2/2)"
# =====================================================================
header('Exercise "Frequency Table" (cafe ratings)')
stars = pd.Series([4, 5, 3, 4, 5, 5, 2, 4, 5, 3, 4, 5])
h_stars = stars.value_counts().sort_index()
f_stars = stars.value_counts(normalize=True).sort_index()
print(pd.DataFrame({"h_j": h_stars,
                    "f_j (fraction)": [f"{h}/{len(stars)}" for h in h_stars],
                    "f_j": f_stars.round(4),
                    "F(x_j)": f_stars.cumsum().round(4)}).T)
# h_j: 1 2 4 5 | f_j: 0.0833 0.1667 0.3333 0.4167 | F: 0.0833 0.25 0.5833 1
print("b) at most 3 stars, F(3):", (stars <= 3).mean())               # 0.25
print("c) at least 4 stars:", 1 - (stars <= 3).mean(),
      "=", (stars >= 4).sum(), "ratings")                             # 0.75 = 9
print("d) most frequent rating:", stars.mode().tolist())              # [5]
f5 = (stars == 5).mean()
print("e) f_4 (5 stars) =", round(100 * f5, 2), "% | change:",
      round(100 * f5 - 30, 2), "percentage points |",
      round((f5 - 0.30) / 0.30 * 100, 1), "%")    # 41.67 % | 11.67 pp | 38.9 %
# Python code exactly as on slide "Solution (2/2) -- Frequency Table"
print(stars.value_counts().sort_index().tolist())   # [1, 2, 4, 5]
F = stars.value_counts(normalize=True).sort_index().cumsum()
print(F.round(4).tolist())                     # [0.0833, 0.25, 0.5833, 1.0]
print((stars <= 3).mean(), (stars >= 4).sum())      # 0.25 9

# =====================================================================
# SUBSECTION "Measures of Central Tendency"
# =====================================================================

# ---------------------------------------------------------------------
# Slide "Measures of Central Tendency -- Example"
# Slides "Measures of Central Tendency with Python (1)" and "(2)"
# ---------------------------------------------------------------------
header('Slides "Measures of Central Tendency -- Example" / "... with Python"')
# Slide "Refresher: Summation and Product Signs" (first three players)
print("Sum of x_1..x_3:    ", data[:3].sum())                       # 117
print("Product of x_1..x_3:", np.prod(data[:3]))                    # 59280
print("Pitfall: 1^2 + 2^2 =", 1**2 + 2**2, "but (1 + 2)^2 =", (1 + 2)**2)  # 5 vs 9

# Slide "Means (1)": trimmed mean by hand -- floor(0.1 * 11) = 1 value per end
k_trim = math.floor(0.10 * n)
xs_sorted = np.sort(data.to_numpy())
print("Values removed per end:", k_trim,
      "| trimmed mean by hand:",
      round(xs_sorted[k_trim:n - k_trim].mean(), 4))                 # 1 | 39.2222

# Slide "Means (2): Geometric Mean -- Averaging Growth Rates" (+20 %, -10 %)
g = np.array([1.20, 0.90])
print("Total factor:", round(np.prod(g), 4),                       # 1.08
      "| geometric mean:", round(stats.gmean(g), 4),               # 1.0392
      "| average growth rate:", round(100 * (stats.gmean(g) - 1), 2), "%")  # 3.92
print("Check 1.0392^2 =", round(1.0392 ** 2, 4),                   # 1.0799 (approx. 1.08)
      "| wrong 5 %: 1.05^2 =", round(1.05 ** 2, 4))                # 1.1025

print("Sum:                ", data.sum())                          # 436
print("Arithmetic mean:    ", round(data.mean(), 4))               # 39.6364

# Geometric mean in three steps (as on the slide) ...
product = np.prod(data)
gmean = product ** (1 / n)
print("Geometric mean:     ", round(gmean, 4))                     # 39.5755
# ... and in one step
print("stats.gmean:        ", round(stats.gmean(data), 4))         # 39.5755

print("Trimmed mean (10%): ", round(stats.trim_mean(data, 0.10), 4))  # 39.2222
print("Median (np.median): ", np.median(data))                     # 39.0
print("Median (course):    ", course_quantile(data, 0.5))          # 39
print("Mode:               ", data.mode().tolist())                # [39]

# ---------------------------------------------------------------------
# Slides "Exercise -- Mean, Median and Mode" / "Solution (1/2), (2/2)"
# (laptops sold on n = 9 days; service ratings of n = 7 customers)
# ---------------------------------------------------------------------
header('Exercise "Mean, Median and Mode" (laptops sold, service ratings)')
laptops = np.array([4, 7, 3, 5, 4, 6, 4, 2, 10])
print("a) sorted:", np.sort(laptops).tolist(),                       # 2 3 4 4 4 5 6 7 10
      "| sum:", laptops.sum(),                                       # 45
      "| mean:", laptops.mean(),                                     # 5.0
      "| median x_(5):", course_quantile(laptops, 0.5),              # 4
      "| mode:", pd.Series(laptops).mode().tolist())                 # [4]
print("   trimmed mean (alpha = 20 %): floor(0.2 * 9) =", math.floor(0.2 * 9),  # 1
      "value per end ->", np.sort(laptops)[1:-1].sum(), "/ 7 =",     # 33 / 7
      round(stats.trim_mean(laptops, 0.20), 4))                      # 4.7143
laptops_b = np.array([4, 7, 3, 5, 4, 6, 4, 2, 19])                   # day 9: 19
print("b) sum:", laptops_b.sum(),                                    # 54
      "| mean:", laptops_b.mean(),                                   # 6.0
      "| median:", course_quantile(laptops_b, 0.5),                  # 4
      "| mode:", pd.Series(laptops_b).mode().tolist(),               # [4]
      "| trimmed mean:", round(stats.trim_mean(laptops_b, 0.20), 4))  # 4.7143
levels = ["poor", "fair", "good", "very good"]                       # ordinal
ratings = pd.Series(pd.Categorical(
    ["good", "very good", "fair", "good", "poor", "good", "very good"],
    categories=levels, ordered=True))
print("c) sorted:", ratings.sort_values().tolist())
print("   median x_(4):", ratings.sort_values().iloc[math.ceil(7 / 2) - 1],  # good
      "| mode:", ratings.mode().tolist(),                            # ['good']
      "| frequency of the mode:", (ratings == "good").sum())         # 3

# ---------------------------------------------------------------------
# Slide "Arithmetic Mean from a Frequency Table"
# ---------------------------------------------------------------------
header('Slide "Arithmetic Mean from a Frequency Table"')
xj, hj = abs_freq.index.to_numpy(), abs_freq.to_numpy()
print("h_j * x_j:", (hj * xj).tolist(), "sum:", (hj * xj).sum())   # [37, 76, 156, 80, 41, 46] 436
print("Weighted mean (h_j):", round((hj * xj).sum() / n, 4),       # 39.6364
      "| sum f_j x_j:", round((rel_freq.to_numpy() * xj).sum(), 4),
      "| np.average:", round(np.average([37, 38, 39, 40, 41, 46],
                                        weights=[1, 2, 4, 2, 1, 1]), 4))

# ---------------------------------------------------------------------
# Slides "Median" (alternative definition) - NumPy averages for even n
# ---------------------------------------------------------------------
even = [34, 37, 40, 41]
print("Even n: np.median =", np.median(even),
      "| course x_(ceil(n/2)) =", course_quantile(even, 0.5))      # 38.5 | 37

# ---------------------------------------------------------------------
# Slides "Quantiles -- Computation", "Quantiles -- Computation Example",
#        "Quantiles -- Worked Example"
# ---------------------------------------------------------------------
header('Slides "Quantiles -- Computation (Example)" / "Worked Example"')
print("Sorted data:", sorted(data))  # 37, 38, 38, 39, 39, 39, 39, 40, 40, 41, 46
xs = np.sort(data.to_numpy())
rows = []
for name, p in [("1st quartile", 0.25), ("2nd quartile", 0.50),
                ("3rd quartile", 0.75), ("17%-quantile", 0.17),
                ("80%-quantile", 0.80), ("5%-quantile", 0.05)]:
    pos = math.ceil(round(n * p, 10))           # round avoids 8.8000000001
    rows.append([name, p, round(n * p, 2), pos, xs[pos - 1],
                 course_quantile(data, p)])
print(pd.DataFrame(rows, columns=["quantile", "p", "n*p", "position",
                                  "value x_(pos)", "np.quantile(inverted_cdf)"])
      .to_string(index=False))
# Expected values: 38, 39, 40, 38, 40, 37
# Slide "Quantiles -- Computation": n = 10, p = 0.2 -> n*p = 2 is an integer
print("n = 10, p = 0.2: n*p =", 10 * 0.2, "-> position", math.ceil(10 * 0.2))  # 2

# ---------------------------------------------------------------------
# Slides "Exercise -- Quantiles of Hotline Waiting Times" /
#        "Solution (1/2), (2/2)"  (waiting times in minutes, n = 12)
# ---------------------------------------------------------------------
header('Exercise "Quantiles of Hotline Waiting Times"')
wait = np.array([3, 1, 5, 2, 6, 4, 2, 8, 3, 4, 2, 5])
n_wait = len(wait)
print("a) sorted:", np.sort(wait).tolist())       # 1 2 2 2 3 3 4 4 5 5 6 8
for name, p_ in [("10%-quantile", 0.10), ("Q1", 0.25), ("Median", 0.50),
                 ("Q3", 0.75), ("90%-quantile", 0.90)]:
    print(f"b) {name:12s}: n*p = {n_wait * p_:.1f}, position "
          f"{math.ceil(round(n_wait * p_, 10))}, value {course_quantile(wait, p_)}")
# Expected: 1.2 -> 2 -> 2 | 3 -> 3 -> 2 | 6 -> 6 -> 3 | 9 -> 9 -> 5 | 10.8 -> 11 -> 6
print("   number of calls with exactly 2 minutes:", (wait == 2).sum())     # 3
print("c) F(6) =", round((wait <= 6).mean(), 4), "(= 11/12)",               # 0.9167
      "| F(5) =", round((wait <= 5).mean(), 4), "(= 10/12)",                # 0.8333
      "| calls above 6 minutes:", (wait > 6).sum())                         # 1
print("d) average of x_(6) and x_(7):", np.median(wait),                    # 3.5
      "| course median x_(6):", course_quantile(wait, 0.5),                 # 3
      "| F(3) =", (wait <= 3).mean())                                       # 0.5

# ---------------------------------------------------------------------
# Slide "Quantiles with Python"
# ---------------------------------------------------------------------
header('Slide "Quantiles with Python"')
p = [0, 0.25, 0.50, 0.75, 1]
print("Standard quantiles:", course_quantile(data, p))         # [37 38 39 40 46]
print("Q1 (25%):          ", course_quantile(data, 0.25))      # 38
print("80%-quantile:      ", course_quantile(data, 0.80))      # 40
print("Pitfall - default (linear) np.quantile(data, 0.25):",
      np.quantile(data, 0.25),                                 # 38.5
      "| data.quantile(0.25):", data.quantile(0.25))           # 38.5

# =====================================================================
# SUBSECTION "Exercises" (Measures of Central Tendency)
# =====================================================================

# ---------------------------------------------------------------------
# Slides "Exercise -- Measures of Central Tendency and Quantiles" /
#        "Solution (1/4) ... (4/4)"  -- salaries in thousand euros
# ---------------------------------------------------------------------
header('Exercise "Measures of Central Tendency and Quantiles" (salaries)')
salary = np.array([34, 42, 28, 120, 36, 31, 45, 34, 50, 39])
print("Sorted:", np.sort(salary).tolist())   # 28 31 34 34 36 39 42 45 50 120
print("a) sum:", salary.sum(), "| mean:", salary.mean(),             # 459 | 45.9
      "| median x_(5):", course_quantile(salary, 0.5),               # 36
      "| mode:", pd.Series(salary).mode().tolist())                  # [34]
print("   employees below the mean:", (salary < salary.mean()).sum())  # 8
print("b) trimmed mean:", stats.trim_mean(salary, 0.10),             # 38.875
      "= (sum of the middle 8 values)", np.sort(salary)[1:-1].sum(), "/ 8")  # 311
for p_ in [0.20, 0.25, 0.75, 0.90]:
    print(f"c) p = {p_:.2f}: n*p = {10 * p_:.1f}, position "
          f"{math.ceil(round(10 * p_, 10))}, value {course_quantile(salary, p_)}")
# Expected: 31, 34, 45, 50
# Python code exactly as on slide "Solution (4/4)"
print(np.sort(salary))
print(salary.mean(), stats.trim_mean(salary, 0.10))
print(pd.Series(salary).mode().tolist())
print(np.quantile(salary, 0.5, method="inverted_cdf"), np.median(salary))
print(np.quantile(salary, [0.2, 0.25, 0.75, 0.9], method="inverted_cdf"))

# ---------------------------------------------------------------------
# Slides "Exercise -- Geometric Mean" / "Solution (1/2), (2/2)"
# start-up revenue 200 thousand euros, growth +10 %, -5 %, +20 %
# ---------------------------------------------------------------------
header('Exercise "Geometric Mean" (start-up revenue)')
factors = np.array([1.10, 0.95, 1.20])
print("a) total factor:", round(np.prod(factors), 4),                # 1.254
      "| revenue after 3 years:", round(200 * np.prod(factors), 1))  # 250.8
r_bar = factors.mean() - 1
print("b) arithmetic mean of the rates:", round(r_bar, 4),           # 0.0833
      "| 1.0833^3 =", round((1 + r_bar) ** 3, 4),                    # 1.2714
      "| revenue:", round(200 * (1 + r_bar) ** 3, 1))                # 254.3
x_geo = stats.gmean(factors)
print("c) geometric mean of the factors:", round(x_geo, 4),          # 1.0784
      "| average growth rate:", round(100 * (x_geo - 1), 2), "%",    # 7.84
      "| check:", round(200 * x_geo ** 3, 1))                        # 250.8
# Python code exactly as on slide "Solution (2/2)"
print(200 * np.prod(factors))       # 250.8
print(factors.mean() - 1)           # 0.0833  (arithmetic: wrong)
print(stats.gmean(factors) - 1)     # 0.0784  (geometric: correct)

# =====================================================================
# SUBSECTION "Measures of Dispersion"
# =====================================================================
four_a = np.array([34, 37, 40, 41])
four_b = np.array([36, 37, 39, 40])


def dispersion(x):
    x = np.asarray(x, dtype=float)
    s2 = np.var(x, ddof=1)                 # sample variance (n-1)
    s = np.std(x, ddof=1)                  # standard deviation
    v = s / np.mean(x)                     # coefficient of variation
    vstar = v / np.sqrt(len(x))            # normalised coeff. of variation
    return {"Mean": np.mean(x), "Median (course)": course_quantile(x, 0.5),
            "Range": np.ptp(x),
            "Interquartile range": course_quantile(x, 0.75) - course_quantile(x, 0.25),
            "Sample variance": s2, "Standard deviation": s,
            "Coefficient of variation": v,
            "Normalised coefficient of variation": vstar}


# ---------------------------------------------------------------------
# Slide "Range and Interquartile Range"
# ---------------------------------------------------------------------
header('Slide "Range and Interquartile Range"')
print("Soccer team: R =", np.ptp(data),                              # 9
      "| IQR = Q3 - Q1 =", course_quantile(data, 0.75), "-",
      course_quantile(data, 0.25), "=",
      course_quantile(data, 0.75) - course_quantile(data, 0.25))     # 40 - 38 = 2
for name, x in [("Four A", four_a), ("Four B", four_b)]:
    print(f"{name}: R = {np.ptp(x)}, Q1 = {course_quantile(x, 0.25)}, "
          f"Q3 = {course_quantile(x, 0.75)}, "
          f"IQR = {course_quantile(x, 0.75) - course_quantile(x, 0.25)}")
# Four A: R = 7, IQR = 40 - 34 = 6 | Four B: R = 4, IQR = 39 - 36 = 3

# ---------------------------------------------------------------------
# Slides "Measures of Dispersion -- Why?", "Sample Variance -- Worked
# Example", "Standard Deviation -- Worked Example", "Coefficient of
# Variation -- Worked Example", "Normalised Coefficient of Variation --
# Worked Example", "Overview of Measures of Dispersion"
# ---------------------------------------------------------------------
header('Slide "Overview of Measures of Dispersion" (Four A vs. Four B)')
overview = pd.DataFrame({"Four A": dispersion(four_a),
                         "Four B": dispersion(four_b)})
print(overview.round(4))
# Expected: mean 38/38, median 37/37, range 7/4, IQR 6/3, s^2 10/3.3333,
#           s 3.1623/1.8257, v 0.0832/0.0480, v* 0.0416/0.0240
print("Deviations A:", (four_a - 38).tolist(), "sum", (four_a - 38).sum(),  # [-4,-1,2,3] 0
      "| B:", (four_b - 38).tolist(), "sum", (four_b - 38).sum())          # [-2,-1,1,2] 0
print("Sum of squares A:", np.sum((four_a - 38) ** 2),             # 30
      "| B:", np.sum((four_b - 38) ** 2))                          # 10

# Slide "Coefficient of Variation": mixed signs -> mean close to 0
print("Mean of -10, -5, 5, 11:", np.mean([-10, -5, 5, 11]))        # 0.25

# Slide "Normalised Coefficient of Variation" (background): for non-negative
# data v is at most sqrt(n) -- extreme case: all values but one are 0
extreme = np.array([0, 0, 0, 5])
v_ext = np.std(extreme, ddof=1) / np.mean(extreme)
print("Extreme case [0, 0, 0, 5]: v =", round(v_ext, 4),
      "= sqrt(4) -> v* =", round(v_ext / np.sqrt(4), 4))             # 2.0 -> 1.0

# ---------------------------------------------------------------------
# Slides "Exercise -- Variance and Standard Deviation" /
#        "Solution (1/2), (2/2)"  (delivery times in days, n = 5 each)
# ---------------------------------------------------------------------
header('Exercise "Variance and Standard Deviation" (two parcel services)')
service_a = np.array([2, 5, 1, 3, 4])
service_b = np.array([4, 3, 5, 4, 4])
for name, x in [("A", service_a), ("B", service_b)]:
    d = x - x.mean()
    print(f"{name}: sum {x.sum()}, mean {x.mean()}, range {np.ptp(x)} "
          f"({x.max()} - {x.min()}), deviations {d.tolist()} (sum {d.sum()}), "
          f"squares {(d ** 2).tolist()}, sum of squares {(d ** 2).sum()}")
    print(f"   s^2 = {np.var(x, ddof=1):.4f}, s = {np.std(x, ddof=1):.4f}")
# A: mean 3, range 4, sum of squares 10, s^2 2.5, s 1.5811
# B: mean 4, range 2, sum of squares  2, s^2 0.5, s 0.7071

# ---------------------------------------------------------------------
# Slide "Variance from a Frequency Table" (soccer team)
# ---------------------------------------------------------------------
header('Slide "Variance from a Frequency Table"')
xbar = data.mean()
dev = xj - xbar
contrib = hj * dev ** 2
print("x_j - xbar:         ", dev.round(4).tolist())
# [-2.6364, -1.6364, -0.6364, 0.3636, 1.3636, 6.3636]
print("h_j * (x_j - xbar)^2:", contrib.round(4).tolist(), "sum", round(contrib.sum(), 4))
# [6.9504, 5.3554, 1.6198, 0.2645, 1.8595, 40.4959] sum 56.5455
s2_soccer = contrib.sum() / (n - 1)
print("s^2 =", round(s2_soccer, 4), "| s =", round(math.sqrt(s2_soccer), 4),  # 5.6545 | 2.3779
      "| same as data.var():", round(data.var(), 4))
print("Share of the value 46:", round(contrib[-1] / contrib.sum() * 100, 1), "%")  # 71.6 -> 72 %

# ---------------------------------------------------------------------
# Slide "Measures of Dispersion with Python"
# ---------------------------------------------------------------------
header('Slide "Measures of Dispersion with Python"')
print("np.ptp(four_a):", np.ptp(four_a))                           # 7
q1, q3 = np.quantile(four_a, [0.25, 0.75], method="inverted_cdf")
print("q3 - q1:", q3 - q1)                                         # 6
print("np.var(four_a, ddof=1):", np.var(four_a, ddof=1))           # 10.0
print("np.std(four_a, ddof=1):", round(np.std(four_a, ddof=1), 4)) # 3.1623
v = np.std(four_a, ddof=1) / np.mean(four_a)
vstar = v / np.sqrt(len(four_a))
print("v =", round(v, 4), "| v* =", round(vstar, 4))               # 0.0832 | 0.0416
print("Pitfall - np.var(four_a) with default ddof=0:", np.var(four_a))  # 7.5
print("pandas .var() / .std() (ddof=1):", pd.Series(four_a).var(),
      round(pd.Series(four_a).std(), 4))                           # 10.0 3.1623

# ---------------------------------------------------------------------
# SUBSECTION "Exercises" (Measures of Dispersion)
# Slides "Exercise -- Measures of Dispersion of the Handball Team" / "Solution"
# Shoe sizes of the handball team (n = 13)
# ---------------------------------------------------------------------
header('Exercise "Measures of Dispersion of the Handball Team"')
handball = np.array([40, 39, 38, 41, 46, 39, 39, 38, 37, 40, 39, 40, 42])
res = dispersion(handball)
print("n =", len(handball))                                         # 13
for key in ["Mean", "Sample variance", "Standard deviation",
            "Coefficient of variation", "Normalised coefficient of variation"]:
    print(f"{key:37s} {res[key]:.4f}")
# Expected: 39.8462, 5.1410, 2.2674, 0.0569, 0.0158
print("Sum:", handball.sum(),                                         # 518
      "| sum of squared deviations:",
      round(((handball - handball.mean()) ** 2).sum(), 4))            # 61.6923
v_soccer = data.std() / data.mean()
print("Soccer team for comparison: s =", round(data.std(), 4),        # 2.3779
      "| v =", round(v_soccer, 4),                                    # 0.0600
      "| v* =", round(v_soccer / math.sqrt(n), 4))                    # 0.0181

# ---------------------------------------------------------------------
# Slides "Exercise -- Comparing the Dispersion of Two Branches" /
#        "Solution (1/3) ... (3/3)"  (bakery, thousand euros, n = 6)
# ---------------------------------------------------------------------
header('Exercise "Comparing the Dispersion of Two Branches"')
city = np.array([120, 130, 125, 135, 115, 125])
rural = np.array([20, 24, 22, 26, 18, 22])
for name, x in [("City", city), ("Rural", rural)]:
    d = x - x.mean()
    print(f"{name}: sum {x.sum()}, mean {x.mean()}, deviations {d.tolist()}, "
          f"squares {(d ** 2).tolist()}, sum of squares {(d ** 2).sum()}")
    res = dispersion(x)
    print(f"   s^2 = {res['Sample variance']:.4f}, s = {res['Standard deviation']:.4f}, "
          f"v = {res['Coefficient of variation']:.4f}, "
          f"v* = {res['Normalised coefficient of variation']:.4f}")
# City:  125, 250, s^2 50, s 7.0711, v 0.0566, v* 0.0231
# Rural:  22,  40, s^2  8, s 2.8284, v 0.1286, v* 0.0525
print("sqrt(6) =", round(math.sqrt(6), 4))                            # 2.4495
# Python code exactly as on slide "Solution (3/3)"
for x in (city, rural):
    s = x.std(ddof=1)
    print(x.mean(), x.var(ddof=1), round(s, 4), round(s / x.mean(), 4))

# =====================================================================
# SUBSECTION "Exam-Style Exercise" -- Books per order
# (adapted from mock exam 4, task 1)
# =====================================================================
header('Exam-Style Exercise "Books per Order"')
x_books = np.array([1, 2, 3, 4, 5])
h_books = np.array([3, 5, 9, 5, 3])
n_books = h_books.sum()
f_books = h_books / n_books
print("a) f_j:", f_books.tolist(),                                    # 0.12 0.2 0.36 0.2 0.12
      "| H_j:", h_books.cumsum().tolist(),                            # 3 8 17 22 25
      "| F(x_j):", f_books.cumsum().round(4).tolist())                # 0.12 0.32 0.68 0.88 1
print("b) at most 2:", round(f_books[:2].sum(), 4),                   # 0.32
      "| at least 4: 1 - F(3) =", round(1 - f_books[:3].sum(), 4))    # 0.32
books = np.repeat(x_books, h_books)                 # expand the table (25 values)
for name, p_ in [("Q1", 0.25), ("Median", 0.50), ("Q3", 0.75)]:
    pos = math.ceil(n_books * p_)
    print(f"c) {name}: n*p = {n_books * p_}, position {pos}, "
          f"value {course_quantile(books, p_)}")
# Q1: 6.25 -> 7 -> 2 | median: 12.5 -> 13 -> 3 | Q3: 18.75 -> 19 -> 4
print("   mode:", x_books[h_books.argmax()], "| IQR:",
      course_quantile(books, 0.75) - course_quantile(books, 0.25))    # 3 | 2
print("e) h_j*x_j:", (h_books * x_books).tolist(), "sum", (h_books * x_books).sum(),
      "| mean:", (h_books * x_books).sum() / n_books)                 # [3,10,27,20,15] 75 | 3.0
ss_books = h_books * (x_books - 3) ** 2
print("f) h_j*(x_j-3)^2:", ss_books.tolist(), "sum", ss_books.sum())  # [12,5,0,5,12] 34
s2_b = ss_books.sum() / (n_books - 1)
print("   s^2 =", round(s2_b, 4), "| s =", round(math.sqrt(s2_b), 4),  # 1.4167 | 1.1902
      "| v =", round(math.sqrt(s2_b) / 3, 4))                         # 0.3967
# Python code exactly as on slide "Solution (4/4)"
books = np.repeat([1, 2, 3, 4, 5], [3, 5, 9, 5, 3])       # expand the table
print(len(books), (books <= 2).mean(), (books >= 4).mean())
print(pd.Series(books).mode().tolist(),
      np.quantile(books, [0.25, 0.5, 0.75], method="inverted_cdf"))
s = books.std(ddof=1)
print(books.mean(), round(s**2, 4), round(s, 4), round(s / books.mean(), 4))

# =====================================================================
# SECTION "Summary" - Slides "Summary 4: Key Python Commands (1)" / "(2)"
# =====================================================================
header('Slides "Summary 4: Key Python Commands (1)" / "(2)"')
print(data.value_counts().sort_index())                     # Absolute frequencies
print(data.value_counts(normalize=True).sort_index())       # Relative frequencies
print(data.value_counts(normalize=True).sort_index().cumsum())  # Cumulative
print("mean:", np.mean(data))                               # Arithmetic mean
print("gmean:", stats.gmean(data))                          # Geometric mean
print("trim_mean:", stats.trim_mean(data, 0.10))            # Trimmed mean (10%)
print("gmean - 1:", stats.gmean(factors) - 1)               # Average growth rate
print("mode:", data.mode().tolist())                        # Mode
print("np.average:", np.average([37, 38, 39, 40, 41, 46],
                                weights=[1, 2, 4, 2, 1, 1]))  # Mean from a frequency table
print("np.repeat:", np.repeat([37, 38], [1, 2]))            # Frequency table -> raw data
print("median:", np.median(data))                           # Median
print("Q1:", np.quantile(data, 0.25, method="inverted_cdf"))  # Quantiles (e.g. Q1)
print("range:", np.ptp(data))                               # Range
q1, q3 = np.quantile(data, [0.25, 0.75], method="inverted_cdf")
print("IQR:", q3 - q1)                                      # Interquartile range
print("var:", np.var(data, ddof=1))                         # Sample variance
print("std:", np.std(data, ddof=1))                         # Standard deviation
print("v:", np.std(data, ddof=1) / np.mean(data))           # Coefficient of variation
print("v*:", np.std(data, ddof=1) / np.mean(data) / np.sqrt(len(data)))  # Norm. coeff.
