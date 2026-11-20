# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/airdropgodx24/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/airdropgodx24/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Leonida flu: a GTA 6 launch-day meme, drawn entirely in code. A gamer who waited thirteen years for GTA 6 calls in sick on launch day, while make.fun's ghost mascot, working the beach club next door with its magenta star coin, needs no sick note at all. The meme is the first picture of a public post on X, and that post is the entry: the house reads it from X and an AI judge compares it with the other posts, two at a time, for a share of $500.

What is in here:

- `make_meme.py` draws `meme.png` from basic shapes with Pillow: the Leonida sunset, the skyline and its make.fun beach-club sign, the sick gamer, and the ghost. No image files are loaded, so the picture is made here, end to end.
- `meme.png` is the picture that goes on the post, 1200 by 1200.
- `CAPTION.txt` is the exact text of the post, play code and all.
- `POST.json` names the post on X once it is up.
- `main.ts` copies `POST.json` to the output directory, which is all the grader asks the program to do.

## Run it

```sh
python3 make_meme.py
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ty7xpzdw&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
