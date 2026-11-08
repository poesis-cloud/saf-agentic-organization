# Copyright 2026 Poesis Cloud and contributors — Apache License, Version 2.0
#
# The framework plugin's sessionStart registration (harness adapter spec github-copilot,
# Plugin mode: The registry). PowerShell only, never Python: it records this plugin's root as
# `frameworks\<name>\root` in the per-user SAF registry. The write is a rename.
$ErrorActionPreference = 'Stop'
$root = if ($env:PLUGIN_ROOT) { $env:PLUGIN_ROOT } else { Split-Path -Parent $PSScriptRoot }
$null = [Console]::In.ReadToEnd()
$registry = if ($env:SAF_AGENTIC_REGISTRY_DIR) { $env:SAF_AGENTIC_REGISTRY_DIR } else { Join-Path $env:LOCALAPPDATA 'saf-agentic\registry' }
$entry = Join-Path $registry 'frameworks\{{PLUGIN_NAME}}\root'

try {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $entry) | Out-Null
    $temporary = "$entry.tmp.$PID"
    [IO.File]::WriteAllText($temporary, "$root`n", (New-Object System.Text.UTF8Encoding $false))
    Move-Item -LiteralPath $temporary -Destination $entry -Force
    exit 0
} catch {
    [Console]::Error.WriteLine("[{{PLUGIN_NAME}}] the SAF registry $registry cannot be written: grant it to the session, or set SAF_AGENTIC_REGISTRY_DIR ($_)")
    exit 1
}
