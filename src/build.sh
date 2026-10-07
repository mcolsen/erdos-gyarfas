#!/bin/bash
# Build p2check + geng variants with the p2 prune plugin.
# Usage: ./build.sh /path/to/nauty-src-dir /path/to/output-bin-dir
set -euo pipefail
NAUTY=${1:?nauty source dir}
BIN=${2:?output bin dir}
SRC=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$BIN"

CFL="-O3 -march=native -fomit-frame-pointer"
NSRC="geng.c gtools.c nauty.c nautil.c naugraph.c schreier.c naurng.c"

# 1. standalone checker
gcc $CFL -o "$BIN/p2check" "$SRC/p2check.c"

# 2. geng with prune, WORDSIZE=32 (n <= 32); compile nauty sources directly so
#    every object shares MAXN/WORDSIZE flags
( cd "$NAUTY"
  gcc $CFL -I. -o "$BIN/geng_p2" -DMAXN=32 -DWORDSIZE=32 -DPRUNE=p2_prune \
      geng.c "$SRC/p2prune.c" gtools.c nauty.c nautil.c naugraph.c schreier.c naurng.c )

# 3. geng with prune, WORDSIZE=64 (n <= 64) — for n >= 33 runs
( cd "$NAUTY"
  gcc $CFL -I. -o "$BIN/geng_p2_64" -DMAXN=64 -DWORDSIZE=64 -DPRUNE=p2_prune \
      geng.c "$SRC/p2prune.c" gtools.c nauty.c nautil.c naugraph.c schreier.c naurng.c )

echo "build OK -> $BIN"
