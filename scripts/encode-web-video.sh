#!/usr/bin/env bash
# Re-encode the 4K masters in CLIPS_BACKUP/ into web-deliverable loops.
#
# Why this exists: the masters are 3840x2160 at 26-43 Mbps. Shipping a lightly
# recompressed 4K file as a full-bleed background loop is what made the landing
# page stall -- a 3.5s clip at 15 Mbps cannot stream in real time, so the browser
# sat on the poster instead. Downscaling to the size actually displayed and
# spending the bits there looks *better* and starts in a fraction of the time.
#
# Three things matter beyond resolution:
#   -g 24 / -keyint_min 24 / -sc_threshold 0  ->  a keyframe every second. The
#       masters carry 1-4 keyframes total, so looping or seeking forced a decode
#       from the top of the clip. That was the hitch at the loop seam.
#   -movflags +faststart                      ->  moov atom ahead of mdat so
#       playback can begin on the first bytes.
#   -an                                       ->  these are silent background
#       loops; the audio track was dead weight and blocks autoplay heuristics.
#
# Mobile gets a portrait crop rather than a downscaled landscape frame. The CSS
# already does object-fit: cover, so a 16:9 source on a phone is cropped to a
# narrow slice and then upscaled ~2.3x -- that upscale is the single biggest
# reason the clips read as "low quality" on a phone. Cropping at encode time
# bakes in the same framing the CSS was going to apply anyway, at native res.
#
# Usage: ./scripts/encode-web-video.sh [outdir]   (default: CLIPS/)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SRC_DIR="CLIPS_BACKUP"
OUT_DIR="${1:-CLIPS}"
MOBILE_DIR="$OUT_DIR/mobile"
POSTER_DIR="IMAGES/video-posters"

command -v ffmpeg >/dev/null || { echo "ffmpeg not found (brew install ffmpeg)"; exit 1; }
[[ -d "$SRC_DIR" ]] || { echo "missing $SRC_DIR -- 4K masters are required"; exit 1; }

mkdir -p "$OUT_DIR" "$MOBILE_DIR" "$POSTER_DIR"

# output basename | master file | mobile crop anchor (skip = no mobile variant)
# The anchor mirrors the CSS object-position for that slide so the portrait crop
# frames the same part of the shot the landing page was already showing.
CLIPS=(
  "01_AWAGA_1|AWAGA_1.mov|skip"
  "02_SAS_1|SAS_1.mov|0.18"
  "03_Fire_lookout_1|Fire_lookout_1.mp4|0.5"
  "04_abott_2|abott_2.mp4|skip"
  "05_Icefileds_1|Icefileds_1.mov|0.5"
  "06_abott_1|abott_1.mp4|skip"
  "07_Fire_lookout_2|Fire_lookout_2.mp4|skip"
  "08_Icefileds_2|Icefileds_2.mov|skip"
  "09_SAS_2|SAS_2.mov|skip"
)

# Shared H.264 settings. High profile / level 4.0 decodes in hardware everywhere
# that matters, including older iPhones.
common_v=(
  -c:v libx264 -profile:v high -level 4.0 -preset slow
  -g 24 -keyint_min 24 -sc_threshold 0
  -pix_fmt yuv420p
  -colorspace bt709 -color_primaries bt709 -color_trc bt709
  -movflags +faststart -an -map_metadata -1 -fflags +bitexact
)

for row in "${CLIPS[@]}"; do
  IFS='|' read -r name master anchor <<< "$row"
  src="$SRC_DIR/$master"
  if [[ ! -f "$src" ]]; then
    echo "SKIP $name -- master $master not found"
    continue
  fi

  # ---- landscape 1080p (desktop + gallery tiles) ----
  # maxrate, not CRF, is the real control here: this footage is detailed enough
  # that CRF 21-23 all clamp against the VBV buffer and land within 7% of each
  # other. Measured VMAF against a lossless 1080p downscale of the master, on
  # the hardest clip (SAS_1, moving camera over prairie grass):
  #     6000k -> 92.4 | 5000k -> ~90 | 4000k -> 87.5 | 3000k -> 82.8 | 2000k -> 74.6
  # 5000k sits just above the knee. Startup is no longer bitrate-bound anyway --
  # with a 1s GOP and faststart the browser only needs the first GOP (~625 KB)
  # before it can paint, where the old 4K file needed 15 Mbps sustained.
  ffmpeg -nostdin -v error -y -i "$src" \
    -vf "scale=1920:1080:flags=lanczos" \
    "${common_v[@]}" -crf 21 -maxrate 5000k -bufsize 10000k \
    "$OUT_DIR/$name.mp4"
  printf "  %-22s %7.2f MB\n" "$name.mp4" \
    "$(echo "scale=2; $(stat -f%z "$OUT_DIR/$name.mp4") / 1048576" | bc)"

  # Poster is pulled from the *encoded* file, not the master, so frame 0 of the
  # poster is byte-identical to frame 0 of playback and the handoff is invisible.
  ffmpeg -nostdin -v error -y -i "$OUT_DIR/$name.mp4" -frames:v 1 \
    -vf "scale=1600:900:flags=lanczos" -q:v 4 "$POSTER_DIR/$name.jpg"

  [[ "$anchor" == "skip" ]] && continue

  # ---- portrait 1080x1920 (phones) ----
  # 2160 * 9/16 = 1215 -> 1216 to keep the crop width even for yuv420p.
  crop_w=1216
  crop_x=$(printf '%.0f' "$(echo "(3840 - $crop_w) * $anchor" | bc -l)")
  (( crop_x % 2 == 1 )) && crop_x=$((crop_x - 1))

  # Same pixel count as the landscape encode, but a narrower field of view means
  # less per-frame detail, so it holds up at a lower ceiling -- which is what we
  # want on cellular anyway.
  ffmpeg -nostdin -v error -y -i "$src" \
    -vf "crop=${crop_w}:2160:${crop_x}:0,scale=1080:1920:flags=lanczos" \
    "${common_v[@]}" -crf 22 -maxrate 3500k -bufsize 7000k \
    "$MOBILE_DIR/$name.mp4"
  printf "  %-22s %7.2f MB  (portrait, crop x=%s)\n" "mobile/$name.mp4" \
    "$(echo "scale=2; $(stat -f%z "$MOBILE_DIR/$name.mp4") / 1048576" | bc)" "$crop_x"

  ffmpeg -nostdin -v error -y -i "$MOBILE_DIR/$name.mp4" -frames:v 1 \
    -vf "scale=900:1600:flags=lanczos" -q:v 4 "$POSTER_DIR/$name-m.jpg"
done

echo "Done."
