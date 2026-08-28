#!/usr/bin/env bash
# Turn camera originals into web-deliverable loops.
#
# Reads from _masters/video/ (git-ignored, never published) and writes to
# assets/video/. Originals stay on disk, so this is re-runnable and the
# repository only ever carries the web copies.
#
# Why the settings are what they are. The masters are 4K at 25-45 Mbps. Shipping
# a lightly recompressed 4K file as a background loop is what used to stall the
# landing page: a 3.5s clip at 15 Mbps cannot stream in real time, so the browser
# sat on the poster instead. Downscaling to the size actually displayed and
# spending the bits there looks better and starts in a fraction of the time.
#
#   -g 24 / -keyint_min 24 / -sc_threshold 0
#       A keyframe every second. The masters carry 1-4 keyframes in total, so
#       looping or seeking forced a decode from the top of the clip.
#   -movflags +faststart
#       moov atom ahead of mdat, so playback can begin on the first bytes.
#   -an
#       These are silent background loops; an audio track is dead weight and
#       trips autoplay heuristics.
#   -crf 21 -maxrate 5000k
#       maxrate, not CRF, is the real control: this footage is detailed enough
#       that CRF 21-23 all clamp against the VBV buffer. Measured with libvmaf
#       against a lossless 1080p downscale of the hardest clip (a moving camera
#       over prairie grass): 6000k -> 92.4, 5000k -> ~90, 4000k -> 87.5,
#       3000k -> 82.8, 2000k -> 74.6. 5000k sits just above the knee.
#
# Orientation is preserved: the long edge is capped at 1920, so a landscape
# master lands at 1920x1080 and a vertical one at 1080x1920. Vertical clips are
# vertical tiles in the mosaic rather than a 16:9 crop that throws the shot away.
#
# Usage:  ./scripts/encode-video.sh [--force]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SRC_DIR="_masters/video"
OUT_DIR="assets/video"
MOBILE_DIR="$OUT_DIR/mobile"
POSTER_DIR="assets/posters"
FORCE="${1:-}"

command -v ffmpeg >/dev/null || { echo "ffmpeg not found (brew install ffmpeg)"; exit 1; }
[[ -d "$SRC_DIR" ]] || { echo "missing $SRC_DIR — put the originals there first"; exit 1; }
mkdir -p "$OUT_DIR" "$MOBILE_DIR" "$POSTER_DIR"

# Landing-page clips also get a portrait crop. object-fit: cover reduces a 16:9
# frame to a narrow strip on a phone and then upscales it ~2.3x, which costs more
# visible quality than the codec does. The anchor mirrors the CSS object-position
# for that slide, so the crop frames what the page was already showing.
#   <output slug>|<crop anchor 0..1>
MOBILE_CROPS=(
  "saskatchewan-1|0.18"
  "fire-lookout-1|0.5"
  "icefields-1|0.5"
)

common=(
  -c:v libx264 -profile:v high -level 4.0 -preset slow
  -g 24 -keyint_min 24 -sc_threshold 0
  -pix_fmt yuv420p
  -colorspace bt709 -color_primaries bt709 -color_trc bt709
  -movflags +faststart -an -map_metadata -1
)

# GARIBALDI_CLIP.mp4 -> garibaldi, "PACIFIC SPIRIT_CLIP.mov" -> pacific-spirit
slugify() {
  basename "$1" | sed -E 's/\.[A-Za-z0-9]+$//; s/_?CLIPS?$//I; s/[^A-Za-z0-9]+/-/g; s/-{2,}/-/g; s/^-|-$//g' \
    | tr '[:upper:]' '[:lower:]'
}

shopt -s nullglob
for src in "$SRC_DIR"/*.{mp4,mov,MP4,MOV}; do
  slug="$(slugify "$src")"
  out="$OUT_DIR/$slug.mp4"

  if [[ -f "$out" && "$FORCE" != "--force" ]]; then
    echo "  skip   $slug.mp4  (exists; --force to redo)"
    continue
  fi

  # Cap the long edge at 1920 without changing orientation.
  scale="scale='if(gt(iw,ih),1920,-2)':'if(gt(iw,ih),-2,1920)':flags=lanczos"
  ffmpeg -nostdin -v error -y -i "$src" -vf "$scale" \
    "${common[@]}" -crf 21 -maxrate 5000k -bufsize 10000k "$out"

  dims=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$out")
  printf "  ok     %-24s %-10s %7.2f MB\n" "$slug.mp4" "$dims" \
    "$(echo "scale=2; $(stat -f%z "$out") / 1048576" | bc)"

  # Poster comes from the encoded file, not the master, so frame 0 of the poster
  # is identical to frame 0 of playback and the handoff is invisible.
  ffmpeg -nostdin -v error -y -i "$out" -frames:v 1 -q:v 4 "$POSTER_DIR/$slug.jpg"

  for row in "${MOBILE_CROPS[@]}"; do
    IFS='|' read -r want anchor <<< "$row"
    [[ "$slug" == "$want" ]] || continue
    # 2160 * 9/16 = 1215 -> 1216 keeps the crop width even for yuv420p.
    crop_w=1216
    crop_x=$(printf '%.0f' "$(echo "(3840 - $crop_w) * $anchor" | bc -l)")
    (( crop_x % 2 == 1 )) && crop_x=$((crop_x - 1))
    ffmpeg -nostdin -v error -y -i "$src" \
      -vf "crop=${crop_w}:2160:${crop_x}:0,scale=1080:1920:flags=lanczos" \
      "${common[@]}" -crf 22 -maxrate 3500k -bufsize 7000k "$MOBILE_DIR/$slug.mp4"
    ffmpeg -nostdin -v error -y -i "$MOBILE_DIR/$slug.mp4" -frames:v 1 -q:v 4 \
      "$POSTER_DIR/$slug-m.jpg"
    printf "  ok     %-24s %-10s %7.2f MB  (portrait, crop x=%s)\n" "mobile/$slug.mp4" "1080x1920" \
      "$(echo "scale=2; $(stat -f%z "$MOBILE_DIR/$slug.mp4") / 1048576" | bc)" "$crop_x"
  done
done

echo "Done."
