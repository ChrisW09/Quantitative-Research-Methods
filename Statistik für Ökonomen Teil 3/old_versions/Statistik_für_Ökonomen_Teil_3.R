# =====================================================================
# R code from: presentation.tex
#   (Statistik für Ökonomen -- Teil 3: Regression)
# Generated/updated on: 2026-05-03
#
# Description:
#   Dieses Skript enthält den gesamten R-Code, der in der Beamer-
#   Präsentation "Statistik für Ökonomen Teil 3" verwendet wird,
#   inkl. Beispieldaten (Preis-Absatz-Beispiel und Übungsbeispiel
#   Körpergröße/Schuhgröße), damit jeder Codeblock eigenständig
#   lauffähig ist.
#
# Overview (Slide -> Topic):
#   Slide 18 : Kovarianz und Korrelation mit R
#   Slide 30 : Lineare Regression mit R
#   Slide 40 : Residuenplot mit R erstellen
#   Slide 45 : QQ-Plot mit R erzeugen
#   Slide 52 : QQ-Plot der Residuen gegen Normalverteilung in R
#   Slide 74 : Bestimmtheitsmaß von R ausgeben lassen
#   Slide 95 : Zusammenfassung -- Wichtige R-Befehle (1/2)
#   Slide 96 : Zusammenfassung -- Wichtige R-Befehle (2/2)
#
# Required R packages:
#   None (only base R: stats, graphics, grDevices).
#
# How to run:
#   Rscript presentation.R
#   ...or open in RStudio and step through section by section.
# =====================================================================


# =====================================================================
# Beispieldaten
# (nicht direkt aus einer Folie; werden gebraucht, damit die Code-
#  blöcke der Folien lauffähig sind)
# =====================================================================

# --- Preis-Absatz-Beispiel (Folie 7: "Regression -- ein Beispiel") ----
preis <- c( 80,  85,  90,  95, 100, 105, 110, 115, 120)
menge <- c( 20,  17,  15,   9,  11,   8,   4,   4,   2)
x     <- preis  # generische Aliase für die R-Folien
y     <- menge

# --- Übungsbeispiel Körpergröße / Schuhgröße (Folie 76) ---------------
koerpergroesse <- c(164, 162, 168, 198, 166, 166, 192, 160, 151,
                    175, 180, 160, 168, 175, 168)
schuhgroesse   <- c( 39,  38,  39,  46,  40,  39,  45,  37,  36,
                     42,  43,  38,  41,  40,  39)

# Beispieldaten für die Zusammenfassung (Folie 95)
daten <- c(38, 39, 39, 39, 40, 40, 40, 41, 41, 41,
           42, 42, 42, 42, 43, 43, 44, 44, 45, 46)


# ---------------------------------------------------------------------
# SLIDE 18: "Kovarianz und Korrelation mit R"
# Section: Regression
# Subsection: (vor Streuungsdiagramm/Kleinste-Quadrate)
# ---------------------------------------------------------------------

# Kovarianz
cov(x, y)

# Korrelationskoeffizient
cor(x, y)

# Nach Pearson (Standard)
cor(x, y, method = "pearson")


# --- end SLIDE 18 ---


# ---------------------------------------------------------------------
# SLIDE 30: "Lineare Regression mit R"
# Section: Regression
# Subsection: Kleinste-Quadrate-Schätzung
# ---------------------------------------------------------------------

# --- Block 1: Koeffizienten manuell -----------------------------------
(beta1 <- cov(preis, menge) / var(preis))
(beta0 <- mean(menge) - beta1 * mean(preis))

# --- Block 2: Korrelationskoeffizient (alternativ) --------------------
beta1 * sd(preis) / sd(menge)   # = cor(preis, menge)

# --- Block 3: Streuungsdiagramm mit Regressionsgeraden ---------------
# Hinweis: In der LaTeX-Quelle steht 'lm(menge \(\sim\) preis)' --
# das \sim ist die LaTeX-Schreibweise für die Tilde '~' in R.
reg <- lm(menge ~ preis)
plot(preis, menge, xlim = c(0, 125), ylim = c(0, 22))
abline(reg)

# --- end SLIDE 30 ---


# ---------------------------------------------------------------------
# SLIDE 40: "Residuenplot mit R erstellen"
# Section: Regression
# Subsection: Residuenanalyse
# ---------------------------------------------------------------------

# --- Block 1: Grund-R-Befehle -----------------------------------------
# Hinweis: Im LaTeX-Quelltext steht versehentlich 'lm(menge - preis)'.
# Das ist ein Tippfehler -- in R muss zwischen abhängiger und
# unabhängiger Variable eine Tilde stehen: 'menge ~ preis'.
reg <- lm(menge ~ preis)
plot(fitted(reg), resid(reg))
abline(h = 0, lty = 2)                  # Nulllinie als Orientierung

# --- Block 2: Lesbarer gestalten --------------------------------------
plot(fitted(reg), resid(reg),
     xlab = "geschaetzte Werte", ylab = "Residuen", main = "Residuenplot")
abline(h = 0, lty = 2)

# --- end SLIDE 40 ---


# ---------------------------------------------------------------------
# SLIDE 45: "QQ-Plot mit R erzeugen"
# Section: Regression
# Subsection: QQ-Plot
# ---------------------------------------------------------------------

# --- Block 1: QQ-Plot zeichnen ----------------------------------------
qqplot(preis, menge)

# --- Block 2: Gerade in den QQ-Plot zeichnen --------------------------
qqline(menge,
       distribution = function(p) quantile(preis, prob = p),
       lty = 2)

# --- end SLIDE 45 ---


# ---------------------------------------------------------------------
# SLIDE 52: "QQ-Plot der Residuen gegen Normalverteilung in R erzeugen"
# Section: Regression
# Subsection: QQ-Plot
# ---------------------------------------------------------------------

# --- Block 1: QQ-Plot erzeugen ----------------------------------------
qqnorm(resid(reg))

# --- Block 2: Gerade zwischen den Quartilen einzeichnen ---------------
qqline(resid(reg))

# --- end SLIDE 52 ---


# ---------------------------------------------------------------------
# SLIDE 74: "Bestimmtheitsmaß von R ausgeben lassen"
# Section: Regression
# Subsection: Bestimmtheitsmaß
# ---------------------------------------------------------------------

# --- Block 1: R-Befehl ------------------------------------------------
summary(reg)

# --- Block 2: Manuelle Varianten --------------------------------------
# Direkt aus dem summary-Objekt
summary(reg)$r.squared

# Oder über die Korrelation (Einfachregression)
cor(x, y)^2

# --- end SLIDE 74 ---


# ---------------------------------------------------------------------
# SLIDE 95: "Zusammenfassung: Wichtige R-Befehle (1/2)"
# Section: (Zusammenfassung)
# ---------------------------------------------------------------------

# --- Block 1: Grafische Darstellungen ---------------------------------
plot(ecdf(daten))                   # Empirische VF
hist(daten, freq = FALSE)           # Histogramm (Dichte)
hist(daten, breaks = c(37, 39, 41, 43, 45, 47))   # Eigene Klassen
# Hinweis: In der LaTeX-Quelle stehen nur drei Klassengrenzen
#   c(37, 39, 41); damit lägen aber Werte > 41 außerhalb. Hier wurden
#   die Grenzen auf den vollen Datenbereich erweitert, damit der Plot
#   funktioniert. (Original-Befehl: hist(daten, breaks = c(37,39,41)))
boxplot(daten)                      # Boxplot

# --- Block 2: Kovarianz und Korrelation -------------------------------
cov(x, y)                          # Kovarianz
cor(x, y)                          # Korrelationskoeffizient

# --- end SLIDE 95 ---


# ---------------------------------------------------------------------
# SLIDE 96: "Zusammenfassung: Wichtige R-Befehle (2/2)"
# Section: (Zusammenfassung)
# ---------------------------------------------------------------------

# --- Block 1: Regression ----------------------------------------------
reg <- lm(y ~ x)                   # Lineares Modell
summary(reg)                        # Ergebnisse inkl. R^2

# --- Block 2: Modelldiagnostik ----------------------------------------
plot(fitted(reg), resid(reg))       # Residuenplot
abline(h = 0, col = "red")          # Nulllinie
qqnorm(resid(reg))                  # QQ-Plot
qqline(resid(reg))                  # Referenzlinie

# --- end SLIDE 96 ---
