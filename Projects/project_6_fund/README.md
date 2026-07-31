# Project 6 — How many of these managers can actually pick stocks?

> **The situation.** A pension trustee has the track records of **2,000 fund managers** over **50 months**, and an adviser's shortlist of "managers with statistically significant outperformance". The adviser's method was a $t$-test on each manager's excess returns at $p < 0.05$; the shortlist is not short. The trustee is on the point of moving real money onto it, and has asked you for an independent second opinion on the only question that matters: **how many of these managers are genuinely skilled?** They want one number. Fees are the reason they are asking — a manager with no skill still charges 80 basis points a year, and a scheme that funds a hundred of them has converted its members' retirement income into somebody's revenue. If the honest answer is **zero**, say zero: a trustee who is told zero keeps the money in an index fund and loses nothing. A trustee who is told two hundred and is wrong pays fees for a decade to find out.

**Data:** `Fund.csv` (50 × 2,000) — monthly excess returns, in per cent, for 2,000 fund managers over the same 50 months. Rows are months, columns are managers. An excess return is already net of the benchmark, so a manager with no skill has a true mean of exactly zero.
**Methods:** Chapter 13 (FWER, Bonferroni, Holm, FDR, Benjamini–Hochberg) with Chapter 0 §7 (hypothesis tests, $p$-values, power) · **After:** Lecture 12 · **Time:** 3–5 hours
**Deliverable:** one number for the trustee, plus a one-page memo in the notebook's final markdown cell.

This is the last project of the course, and it is the one where the machinery most sharply contradicts the intuition. Read your own conclusion twice before you send it.

## The challenge

1. **Reproduce the adviser's shortlist.** Run the one-sample $t$-test against zero on all 50 months for every manager — `ttest_1samp(fund, 0.0, axis=0)` does all 2,000 at once — and report how many reach $p < 0.05$. This is the object under audit; it is not yet a finding.
2. **Say what chance alone would produce.** Compute the **expected number of false positives** under the *global null* — the hypothesis that not one of the 2,000 managers has any skill — at $\alpha = 0.05$ with $m = 2{,}000$. Then obtain the same quantity empirically, with its spread, using the sign-flip permutation of Chapter 13 §4. Both numbers go in the memo. Until you have them, you cannot say whether the adviser's shortlist is remarkable or unremarkable.
3. **Control the family-wise error rate.** Apply **Bonferroni** and **Holm** at a FWER of 0.05. Report how many managers survive each, and state in one sentence what the surviving set is a guarantee *about*.
4. **Control the false discovery rate.** Apply **Benjamini–Hochberg** at $q = 0.05$ **and** at $q = 0.10$, and plot the sorted $p$-values against the BH line. Report both counts. You will find that the answer to the trustee's question depends on a threshold nobody ever stated, and you must **argue your choice from the consequence** — what it costs *this* trustee to fund one unskilled manager, against what it costs them to overlook one skilled manager. "0.05 is conventional" is not an argument; it is a way of not making the decision.
5. **Read the survivors, do not merely count them.** The adviser claimed *outperformance*. Your test was two-sided. Break every set you have produced down by the **sign** of the $t$-statistic and report the table. Three lines of code, and it changes the number you hand over.
6. **Ask whether the global null is itself tenable.** Steps 3–5 ask which *individual* managers can be named. This step asks the much weaker population question: is it credible that **none** of the 2,000 has any skill at all? That is a single hypothesis, so no correction applies to it. Two routes are open — the **dispersion** of the 2,000 track records against the dispersion the null permits, and the **persistence** of a manager's average from one set of months to a disjoint set. Check the alternative explanations (fat tails, unequal volatilities, correlation between managers, autocorrelation within one) before you believe your answer.
7. **Break the seal, once.** Design one selection rule on the 35 training months alone, write down what you expect of it, and then call `evaluate_selection()` a single time on the 15 sealed months.
8. **Commit to one number,** and defend it in the memo.

## Rules

- **The audit uses all 50 months.** Steps 1–6 are an audit of the adviser's claim, and the adviser's claim rests on the whole record. Those steps yield counts rather than a portfolio, so they cannot contaminate Step 7.
- **The holdout months are sealed.** Any selection rule evaluated in Step 7 must be fitted on months 1–35 only. No threshold tuned on the holdout, no exploratory glance, no second attempt. The split is chronological, fixed in the starter at 35/15, and identical for every student — do not change it, and your number is then directly comparable with everyone else's.
- **One evaluation.** A held-out set is spent once. If you evaluate, adjust and evaluate again, your number has stopped estimating anything and the memo must say so.
- **Selecting nobody is a legal answer** in Step 7. Its holdout return is exactly zero, and zero beats a negative number. If that is where your reasoning leads, take it and defend it.
- **Every count needs its reference.** A count of significant results is meaningless without the count chance alone would have produced. Report them together, every time.
- **You may use** `numpy`, `pandas`, `matplotlib`, `scipy`, `statsmodels`, `scikit-learn`, `pygam`. No `seaborn`.
- **Seed everything.** `np.random.default_rng(2024)` or `random_state=2024`.

## What you must report

The final markdown cell is a memo to the trustee. It must contain, as explicit numbers:

| # | Quantity | Form |
|---|---|---|
| 1 | Managers with a **naive $p < 0.05$** over the 50 months | a count |
| 2 | **Expected false positives** under the global null at $\alpha = 0.05$ | a count from arithmetic, **and** the permutation mean and standard deviation |
| 3 | Managers surviving **Bonferroni** at 0.05 | a count |
| 4 | Managers surviving **Holm** at 0.05 | a count |
| 5 | Managers surviving **BH at $q = 0.05$** | a count |
| 6 | Managers surviving **BH at $q = 0.10$** | a count |
| 7 | The **sign breakdown** of the naive shortlist and of each surviving set | a small table: how many outperform, how many underperform |
| 8 | The **threshold you chose**, and why | one paragraph arguing from the cost of each kind of error to this trustee |
| 9 | Your verdict on the **global null**, with the statistic and its null reference | one number plus one sentence |
| 10 | Your **Step 7 rule** and its holdout result | holdout mean %/month, the gap to Baseline A and to Baseline B, the permutation $p$ |
| 11 | **The single number for the trustee** | one integer, in the first two lines of the memo, before any method |
| 12 | The **caveat** | one paragraph distinguishing what you failed to find from what is not there |

Number 12 is not decoration and it is not hedging. With 50 months and the volatility these funds carry, work out from the starter's §1 table how much skill a manager would need before your test could see it at all. A procedure that cannot detect a manager who beats their benchmark by ten per cent a year has not established that no such manager exists. **"We cannot identify skill" and "no manager is skilled" are different claims, and the trustee will act very differently on each.** Say which one you are making.

## How this is judged

| | Weak | Solid | Strong |
|---|---|---|---|
| **The count** | Reports the naive count as the answer | Reports it alongside what chance alone produces | Treats the naive count as an object to be explained, and explains it |
| **Correction** | One procedure, or `multipletests` called without knowing what it did | Bonferroni, Holm and BH at both $q$, correctly computed and correctly named | Also states what each procedure guarantees, and notices how fragile the BH count is to the threshold |
| **The threshold** | Uses 0.05 because it is 0.05 | Chooses and justifies a $q$ | Argues it from the trustee's asymmetric costs, and says what would change the choice |
| **Direction** | Never checks the sign; counts significant underperformers as evidence of skill | Reports the sign breakdown | Draws the inference the breakdown supports about the population, not just about the shortlist |
| **Discipline** | Holdout touched early, or more than once | Sealed until Step 7, one call | Sealed, *and* the memo records the expectation before the seal was broken and compares it with the result |
| **The caveat** | Absent, or "more data would help" | States that a null result is not proof of absence | Quantifies it — the smallest skill this design could have detected — and separates the population claim from the individual claims |
| **Honesty** | Hands the trustee a large number the evidence will not carry | Hands over a small number and defends it | Hands over the number the evidence supports even when it is zero, *and* declines to overclaim in the other direction either |

A memo that concludes **"no individual manager in this data set can be identified as skilled, here is the evidence, and here is what that does and does not mean"** scores *above* a memo naming two hundred stars it cannot support. **A correct negative result beats an overstated positive one** — that is the whole point of the course, and this is the project where it costs someone money. The one thing that earns no credit either way is a number that cannot be reproduced from the notebook that produced it.

## Getting started

Open [`project_6_starter.ipynb`](./project_6_starter.ipynb). It loads the data, prints the standard error that governs what this design can and cannot see, seals months 36–50, computes the two baselines you have to beat — Baseline A, allocating to all 2,000; Baseline B, the adviser's own rule fitted honestly — and gives you `evaluate_selection()`, which makes your number comparable with everyone else's. Note that **Baseline B's holdout return is negative**; it is a real baseline and beating it is not automatic. Your work begins at the cell marked **Step 1**.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ChrisW09/Quantitative-Research-Methods/blob/main/Projects/project_6_fund/project_6_starter.ipynb)

Do not read `SOLUTION_NOTES.md` until you have a memo of your own.
