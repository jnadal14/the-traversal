# New photos for the gallery

1. Use **URL-safe names** (kebab-case, no `&`, `<`, or spaces), e.g. `coast-morning.jpg`.
2. Drop files here, then add `image('IMAGES/new/your-file.jpg', width, height),` in **`gallery-manifest.js`** where you want the image in the scroll. Including the pixel dimensions prevents layout shifts while the image loads.
3. After adding large scans, run from the project root:
   ```bash
   ./scripts/optimize-gallery-images.sh
   ```
   This resizes long edges to 2200px and recompresses JPEGs so the site stays fast.
