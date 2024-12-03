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
CITY_MMDB = DATA_PATH / 'GeoLite2-City.mmdb'
ASN_MMDB = DATA_PATH / 'GeoLite2-Asn.mmdb'
QQWRY_DB: Path = DATA_PATH / "qqwry.dat"

GEO = geoip2.database.Reader(CITY_MMDB)
ASN = geoip2.database.Reader(ASN_MMDB)
QQWRY = QQwry()
QQWRY.load_file(str(QQWRY_DB))


def query_qqwry(ip: str) -> tuple[str, str, str]:
    country = ""
    city = ""
    provider = ""

    result = QQWRY.lookup(ip)
    if result:
        if "–" in result[0]:
            country, city = result[0].split("–", maxsplit=1)
        else:
            country = result[0]
        provider = result[1] if result[1].strip() != "CZ88.NET" else ""
    return country.strip(), city.strip(), provider.strip()


def query_geoip(ip: str) -> tuple[str, str, str]:
    country = ""
    city = ""
    provider = ""

    if ip == "127.0.0.1":
        return country.strip(), city.strip(), provider.strip()
    try:
        response = GEO.city(ip)
        country = response.country.name if response.country.name else ""
        city = response.city.name if response.city.name else ""
        country = response.country.names.get("zh-CN", country)
        city = response.city.names.get("zh-CN",city)
    except Exception as e:
        print(e)

    try:
        _res = ASN.asn(ip).autonomous_system_organization
        provider = _res if _res else ""
    except Exception as e:
        print(e)
    return country.strip(), city.strip(), provider.strip()

def merge_results(*res: str) -> str:
    if len(set(res)) == 1:
        return res[0]
    else:
        return " | ".join([r for r in res if r.strip()])


def query_ip(ip: str) -> QueryResult:
    country: str = ""
    city: str = ""
    provider: str | None  = None

    country_qqwry, city_qqwry, provider_qqwry = query_qqwry(ip)
    country_geo, city_geo, provider_geo = query_geoip(ip)

    country = merge_results(country_qqwry, country_geo)
    city = merge_results(city_qqwry, city_geo)
    provider = merge_results(provider_qqwry, provider_geo)

    return QueryResult(country, city, provider)


if __name__ == "__main__":
    print(query_ip("101.43.24.252"))