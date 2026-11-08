# =====================================================================
# R code from: presentation_didaktisch.tex (Vorgängerfassung, dieser Ordner)
#   (Statistik für Ökonomen -- Teil 3: Regression, überarbeitete Fassung)
# Generated/updated on: 2026-10-28
#
# Description:
#   Dieses Skript enthält den gesamten R-Code, der in der didaktisch
#   überarbeiteten Beamer-Präsentation "Statistik für Ökonomen Teil 3"
#   (presentation_didaktisch.tex, 126 Folien inkl. Anhang) verwendet wird,
#   inkl. Beispieldaten, damit jeder Codeblock eigenständig lauffähig ist.
#   Zusätzlich werden die auf den Folien gezeigten Zahlen nachgerechnet
#   (Werbeaufwand/Umsatz, Übungsaufgabe, Sättigungsbeispiel, Bestimmtheits-
#   maß, Rechenabkürzungen, Übung Körpergröße/Schuhgröße, QQ-Plots).
#   Die Foliennummern sind die in der Fußzeile gedruckten Nummern dieser
#   Vorgängerfassung (nicht der Hauptfassung Statistik für Ökonomen Teil 3.tex).
#
#   Archiviert am 2026-11-06. Das Skript zur Hauptfassung liegt in
#   ../Statistik_für_Ökonomen_Teil_3.R, das zur ursprünglichen Fassung
#   (presentation.tex) unverändert in Statistik_für_Ökonomen_Teil_3.R (dieser Ordner).
#
# Overview (Folie -> Thema):
#   Folie  18 : Kovarianz und Korrelation mit R
#   Folien 20-44 : Beispiel Werbeaufwand/Umsatz (12 Filialen) nachrechnen
#   Folien 46-49 : Übungsaufgabe (5 Monate) nachrechnen
#   Folien 53-54 : Leuchte-Beispiel (Preis/Absatz) nachrechnen
#   Folie  55 : Lineare Regression mit R
#   Folien 56-59 : Übungsaufgabe Koeffizienten deuten, Prognosen, Einheiten (Möbelhaus)
#   Folien 63-75 : Residuenanalyse nachrechnen (Sättigung, Filialen, Übung)
#   Folie  73 : Residuenplot mit R erstellen
#   Folien 76-77 : Übungsaufgabe Residuenplots diagnostizieren (nur Grafiken, kein R-Code)
#   Folien 79-91 : Bestimmtheitsmaß nachrechnen
#   Folie  89 : Bestimmtheitsmaß von R ausgeben lassen
#   Folien 92-94 : Übungsaufgabe Quadratsummen, R^2 und r (Heizkosten)
#   Folien 96-101 : Umformungen (drei Summen, Verschiebungssatz)
#   Folien 102-107 : Übung Körpergröße / Schuhgröße
#   Folie 111 : Zusammenfassung -- Wichtige R-Befehle (1/2)
#   Folie 112 : Zusammenfassung -- Wichtige R-Befehle (2/2)
#   Anhang QQ-Plot:
#   Folien 116-118 : QQ-Plot zweier Stichproben (Folie 118: R)
#   Folien 119-121 : QQ-Plot der Residuen, Beispiel Leuchte
#   Folie 123 : QQ-Plot der Residuen gegen Normalverteilung in R
#   Folien 124-126 : Übung (Aufgabe 6) QQ-Plot Körpergröße / Schuhgröße
#
# Required R packages:
#   None (only base R: stats, graphics, grDevices).
#
# How to run:
#   Rscript Statistik_für_Ökonomen_Teil_3_didaktisch.R
#   ...or open in RStudio and step through section by section.
# =====================================================================


# =====================================================================
# Beispieldaten
# =====================================================================

# --- Preis-Absatz-Beispiel Leuchte (Folie 8, Folien 53-54) ------------
preis <- c( 80,  85,  90,  95, 100, 105, 110, 115, 120)
menge <- c( 20,  17,  15,   9,  11,   8,   4,   4,   2)
x     <- preis  # generische Aliase für die R-Folien
y     <- menge

# --- Werbeaufwand und Umsatz, 12 Filialen (Folie 20) ------------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 30 + 1,2 x)
werbung <- c( 1,  3,  4,  5,  6,  8,  8,  9, 10, 11, 12, 13)
umsatz  <- c(33, 30, 37, 33, 38, 41, 39, 43, 45, 40, 42, 47)

# --- Übungsaufgabe: Online-Shop, 5 Monate (Folie 46) ------------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 20 + 2 x)
werbung_ue <- c( 1,  2,  3,  4,  5)
umsatz_ue  <- c(21, 26, 24, 30, 29)

# --- Übungsbeispiel Körpergröße / Schuhgröße (Folie 102) ---------------
koerpergroesse <- c(164, 162, 168, 198, 166, 166, 192, 160, 151,
                    175, 180, 160, 168, 175, 168)
schuhgroesse   <- c( 39,  38,  39,  46,  40,  39,  45,  37,  36,
                     42,  43,  38,  41,  40,  39)

# --- Übungsaufgabe Möbelhaus: 6 Wochen (Folie 56) ---------------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 40 + 2,5 x)
werbung_mh <- c( 2,  4,  6,  8, 10, 12)
umsatz_mh  <- c(44, 49, 58, 62, 61, 71)

# --- Übungsaufgabe Heizkosten: 5 Wochen (Folie 92) --------------------
# (Außentemperatur in Grad C, Heizkosten in Euro je Tag;
#  KQ-Gerade exakt  yhat = 78 - 3 x;  SQT = 1000, SQE = 810, SQR = 190)
temp   <- c( 0,  3,  6,  9, 12)
kosten <- c(82, 65, 63, 41, 49)

# --- Sättigungsbeispiel: 10 Regionen (Folien 63, 70, 86) --------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 86/3 + 7/3 x)
werbung_s <- 1:10
umsatz_s  <- c(25, 32, 37, 41, 44, 46, 47, 48, 48, 47)

# Beispieldaten für die Zusammenfassung (Folie 111)
daten <- c(38, 39, 39, 39, 40, 40, 40, 41, 41, 41,
           42, 42, 42, 42, 43, 43, 44, 44, 45, 46)


# ---------------------------------------------------------------------
# FOLIE 18: "Kovarianz und Korrelation mit R"
# ---------------------------------------------------------------------

# Kovarianz
cov(x, y)

# Korrelationskoeffizient
cor(x, y)

# Nach Pearson (Standard)
cor(x, y, method = "pearson")

# --- end FOLIE 18 ---


# ---------------------------------------------------------------------
# FOLIEN 20-44: Beispiel Werbeaufwand/Umsatz nachrechnen
#   (Streudiagramm, Vergleichsgeraden A-D, Residuen, Residuensummen,
#    Residuenquadratsummen, KQ-Schätzer über Kovarianz und Varianz)
# ---------------------------------------------------------------------

# Streudiagramm (Folie 21)
plot(werbung, umsatz, xlim = c(0, 14), ylim = c(24, 52),
     xlab = "Werbeaufwand x (Tsd. Euro)", ylab = "Umsatz y (Tsd. Euro)",
     pch = 19, col = "blue")

# Die vier Kandidatengeraden der Folie 22
geraden <- data.frame(
  name = c("A (zu steil)", "B (zu flach)", "C (zu hoch)", "D (passt)"),
  b0   = c(24,   34.5, 35,  30),
  b1   = c(2,    0.6,  1.2, 1.2)
)
for (i in seq_len(nrow(geraden))) abline(geraden$b0[i], geraden$b1[i], col = "grey50")

# Residuensumme und Residuenquadratsumme je Gerade (Folien 31 und 34)
geraden$residuensumme <- NA
geraden$sqr           <- NA
for (i in seq_len(nrow(geraden))) {
  u <- umsatz - (geraden$b0[i] + geraden$b1[i] * werbung)
  geraden$residuensumme[i] <- sum(u)
  geraden$sqr[i]           <- sum(u^2)
}
geraden
#   A, B, D: Residuensumme 0 (alle drei verlaufen durch den Schwerpunkt),
#   C: -60; Residuenquadratsummen 164,0 / 120,6 / 364,8 / 64,8

# Residuen der Geraden D (Folien 28-29, 32)
u_D <- umsatz - (30 + 1.2 * werbung)
round(u_D, 1)        # 1,8  -3,6  2,2  -3,0  0,8  1,4  -0,6  2,2  3,0  -3,2  -2,4  1,4
round(u_D^2, 2)      # quadrierte Residuen
sum(u_D^2)           # 64,8

# KQ-Schätzer über Kovarianz und Varianz (Folien 40-44)
mean(werbung); mean(umsatz)                                  # 7,5 und 39
sum((werbung - mean(werbung)) * (umsatz - mean(umsatz)))     # 186
sum((werbung - mean(werbung))^2)                             # 155
cov(werbung, umsatz)                                         # 16,91 (= 186/11)
var(werbung)                                                 # 14,09 (= 155/11)
(beta1_w <- cov(werbung, umsatz) / var(werbung))             # 1,2
(beta0_w <- mean(umsatz) - beta1_w * mean(werbung))          # 30
coef(lm(umsatz ~ werbung))                                   # Kontrolle: 30 und 1,2

# --- end FOLIEN 20-44 ---


# ---------------------------------------------------------------------
# FOLIEN 46-49: Übungsaufgabe nachrechnen
# ---------------------------------------------------------------------

mean(werbung_ue); mean(umsatz_ue)                            # 3 und 26
cov(werbung_ue, umsatz_ue)                                   # 5   (= 20/4)
var(werbung_ue)                                              # 2,5 (= 10/4)
(beta1_ue <- cov(werbung_ue, umsatz_ue) / var(werbung_ue))   # 2
(beta0_ue <- mean(umsatz_ue) - beta1_ue * mean(werbung_ue))  # 20
reg_ue <- lm(umsatz_ue ~ werbung_ue)
coef(reg_ue)                                                 # 20 und 2
resid(reg_ue)                                                # -1  2  -2  2  -1
sum(resid(reg_ue)^2)                                         # 14
plot(werbung_ue, umsatz_ue, xlim = c(0, 6), ylim = c(16, 34),
     xlab = "Werbeaufwand x (Tsd. Euro)", ylab = "Umsatz y (Tsd. Euro)",
     pch = 19, col = "blue")
abline(reg_ue, col = "blue")

# --- end FOLIEN 46-49 ---


# ---------------------------------------------------------------------
# FOLIEN 53-54: Leuchte-Beispiel nachrechnen (Arbeitstabelle)
# ---------------------------------------------------------------------

mean(preis); mean(menge)                                     # 100 und 10
sum((preis - mean(preis)) * (menge - mean(menge)))           # -670
sum((preis - mean(preis))^2)                                 # 1500
cov(preis, menge)                                            # -83,75
var(preis)                                                   # 187,5

# --- end FOLIEN 53-54 ---


# ---------------------------------------------------------------------
# FOLIE 55: "Lineare Regression mit R"
# ---------------------------------------------------------------------

# --- Block 1: Koeffizienten manuell (Schritte 2 bis 5) ----------------
(beta1 <- cov(preis, menge) / var(preis))
(beta0 <- mean(menge) - beta1 * mean(preis))

# --- Block 2: Dasselbe mit der Funktion lm() --------------------------
reg <- lm(menge ~ preis)
coef(reg)                      # Achsenabschnitt und Steigung

# --- Block 3: Streuungsdiagramm mit Regressionsgeraden ---------------
plot(preis, menge, xlim = c(0, 125), ylim = c(0, 22))
abline(reg)

# --- end FOLIE 55 ---


# ---------------------------------------------------------------------
# FOLIEN 56-59: Übungsaufgabe Koeffizienten deuten und Prognosen ableiten
#   (Möbelhaus; Folie 59: "Kontrolle mit R")
# ---------------------------------------------------------------------

werbung <- werbung_mh; umsatz <- umsatz_mh
reg <- lm(umsatz ~ werbung)
coef(reg)                                            # 40.0   2.5
predict(reg, newdata = data.frame(werbung = c(5, 30)))   # 52.5 115.0
coef(lm(umsatz ~ I(1000 * werbung)))                 # 40.0000   0.0025
coef(lm(I(1000 * umsatz) ~ I(1000 * werbung)))       # 40000.0   2.5
resid(reg)                                           # -1 -1 3 2 -4 1 (bis +-4)
40 + 2.5 * c(4, 6, 10, 12)                           # 50 55 65 70 (Folie 57)

# --- end FOLIEN 56-59 ---


# ---------------------------------------------------------------------
# FOLIEN 63-75: Residuenanalyse nachrechnen
# ---------------------------------------------------------------------

# Sättigungsbeispiel (Folien 63, 70): Gerade passt rechnerisch, aber Bogen
reg_s <- lm(umsatz_s ~ werbung_s)
coef(reg_s)                                   # 28,67 und 2,33 (= 86/3, 7/3)
round(resid(reg_s), 2)                        # -6 -1,33 1,33 3 3,67 3,33 2 0,67 -1,67 -5
summary(reg_s)$r.squared                      # 0,81 (Folie 86)
plot(fitted(reg_s), resid(reg_s), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)

# Filialen (Folien 66, 71): Residuenplot zu  yhat = 30 + 1,2 x
reg_w <- lm(umsatz ~ werbung)
cbind(yhat = fitted(reg_w), u = round(resid(reg_w), 1))
plot(fitted(reg_w), resid(reg_w), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)

# Übungsaufgabe (Folien 74-75): Residuenplot zu  yhat = 20 + 2 x
cbind(yhat = fitted(reg_ue), u = resid(reg_ue))   # 22..30 und -1 2 -2 2 -1
plot(fitted(reg_ue), resid(reg_ue), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)

# --- end FOLIEN 63-75 ---


# ---------------------------------------------------------------------
# FOLIE 73: "Residuenplot mit R erstellen"
# ---------------------------------------------------------------------

# --- Block 1: R-Befehle (Beispiel Leuchte) ----------------------------
reg <- lm(menge ~ preis)
plot(fitted(reg), resid(reg),
     xlab = "angepasste Werte", ylab = "Residuen", main = "Residuenplot")
abline(h = 0, lty = 2)                  # Nulllinie als Orientierung

# --- Block 2: Kontrolle -----------------------------------------------
sum(resid(reg))      # praktisch 0 (Rundung): Bedingung erster Ordnung

# --- end FOLIE 73 ---


# ---------------------------------------------------------------------
# FOLIEN 79-91: Bestimmtheitsmaß nachrechnen
# ---------------------------------------------------------------------

# Filialen (Folien 79-83, 85): SQT = SQE + SQR
SQT_w <- sum((umsatz - mean(umsatz))^2)              # 288
SQE_w <- sum((fitted(reg_w) - mean(umsatz))^2)       # 223,2
SQR_w <- sum(resid(reg_w)^2)                         # 64,8
c(SQT_w, SQE_w, SQR_w, SQE_w + SQR_w)
SQE_w / SQT_w                                        # R^2 = 0,775
cor(werbung, umsatz)^2                               # 0,775 (r = 0,8803)

# Filiale 12 (Folie 80): 8 = 6,6 + 1,4
c(umsatz[12] - mean(umsatz), fitted(reg_w)[12] - mean(umsatz), resid(reg_w)[12])

# Leuchte (Folie 88)
SQT_l <- sum((menge - mean(menge))^2)                # 316
SQR_l <- sum(resid(reg)^2)                           # 16,73
1 - SQR_l / SQT_l                                    # 0,9470

# Übungsaufgabe (Folien 90-91)
SQT_ue <- sum((umsatz_ue - mean(umsatz_ue))^2)       # 54
SQR_ue <- sum(resid(reg_ue)^2)                       # 14
1 - SQR_ue / SQT_ue                                  # 0,741 (= 40/54)

# --- end FOLIEN 79-91 ---


# ---------------------------------------------------------------------
# FOLIEN 92-94: Übungsaufgabe Von den Quadratsummen zum
#   Korrelationskoeffizienten (Heizkosten; Folie 94: "Mit R")
# ---------------------------------------------------------------------

reg <- lm(kosten ~ temp)
coef(reg)                   # 78 und -3
summary(reg)                # Zeile "Multiple R-squared:  0.81"
summary(reg)$r.squared      # 0.81
cor(temp, kosten)           # -0.9
sum(resid(reg)^2)           # 190  (SQR)
sum((kosten - mean(kosten))^2)              # 1000 (SQT)
sum((fitted(reg) - mean(kosten))^2)         # 810  (SQE = (-3)^2 * 90)
sum((temp - mean(temp))^2)                  # 90

# --- end FOLIEN 92-94 ---


# ---------------------------------------------------------------------
# FOLIE 89: "Bestimmtheitsmaß von R ausgeben lassen"
# ---------------------------------------------------------------------

# --- Block 1: Komplette Ausgabe ---------------------------------------
reg <- lm(menge ~ preis)
summary(reg)               # Zeile "Multiple R-squared: 0.947"

# --- Block 2: Drei Wege zum selben Wert -------------------------------
summary(reg)$r.squared                                   # direkt
1 - sum(resid(reg)^2) / sum((menge - mean(menge))^2)     # 1 - SQR/SQT
cor(preis, menge)^2                                      # r^2 (Einfachregression)

# --- end FOLIE 89 ---


# ---------------------------------------------------------------------
# FOLIEN 96-101: Umformungen -- alles aus drei Summen
# ---------------------------------------------------------------------

SP_xy <- sum((werbung - mean(werbung)) * (umsatz - mean(umsatz)))   # 186
SQ_x  <- sum((werbung - mean(werbung))^2)                           # 155
SQ_y  <- sum((umsatz - mean(umsatz))^2)                             # 288
SP_xy / SQ_x                       # beta1 = 1,2
SP_xy / sqrt(SQ_x * SQ_y)          # r = 0,8803
SP_xy^2 / (SQ_x * SQ_y)            # R^2 = 0,775
(SP_xy / SQ_x) * SP_xy             # SQE = 223,2
SQ_y - (SP_xy / SQ_x) * SP_xy      # SQR = 64,8
(SP_xy / SQ_x) * sqrt(SQ_x / SQ_y) # r als standardisierte Steigung (Folie 101)

# Verschiebungssatz (Folie 100), Probe am Online-Shop
n_ue <- length(werbung_ue)
sum(werbung_ue * umsatz_ue) - n_ue * mean(werbung_ue) * mean(umsatz_ue)   # 20
sum(werbung_ue^2) - n_ue * mean(werbung_ue)^2                            # 10
sum(umsatz_ue^2)  - n_ue * mean(umsatz_ue)^2                             # 54

# --- end FOLIEN 96-101 ---


# ---------------------------------------------------------------------
# FOLIEN 102-107: Übung Körpergröße / Schuhgröße
# ---------------------------------------------------------------------

k <- koerpergroesse; s <- schuhgroesse; n_k <- length(k)
c(sum(k), sum(s), sum(k * s), sum(k^2), sum(s^2))   # Hilfssummen (Folie 102)
mean(k); mean(s)                                    # 170,2 und 40,13
SP_ks <- sum(k * s) - sum(k) * sum(s) / n_k         # 471,6
SQ_k  <- sum(k^2) - sum(k)^2 / n_k                  # 2122,4
SQ_s  <- sum(s^2) - sum(s)^2 / n_k                  # 111,73
cov(k, s); cor(k, s)                                # 33,69 und 0,9684
reg_k <- lm(s ~ k)
coef(reg_k)                                         # 2,3147 und 0,2222
plot(k, s, xlab = "Körpergröße k (cm)", ylab = "Schuhgröße s", pch = 19)
abline(reg_k)
round(resid(reg_k), 4)                              # zwischen -1,20 und 1,36
plot(fitted(reg_k), resid(reg_k), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)
summary(reg_k)$r.squared                            # 0,9379

# --- end FOLIEN 102-107 ---


# ---------------------------------------------------------------------
# FOLIE 111: "Zusammenfassung: Wichtige R-Befehle (1/2)"
# ---------------------------------------------------------------------

# --- Block 1: Grafische Darstellungen ---------------------------------
plot(ecdf(daten))                   # Empirische VF
hist(daten, freq = FALSE)           # Histogramm (Dichte)
hist(daten, breaks = c(37, 39, 41, 43, 45, 47))   # Eigene Klassen
# Hinweis: Auf der Folie stehen nur drei Klassengrenzen c(37, 39, 41);
#   damit lägen aber Werte > 41 außerhalb. Hier wurden die Grenzen auf
#   den vollen Datenbereich erweitert, damit der Plot funktioniert.
boxplot(daten)                      # Boxplot

# --- Block 2: Kovarianz und Korrelation -------------------------------
cov(x, y)                          # Kovarianz
cor(x, y)                          # Korrelationskoeffizient

# --- end FOLIE 111 ---


# ---------------------------------------------------------------------
# FOLIE 112: "Zusammenfassung: Wichtige R-Befehle (2/2)"
# ---------------------------------------------------------------------

# --- Block 1: Regression ----------------------------------------------
reg <- lm(y ~ x)                   # Lineares Modell
summary(reg)                        # Ergebnisse inkl. R^2

# --- Block 2: Modelldiagnostik ----------------------------------------
plot(fitted(reg), resid(reg))       # Residuenplot
abline(h = 0, col = "red")          # Nulllinie
qqnorm(resid(reg))                  # QQ-Plot
qqline(resid(reg))                  # Referenzlinie

# --- end FOLIE 112 ---


# =====================================================================
# ANHANG: QQ-Plot
# =====================================================================

# ---------------------------------------------------------------------
# FOLIEN 116-118: QQ-Plot zweier Stichproben (Folie 118: "QQ-Plot zweier
#   Stichproben mit R")
# ---------------------------------------------------------------------

sort(preis); sort(menge)                 # getrennt sortiert (Folie 116)
quantile(preis, c(0.25, 0.75))           # 90 und 110
quantile(menge, c(0.25, 0.75))           # 4 und 15  -> Gerade y = -45,5 + 0,55 x

# --- Block 1: QQ-Plot zeichnen ----------------------------------------
qqplot(preis, menge)

# --- Block 2: Referenzgerade durch die Quartile -----------------------
qqline(menge,
       distribution = function(p) quantile(preis, prob = p),
       lty = 2)

# --- end FOLIEN 116-118 ---


# ---------------------------------------------------------------------
# FOLIEN 119-121: QQ-Plot der Residuen, Beispiel Leuchte
# ---------------------------------------------------------------------

reg <- lm(menge ~ preis)
u_sort <- sort(resid(reg))
p_i    <- (seq_along(u_sort) - 0.5) / length(u_sort)
z_i    <- qnorm(p_i)
round(cbind(u_sort, p_i, z_i), 4)        # Tabelle Folie 120
qnorm(c(0.1, 0.3, 0.5, 0.7, 0.9))        # n = 5: -1,28 -0,52 0 0,52 1,28 (Folie 119)
plot(z_i, u_sort, xlab = "theoretische Quantile", ylab = "sortierte Residuen")
qqline(resid(reg), lty = 2)              # 0,5833 + 0,5189 z (Folie 121)

# --- end FOLIEN 119-121 ---


# ---------------------------------------------------------------------
# FOLIE 123: "QQ-Plot der Residuen gegen die Normalverteilung in R"
# ---------------------------------------------------------------------

# --- Block 1: QQ-Plot erzeugen ----------------------------------------
reg <- lm(menge ~ preis)
qqnorm(resid(reg))

# --- Block 2: Referenzgerade durch die Quartile -----------------------
qqline(resid(reg))

# --- end FOLIE 123 ---


# ---------------------------------------------------------------------
# FOLIEN 124-126: Übung (Aufgabe 6) QQ-Plot Körpergröße / Schuhgröße
# ---------------------------------------------------------------------

u_k <- sort(resid(reg_k))
round(cbind(u_k, p = (1:15 - 0.5) / 15, z = qnorm((1:15 - 0.5) / 15)), 4)  # Folie 125
qqnorm(resid(reg_k))
qqline(resid(reg_k))                     # -0,0056 + 0,7002 z (Folie 126)

# --- end FOLIEN 124-126 ---
