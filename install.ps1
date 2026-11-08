# Copyright 2026 Poesis Cloud and contributors — Apache License, Version 2.0
#
# One-command install of the SAF Copilot plugins: the harness (poesis-saf-agentic-harness) and
# this organization (poesis-saf-agentic-organization), from the marketplace
# poesis-cloud/saf-marketplace, for every GitHub Copilot host (Copilot CLI, GitHub Copilot app,
# VS Code with Session Target: Copilot). Idempotent: an existing marketplace or plugin is kept.
#
#   irm https://raw.githubusercontent.com/poesis-cloud/saf-agentic-organization/main/install.ps1 | iex
#   .\install.ps1 [-Preview] [-DryRun]
[CmdletBinding()]
param(
    [switch]$Preview,
    [switch]$DryRun,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'
$Repository = 'poesis-cloud/saf-marketplace'
$Plugins = @('poesis-saf-agentic-harness', 'poesis-saf-agentic-organization')

if ($Help) {
    @'
usage: install.ps1 [-Preview] [-DryRun] [-Help]

Installs the SAF harness and organization plugins with the Copilot CLI.

  -Preview   use the pre-release channel (marketplace poesis-saf-preview, branch `preview`)
             instead of the stable one (marketplace poesis-saf, branch `main`)
  -DryRun    print the copilot commands without running them
  -Help      show this help
'@ | Write-Output
    return
}

if ($Preview) {
    $Marketplace = 'poesis-saf-preview'
    $Source = "$Repository#preview"
} else {
    $Marketplace = 'poesis-saf'
    $Source = $Repository
}

function Say([string]$Message) { Write-Host "[saf] $Message" }

function Invoke-Copilot([string[]]$Arguments) {
    Say ("copilot " + ($Arguments -join ' '))
    if ($DryRun) { return }
    & copilot @Arguments
    if ($LASTEXITCODE -ne 0) { throw "copilot $($Arguments -join ' ') failed with exit code $LASTEXITCODE" }
}

$Marketplaces = ''
$Installed = @()
if (Get-Command copilot -ErrorAction SilentlyContinue) {
    $Marketplaces = (& copilot plugin marketplace list 2>$null) -join "`n"
    $Json = (& copilot plugin list --json 2>$null) -join "`n"
    if ($Json) {
        try { $Installed = @($Json | ConvertFrom-Json) } catch { $Installed = @() }
    }
} elseif ($DryRun) {
    Say 'the Copilot CLI (copilot) is not on PATH (dry run: continuing)'
} else {
    Say 'the Copilot CLI (copilot) is not on PATH: install it first (npm install -g @github/copilot)'
    exit 1
}

# Re-adding a registered marketplace is an error: add it only when absent.
if ($Marketplaces -match "(^|[^A-Za-z0-9-])$([regex]::Escape($Marketplace))([^A-Za-z0-9-]|$)") {
    Say "marketplace $Marketplace is already registered"
} else {
    Invoke-Copilot @('plugin', 'marketplace', 'add', $Source)
}

$Status = 0
foreach ($Plugin in $Plugins) {
    $Row = $Installed | Where-Object { $_.name -eq $Plugin } | Select-Object -First 1
    if (-not $Row) {
        Invoke-Copilot @('plugin', 'install', "$Plugin@$Marketplace")
    } elseif ($Row.marketplace -eq $Marketplace) {
        Say "$Plugin is already installed from $Marketplace"
    } else {
        Say "$Plugin is installed from another marketplace: run ``copilot plugin uninstall $Plugin``, then re-run this installer"
        $Status = 1
    }
}

if ($Status -ne 0) { exit $Status }
Say 'done. In a Git repository, start a session and ask to initialise it as a SAF workspace (skill poesis-saf-agentic-organization:init).'
