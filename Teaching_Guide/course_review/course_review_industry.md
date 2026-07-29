# Quantitative Research Methods — review: industry relevance and employability

**Reviewer remit:** industry relevance and employability alignment only.
**Repo state examined:** `main`, clean, decks last rebuilt 2026-07-28.
**Read-only review.** No repository file was modified.

**Conventions used below.** *Observation* = something I verified in the files, anchored to
`file:line` or a named frame. *Recommendation* = my judgement. For every regulation or legal
instrument I cite I mark **(confident)** or **(verify)** — the latter means I believe it is real
and relevant but you should check the current citation, article number or timeline before it goes
on a slide. I have invented nothing; where I could not verify a detail I say so instead of
supplying one.

**One caveat on line numbers.** While I was reading, other work was in flight on
`Lecture_Slides/chapter_03/chapter_03.tex`, `Lab_Notebooks/chapter_03_lab.ipynb`, the `Makefile`,
`README.md`, `Teaching_Guide/semester_plan.md` and `docs/exams.md`. My `chapter_03.tex` line numbers
were read from the working copy at review time and may have shifted by a few lines since; the frame
titles and the quoted text are the reliable handles. All other decks were untouched during the review.

---

## 0. What I examined

- All 12 deck sources (`Lecture_Slides/chapter_*/chapter_*.tex`, 22,399 lines total).
- Every `industry` callout, every **"Where this chapter is used in industry"** frame, every
  **"Industry case in depth"** frame, and the **"Two business problems we follow all semester"**
  frame — **25 chapter-level frames** (12 + 12 + 1) and **86 `industry` environments** in total, of
  which 26 sit inside those 25 frames and **60 are inline callouts on technique slides**. All
  extracted in full and read.
- `Teaching_Guide/`: `semester_plan.md`, all 12 runsheets, `slide_index.md`, `before_class.md`,
  `check_decks.py`, `make_index.py`.
- All 15 lab notebooks (grep-level audit of the data-handling verbs actually used).
- `Mock_Exams/` (read-only): problem inventories for all three papers, plus the full text of
  Exam 2 Problem 3 as a representative sample.
- `README.md`, `docs/*.md`, `requirements.txt`, `Makefile` targets, `ALL CSV FILES - 2nd Edition/`
  (row and column counts for all 22 datasets).

---

## 1. Honest assessment of the industry layer as it stands

### 1.1 It is better than most attempts, and a practitioner would say so

The layer is not decoration. Three things in it are the kind of thing you only write if you have
actually seen a model go into production, and a practitioner will notice them immediately:

- **`chapter_01.tex:939–944`** — "the equivalent table does not exist in a firm: it has to be built
  by joining warehouse tables *as of the decision date* … Pulling in a field that was only recorded
  *after* the decision is the classic leakage bug." That is the single most credible sentence in the
  1,168 slides. Most textbook courses never say it.
- **`chapter_01.tex:1130–1134`** — "what kills a model project": leakage, population shift, nobody
  owning the live model, a score nobody can explain. All four are correct and in roughly the right
  order.
- **`chapter_02.tex:811–815`** — "Procurement: buying a model from a vendor … ask for performance on
  a *later* period." This is the actual task a business graduate will face, and almost nobody teaches
  it.

The **"who signs it off"** field in every depth case is the layer's best structural idea. It converts
each case from a technique story into an organisational one, which is exactly right for a
business-school cohort who will mostly *commission and challenge* models, not build them.

The honest caveats are genuinely honest, not ritual. `chapter_01.tex:206–210` (a predictive-maintenance
model degrades its own training data by preventing the failures it predicts) and
`chapter_02.tex:227–232` (the recommender's feedback loop creates the co-view data the next model
trains on) are both correct and both non-obvious.

### 1.2 The layer is entirely declarative — and that is the central weakness

Nothing in the industry layer is ever *done* by a student. It is asserted on a slide and then
abandoned. Three anchored examples where the deck names a practice and the course never practises it:

| The deck asserts | Anchor | What the course then does |
|---|---|---|
| "Fraud teams therefore price each cell of the matrix, and set the threshold to the number of alerts their reviewers can work through" | `chapter_04.tex:1573–1579` | `grep -i "expected cost\|cost matrix"` over all 12 decks returns **zero hits**. No exercise, lab cell or exam question ever computes a cost-optimal threshold. Exercise 4.4 (`chapter_04.tex:737–751`) moves the threshold from 0.5 to 0.2 because "the bank now lowers the threshold", with no cost ratio anywhere. |
| "risk teams report permutation importance or SHAP instead — the same attributions that produce the reason codes a declined applicant must be given" | `chapter_08.tex:727–729` | "SHAP" appears exactly **twice** in the whole repo, both times inside industry callouts. It is never shown, never computed, never in a lab. |
| "campaign teams compare models at the *top decile*, because that is where the budget goes" | `chapter_04.tex:1455–1459` | "lift curve" — **zero hits**. "decile" — **one** hit, that sentence. No lift/gains chart exists anywhere. |
| "most of a project's time goes into that join" | `chapter_01.tex:939–944` | Across all 15 notebooks: `merge(` — **0**; `to_datetime` — **0**; `isna`/`fillna` — **0**; `duplicated` — **0**; `SimpleImputer` — **0**; `Pipeline` — **0**. Only `dropna` (11 hits, mostly `Hitters` salary). Every lab begins with `read_csv` on a clean, pre-joined rectangle. |

A practitioner reading the decks would say: *this person knows the job.* A practitioner watching a
graduate of the course would say: *they can recite the job.* That gap is the thing worth fixing, and
it is fixable cheaply — see R4 and A4.

### 1.3 The layer has no teaching apparatus, so it will silently decay

**Observation.** `grep -rn "industr" Teaching_Guide/ docs/ README.md` returns **four** hits, all four
in the author biography (`README.md:386,390`, `docs/citation.md:57,61`). The industry layer is
mentioned nowhere in the semester plan, any of the 12 runsheets, the slide index, or the
before-class checklist.

The consequence is concrete. Computing the deck page number of each industry frame and comparing it
with the runsheet running orders:

| Deck | Industry frames on pages | Runsheet block they land in | Minutes allocated | Mentioned in the block's notes? |
|---|:--:|---|:--:|:--:|
| `chapter_00` | 9, 10 | 10 min · pp. 9–18 "Data, variables and notation" | — | no |
| `chapter_00b` | 7, 8 | 20 min · pp. 7–15 "Reading mathematical notation" | — | no |
| `chapter_01` | 7, 8, **9** | 10 min · pp. 1–15 "Course mechanics" | — | no — and the block says "Slides 9-12 are motivation only … and move" (`runsheets/lecture_01.md:11`), which is where the *Two business problems we follow all semester* frame sits |
| `chapter_02` | 8, 9 | 20 min · pp. 1–16 | — | no |
| `chapter_03` | 15, 16 | 25 min · pp. 1–21 "Framing (Advertising)" | — | no |
| `chapter_04` | **15, 16** | **neither block** — block 1 is pp. 1–14, block 2 resumes at p. 17 | **0** | no |
| `chapter_05` | 12, 13 | 14 min · pp. 12–19 "Validation set" | — | no |
| `chapter_06` | 11, 12 | 13 min · pp. 11–18 "Subset selection" | — | no |
| `chapter_07` | 11, 12 | 14 min · pp. 11–18 "Polynomials and step functions" | — | no |
| `chapter_08` | 11, 12 | 20 min · pp. 11–20 "Regression trees" | — | no |
| `chapter_10` | 10, 11 | 18 min · pp. 10–18 "The single hidden layer" | — | no |
| `chapter_13` | 8, 9 | 20 min · pp. 1–14 | — | no |

So: in eleven decks the two industry frames open a timed block whose title and teaching notes are
about a completely different topic, and in `chapter_04` they fall in the one two-page gap the
runsheet skips. Twenty-five frames have no minutes and no notes. `semester_plan.md:48–64` ("If you
are behind") does not list them either way — they are neither protected nor on the cut list.

The prediction is easy: in a real 180-minute session running six minutes late, these frames get
flipped past. The investment is already made; it is currently unbankable.

### 1.4 Sector spread: over-indexed on regulated finance and on life sciences

I classified all 72 rows of the twelve sector tables:

| Sector group | Rows | Share |
|---|:--:|:--:|
| Financial services (banking, insurance, payments, asset management, fixed income, pensions) | ~25 | **~35 %** |
| Retail / e-commerce / consumer goods | ~16 | ~22 % |
| Manufacturing / industrial / energy / chemicals | ~13 | ~18 % |
| Pharma / healthcare / biotech / genomics | 8 | ~11 % |
| Tech / platforms / telco | ~8 | ~11 % |
| **Logistics** | **1** (`chapter_00.tex:263`) | 1.4 % |
| **Public sector / administration** | **0** | 0 % |
| **Professional services (consulting, audit, tax)** | **0** | 0 % |
| **Controlling / FP&A / corporate finance function** | **0** | 0 % |

Word-level checks: "automotive" appears **once** in all 12 decks (`chapter_10.tex:215`);
"Logistics" **once**; "Mittelstand", "SME", "public sector", "government", "municipal" — **zero**.
"controlling" has six hits, all of them the statistical sense ("controlling the FWER"), never the
German *Controlling* function.

**This is the biggest audience mismatch in the layer.** The single most likely destination for an HSBI
business graduate is not a bank's model-validation unit; it is a controlling, sales-operations,
purchasing, supply-chain or key-account seat in a regional Mittelstand manufacturer, a food producer,
a logistics operator, or a professional-services firm serving them. OWL's industrial base
(machinery, food, household appliances, furniture, the *it's OWL* technology cluster — **confident**)
is barely represented, while genomics gets a row and NIR spectroscopy gets a whole flagship case.

The twelve **depth cases** are better balanced than the tables (2 banking, 1 insurance, 2
manufacturing, 3 retail/e-commerce, 1 CPG, 1 pharma, 1 tech, 1 airline/retail), but they still contain
**two consecutive banking cases** — credit scoring (ch04) and credit-risk model validation (ch05) —
and **zero** logistics, energy, public-sector, HR or controlling cases.

**Strongest depth cases for this cohort** (keep, protect, expand):
1. **Marketing mix modelling** (`chapter_03.tex:366–401`). Best case in the set. It is a real
   business decision, the coefficient *is* the deliverable, every Chapter-3 diagnostic genuinely
   shows up, and the caveat is honest. A marketing graduate will meet this.
2. **Price elasticity** (`chapter_00b.tex:228–254`). The `0.9^{-1.8}-1 ≈ 21 %` calculation is the
   single most immediately usable number in the course.
3. **Retail demand forecasting** (`chapter_08.tex:223–234`). The service-level quantile and the
   "trees cannot extrapolate" caveat are both exactly right.
4. **A/B test** (`chapter_00.tex:275–299`) and **the experimentation platform** (`chapter_13.tex:196–217`).
   Correct, current, and directly employable in any e-commerce or product role.

**Weakest for this cohort:**
1. **NIR spectroscopy and PLS** (`chapter_06.tex:256–278`). Pedagogically it is the best possible
   motivation for *p ≫ n* — and no business graduate will ever be within three floors of it. The
   vocabulary (absorbance, % w/w, real-time release, validated analytical method) is opaque and
   costs you the room. The same statistical point is available from row 1 of the *same* table
   ("attribute shortlisting for a credit scorecard") or from a wide customer/SKU feature table.
2. **Credit-risk model validation** (`chapter_05.tex:268–292`). Excellent content, wrong slot — it is
   the second banking case in two chapters. Chapter 5's own table already offers "Retail, energy:
   walk-forward backtest of a demand or load forecast" (`chapter_05.tex:243–245`), which would fix
   both the sector balance and the redundancy at zero conceptual cost.
3. The **genomics** row in ch13 (`chapter_13.tex:177–178`) and the 5×10⁻⁸ constant. Accurate and
   memorable, but zero employability content; fine as the hook it is, not worth defending if time is
   short.

### 1.5 Thin, generic or dated specifics a practitioner would flag

- **`chapter_10.tex:194–195`** and **`745–749`**: "many AI imaging devices are cleared by regulators,
  mostly in radiology" / "hold regulatory clearance". This hedge is a tell — it is the one place the
  layer sounds like it is avoiding a fact it does not have. The concrete anchor exists (see §2).
- **`chapter_04.tex:370`**: "SR 11-7, ECB TRIM". TRIM (the ECB's Targeted Review of Internal Models)
  concluded with its final report in **2021** (**confident**); citing it as the live supervisory
  anchor in 2026 dates the deck. `chapter_05.tex:284–285` is better — "euro area: ECB supervisory
  model reviews" is timeless.
- **`chapter_08.tex:226`**: "LightGBM-based solutions dominated the M5 forecasting competition."
  Accurate (**confident**) but M5 ran in 2020. Keep it — it is still the standard citation — but it
  is the layer's only benchmark reference and it is six years old.
- The depth cases never name **the seat the student will actually occupy**. Every one names the owner
  and the sign-off — actuarial function, independent validation unit, quality engineering,
  personalisation team — and all of them are specialist quant roles. A one-line addition (*"where you
  are likely to sit: the category manager who has to accept or reject this elasticity"*) would convert
  each case from "here is a job you won't have" to "here is a number you will have to challenge".
- **`chapter_02.tex:383–388`** (churn) states the uplift problem — "the discount budget goes to
  customers who would have stayed anyway" — and then never names or supplies the fix. Half a lesson.

### 1.6 Currency and regulatory geography: the course is taught in dollars

**Observation.** Escaped currency symbols across the twelve decks:

- **US dollars: 77 occurrences** — `chapter_04.tex` (36), `chapter_03.tex` (30), plus 11 in
  ch01/ch02/ch06.
- **Euros: 27 occurrences** — of which **26 are in `chapter_00`** and 1 in `chapter_00b`, i.e. the two
  **optional** precourse decks.

So in the twelve sessions that are actually taught, money is denominated in dollars; euros appear
only in the sessions a student may skip. The flagship credit exercise
(`chapter_04.tex:738–751`) prices default risk at balances of \$1,800 / \$2,000 / \$2,200.

**Observation.** The complete European regulatory footprint of all 1,168 slides is: "ECB" ×2
(`chapter_04.tex:370`, `chapter_05.tex:285`), "EU" ×1 and "AI Act" ×1 (both `chapter_10.tex:1033`).
Zero hits for GDPR, DSGVO, "data protection", "privacy", "personal data", "consent", BaFin, Solvency,
EBA, "Germany", "German", "European". Against that: SR 11-7 ×2, US ECOA/Reg B ×1, FDA ×1.

One EU anchor in the whole course is not under-anchoring; it is a systematic orientation. And it is
a pity, because the one that *is* there is very good — see §5.

---

## 2. German and European specificity: what to re-anchor, with checkable equivalents

This is the highest-leverage, lowest-risk change available, because the pedagogy does not move at
all. You are swapping the proper nouns.

### 2.1 Credit scoring — Chapter 4 and Chapter 5

Replace the US adverse-action framing (`chapter_04.tex:373–374`) rather than deleting it; the contrast
is instructive.

- **CJEU Case C-634/21, *SCHUFA Holding*, judgment of 7 December 2023 (confident).** The Court held
  that the automated establishment by a credit-information agency of a probability value concerning a
  person's ability to meet payment commitments constitutes a "decision" within GDPR Art. 22(1) where a
  third party draws strongly on that value in deciding whether to contract. **This is the perfect
  slide for this course**: it is German, it is about exactly the model in your depth case, and it
  makes GDPR Art. 22 concrete instead of abstract. It also directly motivates why the scorecard stays
  logistic.
- **GDPR Art. 22 (automated individual decision-making) plus the information duties in Arts 13–15
  (confident)** — the functional European counterpart to ECOA/Reg B reason codes.
- **§ 31 BDSG** is the German provision specifically governing scoring and credit reporting
  (**confident that it is the scoring provision**; **verify** the current wording and the state of the
  debate about its GDPR compatibility, which the SCHUFA litigation put in play).
- **CJEU Case C-203/22, *Dun & Bradstreet Austria*, 2025 (verify)** — on how much must be disclosed
  about automated-decision logic; my recollection is that disclosing the algorithm itself is not
  sufficient and the controller must explain the procedure and principles actually applied. Check the
  citation and holding before using it.
- **Supervisory anchors:** replace "ECB TRIM" with **the ECB Guide to internal models** and ongoing
  internal-model investigations (**confident these exist**; **verify** the current edition date).
  Add **EBA Guidelines on loan origination and monitoring, EBA/GL/2020/06 (confident)**, which
  address creditworthiness assessment and automated model use directly. **BaFin/Bundesbank MaRisk**
  is the German administrative anchor (**confident it exists and is the relevant circular**; I am
  **not** confident of the section number for model risk — do not put one on a slide without
  checking). BaFin has also published principles on the use of algorithms in decision-making
  processes (**verify** the current title and status).
- **CRR/CRD** is how Basel actually binds in the EU; CRR3 (Regulation (EU) 2024/1623) applies from
  1 January 2025 (**reasonably confident** — verify). IFRS 9 (already cited at `chapter_04.tex:368`
  and `chapter_01.tex:177`) is correct and needs no change.
- **DORA, Regulation (EU) 2022/2554, applying from 17 January 2025 (confident)** — one sentence,
  because "who owns the model once it is live" (`chapter_01.tex:1130–1134`) now has a named legal home
  for financial firms.

### 2.2 Motor insurance pricing — Chapter 7

Your rating-factor list (`chapter_07.tex:231`) is `f(driver age) + f(vehicle age) + f(mileage) +
region + bonus-malus`. Note that **sex is absent** — which is correct, and is a missed teaching moment.

- **CJEU Case C-236/09, *Test-Achats*, judgment of 1 March 2011 (confident)** invalidated the
  derogation in Directive 2004/113/EC, so unisex premiums have been required in the EU since
  21 December 2012. One sentence turns your omission into the best "a legal constraint is a modelling
  constraint" example in the course — and it lands harder than any accuracy argument for why the
  actuarial function reviews each `f_j`.
- **German tariff structure is a gift here (confident):** *Typklasse*, *Regionalklasse* and
  *Schadenfreiheitsklasse* (SF-Klasse) are the actual factors, with the Typklassen and Regionalklassen
  published annually by the GDV. Your abstract "region + bonus-malus" is precisely these two, and
  naming them makes the frame instantly recognisable to any German student who owns a car.
- **Solvency II (Directive 2009/138/EC) (confident)** for the capital and technical-provisions side;
  the 2024/25 Solvency II review is real but I am **not** confident of its citation or application
  date — verify. **EIOPA has issued supervisory material on differential pricing practices (verify
  the exact instrument and date)**, which is directly relevant to what a pricing model is allowed to
  do at renewal.

### 2.3 People analytics and pay equity — Chapter 3

`chapter_03.tex:353` and `1671–1676` (the adjusted pay gap) are strong and currently unanchored. In
Germany this is not a governance nicety; it is co-determination law and, from 2026, reporting law.

- **BetrVG § 87(1) no. 6 (confident):** the works council has a genuine co-determination right where
  technical devices are introduced that are *suitable* for monitoring employee behaviour or
  performance. "Suitable for" is the operative phrase — intent is irrelevant. Any HR model touching
  individual employees needs the *Betriebsrat*, and no amount of model quality substitutes for that.
  **§ 90 BetrVG** (information and consultation on planning of technical plant and work processes)
  and the 2021 *Betriebsrätemodernisierungsgesetz* changes concerning AI and expert support under
  § 80(3) / selection guidelines under § 95 are relevant (**verify** the precise provisions).
- **Entgelttransparenzgesetz (EntgTranspG, 2017) (confident)** — the existing German pay-transparency
  statute.
- **EU Pay Transparency Directive (EU) 2023/970 (confident it exists)**, transposition deadline
  7 June 2026, with a joint pay assessment triggered by an unjustified gap in a category of workers
  above a threshold (my recollection is 5 %) that is not remedied. **Verify the threshold and the
  mechanics** — but the point stands and is now live law: *your adjusted-gap coefficient has acquired
  a statutory trigger.* That is a remarkable thing to be able to tell a business cohort about an OLS
  coefficient.

### 2.4 The EU AI Act — and it belongs in Chapter 4, not only Chapter 10

**`chapter_10.tex:1031–1037` is the best single paragraph in the industry layer** and it is accurate:
creditworthiness assessment of natural persons and employment/worker-management uses are Annex III
high-risk areas under Regulation (EU) 2024/1689, carrying documentation, logging, monitoring and
human-oversight obligations (**confident**).

Two problems:

1. It sits in the **deep-learning** chapter, where it says "that raises the bar for an *opaque*
   model". But the Act is technology-neutral: your logistic scorecard in Chapter 4 is *equally*
   high-risk. Students will draw the wrong inference — that governance is a neural-network problem.
   The callout, or a sibling of it, belongs at `chapter_04.tex:355–377` and at the pay-equity frame in
   Chapter 3.
2. **Timeline.** The Act entered into force 1 August 2024; prohibitions applied from February 2025;
   the Annex III high-risk obligations were scheduled to apply from **2 August 2026** (**reasonably
   confident**). That is *this semester*. However, simplification/delay proposals were under
   discussion in late 2025 and I do **not** know the outcome — **check the current status before you
   put a date on a slide.** Say "from August 2026, subject to the current state of the EU's
   simplification package" rather than an unqualified date.

### 2.5 The remaining seven cases, in one pass

| Deck / frame | Current anchor | European equivalent worth citing |
|---|---|---|
| `chapter_00.tex:249–251` SPC, ±3σ | none | **ISO 9001**, **IATF 16949** for automotive supply, **VDA Band 5** (*Prüfprozesseignung*), **AIAG-VDA FMEA Handbook (2019)** — all **confident**. For an OWL cohort this is the vocabulary of their first job. |
| `chapter_00.tex:260–262` acceptance sampling "against an agreed plan" | vague | **ISO 2859-1** (sampling procedures for inspection by attributes) — **confident**. Name it; the vagueness is doing no work. |
| `chapter_06.tex:256–278` NIR / PLS | "a validated analytical method" | **Ph. Eur. general chapter 2.2.40** (NIR spectrophotometry) and **ICH Q2(R2) / Q14** (analytical procedure validation and development, adopted 2023) — **reasonably confident on both; verify the chapter and reference numbers.** Real-time release sits in the ICH Q8 framework. |
| `chapter_10.tex:194,745` medical imaging "clearance" | FDA-shaped hedge | **EU MDR, Regulation (EU) 2017/745**, CE marking via a notified body; software-as-medical-device classification under MDCG guidance and Rule 11 of Annex VIII — **confident**. This replaces the hedge with a fact. |
| `chapter_13.tex:601–603` FDA multiple-endpoint guidance | US | **ICH E9** *Statistical Principles for Clinical Trials* and the **E9(R1) estimand addendum (2019)** — **confident**. **EMA/CHMP guideline on multiplicity issues in clinical trials** — **confident it exists; verify the reference number.** |
| `chapter_13.tex:196–217` experimentation platform | none | **GDPR + the German TDDDG** (the renamed TTKG/TTDSG, effective May 2024) — **reasonably confident on the rename; verify.** This matters practically: consent requirements mean EU client-side experiment populations are *selected*, which is a live threat to external validity your students will actually hit. A genuinely European addition to the case, not a compliance footnote. |
| `chapter_10.tex:213–234` visual inspection that can stop the line | none | **Machinery Regulation (EU) 2023/1230**, applying from January 2027, which addresses machinery with self-evolving behaviour — **reasonably confident; verify.** |
| *(new, see A7)* supplier risk | — | **LkSG** (German Supply Chain Due Diligence Act, in force 2023 for ≥3,000 employees, ≥1,000 from 2024) and **CSDDD, Directive (EU) 2024/1760** — **confident they exist; the CSDDD was under omnibus revision in 2025, so verify status.** German firms now have a *statutory* obligation to run a supplier risk analysis. That is a classification problem with a legal driver, and it is the most Mittelstand-relevant modelling task in existence. |

---

## 3. The gap between the course and the job

Ranked strictly by **value per hour of teaching for this cohort**, with an honest statement of what
each one costs and where it goes.

### Tier 1 — do these; they are cheap and they are what the course is already claiming

| # | Gap | Value/hour | Why, for *this* course | Where it goes |
|:--:|---|:--:|---|---|
| 1 | **Cost–benefit framing of a model decision** | Highest | The deck asserts it three times (`chapter_04.tex:1573–1579`, `1455–1459`, `chapter_10.tex:222–227`) and never computes it once. `grep "expected cost\|cost matrix"` = 0. It costs ~25 minutes of teaching and it reframes every subsequent chapter: a threshold is a business parameter, not 0.5. | 20 min inside Lecture 6 (ch04 evaluation block, `runsheets/lecture_04.md` pp. 72–89, currently 45 min), plus one exercise and one exam problem. See **R4**. |
| 2 | **Communicating to a non-technical stakeholder** | Very high | The layer already says "someone has to defend that number in a meeting" (`chapter_03.tex:360–362`) and "the interval, not the point estimate" (`chapter_03.tex:821–825`). Nothing ever asks a student to write for a manager. The best exercise in the repo — Extended Exercise 0.4, *Reviewing an analysis end to end* (`chapter_00.tex:2081–2104`), critiquing a consultancy's loyalty-programme claim — sits in the **optional** precourse deck. | Zero new teaching hours: it is the graded project's memo deliverable (**A1**). Promote Ext. Ex. 0.4 into Lecture 1 or make the precourse non-optional in the module description. |
| 3 | **Data cleaning, joins and as-of correctness** | Very high | Anchored in §1.2: the course tells students the join is most of the work and never joins anything. This is also where leakage becomes visceral rather than notional. | One new 90-minute self-study lab (**A4**), zero contact hours, plus 10 minutes of framing in Lecture 1 pointing at it. |
| 4 | **Model documentation / governance** | High | "model card" = 0 hits; "monitoring" = 6 hits, all rhetorical. The AI Act makes this an employability fact, not a nicety, from August 2026. And it is *cheap*: one page, twenty minutes. | 20 min appended to the Lecture 11 (ch10) governance callout at `chapter_10.tex:1031–1037`, which already sets it up. One-page template as a project deliverable. |
| 5 | **Experimentation practice** | High | Nearly free — ch00 and ch13 already carry the theory, the sizing rule of thumb (`chapter_00.tex:286–292`) and the pre-registration discipline (`chapter_13.tex:205–210`). What is missing is a student ever *sizing* and *pre-registering* one. | 15 min in the ch00 precourse or Lecture 12; one exercise. |

### Tier 2 — real value, but they cannot come out of the twelve sessions

| # | Gap | Verdict |
|:--:|---|---|
| 6 | **SQL and data access** | The single most-requested tool in analyst job ads, and it genuinely cannot be taught in a full 12-session statistics module. **But there is a nearly-free route you should take:** `duckdb` in the notebook, querying the CSVs already in `ALL CSV FILES - 2nd Edition/`. No server, no DBA, no install beyond one pip line, and `duckdb.sql("select ... from 'Credit.csv'")` works immediately. Three to four hours of guided self-study exercises (joins, group-by, window functions for the as-of join), zero contact time, gated by the project requiring one SQL step. This is the highest-value item in the whole review per hour of *your* effort. |
| 7 | **Git and collaboration** | Moderate value, near-zero teaching cost — *if* the project (A1) is submitted as a repository with at least three commits per group member. Do not teach git; require it. Your repo is already a git repo with CI (`.github/workflows/docs.yml`), so you have a live example to point at. |
| 8 | **Working with an LLM as an analyst** | Genuinely a hole (see §5), but the teachable content is 15–20 minutes of *verification discipline*, not prompting. Cheap. See **A3**. |
| 9 | **Dashboards / BI** | Employers in the German mid-market do want Power BI. It is a poor fit for a statistics module, expensive to support (licences, versions, per-student debugging), and it competes with nothing you teach. **Say so explicitly to students** — "this is a real gap in your CV, here is where to close it" — and put it in a follow-on module or another chair's course. Do not absorb it. |
| 10 | **Cloud and MLOps** | Lowest value per hour for this cohort. A business graduate will not own the pipeline; they will be a stakeholder of it. `chapter_10.tex:998–1002` ("Projects stall on that plumbing far more often than on the optimiser") is already **exactly the right amount of MLOps for this audience.** Add nothing. Resist. |

### What I would actually displace, with the arithmetic

You are right that twelve sessions are full. Here are five specific, defensible cuts totalling
**~58 minutes across the semester**, all anchored in the runsheets:

| Cut | Anchor | Minutes | Why it is safe |
|---|---|:--:|---|
| Backprop by hand on a 2-2-1 net | `runsheets/lecture_10.md`, "Extended Exercise 10.1", pp. 25–28 | **18** | The least employable 18 minutes in the course for a business audience. Nobody will ever do this, and the *idea* of the chain rule survives in the one-slide version at `chapter_10.tex:1590+`. Keep the exercise as assigned homework with its solution in the deck. |
| KNN-vs-OLS comparison | `runsheets/lecture_03.md`, pp. 124–144 block (20 min) | **12** | Chapter 2 already teaches KNN and the bias–variance story properly (Lecture 2, pp. 67–87, 52 min). This is the third pass. |
| Smoothing splines / LOESS | `runsheets/lecture_07.md`, pp. 40–50 block (20 min) | **8** | Penalised regression splines inside a GAM are the production choice, and the GAM block follows immediately. Trim, don't delete. |
| Extended Exercise 13.1 (three procedures on ten p-values) | `runsheets/lecture_13.md`, pp. 39–42 (15 min) | **10** | Exercises 13.2–13.5 already run live on the same six p-values (pp. 23–26 and 33–38, 34 min combined). This is a fourth repetition. |
| Naive Bayes trim | `runsheets/lecture_04.md`, pp. 62–71 block (35 min) | **10** | Of the five classifiers, naive Bayes is the one your own deck says least about in industry terms. Keep the method, compress the comparison. |

**That funds:** 25 min for the industry frames (R1, 2 min per deck), 25 min for the causal-thinking
insert (A2), and 8 min spare. No new sessions, no lost content that isn't duplicated elsewhere.

---

## 4. Prioritised recommendations — *changes* to what exists

| Pri | Recommendation | Effort | Displaces |
|:--:|---|:--:|---|
| **R1** | **Bank the industry layer in the teaching apparatus.** Give each pair of industry frames an explicit 2-minute block in its runsheet with a one-line note ("do the sector table as a show-of-hands: who has worked in one of these six?"), name them in `semester_plan.md`, and add them to the protected list at `semester_plan.md:62–64` rather than leaving them unlisted. Fix the `chapter_04` gap (runsheet jumps pp. 14→17) and the overlapping page ranges in `runsheets/lecture_10.md` (two blocks both start at p. 45). | **4 h** | 2 min per session, funded above |
| **R2** | **Re-anchor to Europe.** Work through §2: SCHUFA C-634/21 and GDPR Art. 22 into ch04; Test-Achats and the Typklasse/Regionalklasse/SF-Klasse vocabulary into ch07; BetrVG § 87(1) no. 6 and the Pay Transparency Directive into ch03; ISO 2859-1 and VDA/IATF into ch00; MDR into ch10; ICH E9 alongside the FDA sentence in ch13; replace "ECB TRIM" with the ECB internal-models guide. Keep the US anchors as explicit contrasts — "in the US this is ECOA; here it is Art. 22" is *better* pedagogy than either alone. | **8–10 h** incl. source checking | Nothing — pure substitution |
| **R3** | **Fix the currency geography.** Do **not** blanket-convert: `Default`, `Credit`, `Carseats` and `Hitters` are US datasets and their dollar figures are facts, so relabelling them would introduce an error. Instead: (a) add one sentence in ch01 naming the ISLP datasets as US data, which is itself a useful lesson about population shift; (b) denominate every *newly written* business framing, exercise and exam scenario in euros; (c) at minimum, add a euro-denominated parallel to Exercise 4.4 (`chapter_04.tex:738`) since that is the flagship decision exercise. | **3–4 h** | Nothing |
| **R4** | **Make the cost-optimal threshold a computed thing.** One exercise pair in ch04: given `c_FP` and `c_FN` in euros, derive `p* = c_FP/(c_FP+c_FN)`, apply it to a confusion matrix, and compare expected cost against "flag nobody" and "flag everybody". Then one exam problem. This is the single highest-value 25 minutes available to you and it discharges the promise already made at `chapter_04.tex:1573–1579`. Exam 2 Problem 3(b) (`Mock_Exams/Exam_2_after_Lecture_08/mock_exam_2.tex:289–292`) already asks for "a business reason" qualitatively — this is the quantitative sibling. | **3 h** | 20 min from the ch04 naive-Bayes block |
| **R5** | **Rebalance the sector tables and one depth case.** Re-cast the ch05 depth case from credit-model validation to the **walk-forward backtest of a demand or load forecast** already sitting in its own table (`chapter_05.tex:243–245`) — same statistical content, removes the double banking case, adds energy/retail. Then rewrite ~8 table rows to add: a logistics row beyond the single one; a public-administration row (municipal capacity planning off Destatis/registry data — safe to state as a data source without asserting any authority's current practice); a controlling/FP&A row (budget-variance and rolling-forecast); and a professional-services row (audit sampling, which is genuinely ISO-2859-shaped). | **5 h** | Nothing |
| **R6** | **Add "where you are likely to sit" to all twelve depth cases.** One line each, naming the *consumer* of the model rather than its builder. This is the cheapest thing in this document and it changes how the whole layer reads for a business cohort. | **1.5 h** | Nothing |
| **R7** | **Demote the NIR/PLS depth case to the appendix** and promote the credit-scorecard attribute-shortlisting row (`chapter_06.tex:229–231`) — or a wide customer/SKU table — into the flagship slot. Same *p ≫ n* motivation, vocabulary the room already has. Keep NIR as the sidebar it deserves to be; it is a lovely example, just not a flagship for these students. | **2 h** | Nothing |
| **R8** | **Extend `make_index.py` to index the industry frames.** ~20 lines: scan the `.tex` for `used in industry` / `case in depth` / `begin{industry}` and emit their page numbers into `slide_index.md`. Then `make index` keeps the runsheets honest when pages shift, which is the mechanism that will otherwise silently break R1 the first time you edit a deck. `check_decks.py` and `make_index.py` already establish this pattern. | **2 h** | Nothing |

---

## 5. Recommendations — *additions*

### A1 — The applied project (highest-value addition; do this one first)

**Observation.** Assessment is exams only (`semester_plan.md:66–77`; `docs/exams.md`). All 18 exam
problems across the three papers are technique-titled — "by hand" (×4), "concepts", "interpreting
Python output". Exercise tags across the whole course are Math 57 / Concept 32 / Python 26 /
Integrative 8; there is no business, decision or communication tag. Students optimise for what is
graded, so at present the industry layer carries **zero assessment weight** — which, combined with
§1.3, is why it will not survive contact with a semester.

**Design: "One decision, one model, one memo."**

**Business question (stipulated brief — the numbers below are yours to set, not data-derived).**
A mid-sized German insurer plans a direct-mail cross-sell campaign for caravan cover to its 100,000
existing customers. A mailer costs **€4.50** all-in; an acquired policy is worth **€60** in expected
contribution. *Who should be contacted, and what is the expected profit against the alternatives of
mailing everyone and mailing nobody?*

**Data: `ALL CSV FILES - 2nd Edition/Caravan.csv` — it suffices, and no external dataset is needed.**
5,822 rows, 85 predictors, response `Purchase` = 348 Yes / 5,474 No (**5.98 %**, verified). Three
properties make it a genuinely good project dataset rather than a toy:

1. **The economics bite.** At a 5.98 % base rate, mailing everyone loses money:
   100,000 × (0.0598 × 60 − 4.50) ≈ **−€91,000**. Mailing nobody earns €0. The break-even response
   rate is 4.50/60 = **7.5 %**, *above* the base rate. So the model must find a segment better than
   average or there is no campaign — which is precisely the conversation a real analyst has, and it is
   impossible to fake with a high accuracy figure.
2. **The naive answer is exposed automatically.** "Predict No for everyone" scores 94 % accuracy and
   is worth exactly nothing. Students discover this themselves; you do not have to warn them.
3. **The column names are opaque** (`MOSTYPE`, `MAANTHUI`, `MGEMOMV`, `MOSHOOFD`, …). This is the
   COIL 2000 / *Insurance Company Benchmark* dataset (**confident it is on the UCI ML Repository with
   a published codebook**). Finding and reading a codebook for undocumented columns is a real job
   task and costs them an authentic afternoon.

**Deliverables (three, deliberately).**
1. A **4-page decision memo** to the "Head of Cross-Sell": no equations, at most two charts, an
   explicit euro recommendation, a stated contact volume, and one named risk that would change the
   recommendation. Hard page limit.
2. A **reproducible notebook** — runs top to bottom on Colab, one SQL step (DuckDB over the CSV, per
   Tier-2 item 6), out-of-sample evaluation, and the threshold derived from the cost ratio.
3. A **one-page model card**: target definition and horizon, scoring population, validation design,
   the metric and why, monitoring trigger, and a one-line GDPR/AI-Act status note (is this
   creditworthiness? no — so what *is* the legal basis for the processing?).

**Marking basis (100 points).**

| Weight | Criterion | What earns the marks |
|:--:|---|---|
| 40 | **Decision quality** | Threshold derived from €4.50/€60, not from 0.5. Both baselines (all/none) computed. Expected profit stated with an interval or a sensitivity to the margin assumption. A lift or gains curve used to answer "and if we only have budget for 20,000 mailers?" |
| 25 | **Method soundness** | Honest out-of-sample estimate; no leakage; class imbalance addressed *and the choice justified*; some check that probabilities mean what they say. Boosting beating logistic regression earns nothing on its own. |
| 20 | **Communication** | Would a head of cross-sell act on this memo without asking a follow-up question? Marked by reading only the memo. |
| 15 | **Reproducibility and documentation** | Notebook runs clean from a fresh kernel; git repo with commits from every group member; model card complete. |

**Time.** Student: **18–25 hours** for a group of three (~7 h each) — realistic for a 5-ECTS module's
project component. Marker: **25–35 minutes per group** with this rubric (memo 10, notebook 15,
card 5), so **10–12 hours for 20 groups**. Design cost to you: **12–16 h** the first year, ~3 h/year
thereafter to refresh the brief numbers.

**The real constraint is not hours; it is the Modulhandbuch.** Moving from *Klausur* to *Klausur +
Projektarbeit* is a module-description and examination-regulation change with lead time, and it must
be in place before the semester starts. That is the item to start on now — the pedagogy is the easy
part.

**Two variants, honestly costed.**

- **Zero-setup fallback — `Bikeshare.csv`** (8,645 hourly rows, verified; `season`, `mnth`, `day`,
  `hr`, `weathersit`, `temp`, `hum`, `windspeed`, `casual`/`registered`/`bikers`). Question:
  how many bikes to reposition, and what does a forecast error cost? Uses the ch07 temperature
  response curve, the ch08 booster, and ch05 walk-forward validation. Requires constructing a time
  index from `mnth`/`day`/`hr` — a small, genuine wrangling step. Cheapest possible option; slightly
  less business-decision-shaped than Caravan.
- **Ambitious / follow-on version — German electricity load.** **SMARD.de** (Bundesnetzagentur) for
  load and generation and **DWD Open Data / Climate Data Center** for hourly temperature — both real,
  free, no registration (**confident**); **ENTSO-E Transparency Platform** as an alternative
  (**confident**). This forces everything the course currently never does: timestamp parsing, a join
  on time, missing hours, and the German DST changeover with its duplicated 02:00–03:00 hour — which
  is the most memorable data-quality lesson available anywhere. Costs: you must pin a data snapshot in
  the repo (the sites change), and marking variance rises. I would offer it to two or three ambitious
  groups, or make it the follow-on module's project.

**Other genuinely available external options, if you want a second brief in rotation** (all
**confident** that they exist and are freely accessible; row counts approximate):

| Dataset | Source | Why it fits |
|---|---|---|
| **Bank Marketing** (Moro et al.), ~41k rows | UCI ML Repository | Direct-marketing campaign targeting with a real response variable. Closest external substitute for the Caravan brief, at 7× the size. |
| **Statlog German Credit** (Hofmann), 1,000 loans, 20 attributes | UCI ML Repository | *German*, and it **ships an asymmetric cost matrix** (bad-classified-as-good penalised several times more heavily than the reverse) — a ready-made R4 exercise. **Verify the exact 5:1 ratio on the UCI page.** |
| **Online Retail II**, ~1M invoice lines, UK retailer 2009–2011 | UCI ML Repository | Genuinely messy: cancellations, negative quantities, missing customer IDs. The best available "clean this before you model it" dataset, and RFM segmentation falls out naturally. |
| **Bike Sharing** (Fanaee-T & Gama) | UCI ML Repository | The full 2011–2012 series behind ISLP's `Bikeshare`. |
| **Destatis GENESIS-Online**, **Eurostat**, **Deutsche Bundesbank**, **ECB Data Portal**, **GovData.de** | official | For any brief needing German or EU macro/sector context. Free, stable, citable. |

### A2 — Causal thinking: the highest-value modern addition

**Observation.** Causality currently appears only as a *prohibition*. All hits: `chapter_03.tex:328`
("a coefficient is an association, not…"), `1409`, `2794`; `chapter_01.tex:519`, `1123`;
`chapter_08.tex:1164`; plus eight in the **optional** `chapter_00`. "difference-in-differences"
appears **once**, at `chapter_00.tex:1577`, inside the solution to an extended exercise in a session
students may skip. No potential outcomes, no propensity scores, no uplift, no DAGs beyond a single
word.

Meanwhile the industry layer walks into the wall four times and stops:

- `chapter_03.tex:396–399` — "MMM estimates *association*, so turning a coefficient into a budget
  decision is a judgement — good teams cross-check it against geo experiments or holdout regions."
- `chapter_00b.tex:247–253` — "past prices were cut *because* demand was weak, so the estimate is
  confounded unless it comes from experiments or genuinely exogenous price moves."
- `chapter_02.tex:383–388` — "the discount budget goes to customers who would have stayed anyway."
- `chapter_01.tex:206–210` — the maintenance model censors its own labels.

**Recommendation.** Not a new session — **~25 minutes redistributed**, in two places:

1. **Lecture 4 (ch03), immediately after the MMM depth case (`chapter_03.tex:401`) — 15 minutes.**
   One slide: *the ladder of evidence for a coefficient you are about to spend money on.*
   Randomise (A/B test, geo holdout) → exploit a policy change or a staggered rollout
   (difference-in-differences) → control and hope (MMM, hedonic pricing, pay-equity regressions).
   State what each buys and what it assumes. The MMM caveat already names rung one — make the
   cross-check the lesson instead of the disclaimer. This is a *framing* slide, not new machinery:
   no potential-outcomes notation required.
2. **Lecture 12 (ch13), inside the "p-hacking / post-selection" block (pp. 43–48) — 10 minutes.**
   Uplift: rank by *treatment effect*, not by *propensity*. Requires a randomised treat/control
   holdout, which the chapter already has the apparatus for. One slide closes the loop on
   `chapter_02.tex:383–388`, and it is the most commercially valuable single idea in modern CRM
   analytics.

**Effort 6–8 h** (≈6 new slides plus one exercise). **Displaces** the cuts in §3. This is the highest
value-per-hour modernisation available, because the demand for it is already written into your own
industry frames.

### A3 — The LLM as an analyst's tool

**Observation.** `chapter_10.tex:1577–1587` covers self-attention correctly and cites Vaswani et al.
(2017); `chapter_10.tex:967–972` mentions LLMs over retrieved document embeddings, correctly framed on
handling time rather than accuracy. That is the whole coverage — and it is all about LLMs as an
*object of study*, never as the tool every one of your students is already using on the labs.

**Recommendation — 15 minutes and one rule, not a session.** Attach to the ch00b block "The Python
you will actually write" (`runsheets/lecture_00b.md`, pp. 34–40, 22 min).

- The 15 minutes are about **verification discipline**, not prompting: after an LLM drafts your
  pandas, you check row counts before and after every join, you check dtypes, and you hand-compute one
  value. Frame it exactly as the deck already frames vendor models
  (`chapter_02.tex:811–815`): you are accepting a deliverable you did not build, so you test it.
- The rule: **LLM use in the labs and the project is allowed and must be disclosed** in a one-line
  comment. This is honest, it is enforceable, and it protects exam integrity precisely because the
  exams are already closed-book — you do not need to fight the tool, you need to separate the two
  assessment modes. Say that out loud in Lecture 1.
- **Do not** add RAG, agents, or fine-tuning. Not for this cohort, not in this module.

**Effort 3 h.** Displaces ~15 min of the ch00b Python block, which the runsheet already treats as the
most compressible material in that deck.

### A4 — One data-plumbing lab

**Effort 6–8 h; zero contact hours.** A single new self-study notebook that does what all 15 current
labs never do: read two files, parse dates, do an **as-of** join that would leak if done naively,
find and handle duplicates and missings, then fit the *same* model with and without an sklearn
`Pipeline` and show the CV score change. `Pipeline` is already correctly explained on slides
(`chapter_05.tex:1305–1314`, `chapter_03.tex:3054–3072`, `chapter_06.tex:1190–1195`) and appears in
**zero notebooks** — so the mechanism practitioners actually use to prevent leakage is taught as prose
only. Extended Exercise 5.3 (`chapter_05.tex:1265–1282`) is the perfect conceptual anchor; this lab is
its executable twin. `Bikeshare.csv` plus a small hand-made "promotions" or "weather" table is enough;
no external data required.

### A5 — A one-page model card template

**Effort 2 h.** Target and horizon; scoring population; predictors and their availability *at decision
time*; validation design; metric and threshold with its cost basis; monitoring trigger; owner; legal
status. It operationalises `chapter_01.tex:1130–1134` and `chapter_10.tex:1031–1037`, it is a project
deliverable, and — genuinely — it is a document a graduate can put in front of an employer.

### A6 — A calibration and lift slide pair

**Effort 3 h.** "calibrat*" appears 14 times as a word (`chapter_04.tex:239, 307, 364, 1414, 2256`)
but no reliability diagram, Brier score or calibration plot exists anywhere; "lift curve" is 0 hits.
Two slides plus two lab cells in ch04: a reliability diagram, and a gains/lift chart with the top-decile
comparison the deck already promises at `chapter_04.tex:1455–1459`. These are the two charts that
actually appear in a model-review pack, and they are also what the A1 project needs to answer "what if
we can only afford 20,000 mailers?".

### A7 — A supplier-risk row and callout (the Mittelstand hook)

**Effort 1 h.** German firms above the LkSG thresholds have a *statutory* obligation to run a supplier
risk analysis (**confident**; CSDDD status **to verify**). That is a classification problem, with
imbalanced labels, a cost-asymmetric threshold, an audit trail requirement, and a legal driver — and it
is the most Mittelstand-relevant modelling task available. One table row in ch04 or ch08 and one
callout. It also gives you the logistics/procurement representation the tables currently lack (1 row
in 72).

---

## 6. Guest practice and keeping it current — with honest maintenance costs

| Mechanism | Effort to start | Annual burden | Honest assessment |
|---|:--:|:--:|---|
| **A one-page case-sheet template mirroring your depth-case structure** (response / predictors / output / decision / sign-off / caveat) | 1 h | ~30 min per case received | **Do this first.** The structure already exists in twelve worked examples, so a guest fills a form rather than writing slides — which is the difference between "yes" and "I don't have time". It also guarantees new cases are comparable to old ones. |
| **Guests as a 25-minute slot inside an existing session**, not a whole session | 30 min per guest to brief | scheduling only | Protects the runsheet, and avoids the standard failure where a guest overruns and eats the lab. Best matches to cases you have already written: a credit-risk validator (Lecture 7), a pricing or category manager (Lecture 4), a supply-chain planner (Lecture 10), a quality engineer (Lecture 11). |
| **Alumni-sourced case sheets** — one standing question in the alumni mailing | 1 h | 2–4 h | Low cost per item, but be realistic: expect **2–3 usable cases a year**, each needing rewriting by you. Its real value is not volume, it is that "an HSBI graduate three years out does this" is the most persuasive sentence available to you in Lecture 1. |
| **Data from a local firm** | 15–40 h | high, recurring | **Highest credibility, worst cost/benefit for the graded project.** You need an NDA, a GDPR basis and probably a processing agreement, works-council involvement if anything touches employees, and the data cannot be published — which breaks the whole open-repo model this course is built on. **Recommendation:** never in the graded project. Use firm data for a single in-class demo you run yourself, or route it to Bachelor theses, where the one-to-one supervision makes the overhead proportionate. |
| **An annual 60-minute "currency check"** with a fixed checklist | 1 h | **1 h** | The cheapest durable mechanism, and the one I would actually bet on. Checklist: (1) three regulatory dates — AI Act high-risk status, Pay Transparency transposition, CSDDD; (2) three technique defaults — is boosting still the tabular default, is the M5 citation still the right benchmark, what has replaced it; (3) one currency sweep of the depth-case caveats. Slot it into the existing `Teaching_Guide/before_class.md` rhythm as a once-per-semester sibling. |
| **Automate the structural check** (R8) | 2 h | 0 | Extend `make_index.py` so `make index` reports each deck's industry-frame pages. Without it, R1 breaks silently the first time a deck gains a slide — which is exactly how the current runsheet/frame mismatch arose. |

---

## 7. What I examined and judged already strong

So this reads as a review and not a demolition — these are the things I checked specifically looking
for weakness and did not find it.

1. **The depth-case template itself.** Response / predictors / output / which decision / who signs off
   / honest caveat. Six fields, twelve times, no drift. This is a better structure than most
   practitioner-facing case write-ups I have seen, and it is the reason the layer is salvageable
   rather than needing a rewrite.
2. **The "who signs off" field.** Correctly identifies that the analyst is not the decision-maker
   (`chapter_04.tex:367–370`, `chapter_10.tex:222–227`, `chapter_07.tex:236–238`). For a cohort who
   will mostly commission models, this is the most valuable single idea in the layer.
3. **The honest caveats.** Not ritual. `chapter_08.tex:231–233` (trees cannot extrapolate, so keep an
   explicit price or trend term) and `chapter_06.tex:273–277` (calibrations drift when a supplier or
   instrument changes) are both things people learn the hard way in production.
4. **The semester-thread frame** (`chapter_01.tex:213–255`, "Two business problems we follow all
   semester"). Structurally the best idea in the deck set — two decisions, thirteen chapter references,
   and the closing line "Methods are chosen by what the decision needs, never because they are new."
   My only complaint is that it currently has **no minutes** in `runsheets/lecture_01.md` (see R1).
   Fix that and it is worth more than several new frames.
5. **Out-of-sample and out-of-time discipline.** Genuinely excellent and consistently reinforced:
   `chapter_02.tex:811–815`, `chapter_05.tex:287–290` (random folds across origination dates),
   `chapter_05.tex:674–678`, `chapter_08.tex:899–901`, `chapter_05.tex:1425–1429` ("never report the
   tuned CV score to a steering committee"). This is the thing most courses get wrong and this one
   gets right five times over.
6. **The EU AI Act callout** (`chapter_10.tex:1031–1037`). Accurate on both the Annex III categories
   and the obligation types. My criticism is placement and a timeline caveat, not content.
7. **The tabular reality check** (`chapter_10.tex:176–182`): boosting usually matches or beats a
   neural network on wide business tables at a fraction of the cost and is easier to document. Correct,
   current, and commercially useful — and admirably unfashionable to say in a deep-learning chapter.
8. **Extended Exercise 0.4** (`chapter_00.tex:2081–2104`), critiquing a consultancy's loyalty-programme
   report — skew, the interval, reconciling *p* < 0.001 with *R²* = 0.04, the *r* = 0.05 fallacy,
   self-selection, and "which two plots would you have asked for first". This is the most job-like
   exercise in the repository. It should not be in an optional session.
9. **The runsheets as artefacts.** The cut lists, the "what they will get wrong" sections and the
   "before you walk in" checklists are unusually good and clearly written from real sessions. That is
   precisely why R1 matters: this apparatus works, and the industry layer is currently outside it.
10. **The build system.** `make check` catching overfull vboxes from the LaTeX logs, `make index`
    regenerating the slide index from `.toc` — the right instinct, already in place. R8 is a small
    extension of a pattern you already established, not a new discipline.

---

## 8. The four things I would do if you only did four

1. **R1 — bank the industry layer in the runsheets (4 h).** Everything else in this document is worth
   less if the frames get flipped past in the room. Cheapest, most urgent.
2. **A1 — the graded project (12–16 h, plus a Modulhandbuch change starting now).** Without an
   assessment stake, the industry layer is signalling. With it, the layer becomes the course. Start the
   examination-regulation paperwork first; it has the longest lead time and it is the actual
   bottleneck.
3. **R2 + R4 — Europe, and one euro-denominated cost-optimal threshold (11–14 h).** Together these
   turn "here is what banks in America do" into "here is the decision you will be asked to defend, in
   the currency and the legal order you will defend it in".
4. **A2 — the 25-minute causal-thinking insert (6–8 h).** Your own industry frames ask for it four
   times. Answering them costs less than half a session and it is the difference between a graduate
   who can fit a model and one who knows when the coefficient may be spent.
