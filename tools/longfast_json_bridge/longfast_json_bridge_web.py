#!/usr/bin/env python3
"""Compatibility launcher for the relocated LongFast JSON Bridge web server."""

from __future__ import annotations

from pathlib import Path
import runpy
import sys

TARGET = (
    Path(__file__).resolve().parents[2]
    / "longfast_json_bridge"
    / "pc_webserver"
    / "longfast_json_bridge_web.py"
)

if not TARGET.exists():
    raise SystemExit(f"Missing relocated bridge server: {TARGET}")

sys.path.insert(0, str(TARGET.parent))
runpy.run_path(str(TARGET), run_name="__main__")
