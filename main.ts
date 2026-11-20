// Entry program for the make.fun gta6-meme-x-01 bounty.
//
// The entry itself is a public post on X: its first picture is the meme
// in meme.png (drawn by make_meme.py) and its text is in CAPTION.txt.
// The house reads that post from X on its own. All this program has to
// do is hand the house the post's address, which lives in POST.json at
// the root of this repository, by copying it into the output directory.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

function handOverPostFile(from: string, to: string): void {
  copyFileSync(from, to);
}

try {
  handOverPostFile(source, target);
} catch (error) {
  console.error(`could not copy POST.json from ${source}: ${(error as Error).message}`);
  process.exit(1);
}
