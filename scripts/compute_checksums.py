#!/usr/bin/env python3
"""
scripts/compute_checksums.py

Compute SHA256 checksums for dataset and model artifacts in the repository.
Run this from the repository root (after checkout of consolidatedbranch):

    python scripts/compute_checksums.py --out docs/checksums.csv

The script scans Week* folders and dataset/ for files with extensions: .csv, .joblib, .pkl
and writes a CSV with: path, size_bytes, sha256_hex.

This is intentionally read-only and does not modify repository files.
"""

import argparse
import hashlib
import os
from pathlib import Path
import csv

DEFAULT_EXTS = ['.csv', '.joblib', '.pkl']


def sha256_of_file(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            h.update(block)
    return h.hexdigest()


def find_files(root, exts=None):
    exts = exts or DEFAULT_EXTS
    for p in Path(root).rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            yield p


def main():
    parser = argparse.ArgumentParser(description='Compute SHA256 checksums for dataset/model files')
    parser.add_argument('--root', default='.', help='Repository root to scan')
    parser.add_argument('--out', default='docs/checksums.csv', help='Output CSV path')
    parser.add_argument('--exts', nargs='+', help='File extensions to include (e.g. .csv .joblib .pkl)')
    args = parser.parse_args()

    exts = args.exts if args.exts else DEFAULT_EXTS
    files = list(find_files(args.root, exts))
    files = sorted(files, key=lambda p: str(p))

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open('w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['path', 'size_bytes', 'sha256'])
        for p in files:
            try:
                sha = sha256_of_file(p)
                size = p.stat().st_size
                writer.writerow([str(p.as_posix()), str(size), sha])
            except Exception as e:
                writer.writerow([str(p.as_posix()), 'ERROR', str(e)])

    print(f'Wrote checksums for {len(files)} files to {out_path}')


if __name__ == '__main__':
    main()
