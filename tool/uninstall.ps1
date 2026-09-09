<#
.SYNOPSIS
  Remove ai-session-skills wiring on Windows. Thin shim over uninstall.py.

.EXAMPLE
  .\uninstall.ps1
  .\uninstall.ps1 -Only cursor
#>
[CmdletBinding()]
param([string[]]$Only)

$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'uninstall.py'

function Resolve-Python {
    foreach ($candidate in @(
        @{ Exe = 'py';      Args = @('-3') },
        @{ Exe = 'python3'; Args = @() },
        @{ Exe = 'python';  Args = @() }
    )) {
        if (Get-Command $candidate.Exe -ErrorAction SilentlyContinue) { return $candidate }
    }
    throw 'Python 3 is required but was not found.'
}

$py = Resolve-Python
$argv = @($py.Args) + @($script)
if ($Only) { $argv += @('--only', ($Only -join ',')) }

& $py.Exe @argv
exit $LASTEXITCODE
