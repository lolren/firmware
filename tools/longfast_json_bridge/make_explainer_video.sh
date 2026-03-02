#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="$ROOT_DIR/docs/assets"
TMP_DIR="$OUT_DIR/.video_tmp"
OUT_FILE="$OUT_DIR/longfast-json-bridge-explainer.mp4"
FONT_FILE="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

mkdir -p "$OUT_DIR"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

if [[ ! -f "$FONT_FILE" ]]; then
  FONT_FILE=""
fi

make_slide() {
  local idx="$1"
  local title="$2"
  local line1="$3"
  local line2="$4"
  local dur="$5"
  local file="$TMP_DIR/slide_${idx}.mp4"

  local draw="drawtext=fontsize=60:fontcolor=white:text='${title}':x=(w-text_w)/2:y=120,"
  draw+="drawtext=fontsize=34:fontcolor=#cbd5e1:text='${line1}':x=(w-text_w)/2:y=280,"
  draw+="drawtext=fontsize=34:fontcolor=#93c5fd:text='${line2}':x=(w-text_w)/2:y=350,"
  draw+="drawtext=fontsize=24:fontcolor=#94a3b8:text='LongFast JSON Bridge':x=(w-text_w)/2:y=650"

  local vf="${draw}"
  if [[ -n "$FONT_FILE" ]]; then
    vf="${vf}:fontfile=${FONT_FILE}"
  fi

  ffmpeg -y \
    -f lavfi -i "color=c=#0f172a:s=1280x720:d=${dur}" \
    -vf "$vf" \
    -c:v libx264 -pix_fmt yuv420p -r 30 "$file" >/dev/null 2>&1
}

make_slide 1 "LongFast JSON Bridge" "JSON chat and node config for Meshtastic" "Runs over Wi-Fi on local LAN" 7
make_slide 2 "Custom Chat API" "Send channel and private messages via JSON" "Endpoints /json/chat/send and /json/chat/messages" 8
make_slide 3 "Node Config API" "Set name and Wi-Fi from JSON" "Endpoint /json/config/node" 8
make_slide 4 "Web UI Included" "Python bridge serves browser UI" "Right-click node menu for fast private messaging" 8
make_slide 5 "Reproducible Setup" "Build firmware flash and run UI" "See docs longfast-json-bridge.md" 7

cat > "$TMP_DIR/concat.txt" <<LIST
file '$TMP_DIR/slide_1.mp4'
file '$TMP_DIR/slide_2.mp4'
file '$TMP_DIR/slide_3.mp4'
file '$TMP_DIR/slide_4.mp4'
file '$TMP_DIR/slide_5.mp4'
LIST

ffmpeg -y -f concat -safe 0 -i "$TMP_DIR/concat.txt" -c copy "$OUT_FILE" >/dev/null 2>&1

rm -rf "$TMP_DIR"
echo "Created: $OUT_FILE"
