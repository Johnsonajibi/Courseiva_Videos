#!/bin/bash
# Downloads the Kokoro TTS model files (from GitHub releases) into tts-models/ if missing.
set -e
cd "$(dirname "$0")/.."
mkdir -p tts-models
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s tts-models/kokoro-v1.0.onnx ] || curl -fL --retry 3 -o tts-models/kokoro-v1.0.onnx $B/kokoro-v1.0.onnx
[ -s tts-models/voices-v1.0.bin ] || curl -fL --retry 3 -o tts-models/voices-v1.0.bin $B/voices-v1.0.bin
ls -la tts-models
