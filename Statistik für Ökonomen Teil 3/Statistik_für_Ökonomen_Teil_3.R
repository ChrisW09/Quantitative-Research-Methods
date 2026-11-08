# =====================================================================
# R code from: Statistik für Ökonomen Teil 3.tex
#   (Statistik für Ökonomen -- Teil 3: Regression, Hauptfassung seit 2026-11-06)
# Generated/updated on: 2026-11-06
#
# Description:
#   Dieses Skript enthält den gesamten R-Code, der in der Beamer-Präsentation
#   "Statistik für Ökonomen Teil 3" (136 Folien inkl. Anhang) verwendet wird,
#   inkl. Beispieldaten, damit jeder Codeblock eigenständig lauffähig ist.
#   Zusätzlich werden die auf den Folien gezeigten Zahlen nachgerechnet:
#   Leuchte, zwölf Filialen, die durchgehende Übung Online-Shop (1)-(9) mit
#   den Zusatzübungen (A) und (B), Möbelhaus, Heizkosten, Körper-/Schuhgröße
#   (Aufgaben 1-6), Sättigungsbeispiel, Residuenplots und QQ-Plots.
#   Die Foliennummern sind die in der Fußzeile gedruckten Nummern
#   (Frame-Nummern; das PDF hat wegen Überblendungen 171 Seiten).
#   Abschnitte mit "(R-Code der Folie)" geben den Code der Folie wörtlich wieder.
#
#   Ältere Fassungen in old_versions/: Statistik_für_Ökonomen_Teil_3_didaktisch.R
#   (Vorgängerfassung presentation_didaktisch.tex, 126 Folien) und
#   Statistik_für_Ökonomen_Teil_3.R (ursprüngliche Fassung presentation.tex).
#
# Overview (Folie -> Thema):
#   Folien  8-13  : Leuchte: Streuungsdiagramm und Kovarianz
#   Folien 14-15  : Übung Online-Shop (1): Streuungsdiagramm und Kovarianz
#   Folien 16-17  : Korrelationskoeffizient, Beispiel Leuchte
#   Folien 18-19  : Übung Online-Shop (2): Korrelationskoeffizient
#   Folie  21     : Kovarianz und Korrelation mit R (R-Code der Folie)
#   Folien 23-40  : Zwölf Filialen: Geraden A-D, Residuen, Quadratsummen, KQ-Schätzer
#   Folien 27-28  : Übung Online-Shop (3): Residuen zweier Geraden, beide
#                   mit Summe 0
#   Folien 29-30  : Übung Online-Shop (4): Residuen quadrieren
#   Folien 41-43  : Übung Online-Shop (5): Die KQ-Gerade für einen zweiten Shop
#   Folie  47     : Leuchte: KQ-Gerade und Prognose
#   Folie  49     : Lineare Regression mit R (R-Code der Folie)
#   Folien 50-53  : Übung Möbelhaus (Folie 53: Kontrolle mit R)
#   Folien 55-61  : Streuungszerlegung und Bestimmtheitsmaß (Filialen)
#   Folien 58-59  : Übung Online-Shop (6): Die Streuungszerlegung nachrechnen
#   Folien 63-65  : R^2 = r^2 (Filialen), Leuchte, Sättigungsbeispiel
#   Folien 67-68  : Übung Online-Shop (7): Bestimmtheitsmaß
#   Folie  69     : Bestimmtheitsmaß von R ausgeben lassen (R-Code der Folie)
#   Folien 70-72  : Übung Heizkosten (Folie 72: Kontrolle mit R)
#   Folien 74-78  : Übung Körpergröße und Schuhgröße, Aufgaben 1-4
#   Folien 82-83  : Zusammenfassung: Wichtige R-Befehle (R-Code der Folien)
#   Anhang:
#   Folien 85-93  : Herleitung; Folien 90-91 Zusatzübung Online-Shop (A)
#   Folien 94-100 : Rechenabkürzung -- drei Summen; Folien 98-99 Zusatzübung (B)
#   Folien 101-121: Residuenanalyse (Sättigung, Online-Shop (8), Filialen,
#                   Leuchte, Folie 115 R-Code, Körpergröße Aufgabe 5)
#   Folien 122-136: QQ-Plot (Folie 126 und 133 R-Code, Leuchte,
#                   Online-Shop (9), Körpergröße Aufgabe 6)
#
# Required R packages:
#   None (only base R: stats, graphics, grDevices).
#
# How to run:
#   Rscript Statistik_für_Ökonomen_Teil_3.R
#   ...or open in RStudio and step through section by section.
# =====================================================================


# =====================================================================
# Beispieldaten
# =====================================================================

# --- Preis-Absatz-Beispiel Leuchte (Folie 8) --------------------------
preis <- c( 80,  85,  90,  95, 100, 105, 110, 115, 120)
menge <- c( 20,  17,  15,   9,  11,   8,   4,   4,   2)

# --- Durchgehende Übung Online-Shop, 5 Monate (Folie 14) ---------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 20 + 2 x)
werbung_os <- c( 1,  2,  3,  4,  5)
umsatz_os  <- c(21, 26, 24, 30, 29)

# --- Übung Online-Shop (5): zweiter Shop, 5 Monate (Folie 41) ----------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 6 + 3 x)
werbung_b <- c( 2,  4,  5,  6,  8)
umsatz_b  <- c(12, 20, 19, 23, 31)

# --- Werbeaufwand und Umsatz, zwölf Filialen (Folie 23) ----------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 30 + 1,2 x)
werbung_fil <- c( 1,  3,  4,  5,  6,  8,  8,  9, 10, 11, 12, 13)
umsatz_fil  <- c(33, 30, 37, 33, 38, 41, 39, 43, 45, 40, 42, 47)

# --- Übung Möbelhaus, 6 Wochen (Folie 50) ------------------------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 40 + 2,5 x)
werbung_mh <- c( 2,  4,  6,  8, 10, 12)
umsatz_mh  <- c(44, 49, 58, 62, 61, 71)

# --- Übung Heizkosten, 5 Wochen (Folie 70) -----------------------------
# (Außentemperatur in Grad C, Heizkosten in Euro je Tag;
#  KQ-Gerade exakt  yhat = 78 - 3 x;  SQT = 1000, SQE = 810, SQR = 190)
temp   <- c( 0,  3,  6,  9, 12)
kosten <- c(82, 65, 63, 41, 49)

# --- Übung Körpergröße / Schuhgröße, 15 Personen (Folie 74) ------------
koerpergroesse <- c(164, 162, 168, 198, 166, 166, 192, 160, 151,
                    175, 180, 160, 168, 175, 168)
schuhgroesse   <- c( 39,  38,  39,  46,  40,  39,  45,  37,  36,
                     42,  43,  38,  41,  40,  39)

# --- Sättigungsbeispiel, 10 Regionen (Folien 65, 103) -----------------
# (jeweils in Tsd. Euro; KQ-Gerade exakt  yhat = 86/3 + 7/3 x)
werbung_s <- 1:10
umsatz_s  <- c(25, 32, 37, 41, 44, 46, 47, 48, 48, 47)


# ---------------------------------------------------------------------
# FOLIEN 8-13: Leuchte -- Streuungsdiagramm und Kovarianz
# ---------------------------------------------------------------------

plot(preis, menge, xlab = "Preis x (Euro)", ylab = "Absatzmenge y (Stück)",
     pch = 19)                                               # Folie 10
mean(preis); mean(menge)                                     # 100 und 10
sum((preis - mean(preis)) * (menge - mean(menge)))           # SP = -670 (Folie 13)
sum((preis - mean(preis))^2)                                 # SQx = 1500
sum((menge - mean(menge))^2)                                 # SQy = 316
cov(preis, menge)                                            # -83,75 (= -670/8)

# --- end FOLIEN 8-13 ---


# ---------------------------------------------------------------------
# FOLIEN 14-15: Übung Online-Shop (1) -- Streuungsdiagramm und Kovarianz
# ---------------------------------------------------------------------

plot(werbung_os, umsatz_os, xlim = c(0, 6), ylim = c(16, 34),
     xlab = "Werbeaufwand x (Tsd. Euro)", ylab = "Umsatz y (Tsd. Euro)",
     pch = 19, col = "blue")
mean(werbung_os); mean(umsatz_os)                                  # 3 und 26
sum((werbung_os - mean(werbung_os)) * (umsatz_os - mean(umsatz_os)))  # 20
cov(werbung_os, umsatz_os)                                         # 5 (= 20/4)

# --- end FOLIEN 14-15 ---


# ---------------------------------------------------------------------
# FOLIEN 16-17: Korrelationskoeffizient, Beispiel Leuchte
# ---------------------------------------------------------------------

var(preis); var(menge)                                       # 187,5 und 39,5
cov(preis, menge) / (sd(preis) * sd(menge))                  # -0,9732 (Folie 17)

# --- end FOLIEN 16-17 ---


# ---------------------------------------------------------------------
# FOLIEN 18-19: Übung Online-Shop (2) -- Korrelationskoeffizient
# ---------------------------------------------------------------------

sum((werbung_os - mean(werbung_os))^2)                       # SQx = 10
sum((umsatz_os - mean(umsatz_os))^2)                         # SQy = 54
sd(werbung_os); sd(umsatz_os)                                # 1,5811 und 3,6742
cor(werbung_os, umsatz_os)                                   # 0,8607: stark positiv

# --- end FOLIEN 18-19 ---


# ---------------------------------------------------------------------
# FOLIE 21: "Kovarianz und Korrelation mit R" (R-Code der Folie)
# ---------------------------------------------------------------------

preis <- c(80, 85, 90, 95, 100, 105, 110, 115, 120)
menge <- c(20, 17, 15,  9,  11,   8,   4,   4,   2)

plot(preis, menge)     # Streuungsdiagramm
cov(preis, menge)      # Kovarianz: -83.75
var(preis)             # Varianz: 187.5
cor(preis, menge)      # Korrelationskoeffizient: -0.9732

# --- end FOLIE 21 ---


# ---------------------------------------------------------------------
# FOLIEN 23-40: Zwölf Filialen -- Geraden A-D, Residuen,
#   Residuenquadratsummen, KQ-Schätzer über Kovarianz und Varianz
# ---------------------------------------------------------------------

# Streudiagramm (Folie 24)
plot(werbung_fil, umsatz_fil, xlim = c(0, 14), ylim = c(24, 52),
     xlab = "Werbeaufwand x (Tsd. Euro)", ylab = "Umsatz y (Tsd. Euro)",
     pch = 19, col = "blue")

# Die vier Kandidatengeraden der Folie 24
geraden <- data.frame(
  name = c("A", "B", "C", "D"),
  b0   = c(24,   34.5, 35,  30),
  b1   = c(2,    0.6,  1.2, 1.2)
)
for (i in seq_len(nrow(geraden))) abline(geraden$b0[i], geraden$b1[i], col = "grey50")

# Residuensumme und Residuenquadratsumme je Gerade
geraden$residuensumme <- NA
geraden$sqr           <- NA
for (i in seq_len(nrow(geraden))) {
  u <- umsatz_fil - (geraden$b0[i] + geraden$b1[i] * werbung_fil)
  geraden$residuensumme[i] <- sum(u)
  geraden$sqr[i]           <- sum(u^2)
}
geraden
#   A, B, D: Residuensumme 0 (alle drei verlaufen durch den Schwerpunkt
#   (7,5; 39), vgl. Folie 38), C: -60.  SQR: A 164,0 und D 64,8 (Folie 32);
#   B 120,6 und C 364,8 stehen nicht auf den Folien.

# Residuen der Geraden D (Folie 26: Filiale 9 mit Residuum 3)
u_D <- umsatz_fil - (30 + 1.2 * werbung_fil)
round(u_D, 1)        # 1,8  -3,6  2,2  -3,0  0,8  1,4  -0,6  2,2  3,0  -3,2  -2,4  1,4
sum(u_D)             # 0
sum(u_D^2)           # 64,8 (Folien 32-33)

# KQ-Schätzer über Kovarianz und Varianz (Folien 37-39)
mean(werbung_fil); mean(umsatz_fil)                                   # 7,5 und 39
sum((werbung_fil - mean(werbung_fil)) * (umsatz_fil - mean(umsatz_fil)))  # SP = 186
sum((werbung_fil - mean(werbung_fil))^2)                              # SQx = 155
cov(werbung_fil, umsatz_fil)                                          # 16,91 (= 186/11)
var(werbung_fil)                                                      # 14,09 (= 155/11)
(beta1_fil <- cov(werbung_fil, umsatz_fil) / var(werbung_fil))        # 1,2
(beta0_fil <- mean(umsatz_fil) - beta1_fil * mean(werbung_fil))       # 30
beta0_fil + beta1_fil * 7                                             # 38,4 (Folien 38-39)
coef(lm(umsatz_fil ~ werbung_fil))                                    # Kontrolle: 30 und 1,2

# --- end FOLIEN 23-40 ---


# ---------------------------------------------------------------------
# FOLIEN 27-28: Übung Online-Shop (3) -- Residuen zweier Geraden
#   Gerade 1: 23 + x, Gerade 2: 20 + 2x; beide Summen sind 0
# ---------------------------------------------------------------------

23 + 1 * werbung_os                          # Gerade 1: 24 25 26 27 28
(u_1 <- umsatz_os - (23 + 1 * werbung_os))   # -3  1  -2  3  1
20 + 2 * werbung_os                          # Gerade 2: 22 24 26 28 30
(u_2 <- umsatz_os - (20 + 2 * werbung_os))   # -1  2  -2  2  -1
c(sum(u_1), sum(u_2))                        # 0 und 0 -- obwohl Gerade 2 sichtbar besser passt

# Hintergrund (vgl. Folie 38): Jede Gerade durch den Schwerpunkt
#   (x-quer; y-quer) = (3; 26) hat die Residuensumme 0, z. B. auch 26 und 29 - x.
c(mean(werbung_os), mean(umsatz_os))         # 3 und 26
23 + 1 * 3; 20 + 2 * 3                       # beide 26: beide Geraden gehen hindurch
c(sum(umsatz_os - 26), sum(umsatz_os - (29 - werbung_os)))   # 0 und 0

# --- end FOLIEN 27-28 ---


# ---------------------------------------------------------------------
# FOLIEN 29-30: Übung Online-Shop (4) -- Residuen quadrieren
# ---------------------------------------------------------------------

u_1^2                                        # 9 1 4 9 1
u_2^2                                        # 1 4 4 4 1
c(S1 = sum(u_1^2), S2 = sum(u_2^2))          # 24 und 14: Gerade 2 hat die kleinere Summe

# --- end FOLIEN 29-30 ---


# ---------------------------------------------------------------------
# FOLIEN 41-43: Übung Online-Shop (5) -- Die KQ-Gerade für einen zweiten Shop
# ---------------------------------------------------------------------

# a) Arbeitstabelle (Folie 42)
mean(werbung_b); mean(umsatz_b)                              # 5 und 21
werbung_b - mean(werbung_b)                                  # -3 -1  0  1  3
umsatz_b - mean(umsatz_b)                                    # -9 -1 -2  2 10
(SP_b <- sum((werbung_b - mean(werbung_b)) * (umsatz_b - mean(umsatz_b))))  # 60
(SQ_b <- sum((werbung_b - mean(werbung_b))^2))               # 20

# b) KQ-Schätzer: yhat = 6 + 3 x; c) +1 Tsd. Euro Werbung: +3 Tsd. Euro Umsatz
(beta1_b <- SP_b / SQ_b)                                     # 3
(beta0_b <- mean(umsatz_b) - beta1_b * mean(werbung_b))      # 6
reg_b <- lm(umsatz_b ~ werbung_b)
coef(reg_b)                                                  # Kontrolle: 6 und 3

# d) angepasste Werte und Residuen (Folie 43)
fitted(reg_b)                                                # 12 18 21 24 30
round(resid(reg_b), 10)                                      # 0  2  -2  -1  1
round(sum(resid(reg_b)), 10)                                 # 0

# e) Grafik wie Folie 43
plot(werbung_b, umsatz_b, xlim = c(0, 9), ylim = c(4, 34),
     xlab = "Werbeaufwand x (Tsd. Euro)", ylab = "Umsatz y (Tsd. Euro)",
     pch = 19, col = "blue")
abline(reg_b, col = "blue")
points(mean(werbung_b), mean(umsatz_b), pch = 4)            # Schwerpunkt (5; 21)

# Zum Vergleich (Folie 43): der erste Shop -- die KQ-Gerade ist Gerade 2
var(werbung_os)                                              # 2,5 (= 10/4)
(beta1_os <- cov(werbung_os, umsatz_os) / var(werbung_os))   # 2  (= 20/10)
(beta0_os <- mean(umsatz_os) - beta1_os * mean(werbung_os))  # 20
reg_os <- lm(umsatz_os ~ werbung_os)
coef(reg_os)                                                 # 20 und 2
all.equal(unname(resid(reg_os)), u_2)                        # TRUE: die KQ-Gerade ist Gerade 2
sum(resid(reg_os)^2)                                         # 14 < 24 (Übung (4))

# --- end FOLIEN 41-43 ---


# ---------------------------------------------------------------------
# FOLIE 47: Leuchte -- KQ-Gerade und Prognose
# ---------------------------------------------------------------------

(beta1_l <- cov(preis, menge) / var(preis))                  # -0,4467
(beta0_l <- mean(menge) - beta1_l * mean(preis))             # 54,67
10 * beta1_l                                                 # -4,47: rund -4,5 Stück je +10 Euro
beta0_l + beta1_l * 98                                       # 10,89 Stück bei 98 Euro

# --- end FOLIE 47 ---


# ---------------------------------------------------------------------
# FOLIE 49: "Lineare Regression mit R" (R-Code der Folie)
# ---------------------------------------------------------------------

# --- Block 1: Koeffizienten manuell (Schritte 2 bis 5) ----------------
(beta1 <- cov(preis, menge) / var(preis))
(beta0 <- mean(menge) - beta1 * mean(preis))

# --- Block 2: Dasselbe mit der Funktion lm() --------------------------
reg <- lm(menge ~ preis)
coef(reg)                      # Achsenabschnitt und Steigung

# --- Block 3: Streuungsdiagramm mit Regressionsgeraden ---------------
plot(preis, menge, xlim = c(0, 125), ylim = c(0, 60))
abline(reg)

# --- end FOLIE 49 ---


# ---------------------------------------------------------------------
# FOLIEN 50-53: Übung Möbelhaus -- Koeffizienten deuten und
#   Prognosen ableiten (Folie 53: "Kontrolle mit R", R-Code der Folie)
# ---------------------------------------------------------------------

werbung <- c(2, 4, 6, 8, 10, 12); umsatz <- c(44, 49, 58, 62, 61, 71)
reg <- lm(umsatz ~ werbung)
coef(reg)                                            # 40.0   2.5
predict(reg, newdata = data.frame(werbung = c(5, 30)))   # 52.5 115.0
coef(lm(umsatz ~ I(1000 * werbung)))                 # 40.0000   0.0025

# Zusätzlich nachgerechnet
40 + 2.5 * c(4, 6, 10, 12)                           # 50 55 65 70 (Folie 51 c)
coef(lm(I(1000 * umsatz) ~ I(1000 * werbung)))       # 40000.0   2.5 (Folie 53 d)
resid(reg)                                           # -1 -1 3 2 -4 1 (bis +-4)

# --- end FOLIEN 50-53 ---


# ---------------------------------------------------------------------
# FOLIEN 55-61: Streuungszerlegung und Bestimmtheitsmaß (Filialen)
# ---------------------------------------------------------------------

reg_fil <- lm(umsatz_fil ~ werbung_fil)
SQT_fil <- sum((umsatz_fil - mean(umsatz_fil))^2)            # 288
SQE_fil <- sum((fitted(reg_fil) - mean(umsatz_fil))^2)       # 223,2
SQR_fil <- sum(resid(reg_fil)^2)                             # 64,8
c(SQT_fil, SQE_fil, SQR_fil, SQE_fil + SQR_fil)              # SQT = SQE + SQR (Folie 57)
SQE_fil / SQT_fil                                            # R^2 = 0,775 (Folie 61)
1 - SQR_fil / SQT_fil                                        # dasselbe

# Filiale 12 (Folie 56): gesamt 8 = erklärt 6,6 + Residuum 1,4
c(gesamt   = umsatz_fil[12] - mean(umsatz_fil),
  erklaert = unname(fitted(reg_fil)[12]) - mean(umsatz_fil),
  residuum = unname(resid(reg_fil)[12]))

# --- end FOLIEN 55-61 ---


# ---------------------------------------------------------------------
# FOLIEN 58-59: Übung Online-Shop (6) -- Die Streuungszerlegung nachrechnen
# ---------------------------------------------------------------------

SQT_os <- sum((umsatz_os - mean(umsatz_os))^2)               # 54
SQE_os <- sum((fitted(reg_os) - mean(umsatz_os))^2)          # 40
SQR_os <- sum(resid(reg_os)^2)                               # 14
c(SQT_os, SQE_os + SQR_os)                                   # 54 = 40 + 14

# --- end FOLIEN 58-59 ---


# ---------------------------------------------------------------------
# FOLIEN 63-65: R^2 = r^2 (Filialen), Beispiel Leuchte, Sättigungsbeispiel
# ---------------------------------------------------------------------

# Filialen (Folie 63)
cor(werbung_fil, umsatz_fil)                                 # 0,8803
cor(werbung_fil, umsatz_fil)^2                               # 0,775 = R^2

# Leuchte (Folie 64)
reg_l <- lm(menge ~ preis)
SQT_l <- sum((menge - mean(menge))^2)                        # 316
SQE_l <- beta1_l * sum((preis - mean(preis)) * (menge - mean(menge)))   # 299,27
SQR_l <- sum(resid(reg_l)^2)                                 # 16,73
SQE_l / SQT_l                                                # 0,9470
cor(preis, menge)^2                                          # Kontrolle: (-0,9732)^2

# Sättigung (Folie 65, ausführlich im Anhang ab Folie 103):
#   R^2 = 0,81 -- und trotzdem gekrümmt
reg_s <- lm(umsatz_s ~ werbung_s)
summary(reg_s)$r.squared                                     # 0,81

# --- end FOLIEN 63-65 ---


# ---------------------------------------------------------------------
# FOLIEN 67-68: Übung Online-Shop (7) -- Bestimmtheitsmaß
# ---------------------------------------------------------------------

SQE_os / SQT_os                                              # 0,741 (= 40/54)
1 - SQR_os / SQT_os                                          # 0,741 (= 1 - 14/54)
cor(werbung_os, umsatz_os)^2                                 # 0,8607^2 = 0,741

# --- end FOLIEN 67-68 ---


# ---------------------------------------------------------------------
# FOLIE 69: "Bestimmtheitsmaß von R ausgeben lassen" (R-Code der Folie)
# ---------------------------------------------------------------------

# --- Block 1: Komplette Ausgabe ---------------------------------------
reg <- lm(menge ~ preis)
summary(reg)               # Zeile "Multiple R-squared: 0.947"

# --- Block 2: Drei Wege zum selben Wert -------------------------------
summary(reg)$r.squared                                   # direkt
1 - sum(resid(reg)^2) / sum((menge - mean(menge))^2)     # 1 - SQR/SQT
cor(preis, menge)^2                                      # r^2 (Einfachregression)

# --- end FOLIE 69 ---


# ---------------------------------------------------------------------
# FOLIEN 70-72: Übung Heizkosten -- Von den Quadratsummen zum
#   Korrelationskoeffizienten (Folie 72: "Mit R", R-Code der Folie)
# ---------------------------------------------------------------------

temp <- c(0, 3, 6, 9, 12); kosten <- c(82, 65, 63, 41, 49)
reg <- lm(kosten ~ temp)
summary(reg)                # Zeile "Multiple R-squared:  0.81"
summary(reg)$r.squared      # 0.81
cor(temp, kosten)           # -0.9
sum(resid(reg)^2)           # 190  (SQR)

# Zusätzlich nachgerechnet (Folien 71-72)
coef(reg)                                   # 78 und -3
sum((kosten - mean(kosten))^2)              # 1000 (SQT)
sum((fitted(reg) - mean(kosten))^2)         # 810  (SQE = (-3)^2 * 90)
sum((temp - mean(temp))^2)                  # 90

# --- end FOLIEN 70-72 ---


# ---------------------------------------------------------------------
# FOLIEN 74-78: Übung Körpergröße und Schuhgröße, Aufgaben 1-4
# ---------------------------------------------------------------------

k <- koerpergroesse; s <- schuhgroesse; n_k <- length(k)
c(sum(k), sum(s), sum(k * s), sum(k^2), sum(s^2))   # Hilfssummen (Folie 74):
                                                    # 2553 602 102932 436643 24272
plot(k, s, xlab = "Körpergröße k (cm)", ylab = "Schuhgröße s", pch = 19)  # Folie 75
mean(k); mean(s)                                    # 170,2 und 40,13 (Folie 75)
SP_ks <- sum(k * s) - sum(k) * sum(s) / n_k         # 471,6   (Folie 76)
SQ_k  <- sum(k^2) - sum(k)^2 / n_k                  # 2122,4
SQ_s  <- sum(s^2) - sum(s)^2 / n_k                  # 111,73
cov(k, s); cor(k, s)                                # 33,69 und 0,9684
reg_k <- lm(s ~ k)
coef(reg_k)                                         # 2,3147 und 0,2222 (Folie 77)
abline(reg_k)
(SQE_k <- coef(reg_k)[[2]] * SP_ks)                 # 104,79  (Folie 78)
SQ_s - SQE_k                                        # SQR = 6,94
summary(reg_k)$r.squared                            # 0,9379

# --- end FOLIEN 74-78 ---


# ---------------------------------------------------------------------
# FOLIE 82: "Zusammenfassung: Wichtige R-Befehle (1/2)" (R-Code der Folie)
# ---------------------------------------------------------------------

x <- werbung_os; y <- umsatz_os    # Beispieldaten: Online-Shop

# --- Block 1: Streuungsdiagramm ---------------------------------------
plot(x, y)                          # Streuungsdiagramm

# --- Block 2: Kovarianz, Varianz und Korrelation ----------------------
cov(x, y)                           # Kovarianz
var(x)                              # Varianz
cor(x, y)                           # Korrelationskoeffizient

# --- end FOLIE 82 ---


# ---------------------------------------------------------------------
# FOLIE 83: "Zusammenfassung: Wichtige R-Befehle (2/2)" (R-Code der Folie)
# ---------------------------------------------------------------------

# --- Block 1: Regression ----------------------------------------------
reg <- lm(y ~ x)                    # Lineares Modell
coef(reg)                           # Achsenabschnitt und Steigung
abline(reg)                         # Gerade ins Streuungsdiagramm
predict(reg, data.frame(x = 5))     # Prognose für x = 5
summary(reg)                        # Ergebnisse inkl. R²

# --- Block 2: Modelldiagnostik (Anhang) -------------------------------
plot(fitted(reg), resid(reg))       # Residuenplot
abline(h = 0, col = "red")          # Nulllinie
qqnorm(resid(reg))                  # QQ-Plot
qqline(resid(reg))                  # Referenzlinie

# --- end FOLIE 83 ---


# =====================================================================
# ANHANG: Herleitung und Rechenabkürzung
# =====================================================================

# ---------------------------------------------------------------------
# FOLIEN 90-91: Zusatzübung Online-Shop (A) -- Die Normalgleichungen lösen
# ---------------------------------------------------------------------

n_os <- length(werbung_os)
c(n_os, sum(werbung_os), sum(umsatz_os), sum(werbung_os^2),
  sum(werbung_os * umsatz_os))                       # 5 15 130 55 410
# I:  130 = 5 b0 + 15 b1      II: 410 = 15 b0 + 55 b1
solve(matrix(c(5, 15, 15, 55), nrow = 2), c(130, 410))   # b0 = 20, b1 = 2

# --- end FOLIEN 90-91 ---


# ---------------------------------------------------------------------
# FOLIEN 92-100: Verschiebungssatz und "Alle Kennzahlen aus drei Summen"
# ---------------------------------------------------------------------

# Verschiebungssatz (Folie 92), Probe am Online-Shop
sum(werbung_os * umsatz_os) - n_os * mean(werbung_os) * mean(umsatz_os)  # 20
sum(werbung_os^2) - n_os * mean(werbung_os)^2                            # 10
sum(umsatz_os^2)  - n_os * mean(umsatz_os)^2                             # 54

# Zwölf Filialen aus drei Summen (Folie 97)
SP_xy <- sum((werbung_fil - mean(werbung_fil)) * (umsatz_fil - mean(umsatz_fil)))  # 186
SQ_x  <- sum((werbung_fil - mean(werbung_fil))^2)                                  # 155
SQ_y  <- sum((umsatz_fil - mean(umsatz_fil))^2)                                    # 288
SP_xy / SQ_x                       # beta1 = 1,2
SP_xy / sqrt(SQ_x * SQ_y)          # r = 0,8803
SP_xy^2 / (SQ_x * SQ_y)            # R^2 = 0,775
(SP_xy / SQ_x) * SP_xy             # SQE = 223,2
SQ_y - (SP_xy / SQ_x) * SP_xy      # SQR = 64,8

# Zusatzübung Online-Shop (B), Folien 98-99: SQx = 10, SQy = 54, SPxy = 20
c(beta1 = 20 / 10, beta0 = 26 - 2 * 3, r = 20 / sqrt(10 * 54),
  R2 = 20^2 / (10 * 54), SQE = 2 * 20, SQR = 54 - 2 * 20)   # 2 20 0,8607 0,741 40 14

# Korrelation als standardisierte Steigung (Folie 100)
sqrt(SQ_x / SQ_y)                  # 0,7336
(SP_xy / SQ_x) * sqrt(SQ_x / SQ_y) # r = 1,2 * 0,7336 = 0,8803

# --- end FOLIEN 92-100 ---


# =====================================================================
# ANHANG: Residuenanalyse (Folien 101-121)
# =====================================================================

# ---------------------------------------------------------------------
# FOLIEN 103 und 112: Sättigungsbeispiel -- Gerade passt rechnerisch,
#   der Residuenplot zeigt einen Bogen
# ---------------------------------------------------------------------

coef(reg_s)                                   # 28,67 und 2,33 (= 86/3, 7/3)
round(resid(reg_s), 2)                        # -6 -1,33 1,33 3 3,67 3,33 2 0,67 -1,67 -5
plot(fitted(reg_s), resid(reg_s), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)

# --- end FOLIEN 103 und 112 ---


# ---------------------------------------------------------------------
# FOLIEN 108-109: Übung Online-Shop (8) -- Den Residuenplot zeichnen
# ---------------------------------------------------------------------

cbind(yhat = fitted(reg_os), u = resid(reg_os))   # (22; -1) (24; 2) (26; -2) (28; 2) (30; -1)
plot(fitted(reg_os), resid(reg_os), xlim = c(20, 32), ylim = c(-3, 3),
     xlab = "Angepasster Wert (Tsd. Euro)", ylab = "Residuum (Tsd. Euro)")
abline(h = 0, lty = 2)

# --- end FOLIEN 108-109 ---


# ---------------------------------------------------------------------
# FOLIEN 113-114: Residuenplots Filialen und Leuchte beurteilen
# ---------------------------------------------------------------------

# Filialen (Folie 113): keine Systematik, größtes |Residuum| = 3,6 (Filiale 2)
cbind(yhat = fitted(reg_fil), u = round(resid(reg_fil), 1))
plot(fitted(reg_fil), resid(reg_fil), xlab = "angepasste Werte", ylab = "Residuen")
abline(h = 0, lty = 2)

# Leuchte (Folie 114): Preis 95 Euro -- 9 statt 12,2 Stück
round(fitted(reg_l)[preis == 95], 1)          # 12,2
round(resid(reg_l), 2)

# --- end FOLIEN 113-114 ---


# ---------------------------------------------------------------------
# FOLIE 115: "Residuenplot mit R erstellen" (R-Code der Folie)
# ---------------------------------------------------------------------

# --- Block 1: R-Befehle (Beispiel Leuchte) ----------------------------
reg <- lm(menge ~ preis)
plot(fitted(reg), resid(reg),
     xlab = "angepasste Werte", ylab = "Residuen", main = "Residuenplot")
abline(h = 0, lty = 2)                  # Nulllinie als Orientierung

# --- Block 2: Kontrolle -----------------------------------------------
sum(resid(reg))      # praktisch 0 (Rundung): Eigenschaft der KQ-Geraden

# --- end FOLIE 115 ---


# ---------------------------------------------------------------------
# FOLIEN 118-120: Körper- und Schuhgröße, Aufgabe 5 -- Residuenplot
# ---------------------------------------------------------------------

round(cbind(k, s, s_hat = fitted(reg_k), u = resid(reg_k)), 2)   # Tabelle Folie 119
range(resid(reg_k))                         # -1,20 (Person 14) bis 1,36 (Person 13)
plot(fitted(reg_k), resid(reg_k), xlab = "angepasste Schuhgröße", ylab = "Residuen")
abline(h = 0, lty = 2)                      # Folie 120: keine Systematik

# --- end FOLIEN 118-120 ---


# =====================================================================
# ANHANG: QQ-Plot (Folien 122-136)
# =====================================================================

# ---------------------------------------------------------------------
# FOLIEN 124-125: QQ-Plot zweier Stichproben, Preise gegen Absatzmengen
# ---------------------------------------------------------------------

sort(preis); sort(menge)                 # getrennt sortiert (Folie 124)
quantile(preis, c(0.25, 0.75))           # 90 und 110
quantile(menge, c(0.25, 0.75))           # 4 und 15  -> Gerade y = -45,5 + 0,55 x (Folie 125)

# --- end FOLIEN 124-125 ---


# ---------------------------------------------------------------------
# FOLIE 126: "QQ-Plot zweier Stichproben mit R" (R-Code der Folie)
# ---------------------------------------------------------------------

# --- Block 1: QQ-Plot zeichnen ----------------------------------------
qqplot(preis, menge)

# --- Block 2: Referenzgerade durch die Quartile -----------------------
qqline(menge,
       distribution = function(p) quantile(preis, prob = p),
       lty = 2)

# --- end FOLIE 126 ---


# ---------------------------------------------------------------------
# FOLIEN 127-130: QQ-Plot der Residuen, Beispiel Leuchte
# ---------------------------------------------------------------------

qnorm(c(0.1, 0.3, 0.5, 0.7, 0.9))        # n = 5: -1,28 -0,52 0 0,52 1,28 (Folie 127)
u_sort <- sort(resid(reg_l))
p_i    <- (seq_along(u_sort) - 0.5) / length(u_sort)
z_i    <- qnorm(p_i)
round(cbind(u_sort, p_i, z_i), 4)        # Tabelle Folie 129
plot(z_i, u_sort, xlab = "theoretische Quantile", ylab = "sortierte Residuen")
qqline(resid(reg_l), lty = 2)            # 0,5833 + 0,5189 z (Folie 130)

# --- end FOLIEN 127-130 ---


# ---------------------------------------------------------------------
# FOLIEN 131-132: Übung Online-Shop (9) -- QQ-Plot der Residuen
# ---------------------------------------------------------------------

u_os <- sort(resid(reg_os))                                   # -2 -1 -1 2 2
round(cbind(u_os, p = (1:5 - 0.5) / 5, z = qnorm((1:5 - 0.5) / 5)), 4)   # Folie 132
q_u <- quantile(resid(reg_os), c(0.25, 0.75))                 # -1 und 2
(steigung_os <- diff(q_u) / diff(qnorm(c(0.25, 0.75))))       # 2,224
q_u[[1]] - steigung_os * qnorm(0.25)                          # 0,5 -> 0,5 + 2,224 z
plot(qnorm((1:5 - 0.5) / 5), u_os, xlab = "theoretische Quantile",
     ylab = "sortierte Residuen")
qqline(resid(reg_os), lty = 2)           # bei n = 5 kein Urteil möglich

# --- end FOLIEN 131-132 ---


# ---------------------------------------------------------------------
# FOLIE 133: "QQ-Plot der Residuen gegen die Normalverteilung in R"
#   (R-Code der Folie; für n <= 10 verwendet R p_i = (i - 3/8)/(n + 1/4))
# ---------------------------------------------------------------------

# --- Block 1: QQ-Plot erzeugen ----------------------------------------
reg <- lm(menge ~ preis)
qqnorm(resid(reg))

# --- Block 2: Referenzgerade durch die Quartile -----------------------
qqline(resid(reg))

# --- end FOLIE 133 ---


# ---------------------------------------------------------------------
# FOLIEN 134-136: Körper- und Schuhgröße, Aufgabe 6 -- QQ-Plot der Residuen
# ---------------------------------------------------------------------

u_k <- sort(resid(reg_k))
round(cbind(u_k, p = (1:15 - 0.5) / 15, z = qnorm((1:15 - 0.5) / 15)), 4)  # Folie 135
qqnorm(resid(reg_k))
qqline(resid(reg_k))                     # -0,0056 + 0,7002 z (Folie 136)

# --- end FOLIEN 134-136 ---
