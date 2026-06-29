"""Bronze layer: ingest raw source data verbatim — no cleaning, joins, or renames.

Logic lives here as importable functions so it's testable and callable from a
thin notebook runner. Re-runnable (overwrite mode).

TODO: collect a season's race laps (meetings -> sessions -> laps) and
constructor standings, then write them out partitioned by year.
"""
