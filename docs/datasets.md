# Datasets

The course datasets live in `ALL CSV FILES - 2nd Edition/` and are distributed
by the textbook authors at [statlearning.com](https://www.statlearning.com) for
use with the book.

```{admonition} How the notebooks resolve data
:class: tip

**12 of the 13 datasets used in the labs load straight from the `ISLP`
package**; the one that isn't in ISLP (`Advertising`) streams from the book's
official site, and the bundled CSVs act as an offline fallback. You should
never have to download anything by hand.
```

## What's bundled

| File | Rows | Cols | Contents | Mainly used in |
|---|--:|--:|---|:--:|
| `Advertising.csv` | 200 | 5 | Sales against TV / radio / newspaper budgets | Ch 2–3 |
| `Auto.csv` | 397 | 9 | Fuel economy and specs of 1970s–80s cars | Ch 3, 5, 8 |
| `Bikeshare.csv` | 8 645 | 16 | Hourly bike rentals in Washington DC (counts) | Ch 4 (Poisson) |
| `Boston.csv` | 506 | 14 | Housing values in Boston suburbs | Ch 3, 8 |
| `BrainCancer.csv` | 88 | 9 | Survival times of brain-cancer patients | Ch 11 |
| `Caravan.csv` | 5 822 | 86 | Caravan-insurance purchases (highly imbalanced) | Ch 4 |
| `Carseats.csv` | 400 | 11 | Child car-seat sales at 400 stores | Ch 3, 8 |
| `Ch12Ex13.csv` | 999 | 40 | Gene-expression data for the Ch 12 exercise | Ch 12 |
| `College.csv` | 777 | 19 | Statistics for 777 US colleges | Ch 6 |
| `Credit.csv` | 400 | 11 | Credit-card balances and customer attributes | Ch 3, 6 |
| `Default.csv` | 10 000 | 4 | Credit-card default (the classification workhorse) | Ch 4 |
| `Fund.csv` | 50 | 2 001 | Monthly excess returns of 2 000 fund managers | Ch 13 |
| `Heart.csv` | 303 | 15 | Heart-disease diagnosis | Ch 8 |
| `Hitters.csv` | 322 | 20 | Baseball salaries and career statistics | Ch 6 |
| `Income1.csv` | 30 | 3 | Income vs. years of education (simulated) | Ch 2 |
| `Income2.csv` | 30 | 4 | Income vs. education and seniority (simulated) | Ch 2 |
| `OJ.csv` | 1 070 | 18 | Orange-juice brand purchases | Ch 8–9 |
| `Portfolio.csv` | 100 | 2 | Two asset returns — the bootstrap example | Ch 5 |
| `Publication.csv` | 244 | 10 | Time to publication of clinical trials | Ch 11 |
| `Smarket.csv` | 1 250 | 9 | Daily S&P 500 returns, 2001–2005 | Ch 4 |
| `Wage.csv` | 3 000 | 11 | Wages of Mid-Atlantic male workers | Ch 1, 7 |
| `Weekly.csv` | 1 089 | 9 | Weekly S&P 500 returns, 1990–2010 | Ch 4 |

`Auto.data` is the original whitespace-delimited version of `Auto.csv`, kept for
the exercise that demonstrates reading a non-CSV file.

## Loading a dataset

::::{tab-set}

:::{tab-item} From the ISLP package

```python
from ISLP import load_data

Boston = load_data("Boston")
Boston.head()
```
:::

:::{tab-item} From the bundled CSVs

```python
import pandas as pd
from pathlib import Path

DATA = Path("ALL CSV FILES - 2nd Edition")     # relative to the repo root
Boston = pd.read_csv(DATA / "Boston.csv", index_col=0)
```

Several files carry an unnamed index column (`Boston`, `College`, `Heart`,
`Income1`, `Income2`, `Bikeshare`, `BrainCancer`, `Publication`, `Fund`) —
pass `index_col=0` for those.
:::

:::{tab-item} Advertising (not in ISLP)

```python
import pandas as pd

url = "https://www.statlearning.com/s/Advertising.csv"
Advertising = pd.read_csv(url, index_col=0)
```
:::

::::

```{admonition} Missing values
:class: note

`Auto` contains a handful of rows with `?` in `horsepower`; ISLP's `load_data`
drops them, so a CSV fallback should do the same
(`pd.read_csv(..., na_values="?").dropna()`) for results to match the slides.
```

## Attribution

The datasets are © the textbook authors and are distributed by them at
[statlearning.com](https://www.statlearning.com) for use with the book. They are
bundled here only so the course runs offline — see
[Citation & licence](citation.md).
