# New photos for the gallery

1. Use **URL-safe names** (kebab-case, no `&`, `<`, or spaces), e.g. `coast-morning.jpg`.
2. Drop files here, then add a line in **`gallery-manifest.js`** where you want the image in the scroll.
3. After adding large scans, run from the project root:
   ```bash
   ./scripts/optimize-gallery-images.sh
   ```
   This resizes long edges to 2200px and recompresses JPEGs so the site stays fast.
