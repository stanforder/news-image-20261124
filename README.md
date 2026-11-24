# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/stanforder/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/stanforder/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

The world in one day — Tuesday 24 November 2026, summed up in one image.
Entry for the make.fun bounty
[`news-image-20261124`](https://make.fun/bounty/news-image-20261124):
sum up 24 November 2026's world news in one image.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## The image

A "daylight atlas" poster — ivory paper, deep teal and burnt orange —
drawn programmatically with Pillow by `draw_entry.py` (build-time only).
The submitted program `main.py` only copies the finished `entry.png` to
`/output/entry.png` — standard library only, no network, byte-identical on
every run.

The layout follows the winning anatomy of the 22 Nov final rank 1
(@bagarte, 85.4411%): 29 dated stories in 7 regions — 13 numbered cards
(3 heroes + a "Day in Numbers" sidebar) and 16 briefs, a UTC timeline, a
dotted world map with numbered pins, and a DATE CHECK box that keeps other
days' news off the page.

Headline: **Tuesday 24 November 2026 — The World in One Day**

- **War (hero):** Israeli strikes kill 9 in Gaza on Tuesday, including an
  UNRWA worker; the nominal October ceasefire keeps being violated.
- **Space (hero):** China names the Shenzhou-24 crew — Pakistani pilot
  Muhammad Zeeshan Ali, 40, will be the first foreign astronaut aboard
  Tiangong.
- **Disaster (hero):** the Indonesia candy-factory fire toll rises to 26
  dead, 8 still missing; 600+ rescuers search the second floor.
- **War:** Russia strikes Zaporizhzhia overnight — 2 dead, 22 injured.
- **Football:** Real Madrid rout PSV 5-1 to stay perfect in the Champions
  League; City and Arsenal are held to draws.
- **Markets:** the Dow crosses 50,000 for the first time as Nvidia slides
  5.9% after Monday's 31% surge.
- **Sanctions:** the US hits Iran with new sanctions on its "shadow
  banking" network.
- **Iran:** Netanyahu urges Trump to strike Iran; Mossad's chief is said
  to push for a new war.
- **Oil:** Iraq orders the takeover of Kurdish oilfields and crossings.
- **Quake:** a M5.6 earthquake shakes Nepal's Tibet border region.
- **Blast:** a car bomb wounds 23 outside the governor's office in
  Villavicencio, Colombia.
- **War:** a Sudan drone attack kills 4 civilians in Khartoum and damages
  a UN building.
- **Defence:** a Russian aircraft enters South Korea's air defence zone.
- Plus 16 more stories in the briefs, a world map with numbered pins, and a
  date check that keeps other days' news off the page.

Sources checked 24–25 Nov 2026: Reuters, AP, BBC, Xinhua, The Hindu,
Daily Summary of World, UEFA.

To regenerate the image from its source (needs Pillow, build-time only):

```sh
python3 draw_entry.py
```

## Licence

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zqrkg9m9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
