// news-image-20261118: a program that writes one image summing up
// Wednesday 18 November 2026's world news to /output/entry.png.
//
// The image is drawn in advance (see draw_news_image.py, which renders
// the 1024x1024 front page with Pillow) and shipped beside this file
// as entry.png. This program only copies it into place, so the graded
// run is deterministic, needs no network, and uses only the Node 22
// standard library. Both graded runs therefore write identical bytes.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// then open out/entry.png.

import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
// The gate allows at most 1 MiB; refuse to ship anything larger.
if (statSync(source).size > 1048576) {
  throw new Error("entry.png is larger than the 1 MiB gate limit");
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
