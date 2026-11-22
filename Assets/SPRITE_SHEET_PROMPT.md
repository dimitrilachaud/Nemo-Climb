# Nemo Climb character sprite-sheet prompt

Use this prompt once for the default character, then reuse it for every new character. Change only the **Character design** paragraph between generations. Save each result as `character_<slug>.png` (for example, `character_default.png`). Keep the canvas layout and animation poses identical across characters.

## Copy/paste prompt

```text
Create a production-ready 2D game character sprite sheet for the Nemo Climb vertical platformer. This is a single-character animation asset, not a game screenshot, concept sheet, or character lineup.

CHARACTER DESIGN
Create one original, friendly, readable climbing-game character: a small adventurer with a clear silhouette, expressive face, and a compact outfit suitable for a vertical platform game. Use a distinctive but restrained color palette. Keep the same exact character identity, proportions, face, clothing, accessories, outlines, lighting, and rendering style in every frame. Do not add equipment that changes position or size unpredictably between frames.

ART STYLE
Clean, polished 2D pixel art intended for a small game sprite. Crisp pixel clusters, hard pixel edges, consistent outline thickness, limited coordinated palette, no blur, no gradients that soften the pixels, no antialiasing, no 3D rendering, and no painterly texture. Face the character toward the right in every frame; the game can flip the frames horizontally for leftward movement.

CANVAS AND GRID — FOLLOW EXACTLY
- Deliver one PNG with a genuinely transparent RGBA background (alpha 0 everywhere outside the character and its permitted effect pixels). Do not use a checkerboard to represent transparency.
- Exact canvas size: 256 pixels wide by 320 pixels tall.
- The sheet is exactly 4 columns by 5 rows, with no margins, gutters, dividers, borders, labels, numbering, captions, logos, or watermark.
- Every cell is exactly 64 by 64 pixels. Cell (column 0, row 0) begins at canvas pixel (0, 0). No frame may cross a cell boundary.
- Use native pixel-art resolution. Do not place a white page or colored background behind the sprites.
- Treat each cell as an independent animation frame. Keep each pose centered horizontally and at a consistent scale. Keep the character's normal standing feet on the same baseline, y=60 within its cell, for all grounded poses. Keep all visible character pixels inside x=8..55 and y=3..60 of the cell. Jump poses may be raised but must remain within the cell. Keep effects inside the cell too.
- Leave transparent padding around the silhouette. Do not add a floor, platform, cast shadow, or detached particles that could be mistaken for part of another frame.

ANIMATION GRID — EXACT ROW ORDER, LEFT TO RIGHT
Row 1 (canvas y=0..63), IDLE: four subtle looping idle poses. Frame 1 neutral stance; frame 2 slight breathing rise; frame 3 blink or small expression change; frame 4 return toward the neutral pose. Small changes only; preserve the same feet baseline.
Row 2 (canvas y=64..127), WALK: four readable right-facing walk-cycle poses in this order: right-foot contact, passing pose, left-foot contact, passing pose. Alternate legs and arms clearly. Keep the feet at the same baseline and the body centered in each cell.
Row 3 (canvas y=128..191), JUMP: four poses in this order: takeoff/crouch, rising, apex, falling. Make the silhouette clearly airborne and distinct from the walk row. The sequence should read left-to-right as one continuous jump.
Row 4 (canvas y=192..255), HURT: four poses in this order: impact/flinch, recoil, stagger, recovery. Show a clear hurt reaction through pose and expression only. Do not add blood, text, icons, or a detached flash.
Row 5 (canvas y=256..319), POWER-UP: four poses in this order: gathering energy, energy building, peak power, settling into the normal stance. Use a restrained bright aura or small glow pixels around the character, fully contained inside that frame. Keep the character itself visible and unchanged in identity.

FRAME-TO-FRAME CONSISTENCY
Render exactly one full character in every cell. Do not omit, merge, duplicate, or reorder frames. Keep the head size, body proportions, palette, outline, facing direction, and center of mass consistent. Make adjacent poses visibly different enough to animate, but do not redesign the character between cells. The idle and walk rows must look grounded; jump poses must not touch a platform because no platform should be drawn.

OUTPUT CHECK
Before delivering, verify that the PNG is exactly 256x320, has transparency, and contains a clean 4x5 grid of 64x64 cells in the specified row order. If your image tool cannot produce that exact size or transparent PNG, say so and provide the closest lossless source at the same 4x5 layout without adding labels or a background; do not silently change the row order or cell count.
```

## Sheet layout for integration

| Row | Animation | Frames | Cell coordinates (column, row) |
|---:|---|---:|---|
| 0 | Idle | 4 | `(0,0)` through `(3,0)` |
| 1 | Walk | 4 | `(0,1)` through `(3,1)` |
| 2 | Jump | 4 | `(0,2)` through `(3,2)` |
| 3 | Hurt | 4 | `(0,3)` through `(3,3)` |
| 4 | Power-up | 4 | `(0,4)` through `(3,4)` |

Each cell is `64x64`. For example, the third walk frame is the crop `(x=128, y=64, width=64, height=64)`. The intended filename pattern is `character_<slug>.png`; use `character_default.png` for the first sheet. Keep the transparent background and do not trim individual cells, so all characters share the same crop coordinates and anchor.

## Quick acceptance check

- Image is one transparent PNG, exactly `256x320`.
- There are exactly 20 cells: four columns and five rows, each `64x64`.
- All five rows exist in the listed order, with four frames each.
- The same character faces right in every frame and fits inside each cell.
- No text, grid lines, page background, platform, or watermark is baked into the image.
- File name follows `character_<slug>.png`.
