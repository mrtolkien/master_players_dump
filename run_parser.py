import logging
import os
import json

from datetime import datetime
from concurrent.futures.thread import ThreadPoolExecutor

import riotwatcher

try:
    lol_watcher = riotwatcher.LolWatcher(os.environ["RIOT_API_KEY"])
except KeyError:
    logging.error("'RIOT_API_KEY' environment variable not found.")
    exit(1)

try:
    RANKED_QUEUE_NAME = os.environ["RANKED_QUEUE_NAME"]
except KeyError:
    RANKED_QUEUE_NAME = "RANKED_SOLO_5x5"

try:
    SERVERS = os.environ["SERVERS"].split(",")
except KeyError:
    SERVERS = ["KR", "EUW1"]


print("Starting masters player parsing")

for platform_id in SERVERS:
    print(f"Starting server {platform_id}")

    with ThreadPoolExecutor() as executor:
        masters = executor.submit(lol_watcher.league.masters_by_queue, platform_id, RANKED_QUEUE_NAME)
        gms = executor.submit(lol_watcher.league.grandmaster_by_queue, platform_id, RANKED_QUEUE_NAME)
        challengers = executor.submit(lol_watcher.league.challenger_by_queue, platform_id, RANKED_QUEUE_NAME)

    data = [
        {
            "summonerId": r["summonerId"],
            "summonerName": r["summonerName"],
            "leaguePoints": r["leaguePoints"],
            "wins": r["wins"],
            "losses": r["losses"],
        }
        for r in sorted(
            masters.result()["entries"] + gms.result()["entries"] + challengers.result()["entries"],
            key=lambda x: -x["leaguePoints"],
        )
    ]

    with open(
        f"/dump/{platform_id}-{datetime.now().isoformat(timespec='minutes').replace(':', '-')}.json", "w+"
    ) as file:
        json.dump(data, file)

print("Parsing and dumping down, sleeping for 24 hours")
