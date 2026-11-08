#!/bin/sh
# Copyright 2026 Poesis Cloud and contributors — Apache License, Version 2.0
#
# One-command install of the SAF Copilot plugins: the harness (poesis-saf-agentic-harness) and
# this organization (poesis-saf-agentic-organization), from the marketplace
# poesis-cloud/saf-marketplace, for every GitHub Copilot host (Copilot CLI, GitHub Copilot app,
# VS Code with Session Target: Copilot). Idempotent: an existing marketplace or plugin is kept.
#
#   curl -fsSL https://raw.githubusercontent.com/poesis-cloud/saf-agentic-organization/main/install.sh | sh
#   sh install.sh [--preview] [--dry-run]
set -eu

REPOSITORY=poesis-cloud/saf-marketplace
PLUGINS="poesis-saf-agentic-harness poesis-saf-agentic-organization"
channel=stable
dry_run=

usage() {
    cat <<'EOF'
usage: install.sh [--preview] [--dry-run] [--help]

Installs the SAF harness and organization plugins with the Copilot CLI.

  --preview   use the pre-release channel (marketplace poesis-saf-preview, branch `preview`)
              instead of the stable one (marketplace poesis-saf, branch `main`)
  --dry-run   print the copilot commands without running them
  --help      show this help
EOF
}

for argument in "$@"; do
    case "$argument" in
        --preview) channel=preview ;;
        --dry-run) dry_run=1 ;;
        -h | --help) usage; exit 0 ;;
        *) printf 'install.sh: unknown argument: %s\n' "$argument" >&2; usage >&2; exit 2 ;;
    esac
done

if [ "$channel" = preview ]; then
    marketplace=poesis-saf-preview
    source="$REPOSITORY#preview"
else
    marketplace=poesis-saf
    source=$REPOSITORY
fi

say() { printf '[saf] %s\n' "$*"; }

run() {
    say "copilot $*"
    [ -n "$dry_run" ] || copilot "$@"
}

if ! command -v copilot >/dev/null 2>&1; then
    if [ -z "$dry_run" ]; then
        say "the Copilot CLI (copilot) is not on PATH: install it first (npm install -g @github/copilot)" >&2
        exit 1
    fi
    say "the Copilot CLI (copilot) is not on PATH (dry run: continuing)"
    marketplaces=
    installed=
else
    marketplaces=$(copilot plugin marketplace list 2>/dev/null || true)
    # One installed-plugin row per line, whitespace removed: {"name":"…","marketplace":"…",…}
    installed=$(copilot plugin list --json 2>/dev/null | tr -d ' \t\r\n' | awk '{ gsub(/\},\{/, "}\n{"); print }' || true)
fi

# Re-adding a registered marketplace is an error: add it only when absent.
if printf '%s\n' "$marketplaces" | grep -Eq "(^|[^A-Za-z0-9-])$marketplace([^A-Za-z0-9-]|\$)"; then
    say "marketplace $marketplace is already registered"
else
    run plugin marketplace add "$source"
fi

status=0
for plugin in $PLUGINS; do
    row=$(printf '%s\n' "$installed" | grep -F "\"name\":\"$plugin\"" || true)
    if [ -z "$row" ]; then
        run plugin install "$plugin@$marketplace"
    elif printf '%s\n' "$row" | grep -Fq "\"marketplace\":\"$marketplace\""; then
        say "$plugin is already installed from $marketplace"
    else
        say "$plugin is installed from another marketplace: run \`copilot plugin uninstall $plugin\`, then re-run this installer" >&2
        status=1
    fi
done

[ "$status" -eq 0 ] || exit "$status"
say "done. In a Git repository, start a session and ask to initialise it as a SAF workspace (skill init)."
