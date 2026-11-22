# Nemo Climb background-generation instructions

Use the master prompt below once per game zone. Replace only the bracketed zone fields for each image. Generate one background per request; do not ask for a collage or a sheet of variations. Save each accepted image as `background_<zone>.png`, for example `background_forest.png` or `background_clouds.png`.

## Master prompt

```text
Create one finished 2D game background for Nemo Climb, a vertical platform-jumping game. This image fills the entire game window behind the player and platforms. It is a background environment only, not a gameplay screenshot or a level map.

ZONE
- Zone name: [ZONE NAME]
- Environment and visual idea: [DESCRIBE THIS ZONE IN ONE OR TWO SENTENCES]
- Main colors: [PALETTE]
- Distinctive distant details: [A FEW THEMATIC DETAILS, SUCH AS CLOUDS, FARAWAY TREETOPS, OR DISTANT ROCK FORMATIONS]

STYLE MATCH
Create polished, stylized 2D game environment art with clean shapes, soft depth, and a restrained palette. Use the same illustration style, line treatment, detail density, lighting direction, and overall contrast as the other Nemo Climb zone backgrounds. Make this zone visually distinct through its environment and palette while keeping the game's shared visual style. The look should remain attractive when reduced to 540x720 pixels.

CANVAS AND COMPOSITION — FOLLOW EXACTLY
- One landscape-free, portrait canvas with a 3:4 aspect ratio. Preferred output size: exactly 1080x1440 pixels (the game window is 540x720).
- Fill the full image edge-to-edge. Do not add a frame, border, margin, mockup, device, or page around it.
- Design it to be displayed as a single screen-filling image. Do not include a camera horizon or a foreground floor at the bottom.
- Keep the central play area visually quiet: approximately the middle 60% of the image width and the middle 70% of its height should use broad, low-detail shapes and gentle value changes. Put the most detailed scenery near the outer edges and in the distant background.
- Use soft atmospheric depth so gameplay sprites and platforms remain easy to see over the image. Avoid bright high-contrast details behind the center of the play area.
- Keep a similar overall brightness and contrast to the other zone backgrounds so cross-fading between zones looks smooth. The zone can use its own palette, but avoid a sudden full-frame white, black, or neon treatment.

DO NOT INCLUDE
- Any characters, creatures, silhouettes that could be mistaken for characters, platforms, ledges, stairs, ladders, bridges, ropes, climbable objects, spikes, hazards, coins, collectibles, or gameplay paths.
- UI, score text, labels, letters, numbers, logos, watermarks, interface panels, or a title.
- A foreground object crossing the center of the image or a strong horizontal band that looks like a platform.
- Pixel-art sprite frames, a grid, a collage, multiple alternative images, or a tiled contact sheet.

OUTPUT
Return one finished image file named `background_[ZONE SLUG].png`. Prefer PNG. The image must have the exact same 3:4 framing as every other zone background. If exact dimensions are unavailable, preserve the 3:4 aspect ratio and do not add padding or crop marks.
```

## Example zone descriptions

Use one of these as a starting point for the bracketed environment fields, or write your own:

- **Forest canopy** — A high view through layered evergreen treetops, with distant hills and a few shafts of warm light. Palette: deep teal, leaf green, muted gold.
- **Cloud layer** — Open sky above soft clouds, with distant pale blue mountain shapes and subtle sunlight. Palette: sky blue, cool white, muted lavender.
- **Rock summit** — Tall distant mountain walls and a hazy open sky, with sparse small plants only near the far edges. Palette: slate blue, muted stone, warm sunrise orange.
- **Night climb** — A calm deep-blue night sky with small distant stars and faint cloud shapes. Palette: navy, indigo, muted cyan, a few soft warm lights.

## Consistency checklist

Before adding a background to `Assets/`, confirm that it:

- Is one image, not a collage or a set of variations.
- Uses a portrait 3:4 canvas and can be cropped or resized to 540x720 without changing the composition.
- Contains no characters, platforms, hazards, collectibles, or text.
- Leaves the center calm enough for the player and platforms to stand out.
- Uses the same style and approximate contrast as the other backgrounds.
- Uses the filename `background_<zone>.png` with a short lowercase zone name.
