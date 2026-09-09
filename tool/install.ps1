<#
.SYNOPSIS
  Install ai-session-skills on Windows. Thin shim: all logic is in install.py.

.EXAMPLE
  .\install.ps1
  .\install.ps1 -Only claude,codex
  .\install.ps1 -Kb C:\Users\me\notes\skills -DryRun
#>
[CmdletBinding()]
param(
    [string[]]$Only,
    [string]$Kb,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'install.py'

function Resolve-Python {
    foreach ($candidate in @(
        @{ Exe = 'py';      Args = @('-3') },
        @{ Exe = 'python3'; Args = @() },
        @{ Exe = 'python';  Args = @() }
    )) {
        if (Get-Command $candidate.Exe -ErrorAction SilentlyContinue) { return $candidate }
    }
    throw 'Python 3 is required but was not found. Install it from python.org or the Microsoft Store.'
}

$py = Resolve-Python
$argv = @($py.Args) + @($script)
if ($Only)   { $argv += @('--only', ($Only -join ',')) }
if ($Kb)     { $argv += @('--kb', $Kb) }
if ($DryRun) { $argv += '--dry-run' }

& $py.Exe @argv
exit $LASTEXITCODE
