import requests
from waste_collection_schedule import Collection # type: ignore[attr-defined]
from waste_collection_schedule.service.ICS import ICS

import urllib

TITLE = "Landkreis Bamberg"
DESCRIPTION = "Source for Landkreis Bamberg"
URL = "https://www.abfalltermine-bamberg.de"
TEST_CASES = {
    "Dormitz": {"city": "Strullendorf"},
    "Schlüsselfeld - Obermelsendorf": {"city": "Schlüsselfeld - Obermelsendorf"}
}


class Source:
    def __init__(self, city, area):
        self._city = city
        self._ics = ICS()

    def fetch(self):
        place = urllib.parse.quote(self._city)
        r = requests.get(
            f"https://www.abfalltermine-bamberg.de/Bamberg/Landkreis/{place}/ics?RESTMUELL=true&BIO=true&YELLOW_SACK=true&DIAPER_SACK=true&PAPER=true&SPERRMUELL=true&PROBLEMMUELL=true"
        )
        r.encoding = r.apparent_encoding
        dates = self._ics.convert(r.text)

        entries = []
        for d in dates:
            entries.append(Collection(d[0], d[1]))
        return entries
