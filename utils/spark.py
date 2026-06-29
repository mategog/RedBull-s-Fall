"""get_spark(): return a SparkSession for the current target.

Local PySpark vs Databricks Connect (Free Edition serverless), chosen by the
SPARK_TARGET env var. The rest of the pipeline calls get_spark() instead of
importing SparkSession directly, so the same code runs in both places.

TODO: implement get_spark(app_name). Remember Free Edition needs
DatabricksSession.builder.serverless(True) — there are no classic clusters.
"""
