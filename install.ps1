[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Destination = ''
)

$ErrorActionPreference = 'Stop'
$InstallerArgs = @((Join-Path $PSScriptRoot 'install.py'))
if ($Destination -ne '') {
    $InstallerArgs += @('--destination', $Destination)
}
if ($WhatIfPreference) {
    $InstallerArgs += '--dry-run'
}

if (Get-Command uv -ErrorAction SilentlyContinue) {
    & uv run --no-project python @InstallerArgs
    exit $LASTEXITCODE
}

foreach ($Candidate in @('py', 'python3', 'python')) {
    $Cmds = @(Get-Command $Candidate -All -ErrorAction SilentlyContinue)
    foreach ($Cmd in $Cmds) {
        $PrefixArgs = if ($Candidate -eq 'py') { @('-3') } else { @() }
        $ErrorActionPreference = 'Continue'
        & $Cmd.Source @PrefixArgs -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" 2>$null >$null
        $ProbeExit = $LASTEXITCODE
        $ErrorActionPreference = 'Stop'
        if ($ProbeExit -eq 0) {
            & $Cmd.Source @PrefixArgs @InstallerArgs
            exit $LASTEXITCODE
        }
    }
}

throw 'Python 3.10+ (or uv) is required to run install.py.'
