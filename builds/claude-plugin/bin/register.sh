#!/bin/sh
# Copyright 2026 Poesis Cloud and contributors — Apache License, Version 2.0
#
# The framework plugin's SessionStart registration for Claude Code (harness adapter spec
# claude-code, Plugin mode: The registry). Shell only, never Python: it records this plugin's
# root as `hosts/claude-code/frameworks/<name>/root` in the per-user SAF registry. The write
# is a rename.
root=${CLAUDE_PLUGIN_ROOT:-$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)}
cat >/dev/null 2>&1
registry=${SAF_AGENTIC_REGISTRY_DIR:-${XDG_STATE_HOME:-$HOME/.local/state}/saf-agentic/registry}
entry="$registry/hosts/claude-code/frameworks/{{PLUGIN_NAME}}/root"

if mkdir -p "$(dirname -- "$entry")" &&
    printf '%s\n' "$root" >"$entry.tmp.$$" &&
    mv -f "$entry.tmp.$$" "$entry"; then
    exit 0
fi
rm -f "$entry.tmp.$$" 2>/dev/null
printf '{"systemMessage":"[{{PLUGIN_NAME}}] the SAF registry %s cannot be written: set SAF_AGENTIC_REGISTRY_DIR to a writable folder"}\n' "$registry"
exit 0
