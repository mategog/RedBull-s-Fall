"""Offline unit tests for the OpenF1 client — mock the network, run fast.

TODO: test request shaping (correct URL/params) and error handling
(non-list payload, retries-then-raise). Patch requests.get; don't hit the API.
"""
