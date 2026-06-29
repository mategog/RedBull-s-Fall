# F1 Performance Analysis — The Red Bull Decline, 2023–2026

A data engineering and analytics project that traces Red Bull Racing's path from total
dominance in 2023 to the 2026 regulation reset: when the first cracks appeared, how rivals
closed the gap, and what the new-formula cars reveal in the data.

**Live app:** _coming soon_ · **Stack:** PySpark · Delta Lake · Streamlit

---

## What this answers

A concrete, falsifiable question instead of a generic dashboard: **when and how did Red Bull
lose its edge?** The pipeline ingests real telemetry and race results across four seasons and
four teams, then surfaces the trends — straight-line speed, cornering performance, pit-stop
strategy, and championship progression — that explain the shift.

---

## Architecture — Medallion (Bronze / Silver / Gold)

```
Data sources
├── OpenF1 API     (telemetry, pit stops, per-lap data)
└── Jolpica F1 API (season results, championship standings)
        │
        ▼
Bronze
└── Raw JSON / Parquet, ingested unchanged
        │
        ▼
Silver  (cleaned, normalized — PySpark)
├── Retirements handled
├── Safety-car periods flagged
└── Team / driver joins
        │
        ▼
Gold  (aggregated analyses)
├── Championship progression across a season
├── Straight-line speed trend per team
├── Cornering vs. straight-line performance
├── Pit-stop strategy effectiveness
└── Qualifying vs. race-pace delta
```

The Bronze layer keeps source data verbatim so transformations stay reproducible and
re-runnable. Silver normalizes and joins; Gold holds the analysis-ready aggregates the UI reads.

---

## Tech stack

| Layer        | Tool                                   |
|--------------|----------------------------------------|
| Data sources | OpenF1 API + Jolpica F1 API            |
| Pipeline     | PySpark on Databricks Community Edition |
| Storage      | Delta Lake (medallion architecture)    |
| UI           | Streamlit (single page)                |
| Version ctrl | GitHub                                  |

---

## Data scope

- **Teams:** Red Bull, McLaren, Ferrari, Mercedes
- **Drivers:** 8 (two per team)
- **Seasons:** 2023–2026
- **Volume:** ~8 million rows of telemetry

The team set is intentionally limited to the top four to stay within Community Edition cluster
limits while keeping the narrative focused on the title fight.

---

## Project structure

```
f1-performance-analysis/
├── README.md
├── LICENSE
├── notebooks/
│   ├── 01_bronze_ingestion.ipynb
│   ├── 02_silver_transformation.ipynb
│   └── 03_gold_aggregation.ipynb
├── streamlit/
│   └── app.py
├── utils/
│   ├── openf1_client.py
│   └── jolpica_client.py
└── requirements.txt
```

---

## Running it locally

> **Prerequisites:** Python 3.10+, a Databricks Community Edition workspace (free), and Git.

1. **Clone and install**
   ```bash
   git clone https://github.com/<your-username>/f1-performance-analysis.git
   cd f1-performance-analysis
   pip install -r requirements.txt
   ```

2. **Run the pipeline (Databricks CE)**

   Import the notebooks under `notebooks/` into your Databricks CE workspace and run them in
   order:
   - `01_bronze_ingestion` — pulls from OpenF1 + Jolpica into the Bronze layer
   - `02_silver_transformation` — cleans, normalizes, joins
   - `03_gold_aggregation` — builds the analysis tables the UI consumes

   The clients in `utils/` handle the API calls; no API keys are required for either source.

3. **Launch the UI**
   ```bash
   streamlit run streamlit/app.py
   ```

---

## The UI

Single-page Streamlit app with two modes.

**Controls**
- Season selector: 2023 / 2024 / 2025 / 2026
- View toggle: **Team comparison** / **Driver comparison**

**Team view** — auto-loads a team's two drivers head-to-head:
- Driver-vs-driver performance across the season
- Intra-team top-speed difference
- Intra-team pit-stop times

**Driver / team comparison view** — multi-select, up to 4 at once:
- Championship progression across the season
- Average top speed per race
- Pit-stop strategy effectiveness

_Screenshot: TODO — add once the UI is built._

---

## Deployment

Streamlit needs a persistent Python process, so the primary deploy target is
**Streamlit Community Cloud** (free, native support). A static/serverless host like Vercel
does **not** run Streamlit without an additional adapter, so it is not the default path here.

---

## Known limitations

| Limitation                          | Mitigation                                                      |
|-------------------------------------|----------------------------------------------------------------|
| Community Edition cluster size      | Scope limited to the top 4 teams; partitioned reads            |
| OpenF1 telemetry only from 2023     | Jolpica covers historical season/standings data                |
| Single maintainer, limited hours    | Scope deliberately not expanded beyond the four-team narrative |

---

## Data sources & licensing

The **code** in this repository is released under the [MIT License](LICENSE).

The **data** is **not** redistributed here — it is fetched on demand from third-party APIs and
remains subject to their terms:

- [OpenF1](https://openf1.org/) — live and historical F1 telemetry and timing
- [Jolpica F1 API](https://github.com/jolpica/jolpica-f1) — season results and standings
  (the maintained successor to the deprecated Ergast API)

This is an independent, non-commercial analysis project. It is **not affiliated with, endorsed
by, or associated with** Formula 1, the FIA, or any team. "F1", "Formula 1", and team names are
trademarks of their respective owners and are used here for identification only.
