"""Client for the OpenF1 API (https://openf1.org). Historical data is free, no key.

Wrap only the endpoints this project needs: meetings, sessions, laps, pit, drivers.
Return plain lists of dicts so the bronze layer can write them verbatim.

TODO: implement a request helper (timeout + retry on 429/network) and the
endpoint functions. Confirm the lap fields you depend on: st_speed,
duration_sector_1/2/3.
"""
