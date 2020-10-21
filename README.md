# Master+ Players Dump
A very simple utility to dump all master+ players once a day.

# Usage
- Create a `docker-compose.yml` file with this content:

```yaml
version: "3.8"

services:
  master_players_dump:
    image: mrtolkien/master_players_dump
    environment:
      - RIOT_API_KEY=XXXXXXXXXXXXX
    volumes:
    - type: bind
      source: ./dump
      target: /dump
```

- Change `RIOT_API_KEY=XXX` to you Riot API key.

- *Optional*
    - Add `- SERVERS=...` if you want to specify which servers to save

- Create a `/dump` folder

- Run `docker-compose up -d`

- You’re good to go!
