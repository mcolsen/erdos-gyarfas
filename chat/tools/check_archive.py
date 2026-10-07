#!/usr/bin/env python3
"""Check every packaged file against the outer SHA-256 manifest (stdlib only)."""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = root / 'MANIFEST.sha256'
    if not manifest.is_file():
        print(f'Missing manifest: {manifest}', file=sys.stderr)
        return 2
    errors: list[str] = []
    checked = 0
    seen: set[str] = set()
    for number, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            expected, name = line.split('  ', 1)
            relative = Path(name)
            if (len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected)
                    or relative.is_absolute() or '..' in relative.parts or name in seen):
                raise ValueError('invalid digest/path or duplicate entry')
            seen.add(name)
            path = root / relative
            if not path.is_file() or path.is_symlink():
                errors.append(f'{name}: missing file or symlink')
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                errors.append(f'{name}: SHA-256 mismatch')
            checked += 1
        except ValueError as exc:
            errors.append(f'manifest line {number}: {exc}')
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f'PASS: {checked} files match MANIFEST.sha256.')
    print('Integrity is not a mathematical proof; run the retained certificate verifiers separately.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
