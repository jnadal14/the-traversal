# The Traversal

A film photography portfolio by Jacob Nadal, documenting landscapes and quiet moments through the deliberate eye of analog photography.

🌐 **Live site**: [jnadal14.github.io/the-traversal](https://jnadal14.github.io/the-traversal)

![The Traversal](IMAGES/01.jpg)

## About

The Traversal is an ongoing visual journey, an exploration of light, landscape, and the quiet moments that exist between destinations. Working primarily with 35mm film, each image is a meditation on presence and place. From the rugged peaks of the Pacific Northwest to the golden hours along coastal shores, the work captures the essence of traversing through both geography and time.

## Features

- **Masonry Gallery**: Responsive 3-column layout that adapts to all screen sizes
- **Video Integration**: 9 looping video clips interspersed throughout the gallery
- **Lightbox Viewer**: Click any image to view in full resolution
- **Fullscreen Video**: Click videos to enter fullscreen with audio
- **Minimal Design**: Clean, distraction-free presentation focused on the work

## Tech Stack

- Pure HTML, CSS, and vanilla JavaScript
- No frameworks or build tools required
- Google Fonts (Cormorant Garamond, Darker Grotesque)
- CSS Columns for masonry layout
- Fully responsive design

## Project Structure

```
the-traversal/
├── index.html          # Landing page (infinite-scroll intro; click to enter)
├── mosaic.html         # Main website / mosaic (single-page app)
├── gallery-manifest.js # Overview gallery order (images + videos) — edit to add/reorder
├── README.md           # This file
├── LICENSE             # MIT License
├── CLIPS/              # Gallery videos (order-prefixed) + WORK subfolder
│   ├── 01_AWAGA_1.mp4 … 09_SAS_2.mp4
│   └── WORK/           # Work panel videos
└── IMAGES/             # Photography (numbered gallery files + new/ + WORK/)
    ├── new/            # Drop new photos here, then list paths in gallery-manifest.js
    └── WORK/           # Work panel images
```

### Adding photos to the gallery

Put new files in `IMAGES/new/` with **URL-safe names** (e.g. `my-shot.jpg`, no spaces). Edit **`gallery-manifest.js`** and add a line where you want the image:

`{ type: 'image', src: 'IMAGES/new/my-shot.jpg' },`

After adding large JPEGs, run **`./scripts/optimize-gallery-images.sh`** so pages load in a few seconds on real networks.

Reorder by moving lines. Videos use `{ type: 'video', src: 'CLIPS/...' }`.

## Local Development

No build process required. Simply open `index.html` in a browser or run a local server:

```bash
# Python 3
python -m http.server 8000

# Then visit http://localhost:8000
```

## Contact

- **Email**: jacob24@rogers.com
- **Location**: Vancouver, British Columbia

## License

MIT License - See [LICENSE](LICENSE) for details.

---

*© 2025 Jacob Nadal*

