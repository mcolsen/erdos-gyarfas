#!/usr/bin/env python3
"""Run the retained finite-certificate checkers, not optimization searches."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SUITES = {
    'gadget': ('01-gadget-compression', ['verify.py']),
    'gap64': ('02-gap64', ['verify.py', 'verify_structural.py', 'verify_theta_dilation.py']),
    'phase': ('03-phase-interfaces', ['verify.py']),
    'filters': ('04-interface-filters', ['verify_results.py', 'oracle_regression.py']),
    'joint': ('05-joint-synthesis', ['verify.py', 'verify_learning.py']),
}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--suite', choices=['all', *SUITES], default='all')
    parser.add_argument('--timeout', type=float, default=300.0,
                        help='Per-program seconds; a timeout is UNKNOWN, never a failed mathematical claim.')
    parser.add_argument('--log-dir', type=Path, default=ROOT / '.verification-output')
    args = parser.parse_args()
    if not __debug__:
        parser.error('Do not run with -O; retained verifiers use assertions.')
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    try:
        import networkx  # noqa: F401
    except ImportError:
        print('Install requirements-verify.txt first.', file=sys.stderr)
        return 2
    args.log_dir.mkdir(parents=True, exist_ok=True)
    names = list(SUITES) if args.suite == 'all' else [args.suite]
    records: list[dict] = []
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    for name in names:
        directory, programs = SUITES[name]
        for program in programs:
            log = args.log_dir / f'{directory}--{Path(program).stem}.log'
            command = [sys.executable, '-u', program]
            started = time.monotonic()
            print(f'RUN {directory}/{program}', flush=True)
            with log.open('w', encoding='utf-8') as output:
                try:
                    result = subprocess.run(command, cwd=ROOT / 'experiments' / directory,
                                            stdout=output, stderr=subprocess.STDOUT,
                                            timeout=args.timeout, env=env, check=False)
                    status = 'PASS' if result.returncode == 0 else 'CHECK_FAILED'
                    returncode = result.returncode
                except subprocess.TimeoutExpired:
                    status, returncode = 'TIMEOUT_UNKNOWN', None
                except OSError as exc:
                    output.write(f'Execution error: {exc}\n')
                    status, returncode = 'EXECUTION_ERROR', None
            record = {'suite': name, 'experiment': directory, 'program': program,
                      'status': status, 'returncode': returncode,
                      'elapsed_seconds': round(time.monotonic() - started, 3),
                      'log': str(log.resolve())}
            records.append(record)
            (args.log_dir / 'results.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
            print(f'{status}: {log}', flush=True)
    return 0 if all(r['status'] == 'PASS' for r in records) else 1

if __name__ == '__main__':
    raise SystemExit(main())
