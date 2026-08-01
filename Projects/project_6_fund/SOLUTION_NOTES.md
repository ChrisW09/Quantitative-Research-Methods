# Project 6 — solution notes

> **Read this after you have written a memo of your own.** It ships alongside the brief, exactly as the mock-exam solutions ship alongside the paper; the discipline of attempting the work first is yours to keep. This one is worth the wait — the result surprises most people, and it surprises them twice.

Every number below was computed from `Fund.csv` as shipped, with `scipy.stats.ttest_1samp(fund, 0.0, axis=0)` and `statsmodels.stats.multitest.multipletests`, and is reproducible from the starter notebook.

---

## 1. What a good answer finds

### The audit — all 50 months, $m = 2{,}000$

| Procedure | Threshold | Managers surviving |
|---|---|:--:|
| Naive $t$-test (the adviser's rule) | $p < 0.05$ | **289** |
| Bonferroni | $p < 0.05/2000 = 2.5\times10^{-5}$ | **0** |
| Holm | FWER $= 0.05$ | **0** |
| Benjamini–Hochberg | $q = 0.05$ | **0** |
| Benjamini–Hochberg | $q = 0.10$ | **146** |
| *(for reference)* Benjamini–Hochberg | $q = 0.20$ | *249* |

The adviser's 289 collapses to **zero** under every family-wise procedure *and* under BH at 5%, then jumps to **146** when $q$ moves to 10%. Nothing about the data changed between those last two rows.

Why the FWER procedures find nothing is easy to see: the smallest $p$-value in the whole data set is $1.33\times10^{-4}$, and the Bonferroni cut-off is $2.5\times10^{-5}$. The best manager in a field of two thousand misses the bar by a factor of **5.3**. Holm's first comparison is the identical threshold, so Holm stops at its first step and can never proceed. There was never a near miss.

### Expected false positives under the global null

- **Arithmetic:** $\alpha m = 0.05 \times 2000 = \mathbf{100}$.
- **Sign-flip permutation** (multiply each *month* by $\pm 1$, which destroys any true mean while preserving each manager's volatility and any correlation between managers; 1,000 replicates): mean **99.7**, standard deviation **10.5**, 95th percentile **118**, largest of 1,000 replicates **136**.

So the global null predicts about 100 ± 10 "significant" managers, and never got near 289 in a thousand attempts.

### The two findings that decide the project

**Finding 1 — the survivors are not all winners.** The test is two-sided, so it flags significant *under*performance just as readily. The breakdown by the sign of $t$:

| Set | Total | $t > 0$ (outperform) | $t < 0$ (underperform) |
|---|:--:|:--:|:--:|
| Naive $p < 0.05$ | 289 | **146** | **143** |
| BH $q = 0.10$ | 146 | **72** | **74** |
| BH $q = 0.20$ | 249 | 126 | 123 |

Every set is almost exactly half bad managers. The adviser's shortlist of "managers with significant outperformance" contains 143 managers with significant *underperformance*. Whatever number goes to the trustee, it is not 289 and it is not 146.

*(A coincidence worth pre-empting, because it confuses people every year: **146** is both the number of naive survivors with $t > 0$ and the total number of BH-10% survivors. They are different sets that happen to have the same size.)*

**Finding 2 — the "146" is a knife-edge.** BH is a step-up procedure: it takes the largest $j$ with $p_{(j)} \le jq/m$. At $q = 0.10$ that largest $j$ is 146, and the comparison that licenses it is

$$p_{(146)} = 0.007201 \quad\text{against}\quad \frac{146 \times 0.10}{2000} = 0.007300,$$

a margin of $9.9\times10^{-5}$. One manager's return series perturbed slightly and the count changes. The full sweep shows how unstable the region is:

| $q$ | 0.05 | 0.06 | 0.07 | 0.08 | 0.09 | 0.10 | 0.11 | 0.12 | 0.20 |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| rejections | 0 | 0 | 0 | 128 | 138 | **146** | 159 | 182 | 249 |

The answer is 0 up to $q = 0.07$ and 128 at $q = 0.08$. A recommendation that flips from "nobody" to "a hundred and twenty-eight" on the second decimal place of a convention is not a recommendation; it is a coin toss wearing a lab coat. This discontinuity is the most important single thing to notice in Step 4, and it is what forces the argument-from-consequence that the brief demands.

### Is the global null tenable? (Step 6 — and the second surprise)

No. It is decisively false, and this is where the project stops being a straightforward Chapter 13 exercise.

| Route | Statistic | Null reference | Verdict |
|---|---|---|---|
| **Dispersion** | sd of the 2,000 track records $= 1.360$ %/month | $\sqrt{\overline{s_j^2/n}} = 0.9996$ %/month | variance ratio **1.851** |
| **Dispersion, in $t$ units** | sd of the 2,000 $t$-statistics $= 1.367$ | $\sqrt{\nu/(\nu-2)} = 1.021$ for $\nu = 49$ | far too wide |
| **Persistence**, odd vs even months | $r = 0.2546$ | 0 | $p \approx 6\times10^{-31}$ |
| **Persistence**, months 1–25 vs 26–50 | $r = 0.2895$ | 0 | $p \approx 6\times10^{-40}$ |
| **Count of $p<0.05$** | 289 | 99.7 ± 10.5 (permutation) | ~18 sd above |

The alternative explanations do not survive inspection, and a good answer checks them:

- **Autocorrelation within a manager** would inflate the $t$-statistics by understating their standard errors. The mean per-manager lag-1 autocorrelation is $-0.024$ — *negative*, so it cannot be the cause, and the odd/even split is not the load-bearing one anyway.
- **Correlation between managers** would invalidate the independence behind $\alpha m = 100$. The mean pairwise correlation is $+0.0001$ with a spread of $0.143$, against $1/\sqrt{50} = 0.141$ expected from pure noise: these columns are effectively independent. (The sign-flip permutation preserves whatever correlation exists, which is why it agrees with the arithmetic.)
- **Fat tails** are mild (excess kurtosis 0.84) and the sign-flip permutation does not assume normality, so the 99.7 ± 10.5 reference stands regardless.
- **Unequal volatilities** across managers are real (per-manager sd ranges from 0.22 to 10.0), which is exactly why the dispersion comparison must use $\sqrt{\overline{s_j^2/n}}$ rather than a single pooled figure.

Subtracting the noise leaves an implied dispersion of true skill of about $\sqrt{1.360^2 - 0.9996^2} = \mathbf{0.92}$ **%/month**, roughly **11% a year**, spread roughly symmetrically about zero: this is a population containing genuinely good *and* genuinely bad managers, in about equal measure.

So: **skill exists in this population, and no individual manager can be named.** Both halves are true, and a memo that asserts only one of them is wrong.

### Why nobody can be named, in one line

The starter prints it. Median monthly volatility 7.04%, so the standard error of a 50-month average is 1.00%/month, and with $t_{0.975,49} = 2.01$ a manager needs $|{\rm mean}| > 2.00$ %/month — **24% a year** — before a $t$-test on their own column reaches even naive significance, let alone a Bonferroni-corrected one. The true skill dispersion is 0.92 %/month. The design is asking to see something roughly two standard deviations out in the skill distribution before it will concede that anything is there. **This data set cannot resolve individual managers. That is a fact about 50 months, not a fact about fund management.**

### Step 7 — the sealed months (train = 1–35, holdout = 36–50)

Baselines, in mean excess return per month over the 15 sealed months:

- **Baseline A** — all 2,000 managers, no selection: **−0.0122 %/month**
- **Baseline B** — the adviser's rule ($p < 0.05$, both signs) fitted on months 1–35, selecting 241: **−0.0489 %/month**, permutation $p = 0.62$

What various defensible rules deliver:

| Rule fitted on months 1–35 | $k$ | Holdout %/month | vs A | Perm. $p$ |
|---|:--:|:--:|:--:|:--:|
| Select nobody (defended zero) | 0 | 0.0000 | +0.0122 | — |
| Holm at 0.05 | 0 | 0.0000 | +0.0122 | — |
| **Baseline B:** naive $p<0.05$, both signs | 241 | **−0.0489** | −0.0367 | 0.62 |
| BH $q = 0.05$ or $q = 0.10$, both signs | 3 | +0.0598 | +0.0720 | 0.48 |
| BH $q = 0.20$, both signs | 73 | +0.1116 | +0.1238 | 0.29 |
| BH $q = 0.20$ **and** $t > 0$ | 41 | **+1.0674** | +1.0796 | 0.0006 |
| **Naive $p<0.05$ and $t > 0$** | 121 | **+1.5129** | +1.5250 | < 0.0002 |
| Top-50 by train $t$ | 50 | +1.2696 | +1.2818 | < 0.0002 |
| Top-146 by train $t$ | 146 | +1.4852 | +1.4973 | < 0.0002 |
| Top-500 by train $t$ | 500 | +0.5355 | +0.5477 | < 0.0002 |
| Top-146 by shrunken mean ($\tau = 0.88$) | 146 | +1.3686 | +1.3808 | < 0.0002 |

Three things to draw out of that table.

1. **The single most valuable line of code in the whole project is the sign filter.** Adding `& (t > 0)` to the adviser's own rule moves the holdout result from **−0.049** to **+1.513** %/month. No correction procedure, no shrinkage, no clever modelling comes close to that. The adviser's shortlist was not merely uncorrected; it was pointing half its money at the worst managers available.
2. **The corrections, applied to the allocation decision, are close to useless here.** On only 35 months, BH at $q = 0.05$ and $q = 0.10$ both select **3** managers, and 3 managers is not a portfolio — the holdout result is +0.06 with a permutation $p$ of 0.48, i.e. indistinguishable from picking three names out of a hat. FWER control is the right tool for *naming* a manager and the wrong tool for *allocating* to a population. Those are different decisions and Chapter 13 answers only the first.
3. **Diversified, weakly-selected, sign-respecting sets win**, and they win with permutation $p$-values below 0.0002 against random sets of the same size. Note also that BH-10% on 35 months gives 3 where BH-10% on 50 months gives 146: the count is a statement about how much data you have at least as much as about who is skilled.

### The single number

**0** is the strongest headline, provided it is the answer to the right question and is paired with the caveat: *no individual manager in this data set can be identified as skilled at any defensible error rate.* Bonferroni, Holm and BH-5% all return zero; BH-10% returns 146 on a margin of $10^{-4}$, of which only 72 even point upwards, and BH offers no guarantee about *which* 72 — so 146 will not carry the weight of an allocation to named managers.

**72** is defensible if — and only if — the student argues it from consequence: the trustee accepts an expected false-discovery rate of 10%, funding one unskilled manager is survivable, the 74 significant underperformers are excluded by sign, and the money is spread across all 72 rather than concentrated. Marked as a strong answer when accompanied by the knife-edge caveat.

**146** is weak: it counts 74 significantly *bad* managers as evidence of skill.
**289** is the trap, fully sprung.

And the closing sentence the project exists to produce: *we cannot identify skilled managers here, but we can show that skilled managers exist in this population, and those are different findings.*

---

## 2. The trap

**The obvious answer is 289, and 289 is not the number of skilled managers.**

Under the global null, chance alone produces about **100** significant results out of 2,000 — the permutation gives 99.7 ± 10.5 — so a third of the adviser's shortlist is noise by construction before anything else is said. A student who writes "289 managers show significant outperformance" has committed precisely the error Chapter 13 exists to prevent, and has additionally counted 143 managers with significant *under*performance as talent.

**How to tell whether a student fell in.** The tell is not the arithmetic; almost everyone can call `multipletests`. It is the sentence in the memo. Look for:

- The naive count reported without the expected-false-positive count beside it. Requirement 2 of the brief exists to make this impossible to omit accidentally; if it is missing, the student did not understand why it was asked for.
- **No sign breakdown.** This is the most reliable single diagnostic, because it is three lines of code and it cannot be produced by accident. A memo with no sign table has not read its own output.
- 146 quoted as "managers with significant outperformance", with no acknowledgement that 74 of them underperform.
- The BH-10% count reported as though the choice of $q$ were a technical detail rather than the entire decision.

**There is a second trap in the other direction,** and it catches the better students — the ones who correctly get zero everywhere and then write "there is no evidence of skill in this data, invest in an index fund." The first clause is right and the second overreaches. The dispersion and persistence evidence is overwhelming (variance ratio 1.85; split-half $r \approx 0.26$–$0.29$ at $p \sim 10^{-31}$), and out of sample a sign-respecting selection beats the population by 1.5 %/month at permutation $p < 0.0002$. Step 6 exists specifically to spring this second trap, and a student who ran Step 6 and then ignored its result in the memo should lose more marks than one who never reached it. **Failing to detect individuals is not the same as establishing that there is nothing there** — which is, conveniently, the last thing this course has to teach.

---

## 3. Common wrong turns

**"BH at $q=0.10$ finds 146, so 146 managers are skilled."**
BH controls the *expected proportion* of false discoveries among rejections; at $q = 0.10$ it is telling you that roughly 15 of those 146 are expected to be noise, and it identifies *no particular manager*. Add that 74 of the 146 have negative $t$-statistics and the sentence does not survive its own arithmetic.

**"Zero managers survived correction, so no manager has skill."**
Absence of evidence. Work out what the design could have seen: a manager needs 2.00 %/month — 24% a year — to reach even naive significance on 50 months, while the true dispersion of skill in this population is 0.92 %/month. The test was never capable of resolving individuals, and Step 6 shows the population signal is there anyway.

**"$p < 0.05$ on 2,000 tests means about 5% of the significant ones are wrong."**
It means about 5% of the *2,000 tests*, i.e. 100 tests, will be significant when nothing is there. The false-discovery proportion among the 289 rejections is a different quantity with a different denominator, and confusing $\alpha$ with the FDR is the specific confusion Chapter 13 was written to remove.

**Running Bonferroni against $\alpha = 0.05$ instead of $\alpha/m$, or comparing corrected $p$-values to $\alpha/m$ (correcting twice).**
`multipletests` returns *adjusted* $p$-values, to be compared with $\alpha$. Doing both gives 0 and looks right, which is why it goes unnoticed; ask for the smallest $p$-value ($1.33\times10^{-4}$) and the threshold ($2.5\times10^{-5}$) side by side and the student either understands the comparison or does not.

**Looping `ttest_1samp` over 2,000 columns, or testing rows instead of columns.**
`ttest_1samp(fund, 0.0, axis=0)` is one call. Testing along `axis=1` tests 50 *months* against zero, which is a question about the market rather than about skill, and yields a plausible-looking table of the wrong thing — check that the output has length 2,000.

**Tuning the Step 7 rule on the holdout.** Trying BH, seeing 3 managers and +0.06, then switching to a top-50 rule and reporting +1.27 is not an out-of-sample result, and the difference between the two is precisely the value of the seal. The honest version fixes the rule, records the expectation, then evaluates.

---

## 4. Marking guide

Should the professor choose to grade this, out of 100:

| | Marks | What earns them |
|---|:--:|---|
| **1. The audit** | 20 | All five counts correct: 289 / 0 / 0 / 0 / 146. Full marks require the correct procedure *named* for each, not just five numbers. |
| **2. The chance reference** | 15 | $\alpha m = 100$ stated (8). A working sign-flip permutation with mean ≈ 100 and sd ≈ 10 (7). |
| **3. Direction** | 15 | Sign breakdown computed and tabulated (8). The inference drawn from the near-50/50 split, and 289/146 correctly rejected as answers (7). |
| **4. The threshold argument** | 15 | A chosen $q$ with a consequence-based justification, in the trustee's units — fees, headcount, cost of a mistake (10). Notices the knife-edge: 0 at $q \le 0.07$, 128 at $q = 0.08$ (5). |
| **5. The global null** | 15 | Dispersion *or* persistence computed correctly against the right null reference (10). At least one alternative explanation checked and dismissed on evidence (5). |
| **6. Discipline and Step 7** | 10 | Rule fitted on months 1–35, one evaluation, result reported against both baselines including the permutation $p$ — reported honestly if it went badly. |
| **7. The memo** | 10 | The single number in the first two lines; the absence-of-evidence caveat quantified rather than gestured at; readable by a trustee who does not know what a $p$-value is. |

**Overrides, applied after the rubric:**
- Reporting 289 or 146 as "the number of skilled managers" **caps the total at 45**, however clean the code. It is the one error the project is designed to catch.
- A memo whose headline is 0 and which also asserts "there is no skill in this population", *having computed Step 6*, loses the whole of section 5 and 5 marks from section 7.
- A memo whose headline is 0, with the caveat correct and the population signal reported, is a **full-marks answer** for sections 3, 5 and 7 even if the student never beats a baseline in Step 7. Selecting nobody and defending it is a correct answer.
- A number that cannot be reproduced by re-running the notebook: **zero for the section it appears in.**

The examiner's summary question, if only one can be asked: *does the memo distinguish "we cannot identify skill" from "there is no skill", and does it get both halves right?*

---

## 5. Extensions

- **Storey's $\hat\pi_0$ and $q$-values.** BH implicitly assumes all 2,000 nulls could be true, so with real signal present it is conservative. Estimating $\hat\pi_0$ from the density of large $p$-values gives $\hat\pi_0 = 0.866$ at $\lambda = 0.5$ (stable at 0.88–0.90 for other $\lambda$) — that is, roughly **270 of the 2,000 managers are non-null**, which is the same story the dispersion calculation told. Running BH at the adaptive level $q/\hat\pi_0$ lifts the $q = 0.10$ count from 146 to **163** (`method='fdr_tsbh'` gives 157), and — instructively — leaves $q = 0.05$ at **0**. Adaptivity buys power; it does not rescue the knife-edge. Chapter 13 exercise 3 asks for exactly this construction; here it has a decision attached.
- **Empirical Bayes, properly.** The `tau = 0.88` shrinkage in the table above is a crude two-line moment estimator and it already beats every corrected procedure out of sample. Fit the hierarchical model honestly — a normal-normal model for the manager means, or Efron's `locfdr` construction on the 2,000 $t$-statistics — and report the *posterior probability of skill* for the top manager. That number, unlike a $p$-value, is the one the trustee actually asked for, and it will still not be reassuring.
- **What record length would be needed?** Invert the power calculation. At 7.04% monthly volatility, detecting a manager whose true skill is 0.92 %/month with 80% power needs **457 months (38 years)** at a naive $\alpha = 0.05$ and **1,490 months — 124 years** at a Bonferroni-corrected $\alpha/2000$. Even a manager with three times the typical skill, 2.76 %/month, needs 14 years to clear the corrected bar. No fund manager has a 124-year track record, and no scheme can wait for one: the corrected procedure is not merely strict on this data, it is strict on *any* data a trustee will ever be shown. This is the most persuasive paragraph you can put in front of someone who wants named managers, and it reframes the whole exercise — the right response to an unidentifiable individual signal is diversification, not a longer search.
- **Advanced module A1 — Randomised controlled trials** ([`Advanced/advanced_01_rcts/advanced_01_rcts_lab.ipynb`](../../Advanced/advanced_01_rcts/advanced_01_rcts_lab.ipynb)) is the natural continuation; it lists Chapter 13 among its prerequisites. The multiple-endpoint problem there is this project in a setting where the stakes are clinical rather than financial, and it adds the one instrument this project lacks: **pre-registration**. An adviser who had named their shortlist before seeing the returns could not have produced 289.
- **The design question, for a seminar.** Projects 3 and 6 both end in a judgement call worth arguing about. Ask the group: given that individual managers cannot be resolved on 50 months, what should a trustee actually *do*? The evidence in this notebook supports "hold a broad, sign-filtered, low-fee set and do not pay for named stock-pickers", which is roughly what the professional consensus is — and the students will have derived it themselves rather than been told it.
