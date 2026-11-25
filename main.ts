// news-image-20261125 — "The World — 25 November 2026" (Node 22, standard
// library only): the entry image is entry.png beside this file, drawn by
// render_frontpage.py (Pillow, no network, no randomness), and this program
// copies it to /output/entry.png. The judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
