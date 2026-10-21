# =====================================================================
# Quantitative Research -- Part 4: Regression
# Author:  Prof. Dr. Christoph Weisser (HSBI)
#
# Reproduces every number shown on the slides of Part 4. Run it from the
# folder Part_4_Regression (the data sets are read from ../data).
# Sections follow the sections of the slide deck:
#   1  Correlation              (lamp example)
#   2  Simple regression        (least squares, leverage)
#   3  Goodness of fit          (variance decomposition, R^2)
#   4  Residual analysis        (residual plot, QQ-plot), body heights
#   5  Inference                (SE, t-test, CI, p-value, prediction)
#   6  Multiple regression      (Advertising, Credit)
#   Appendix                  (interactions, diagnostics, collinearity / VIF)
# =====================================================================

# ---------------------------------------------------------------------
# SETUP: lamp example (price in Euro, sales quantity) -- running story
# ---------------------------------------------------------------------
price    <- c(80, 85, 90, 95, 100, 105, 110, 115, 120)
quantity <- c(20, 17, 15,  9,  11,   8,   4,   4,   2)
n <- length(price)

# =====================================================================
# 1 Correlation
# =====================================================================
plot(price, quantity, xlab = "Price (Euro)", ylab = "Sales quantity",
     main = "Scatter plot", pch = 19)
cov(price, quantity)                 # -83.75
cor(price, quantity)                 # -0.9732
sd(price); sd(quantity)              # 13.6931, 6.2849

# Exercise "covariance and correlation by hand"
xa <- c(2, 4, 5, 6, 8); ya <- c(10, 14, 17, 16, 23)
cov(xa, ya); sd(xa); sd(ya); cor(xa, ya)      # 10.25, 2.2361, 4.7434, 0.9664

# =====================================================================
# 2 Simple linear regression
# =====================================================================
# Coefficients by hand
(beta1 <- cov(price, quantity) / var(price))      # -0.4467
(beta0 <- mean(quantity) - beta1 * mean(price))   # 54.6667
beta1 * sd(price) / sd(quantity)                   # = cor(price, quantity)

# The same with lm()
reg <- lm(quantity ~ price)
coef(reg)
plot(price, quantity, xlim = c(0, 125), ylim = c(0, 60), pch = 19)
abline(reg, col = "red")

# Sums of squares used on the slides
Sxx <- sum((price - mean(price))^2)                         # 1500
Sxy <- sum((price - mean(price)) * (quantity - mean(quantity)))  # -670
Syy <- sum((quantity - mean(quantity))^2)                   # 316

# Leverage values h_i = 1/n + (x_i - xbar)^2 / Sxx
hatvalues(reg)                       # 0.378 (ends) ... 0.111 (centre)
4 / n; 6 / n                         # rules of thumb 0.444, 0.667

# Exercise "least squares by hand"
xe <- c(1, 2, 3, 4, 5); ye <- c(3, 4, 2, 5, 6)
coef(lm(ye ~ xe))                    # 1.9, 0.7

# =====================================================================
# 3 Goodness of fit
# =====================================================================
TSS <- sum((quantity - mean(quantity))^2)          # 316
RSS <- sum(resid(reg)^2)                           # 16.7333
ESS <- sum((fitted(reg) - mean(quantity))^2)       # 299.2667
1 - RSS / TSS                                      # R^2 = 0.9470
summary(reg)$r.squared
cor(price, quantity)^2

# =====================================================================
# 4 Residual analysis
# =====================================================================
plot(fitted(reg), resid(reg), xlab = "fitted values", ylab = "residuals",
     main = "Residual plot")
abline(h = 0, lty = 2)

qqplot(price, quantity)              # two empirical distributions
qqline(quantity, distribution = function(p) quantile(price, prob = p), lty = 2)

qqnorm(resid(reg))                   # residuals vs. normal distribution
qqline(resid(reg))
# plotting positions and normal quantiles of the table on the slides
u <- sort(resid(reg)); p <- (1:n - 0.5) / n
cbind(u, p, z = qnorm(p))

# Exercise body heights (k) -- shoe sizes (s)
k <- c(164, 162, 168, 198, 166, 166, 192, 160, 151, 175, 180, 160, 168, 175, 168)
s <- c(39, 38, 39, 46, 40, 39, 45, 37, 36, 42, 43, 38, 41, 40, 39)
cov(k, s); cor(k, s)                 # 33.6857, 0.9684
reg_ks <- lm(s ~ k)
coef(reg_ks)                         # 2.3147, 0.2222
summary(reg_ks)$r.squared            # 0.9379
plot(k, s); abline(reg_ks)
plot(fitted(reg_ks), resid(reg_ks)); abline(h = 0, lty = 2)
qqnorm(resid(reg_ks)); qqline(resid(reg_ks))

# =====================================================================
# 5 Inference in simple regression
# =====================================================================
summary(reg)                         # estimates, SE, t, p, R^2, F
(sigma_hat <- sqrt(RSS / (n - 2)))   # residual standard error 1.5461
(se_b1 <- sigma_hat / sqrt(Sxx))     # 0.03992
(se_b0 <- sigma_hat * sqrt(1 / n + mean(price)^2 / Sxx))  # 4.0252

# t-test H0: beta1 = 0
(T <- beta1 / se_b1)                 # -11.19
qt(0.975, df = n - 2)                # 2.3646
2 * pt(-abs(T), df = n - 2)          # p-value 1.0e-05
# one-sided H1: beta1 < 0
qt(0.95, df = n - 2)                 # 1.8946
pt(T, df = n - 2)                    # p-value 5.1e-06
# H0: beta1 = -0.5
(T2 <- (beta1 - (-0.5)) / se_b1)     # 1.336
2 * pt(-abs(T2), df = n - 2)         # 0.223

# confidence intervals
confint(reg)                         # beta1: [-0.5411, -0.3523]
beta1 + c(-1, 1) * qt(0.975, n - 2) * se_b1

# F-statistic = T^2 in simple regression
T^2                                  # 125.2

# prediction: confidence vs. prediction interval
new <- data.frame(price = c(100, 110, 125))
predict(reg, new, interval = "confidence")
predict(reg, new, interval = "prediction")

# Exercise: inference for the shoe-size regression
summary(reg_ks)
confint(reg_ks)                      # [0.1879, 0.2565]
qt(0.975, df = 13)                   # 2.1604
(T3 <- (coef(reg_ks)[2] - 0.25) / sqrt(vcov(reg_ks)[2, 2]))  # -1.75
2 * pt(-abs(T3), df = 13)            # 0.103
predict(reg_ks, data.frame(k = 180), interval = "prediction")

# Exercise used cars from A to Z
age   <- 1:6
value <- c(19, 18, 17, 15, 12, 9)
car <- lm(value ~ age)
summary(car); confint(car)
predict(car, data.frame(age = 7), interval = "prediction")   # [4.21, 11.79]

# =====================================================================
# 6 Multiple linear regression
# =====================================================================
ad <- read.csv("../data/Advertising.csv", row.names = 1)
summary(lm(sales ~ TV, data = ad))
summary(lm(sales ~ radio, data = ad))$coefficients
summary(lm(sales ~ newspaper, data = ad))$coefficients

m3 <- lm(sales ~ TV + radio + newspaper, data = ad)
summary(m3)                          # R^2 0.897, F 570
confint(m3)
round(cor(ad), 4)                    # cor(radio, newspaper) = 0.354

# F-test by hand
TSS_ad <- sum((ad$sales - mean(ad$sales))^2)            # 5417.15
RSS_ad <- sum(resid(m3)^2)                               # 556.83
((TSS_ad - RSS_ad) / 3) / (RSS_ad / (200 - 3 - 1))       # 570.3
qf(0.95, 3, 196)                                         # 2.65

# dropping newspaper
m2 <- lm(sales ~ TV + radio, data = ad)
summary(m2)
anova(m2, m3)                        # partial F = 0.031, p = 0.86
predict(m2, data.frame(TV = 100, radio = 20), interval = "confidence")
predict(m2, data.frame(TV = 100, radio = 20), interval = "prediction")

# interaction (appendix A.2)
mi <- lm(sales ~ TV * radio, data = ad)
summary(mi)

# qualitative predictors (Credit data)
cr <- read.csv("../data/Credit.csv")
# Exercise "reading a multiple regression output" (Credit data)
mc <- lm(Balance ~ Income + Limit + Student, data = cr)
summary(mc); confint(mc)                      # Income: [-8.380, -7.424]
coef(lm(Balance ~ Income, data = cr))         # alone: +6.05 (confounding)
cor(cr$Income, cr$Limit)                      # 0.79
predict(mc, data.frame(Income = 50, Limit = 5000, Student = c("No", "Yes")),
        interval = "prediction")              # 510.3 [304.7, 715.8]; 937.3

summary(lm(Balance ~ Student, data = cr))$coefficients
summary(lm(Balance ~ Income + Student, data = cr))$coefficients
summary(lm(Balance ~ Region, data = cr))$coefficients   # baseline East

# =====================================================================
# Appendix A.3: Diagnostics in multiple regression
# =====================================================================
plot(fitted(m2), resid(m2)); abline(h = 0, lty = 2)    # curvature
plot(fitted(mi), resid(mi)); abline(h = 0, lty = 2)    # pattern gone

# collinearity: Limit and Rating
cor(cr$Limit, cr$Rating)                               # 0.997
summary(lm(Balance ~ Age + Limit + Rating, data = cr))$coefficients
summary(lm(Balance ~ Age + Limit, data = cr))$coefficients
# VIF_j = 1 / (1 - R^2_j), R^2_j from regressing x_j on the other predictors
vif <- function(x, others) {
  1 / (1 - summary(lm(reformulate(others, x), data = cr))$r.squared)
}
vif("Age", c("Limit", "Rating"))     # 1.01
vif("Limit", c("Age", "Rating"))     # 160.6
vif("Rating", c("Age", "Limit"))     # 160.7

# leverage rule in multiple regression: h_ii > 2(p+1)/n
h <- hatvalues(m2); sum(h > 2 * 3 / 200)
