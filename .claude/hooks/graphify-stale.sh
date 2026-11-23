#!/bin/sh
# Stop hook: when project files changed since graphify-out/ was built, tell Claude
# to update the knowledge graph before finishing. Silent when graphify is missing.
input=$(cat)
case "$input" in *'"stop_hook_active":true'* | *'"stop_hook_active": true'*) exit 0 ;; esac
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
[ -f graphify-out/manifest.json ] || exit 0
bin=$(command -v graphify) || exit 0
py=$(head -1 "$bin" | sed 's/^#!//')
changed=$("$py" - <<'PY' 2>/dev/null
from pathlib import Path
from graphify.detect import detect_incremental
from graphify.paths import out_path
from graphify.watch import _read_build_excludes, _read_build_gitignore
r = detect_incremental(Path('.'), extra_excludes=_read_build_excludes(out_path()), gitignore=_read_build_gitignore(out_path()))
n = sum(len(v) for v in r.get('new_files', {}).values()) + len(r.get('deleted_files', []))
if n:
    print(n)
PY
)
[ -n "$changed" ] || exit 0
echo "graphify: $changed project file(s) were added, changed or deleted since the knowledge graph was built. Run '/graphify . --update' (code-only changes: 'graphify update .'), then commit graphify-out/ together with the change." >&2
exit 2
