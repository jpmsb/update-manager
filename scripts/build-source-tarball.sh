#!/bin/bash
# Build the source tarball expected by SPECS/update-manager.spec
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${1:?Usage: $0 <version>}"
NAME="update-manager"
STAGE="$(mktemp -d)"
DEST="$STAGE/$NAME-$VERSION"

cleanup() { rm -rf "$STAGE"; }
trap cleanup EXIT

mkdir -p "$DEST"
cp -a "$ROOT/usr" "$DEST/"
cp -a "$ROOT/etc" "$DEST/"
cp -a "$ROOT/locale" "$DEST/"
# Drop editor backups and compiled catalogs from the tarball sources
find "$DEST/locale" -name '*.po~' -delete
find "$DEST/locale" -name '*.mo' -delete
find "$DEST/locale" -name '*.pot' -delete 2>/dev/null || true

OUT="$ROOT/$NAME-$VERSION.tar.gz"
tar -C "$STAGE" -czf "$OUT" "$NAME-$VERSION"
echo "$OUT"
