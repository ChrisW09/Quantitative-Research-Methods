# =====================================================================
# Quantitative Research -- Part 5: Classification
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 5. Run it from the
# folder Part_5_Classification (the data are read from ../data):
#     python3 Part_5_Classification.py
# Sections follow the sections of the slide deck:
#   1  Classification problems     (Default data, linear regression fails)
#   2  Logistic regression          (odds, model, ML estimation, inference)
#   3  Multiple logistic regression (student paradox)
#   4  From probabilities to decisions (threshold, decision boundary)
#   5  Evaluating a classifier      (confusion matrix, ROC/AUC, test data)
#   Appendix                        (Bayes classifiers: naive Bayes, LDA)
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

# Exercise "which parameters are more plausible?" (likelihood of A and B)
xb = np.array([1000, 1500, 2000, 2500]); yb = np.array([0, 0, 1, 1])
for b0, b1 in [(-10.65, 0.0055), (-5, 0.002)]:
    pb = 1 / (1 + np.exp(-(b0 + b1 * xb)))
    print(pb.round(4), np.prod(np.where(yb == 1, pb, 1 - pb)).round(4))
# L(A) = 0.5117, L(B) = 0.1128, ratio 4.5

# Slide "Logistic regression with Python"
g1 = smf.logit("y ~ balance", data=df).fit(disp=0)
print(g1.summary2().tables[1])                   # -10.6513, 0.005499
print(np.exp(g1.params))                         # odds ratio per 1 $
print(np.exp(100 * g1.params["balance"]))        # odds ratio per 100 $: 1.733
print(np.exp(1000 * g1.params["balance"]))       # per 1000 $: 244.4

# Slide "Worked example": predicted probabilities
new = pd.DataFrame({"balance": [1000, 1500, 2000, 2500]})
print(g1.predict(new))                           # 0.006 0.083 0.586 0.957
print(g1.predict(new, which="linear"))           # log-odds eta
# by hand: log-odds -> probability
eta = g1.params["Intercept"] + g1.params["balance"] * 1500
print(np.exp(eta) / (1 + np.exp(eta)))           # 0.083
print(-g1.params["Intercept"] / g1.params["balance"])  # p = 0.5 at balance 1937

# Slide "Inference -- balance and student status": Wald CIs and odds ratios
print(g1.conf_int())                             # estimate +- 1.96 SE
print(g1.tvalues["balance"])                     # z = 24.95
print(np.exp(100 * g1.conf_int().loc["balance"]))  # [1.660, 1.810]

g2 = smf.logit("y ~ student", data=df).fit(disp=0)
print(g2.summary().tables[1])                    # student: +0.4049, p = 0.0004
print(g2.pvalues["student[T.Yes]"])              # 0.00043
print(np.exp(g2.params["student[T.Yes]"]))       # 1.499
print(np.exp(g2.conf_int().loc["student[T.Yes]"]))  # [1.20, 1.88]

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
# Appendix: Bayes classifiers
# =====================================================================
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
