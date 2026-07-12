# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Source material for a single conference talk (Python Brasil 2026): **"Caçando bugs em Python: do olho humano à IA"** ("Hunting bugs in Python: from the human eye to AI") by Daniel Diniz (devdanzin). All content — script, slides, code sample — is in Brazilian Portuguese (pt-BR). There is no application, package, build system, or test suite here; the deliverable is the talk itself.

The talk's central metaphor runs through every file: hunting for bugs in code is compared to a biologist surveying fauna in unstudied terrain (manual review = direct observation, static analysis = tracking spoor/footprints, fuzzing = camera traps with bait, AI-based analysis = a team of specialist biologists working in parallel). Keep this metaphor consistent when editing narration or slide text.

## Repository layout

- `roteiro.md` — the full spoken script/outline for the talk, organized with headers matching the slide sections (Introdução, Um breve paralelo, Técnicas, Ferramentas, Resultados e Conclusões, Fechamento). `[...]` marks a deliberate pause/transition in the narration, not missing content.
- `capivara.py` — the single example code snippet shown live during the talk (function `max_power`). Its embedded copy lives inside `apresentacao/espacial.html` (search for `max_power`) and must be kept byte-for-byte identical to the standalone file, since both `roteiro.md` narration and live tool demos depend on its exact shape.
- `apresentacao/espacial.html` — the actual slide deck, built on **impress.js** (a spatial/zooming presentation engine, not a linear slide deck). There is no templating or build step: this file is opened directly in a browser.
- `apresentacao/css/impress-common.css` — impress.js base styles (vendored, don't hand-edit for content changes).
- `apresentacao/css/impress-demo.css` — this talk's actual presentation styling (fonts, layout, animations, slide-specific classes).
- `apresentacao/js/impress.js`, `apresentacao/js/highlight/` — vendored JS libraries (impress.js for the spatial engine, highlight.js for code syntax highlighting in the code-sample slide). Not managed by a package manager; there is no `package.json`.
- `apresentacao/images/` — presentation assets: biology-metaphor photos/gifs (capivaras, footprints, forest background) and tool logos (ruff, mypy, mastodon, etc.).

## How the slide deck is structured

`espacial.html` positions every slide in 3D space via `data-x` / `data-y` / `data-scale` attributes consumed by impress.js — the "camera" flies between coordinates rather than advancing linearly. The file is organized into commented sections marking each camera movement:

- Early slides are grouped into **"VOOS" (flights)** — HTML comments like `<!-- VOO 1 — ... -->` mark each distinct camera position/zoom used while flying over the background forest image (`#fundo`, `images/visao_floresta_05.png`). Slides that share a flight share the same `data-x`/`data-y`/`data-scale`. Some `.step` divs have no content and exist purely as camera waypoints (e.g. `#floresta_01`, `#observacao`).
- After the comment **"FIM DO VOO"**, the camera stops moving: all remaining slides sit at the same fixed position (`data-x="0" data-y="0" data-scale="11"`) and are shown as stacked front-facing cards.
- A final `#overview` step (no content) zooms out to show the whole spatial layout.

Key CSS classes used on slides (defined in `impress-demo.css`):
- `.step` — required impress.js marker for anything the camera visits.
- `.slide` — visual card styling (background, padding, flex-centered content) for content slides; omitted on pure camera-waypoint steps.
- `.appear` — fades the slide in.
- `.substep` — reveals list items/paragraphs one at a time as `.substep` children.
- `.sudden` — an abrupt (non-eased) transition, used where a normal `.appear` fade would be visually wrong.
- `.absolute` — switches an element to `position: absolute` (impress.js otherwise repositions elements as it flies).

When adding a new slide: pick (or reuse) the right `data-x/data-y/data-scale` for its position in the flight path, add `.step` (+ `.slide` if it has visible content), and place it near its narration counterpart in `roteiro.md`.

## The `capivara.py` example and live tool demos

`capivara.py`'s `max_power` function is intentionally buggy: the `else` branch computes `result` but never returns it, so callers reaching that branch get `None`. This is the running "Uai" bug (see `roteiro.md`'s "Desenvolvimento Guiado por Uai" bit) used to demonstrate each bug-hunting technique. The talk runs real tools live against this file — verify these behaviors before changing the file or the narration that describes them:

```bash
ruff check capivara.py              # passes clean by default — the bug is invisible here
ruff check --select RET capivara.py # RET503 flags the missing return (also RET505 re: the else)
mypy capivara.py                    # passes by default (mypy skips bodies of unannotated functions)
# adding `-> int` param/return annotations to max_power makes mypy report
# "Missing return statement" WITHOUT needing --strict
```

If you touch `capivara.py`, re-run these commands and update `roteiro.md`'s tool-demo narration (and the embedded snippet in `espacial.html`) to match the actual output.

## Validating changes to the slide deck

`espacial.html` is checked with `html-validate` (`npx html-validate apresentacao/espacial.html`) before commits that touch it. There is no config file in the repo, and the file consistently uses self-closing void elements (`<img />`, `<meta />`, `<br />`); `html-validate`'s out-of-the-box `void-style` rule flags every one of these as an error. Don't treat that as a regression to fix — it's the file's existing style. Only investigate new `html-validate` output that isn't `void-style`/`doctype-style` noise.
