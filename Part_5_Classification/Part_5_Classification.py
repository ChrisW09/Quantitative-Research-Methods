# =====================================================================
# Quantitative Research -- Part 5: Classification
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 5. Run it from the
# folder Part_5_Classification (the data are read from ../data):
#     python3 Part_5_Classification.py
# Sections follow the sections of the slide deck:
#   1  Classification problems     (Default data, two-way tables and
#                                   conditional probability, linear regression fails)
#   2  Logistic regression          (odds, model, ML estimation, inference)
#   3  Multiple logistic regression (student paradox)
#   4  From probabilities to decisions (threshold, decision boundary)
#   5  Evaluating a classifier      (confusion matrix, base rates and precision,
#                                   ROC/AUC, test data)
#   Appendix                        (total probability, Bayes' theorem,
#                                   Bayes classifiers: naive Bayes, LDA)
# The figures are produced separately by make_figures.py.
# =====================================================================

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB

pd.set_option("display.width", 120)

df = pd.read_csv("../data/Default.csv")
df["y"] = (df.default == "Yes").astype(int)     # 1 = default, 0 = no default
print(df.head())                                 # default, student, balance, income
print(df.default.value_counts())                 # 9667 No, 333 Yes
print(df.default.value_counts(normalize=True))   # 3.33 % defaulters

# =====================================================================
# 1 Classification problems
# =====================================================================
# Slide "Our story: the Default data"
print(df.groupby("default")[["balance", "income"]].mean())

# ---------------------------------------------------------------------
# 1b Two-way tables and conditional probability
# ---------------------------------------------------------------------
# Slide "Default by student status -- a two-way table": counts and joint /
# marginal relative frequencies
tab = pd.crosstab(df.student, df.default, margins=True)
print(tab)                                       # 6850 206 7056 / 2817 127 2944
print(pd.crosstab(df.student, df.default, margins=True,
                  normalize="all").round(4))     # joint 0.0127, marginal 0.2944, 0.0333

# Slide "Conditional relative frequencies" (rows: condition on student status)
print(pd.crosstab(df.student, df.default, normalize="index").round(4))   # 0.0292, 0.0431
print(127 / 2944, 0.0127 / 0.2944)               # 0.0431 = joint / marginal
print(pd.crosstab(df.student, df.default, normalize="columns").round(4))
print(127 / 333)                                 # P(student | default) = 0.381

# Slides "Conditional probability -- definition and two rules" and "Independence"
p_d = df.y.mean()                                # P(default)              0.0333
p_s = (df.student == "Yes").mean()               # P(student)              0.2944
p_ds = ((df.y == 1) & (df.student == "Yes")).mean()  # P(default and student) 0.0127
print(p_ds / p_s, (p_ds / p_s) * p_s)            # 0.0431 and back to 0.0127
print(p_d + p_s - p_ds)                          # addition rule: 0.3150
print(p_d * p_s, 10000 * p_d * p_s)              # 0.0098 -> 98 expected vs 127 observed

# Slide "Classification = estimating P(Y = 1 | x)": default rate by balance class
bal_class = pd.cut(df.balance, [0, 500, 1000, 1500, 2000, np.inf], right=False)
print(pd.crosstab(bal_class, df.default, margins=True))   # 2613 3755 2721 805 106
print(pd.crosstab(bal_class, df.default, normalize="index").round(3))
# default rates 0.000 0.002 0.025 0.220 0.764

# Exercise "newsletter and purchases" (rows: newsletter yes/no, cols: purchase yes/no)
nl = pd.DataFrame([[15, 5], [15, 25]], index=["NL yes", "NL no"],
                  columns=["buy yes", "buy no"])
n_nl = nl.values.sum()                           # 60
f_nl = nl.sum(axis=1) / n_nl                     # 0.333, 0.667
f_buy = nl.sum(axis=0) / n_nl                    # 0.5, 0.5
print(f_nl, f_buy, 15 / 60)                      # joint 0.25
print(f_nl["NL yes"] * f_buy["buy yes"])         # 0.167 under independence
print(n_nl * f_nl["NL yes"] * f_buy["buy yes"])  # 10 expected subscribing buyers
print(nl.div(nl.sum(axis=1), axis=0))            # purchase rates 0.75 / 0.375
print(15 / 30)                                   # P(subscriber | purchase) = 0.5

# Exercise "streaming and gaming" (mock exam style)
pS, pG, pSG = 0.60, 0.50, 0.30
print(pSG / pS)                                  # P(G | S) = 0.50
print(pS + pG - pSG, 1 - (pS + pG - pSG))        # P(S or G) = 0.80, neither 0.20
print(pS * pG, pSG / pG)                         # 0.30 = P(S and G): independent; P(S | G) = 0.60
print(pS - pSG, pG - pSG, 1 - pS - pG + pSG)     # table cells 0.30, 0.20, 0.20

# Slide "Why not simply use linear regression?" (linear probability model)
lpm = smf.ols("y ~ balance", data=df).fit()
print(lpm.params)                                # -0.0752, 0.000130
print((lpm.fittedvalues < 0).sum())              # 3123 negative "probabilities"
print(df.balance[lpm.fittedvalues < 0].max())    # all balances below 579 $

# =====================================================================
# 2 Logistic regression
# =====================================================================
# Slide "Odds -- another way to express a probability"
p = np.array([0.1, 0.2, 0.5, 0.8, 0.9])
print(pd.DataFrame({"p": p, "odds": p / (1 - p),
                    "logodds": np.log(p / (1 - p))}).round(3))

# Exercise "probability, odds and log-odds" (two-way table default x student)
for grp, (yes, no) in {"students": (127, 2817), "non-students": (206, 6850)}.items():
    print(grp, yes / (yes + no), yes / no, np.log(yes / no))
# students 0.0431, 0.0451, -3.099; non-students 0.0292, 0.0301, -3.504
odds_ratio = (127 / 2817) / (206 / 6850)
print(odds_ratio, np.log(odds_ratio))            # 1.50, 0.405
print((127 / 2944) / (206 / 7056))               # probability ratio 1.48
print((0.8 / 0.2) / (0.5 / 0.5))                 # p = 0.8 vs 0.5: odds ratio 4
print(np.exp(-1), np.exp(-1) / (1 + np.exp(-1))) # log-odds -1: odds 0.368, p 0.269

# Exercise "which parameters are more plausible?" (likelihood of A and B)
xb = np.array([1000, 1500, 2000, 2500]); yb = np.array([0, 0, 1, 1])
for b0, b1 in [(-10.65, 0.0055), (-5, 0.002)]:
    pb = 1 / (1 + np.exp(-(b0 + b1 * xb)))
    print(pb.round(4), np.prod(np.where(yb == 1, pb, 1 - pb)).round(4))
# L(A) = 0.5117, L(B) = 0.1128, ratio 4.5

# Slide "Logistic regression with Python"
g1 = smf.logit("y ~ balance", data=df).fit(disp=0)
print(g1.summary2().tables[1])                   # -10.6513, 0.005499, p = 2.0e-137
print(np.exp(g1.params))                         # odds ratio per 1 $
print(np.exp(100 * g1.params["balance"]))        # odds ratio per 100 $: 1.733
print(np.exp(1000 * g1.params["balance"]))       # per 1000 $: 244.4

# Slide "Worked example": predicted probabilities
new = pd.DataFrame({"balance": [1000, 1500, 2000, 2500]})
print(g1.predict(new))                           # 0.0058 0.0829 0.5858 0.9567 (unrounded)
eta_r = -10.65 + 0.0055 * new.balance            # rounded model as on the slide
print((np.exp(eta_r) / (1 + np.exp(eta_r))).round(3))  # 0.006 0.083 0.587 0.957
print(g1.predict(new, which="linear"))           # log-odds eta
# by hand: log-odds -> probability
eta = g1.params["Intercept"] + g1.params["balance"] * 1500
print(np.exp(eta) / (1 + np.exp(eta)))           # 0.083
print(-g1.params["Intercept"] / g1.params["balance"])  # p = 0.5 at balance 1937

# Slide "Inference -- balance and student status": Wald CIs and odds ratios
print(g1.conf_int())                             # estimate +- 1.96 SE
print(g1.tvalues["balance"])                     # z = 24.95
print(g1.pvalues["balance"] < 0.0001)            # True: p = 2.0e-137, reported as p < 0.0001
print(np.exp(100 * g1.conf_int().loc["balance"]))  # [1.660, 1.810]

g2 = smf.logit("y ~ student", data=df).fit(disp=0)
print(g2.summary().tables[1])                    # student: +0.4049, p = 0.0004
print(g2.pvalues["student[T.Yes]"])              # 0.00043
print(np.exp(g2.params["student[T.Yes]"]))       # 1.499
print(np.exp(g2.conf_int().loc["student[T.Yes]"]))  # [1.20, 1.88]
print(g2.params["Intercept"], np.log(206 / 6850))    # -3.504 = log-odds of non-students

# =====================================================================
# 3 Multiple logistic regression
# =====================================================================
# Slide "Multiple logistic regression with Python"
g3 = smf.logit("y ~ balance + income + student", data=df).fit(disp=0)
print(g3.summary().tables[1])                    # student: -0.6468, income n.s.
print(g3.bse)                                    # SE income 8.203e-06, student 0.2363
print(np.exp(g3.params["student[T.Yes]"]))       # 0.524
print(np.exp(g3.conf_int().loc["student[T.Yes]"]))  # [0.330, 0.832]
print(1e4 * g3.conf_int().loc["income"])         # per 10000 $: [-0.130, 0.191]
print(np.exp(1e4 * g3.conf_int().loc["income"])) # OR: [0.878, 1.211]

# Slide "The student paradox"
print(df.groupby("student").balance.mean())      # students carry larger balances
print(pd.crosstab(df.student, df.default, normalize="index"))  # 4.31 % vs 2.92 %

# Exercise "logistic regression from A to Z": customers A and B
AB = pd.DataFrame({"balance": [1000, 2000], "income": [40000, 30000],
                   "student": ["No", "Yes"]})
print(g3.predict(AB))                            # 0.0066, 0.512
eta_A = -10.869 + 0.00574 * 1000 + 0.003 * 40
eta_B = -10.869 + 0.00574 * 2000 + 0.003 * 30 - 0.6468
print(eta_A, eta_B, 1 / (1 + np.exp(-eta_A)), 1 / (1 + np.exp(-eta_B)))  # 0.0066, 0.514
print((10.869 - 0.120) / 0.00574, (10.869 - 0.120 + 0.6468) / 0.00574)  # 1873, 1985
print(0.6468 / 0.00574)                          # a student needs about 113 $ more

# =====================================================================
# 4 From probabilities to decisions
# =====================================================================
# Slide "Decision boundary -- default and balance"
b0, b1 = g1.params
print(-b0 / b1)                                  # boundary for t = 0.5: 1937
print((-b0 + np.log(0.2 / 0.8)) / b1)            # boundary for t = 0.2: 1685

# Exercise "from probability to decision" (balances 1800, 2000, 2200)
eta = -10.65 + 0.0055 * np.array([1800, 2000, 2200])
print(eta, (1 / (1 + np.exp(-eta))).round(3))    # 0.321 0.587 0.810

# =====================================================================
# 5 Evaluating a classifier
# =====================================================================
phat = g3.predict(df)                            # estimated P(default = Yes)
y = df.y

# Slide "Why accuracy alone is not enough": always predict "no default"
print(1 - y.mean())                              # 0.9667

# Slide "Confusion matrix -- Default data, t = 0.5" and exercise t = 0.2
print(pd.crosstab(df.default, phat > 0.5))       # 9627 40 / 228 105
print(pd.crosstab(df.default, phat > 0.2))       # 9390 277 / 130 203


def metrics(y, p, t):
    """Accuracy, sensitivity, specificity, precision for threshold t."""
    tp = ((p > t) & (y == 1)).sum(); fp = ((p > t) & (y == 0)).sum()
    fn = ((p <= t) & (y == 1)).sum(); tn = ((p <= t) & (y == 0)).sum()
    return pd.Series({"accuracy": (tp + tn) / len(y),
                      "sensitivity": tp / (tp + fn),
                      "specificity": tn / (tn + fp),
                      "precision": tp / (tp + fp)})


print(pd.DataFrame({f"t={t}": metrics(y, phat, t) for t in (0.5, 0.2, 0.1)}).T.round(4))

# Slides "The confusion matrix is a two-way table" and "Rates with Python":
# normalise rows (condition on the actual class) or columns (on the prediction)
pred = phat > 0.5
print(pd.crosstab(df.default, pred, normalize="index").round(4))    # sens 0.3153, spec 0.9959
print(pd.crosstab(df.default, pred, normalize="columns").round(4))  # precision 0.7241
print(105 / 333, 9627 / 9667, 105 / 145, (9627 + 105) / 10000, 9627 / 9855)

# Subsection "Base rates and precision": the rule t = 0.2 in other portfolios
sens = 203 / 333                                 # 0.6096
fpr = 277 / 9667                                 # 1 - specificity = 0.0287


def precision(pi, sens, fpr):
    """Precision of a rule with given sensitivity and false-positive rate
    when the positive class has base rate pi (Bayes' theorem)."""
    return sens * pi / (sens * pi + fpr * (1 - pi))


print(sens, fpr, 1 - fpr)
for pi in (0.01, 0.0333, 0.10):
    print(pi, 10000 * pi * sens, 10000 * (1 - pi) * fpr, precision(pi, sens, fpr))
# 1 %: 61 TP, 284 FP, precision 0.177; 3.33 %: 0.423; 10 %: 0.703
print(0.6096 * 0.0333, 0.0287 * 0.9667)          # check on the slide: 0.0203, 0.0277

# Exercise "rapid test and base rate": sensitivity = specificity = 0.9
n_people, prev = 1000, 0.01
ill = n_people * prev; healthy = n_people - ill  # 10, 990
TP = 0.9 * ill; FN = ill - TP; TN = 0.9 * healthy; FP = healthy - TN
print(TP, FN, TN, FP, TP + FP, TN + FN)          # 9 1 891 99 / 108 positive, 892 negative
print((TP + FP) / n_people)                      # P(+) = 0.108
print(TP / (TP + FP), TN / (TN + FN))            # precision 0.083, negatives correct 0.9989
print(precision(0.20, 0.9, 0.1))                 # practice with 20 % ill: 180 / 260 = 0.692

# Slide "The ROC curve" and "AUC": ROC by sklearn and AUC as ranking probability
fpr, tpr, thr = roc_curve(y, phat)               # (1 - specificity, sensitivity)
print(roc_auc_score(y, phat))                    # 0.950
r = phat.rank(); n1 = y.sum(); n0 = len(y) - n1
print((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))   # 0.950 again

# Slide "Honest evaluation: training and test data" and the exercise
train = df.sample(n=7000, random_state=1)        # 70 % training data
test = df.drop(train.index)                      # remaining 30 % test data
g_tr = smf.logit("y ~ balance + income + student", data=train).fit(disp=0)
p_te = g_tr.predict(test)
print(test.y.sum())                              # 112 test defaulters
print(pd.crosstab(test.default, p_te > 0.5))     # 2878 10 / 78 34
print(pd.crosstab(test.default, p_te > 0.2))     # 2824 64 / 45 67
print(pd.DataFrame({f"t={t}": metrics(test.y, p_te, t) for t in (0.5, 0.2)}).T.round(4))
# t=0.5: accuracy 0.971, sensitivity 0.304, specificity 0.997, precision 0.773
# t=0.2: accuracy 0.964, sensitivity 0.598, specificity 0.978, precision 0.511
print(roc_auc_score(test.y, p_te))               # test AUC 0.956 (all data: 0.950)

# =====================================================================
# Appendix: Bayes' theorem and Bayes classifiers
# =====================================================================
# A.1 Slides "Law of total probability" and "Bayes' theorem" (rapid test)
p_pos = 0.9 * 0.01 + 0.1 * 0.99
print(p_pos, 0.9 * 0.01 / p_pos)                 # 0.108, 0.083

# Worked example "the night-time taxi": 5 blue, 25 green, witness 80 % correct
pB = 5 / 30; pW_B = 0.8; pW_notB = 0.2
pW = pW_B * pB + pW_notB * (1 - pB)              # total probability 9/30 = 0.3
print(pW, pW_B * pB / pW)                        # posterior 4/9 = 0.444
print(30 * pW_B * pB, 30 * pW_notB * (1 - pB))   # 4 correct and 5 mistaken "blue" statements

# Exercise "three suppliers"
prior = np.array([0.5, 0.3, 0.2]); lik = np.array([0.02, 0.04, 0.10])
joint = prior * lik
print(joint, joint.sum(), 1000 * joint)          # 0.010 0.012 0.020; P(D) = 0.042; 10 12 20
print(prior[0] * joint.sum())                    # 0.021 != 0.010: not independent
print((joint / joint.sum()).round(3))            # posteriors 0.238 0.286 0.476 -> L3

# Exercise "automated quality test" (mock exam style)
pD, pP_D, pP_notD = 0.02, 0.95, 0.04
paths = [pD * pP_D, pD * (1 - pP_D), (1 - pD) * pP_notD, (1 - pD) * (1 - pP_notD)]
print(paths, sum(paths))                         # 0.019 0.001 0.0392 0.9408, sum 1
p_alarm = paths[0] + paths[2]
print(p_alarm, paths[0] / p_alarm)               # P(+) = 0.0582, P(D | +) = 0.3265
print(10000 * np.array(paths))                   # 190 10 392 9408 of 10 000 parts
print(1 - pP_notD)                               # specificity 0.96

# Exercise "naive Bayes spam filter"
score_spam = 0.4 * 0.6 * 0.7; score_ham = 0.6 * 0.1 * 0.2
print(score_spam, score_ham, score_spam / (score_spam + score_ham))  # 0.933
print(0.42 / (0.42 + 0.02))                      # prior ignored: 0.955

# Exercise "LDA in one dimension":
# boundary x* = (mu0 + mu1)/2 - sigma^2/(mu1 - mu0) * log(pi1/pi0)
print((0 + 2) / 2 - 1 / (2 - 0) * np.log(0.2 / 0.8))   # 1.693

# Slide "Bayes classifiers with Python": LDA and naive Bayes on the Default data
X = pd.get_dummies(df[["balance", "student"]], drop_first=True)  # student_Yes
lda = LinearDiscriminantAnalysis().fit(X, df.default)
# errstate silences spurious floating-point warnings of some BLAS builds
with np.errstate(all="ignore"):
    print(pd.crosstab(df.default, lda.predict(X)))   # 9644 23 / 252 81
    print(roc_auc_score(y, lda.predict_proba(X)[:, 1]))  # AUC 0.950
nb = GaussianNB().fit(X, df.default)             # treats the dummy as normal, too
print(pd.crosstab(df.default, nb.predict(X)))
