from typing import Optional
from dataclasses import dataclass
from pathlib import Path

import geoip2.database
from qqwry import QQwry


@dataclass
class QueryResult:
    country: Optional[str]
    city: Optional[str]
    provider: Optional[str]


# 加载 GeoLite2 数据库
DATA_PATH = Path(__file__).parent / "data"
MMDB = DATA_PATH / 'GeoLite2-City.mmdb'
QQWRY_DB: Path = DATA_PATH / "qqwry.dat"

geo = geoip2.database.Reader(MMDB)
qqwry = QQwry()
qqwry.load_file(str(QQWRY_DB))

def query_ip(ip: str) -> QueryResult:
    country: str | None = None
    city: str | None = None
    provider: str | None = None

    result = qqwry.lookup(ip)
    if result:
        if "–" in result[0]:
            country, city = result[0].split("–", maxsplit=1)
        else:
            country = result[0]
        provider = result[1]
    else:
        try:
            response = geo.city(ip)
        except geoip2.errors.AddressNotFoundError:
            return QueryResult(None, None, None)
        country = response.country.name
        city= response.city.name
    if country:
        country = country.strip()
    if city:
        city = city.strip()
    if provider:
        provider = provider.strip()
    return QueryResult(country, city, provider)


if __name__ == "__main__":
    print(query_ip("101.43.24.252"))