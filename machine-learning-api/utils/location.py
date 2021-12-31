from dataclasses import dataclass
from typing import Optional, Tuple

from uszipcode import SearchEngine

search = SearchEngine(simple_zipcode=True)


@dataclass
class Location:
    zipcode: str
    long: Optional[float] = None
    lat: Optional[float] = None

    def set_lat_and_long(self) -> None:
        result = search.by_zipcode(self.zipcode)
        self.long, self.lat = result.lng, result.lat

    def get_lat_and_long(self) -> Tuple[float, float]:
        return self.lat, self.long
