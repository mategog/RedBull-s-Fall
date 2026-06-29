# notebooks/

Thin Databricks runners (Databricks **source format**, i.e. `.py` files with
`# COMMAND ----------` cell separators — these git-diff cleanly, unlike `.ipynb`).

Each notebook should stay thin: wire up Spark via `utils.spark.get_spark()` and
call the matching `pipeline/` module. Keep logic in `pipeline/`, not here.

Planned:
- `01_bronze_ingestion.py` -> calls `pipeline.bronze`
- `02_silver_transformation.py` -> calls `pipeline.silver`
- `03_gold_aggregation.py` -> calls `pipeline.gold`

## Two ways to create these
- **In Databricks:** connect this repo via Repos (Git folders), then create the
  notebook inside the repo folder and save — it lands here as source format.
- **In PyCharm:** author the `.py` here directly and let Databricks pick it up
  on sync. Use the Databricks plugin or `databricks` CLI to push/run.
