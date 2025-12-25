#!/bin/bash
echo "[*] Creating Project Folders..."
mkdir -p data/chroma_db
mkdir -p tests

echo "[*] Installing Requirements..."
pip install -r requirements.txt

echo "[*] Environment is Ready!"