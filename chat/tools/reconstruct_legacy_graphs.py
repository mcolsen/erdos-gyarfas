#!/usr/bin/env python3
"""Recover explicitly serialized graphs; compare with the archive, never infer missing edges."""
from __future__ import annotations
import argparse
import base64
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def dimacs(edges: set[tuple[int, int]]) -> bytes:
    degree = [0] * 191
    for a, b in edges:
        if not 1 <= a < b <= 190:
            raise ValueError('Invalid or loop edge')
        degree[a] += 1
        degree[b] += 1
    if len(edges) != 285 or any(value != 3 for value in degree[1:]):
        raise ValueError('Reconstruction is not a 190-vertex cubic graph')
    return ('p edge 190 285\n' + ''.join(f'e {a} {b}\n' for a, b in sorted(edges))).encode('ascii')

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out-dir', type=Path, default=ROOT / '.verification-output' / 'reconstructed')
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    edges: set[tuple[int, int]] = set()
    with (ROOT / 'legacy/replay/edge_counts_219531.tsv').open(newline='') as source:
        for row in csv.DictReader(source, delimiter='\t'):
            edge = tuple(sorted((int(row['a']), int(row['b']))))
            if edge in edges:
                raise ValueError(f'Duplicate incidence-table edge: {edge}')
            edges.add(edge)
    results = {'n190_c32_219531.edge': dimacs(edges)}
    operations = json.loads((ROOT / 'provenance/reconstructed_surgeries.json').read_text())['operations']
    for operation in operations:
        for edge in operation['remove']:
            edges.remove(tuple(sorted(edge)))
        for edge in operation['add']:
            pair = tuple(sorted(edge))
            if pair in edges:
                raise ValueError(f'Surgery creates duplicate edge: {pair}')
            edges.add(pair)
        results[f'n190_c32_{operation["reported_c32"]}.edge'] = dimacs(edges)
    payload = (ROOT / 'provenance/n190_220225_serialized_in_chat.base64').read_text().strip()
    results['n190_c32_220225.edge'] = base64.b64decode(payload, validate=True)
    for name, data in results.items():
        expected = (ROOT / 'data/graphs' / name).read_bytes()
        if data != expected:
            raise ValueError(f'{name}: reconstruction differs from archived bytes')
        (args.out_dir / name).write_bytes(data)
        print(name, hashlib.sha256(data).hexdigest())
    print('PASS: five explicit historical checkpoints recovered exactly. This does not recover the lost 224,547 graph.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
