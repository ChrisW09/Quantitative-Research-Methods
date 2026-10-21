# =====================================================================
# Quantitative Research -- Part 5: Classification
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 5. Run it from the
# folder Part_5_Classification (the data are read from ../data).
# Sections follow the sections of the slide deck:
#   1  Classification problems     (Default data, linear regression fails)
#   2  Logistic regression          (odds, model, ML estimation, inference)
#   3  Multiple logistic regression (student paradox)
#   4  From probabilities to decisions (threshold, decision boundary)
#   5  Evaluating a classifier      (confusion matrix, ROC/AUC, test data)
#   Appendix                        (Bayes classifiers: naive Bayes, LDA)
# =====================================================================

df <- read.csv("../data/Default.csv", stringsAsFactors = TRUE)
str(df)                                  # default, student, balance, income
table(df$default)                        # 9667 No, 333 Yes
prop.table(table(df$default))            # 3.33 % defaulters

# =====================================================================
# 1 Classification problems
# =====================================================================
boxplot(balance ~ default, data = df)
boxplot(income ~ default, data = df)

# linear regression on a 0/1 response ("linear probability model")
y <- as.numeric(df$default == "Yes")
lpm <- lm(y ~ balance, data = df)
coef(lpm)                                # -0.0752, 0.000130
sum(fitted(lpm) < 0)                     # 3123 negative "probabilities"

# =====================================================================
# 2 Logistic regression
# =====================================================================
# odds and log-odds
p <- c(0.1, 0.2, 0.5, 0.8, 0.9)
cbind(p, odds = p / (1 - p), logodds = log(p / (1 - p)))

g1 <- glm(default ~ balance, family = binomial, data = df)
summary(g1)                              # -10.6513, 0.005499
exp(coef(g1))                            # odds ratio per 1 $
exp(100 * coef(g1)["balance"])           # odds ratio per 100 $: 1.733
exp(1000 * coef(g1)["balance"])          # per 1000 $: 244.7

# predicted probabilities
predict(g1, data.frame(balance = c(1000, 1500, 2000, 2500)), type = "response")
# by hand: log-odds -> probability
eta <- coef(g1)[1] + coef(g1)[2] * 1500
exp(eta) / (1 + exp(eta))                # 0.083
-coef(g1)[1] / coef(g1)[2]               # p = 0.5 at balance 1937

# Wald confidence intervals (estimate +- 1.96 SE) and odds ratios
confint.default(g1)
exp(100 * confint.default(g1)["balance", ])   # [1.660, 1.810]

g2 <- glm(default ~ student, family = binomial, data = df)
summary(g2)$coefficients                 # student: +0.4049, p = 0.0004
exp(coef(g2)["studentYes"])              # 1.499
exp(confint.default(g2)["studentYes", ])

# =====================================================================
# 3 Multiple logistic regression
# =====================================================================
g3 <- glm(default ~ balance + income + student, family = binomial, data = df)
summary(g3)                              # student: -0.6468, income n.s.
exp(coef(g3)["studentYes"])              # 0.524
exp(confint.default(g3)["studentYes", ]) # [0.330, 0.832]
1e4 * confint.default(g3)["income", ]    # per 10000 $: [-0.130, 0.191]

tapply(df$balance, df$student, mean)     # students carry larger balances
prop.table(table(df$student, df$default), 1)   # 4.31 % vs 2.92 %

# two customers A (non-student, 1000 $, 40000 $) and B (student, 2000 $, 30000 $)
AB <- data.frame(balance = c(1000, 2000), income = c(40000, 30000),
                 student = c("No", "Yes"))
predict(g3, AB, type = "response")       # 0.0066, 0.512

# =====================================================================
# 4 From probabilities to decisions
# =====================================================================
phat <- predict(g3, type = "response")
pred <- ifelse(phat > 0.5, "Yes", "No")
(-coef(g1)[1] + log(0.2 / 0.8)) / coef(g1)[2]   # boundary for t = 0.2: 1685

# =====================================================================
# 5 Evaluating a classifier
# =====================================================================
table(Actual = df$default, Predicted = phat > 0.5)   # 9627 40 / 228 105
table(Actual = df$default, Predicted = phat > 0.2)   # 9390 277 / 130 203

metrics <- function(t) {
  tp <- sum(phat > t & y == 1); fp <- sum(phat > t & y == 0)
  fn <- sum(phat <= t & y == 1); tn <- sum(phat <= t & y == 0)
  c(accuracy = (tp + tn) / length(y), sensitivity = tp / (tp + fn),
    specificity = tn / (tn + fp), precision = tp / (tp + fp))
}
round(rbind(t0.5 = metrics(0.5), t0.2 = metrics(0.2), t0.1 = metrics(0.1)), 4)

# ROC curve and AUC by hand
ts <- sort(unique(c(0, phat, 1)), decreasing = TRUE)
roc <- t(sapply(ts, function(t) c(fpr = mean(phat[y == 0] > t),
                                  tpr = mean(phat[y == 1] > t))))
plot(roc[, "fpr"], roc[, "tpr"], type = "l", xlab = "1 - specificity",
     ylab = "sensitivity"); abline(0, 1, lty = 2)
# AUC = P(phat of a random defaulter > phat of a random non-defaulter)
r <- rank(phat); n1 <- sum(y); n0 <- sum(1 - y)
(sum(r[y == 1]) - n1 * (n1 + 1) / 2) / (n1 * n0)      # 0.950

# training and test data
set.seed(1)
train <- sample(nrow(df), 7000)
g_tr <- glm(default ~ balance + income + student, family = binomial,
            data = df[train, ])
p_te <- predict(g_tr, df[-train, ], type = "response")
table(Actual = df$default[-train], Predicted = p_te > 0.5)  # 2896 2 / 81 21
table(Actual = df$default[-train], Predicted = p_te > 0.2)  # 2839 59 / 44 58
# Exercise "training vs. test data": metrics on the test data
tab5 <- table(df$default[-train], p_te > 0.5); tab2 <- table(df$default[-train], p_te > 0.2)
tab5[2, 2] / sum(tab5[2, ]); tab2[2, 2] / sum(tab2[2, ])   # sensitivity 0.206, 0.569
y_te <- as.numeric(df$default[-train] == "Yes"); r <- rank(p_te)
(sum(r[y_te == 1]) - sum(y_te) * (sum(y_te) + 1) / 2) /
  (sum(y_te) * sum(1 - y_te))                               # test AUC 0.938

# =====================================================================
# Appendix: Bayes classifiers
# =====================================================================
# naive Bayes by hand (spam example)
score_spam <- 0.4 * 0.6 * 0.7; score_ham <- 0.6 * 0.1 * 0.2
score_spam / (score_spam + score_ham)    # 0.933

# LDA with one predictor: boundary x* = (mu0 + mu1)/2 - sigma^2/(mu1 - mu0) * log(pi1/pi0)
(0 + 2) / 2 - 1 / (2 - 0) * log(0.2 / 0.8)   # 1.693

# LDA and naive Bayes on the Default data
library(MASS)                            # lda()
ld <- lda(default ~ balance + student, data = df)
table(Actual = df$default, Predicted = predict(ld)$class)  # 9644 23 / 252 81
library(e1071)                           # naiveBayes()
nb <- naiveBayes(default ~ balance + student, data = df)
table(Actual = df$default, Predicted = predict(nb, df))
