
"""
Format of nginx log:
    [$time_local] - $remote_addr - $host - $uri - $http_referer - $http_user_agent - "$request" - $status';
"""

from datetime import datetime
from urllib.parse import unquote

from query_ip import query_ip
from db import Access, database


def process_log_row(row: str):
    """
    Decode the recode and save it to sqlite.

    Args:
        row (str): One line from the log.
    """
    dt_str, ip, host, uri, referer, agent, *_ = row.split(" - ")

    # filter blog accesses
    uri = unquote(uri.replace("\\x", "%"))
    if host != "blog.catbaron.com":
        return
    if not uri.endswith("html"):
        return
    if referer.endswith(".js"):
        return

    # convert datetime
    # dt_str is in form of "[30/Nov/2024:16:16:02 +0900]"
    dt_format = "%d/%b/%Y:%H:%M:%S %z"
    dt = datetime.strptime(dt_str[1: -1], dt_format)
    dt_str = dt.strftime("%Y/%m/%d %H:%M:%S %z")


    loc = query_ip(ip)
    database.create_tables([Access], safe=True)
    Access.create(
        datetime=dt,
        ip = ip,
        agent = agent,
        country = loc.country,
        city = loc.city,
        provider = loc.provider,
        host = host,
        uri = uri,
        referer = referer
    )
