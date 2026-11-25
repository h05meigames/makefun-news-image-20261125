# The World — 25 November 2026

A newspaper front page summing up Wednesday 25 November 2026's world news
in one image, for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125).

## The day's news

- **Lead — Ukraine war:** Russia's own published figures show almost
  500,000 deaths in the war in Ukraine (BBC, 25 Nov 2026).
- **Tech — Huawei** found guilty of stealing US trade secrets, acquitted of
  racketeering (BBC).
- **Space — Shenzhou-24:** Pakistan's first astronaut, Muhammad Zeeshan Ali,
  becomes the first foreigner on a Chinese crewed mission (BBC).
- **China:** Politburo member and Shanghai party chief Chen Jining probed in
  the widening graft crackdown — the fourth such inquiry since 2025
  (Reuters).
- **United States:** Kilmar Ábrego García leaves the US for Spain, ending
  the Trump deportation battle (BBC).
- **Gaza:** Israeli air strike kills Hamas's internal security chief; land-
  mine casualties soar in Syria (BBC).
- **Also today:** Microsoft declares "Code Red" after a historic outage; the
  US is set to unveil new tariffs on 16 trading partners; Sarkozy and Carla
  Bruni face trial; Senegal reinstated as 2025 Africa Cup of Nations
  winners; the Hera spacecraft returns to the asteroid crash site.

## How it works

`render_frontpage.py` draws the 1024×1024 front page with Pillow — no
network, no randomness, fully deterministic. `main.ts` (Node 22, standard
library only) copies `entry.png` to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` overrides the output directory outside the grader).

## Verify

```sh
python3 render_frontpage.py          # regenerates entry.png, byte-identical
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
sha256sum entry.png out/entry.png    # identical
```

## License

MIT — see `LICENSE`.

---

Built for the make.fun bounty — [https://make.fun/r/0ene8b3q](https://make.fun/r/0ene8b3q)
