# Setup — hybrid local + Databricks Free Edition

You develop and unit-test in a local PySpark venv (fast, offline), and run the
pipeline against **Databricks Free Edition** (serverless) when you want real
scale. The same code runs in both — `utils/spark.get_spark()` picks the backend
from the `SPARK_TARGET` env var.

> **Why two venvs?** `pyspark` and `databricks-connect` both ship the `pyspark`
> Python package and **conflict** if installed together. Keep them separate.

---

## 1. Prerequisites

- Python 3.10+
- Java 11 or 17 (PySpark needs a JVM) — `java -version` to check
- A free **Databricks Free Edition** account: https://www.databricks.com/learn/free-edition
  (Community Edition was retired Jan 1, 2026 — Free Edition replaces it.)

---

## 2. Local environment (default — use this for day-to-day dev)

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env                 # SPARK_TARGET=local is the default
```

Run the tests and a local pipeline:

```bash
pytest -q                            # unit tests, no network
python notebooks/01_bronze_ingestion.py   # writes parquet under ./data
streamlit run streamlit/app.py       # once the UI exists
```

If you ever hit `UnknownHostException` from Spark, the factory already pins the
driver to loopback; as a fallback, `export SPARK_LOCAL_IP=127.0.0.1`.

---

## 3. Databricks environment (when you want to run on Free Edition)

Use a **separate** venv:

```bash
python3 -m venv .venv-databricks
source .venv-databricks/bin/activate
pip install -r requirements-databricks.txt
```

Authenticate (token from Databricks → Settings → Developer → Access tokens):

```bash
export DATABRICKS_HOST="https://dbc-xxxxxxxx-xxxx.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi..."
export SPARK_TARGET=databricks
```

Then the exact same command runs on serverless:

```bash
python notebooks/01_bronze_ingestion.py
```

`get_spark()` calls `DatabricksSession.builder.serverless(True)` — required,
because Free Edition has no classic clusters to attach to.

### Or run inside the Databricks workspace
Repos → Add Repo → paste the GitHub URL, then open
`notebooks/01_bronze_ingestion.py` and run it on serverless. The runner detects
the injected `spark` session automatically.

---

## 4. Project layout

```
config.py                  # scope (teams/seasons) + storage paths
utils/
  spark.py                 # get_spark(): local vs databricks
  openf1_client.py         # OpenF1 API (telemetry, laps, pit)
  jolpica_client.py        # Jolpica API (standings, results)
pipeline/
  bronze.py                # ingestion logic (importable, tested)
  # silver.py, gold.py     # next
notebooks/
  01_bronze_ingestion.py   # thin runner -> pipeline.bronze
tests/                     # offline unit tests
streamlit/app.py           # UI (to build)
```

**Pattern:** logic lives in `pipeline/` and `utils/` as importable, testable
modules. Notebooks stay thin — they wire up Spark and call the modules. This
keeps clean git diffs and real unit tests instead of logic trapped in notebook
JSON.

---

## 5. Suggested build order

1. `pipeline/bronze.py` — already stubbed; run it, confirm parquet lands.
2. `pipeline/silver.py` — clean, normalize, join drivers/teams, flag retirements.
3. `pipeline/gold.py` — the analysis tables (speed-trap trend, pit strategy, etc.).
4. `streamlit/app.py` — read gold, build the two views from the README.
5. Switch local writes from `.parquet` to Delta once you're on Databricks.
