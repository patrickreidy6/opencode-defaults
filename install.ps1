[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Destination = (Join-Path $HOME '.config/opencode')
)

$ErrorActionPreference = 'Stop'
$Destination = [IO.Path]::GetFullPath($Destination)
$ConfigPath = Join-Path $Destination 'opencode.json'
$BackupRoot = Join-Path $Destination ('backups/harness-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
$Utf8 = New-Object System.Text.UTF8Encoding($false)

function Merge-Settings($Current, $Incoming) {
    foreach ($Property in $Incoming.PSObject.Properties) {
        $Existing = $Current.PSObject.Properties[$Property.Name]
        if ($null -eq $Existing) {
            $Current | Add-Member -MemberType NoteProperty -Name $Property.Name -Value $Property.Value
        } elseif (($Existing.Value -is [pscustomobject]) -and ($Property.Value -is [pscustomobject])) {
            Merge-Settings $Existing.Value $Property.Value
        } else {
            $Existing.Value = $Property.Value
        }
    }
}

function Backup-File([string]$Path, [string]$RelativePath) {
    if (Test-Path -LiteralPath $Path) {
        $BackupPath = Join-Path $BackupRoot $RelativePath
        New-Item -ItemType Directory -Path (Split-Path -Parent $BackupPath) -Force | Out-Null
        Copy-Item -LiteralPath $Path -Destination $BackupPath
    }
}

if (Test-Path -LiteralPath (Join-Path $Destination 'opencode.jsonc')) {
    throw 'An opencode.jsonc already exists. Reconcile it with opencode.json before installing.'
}

$Incoming = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'global/opencode.json') -Raw | ConvertFrom-Json
$Current = if (Test-Path -LiteralPath $ConfigPath) {
    Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json
} else {
    [pscustomobject]@{}
}
Merge-Settings $Current $Incoming
$MergedJson = $Current | ConvertTo-Json -Depth 100

$Files = @(
    [pscustomobject]@{ Source = (Join-Path $PSScriptRoot 'global/AGENTS.md'); Relative = 'AGENTS.md' }
)
foreach ($Mapping in @(
    @{ Source = 'global/guides'; Target = 'guides' },
    @{ Source = 'preferences'; Target = 'preferences' },
    @{ Source = '.opencode/skills'; Target = 'skills' },
    @{ Source = '.opencode/commands'; Target = 'commands' }
)) {
    $Root = Join-Path $PSScriptRoot $Mapping.Source
    foreach ($File in (Get-ChildItem -LiteralPath $Root -Recurse -File -Force)) {
        $Relative = $File.FullName.Substring($Root.Length + 1)
        if ($Relative -match '(^|[\\/])(__pycache__|node_modules|\.venv|\.git)([\\/]|$)' -or $Relative -match '\.py[co]$') {
            continue
        }
        $Files += [pscustomobject]@{ Source = $File.FullName; Relative = (Join-Path $Mapping.Target $Relative) }
    }
}

if ($PSCmdlet.ShouldProcess($Destination, 'Back up and install personal OpenCode defaults')) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Backup-File $ConfigPath 'opencode.json'
    [IO.File]::WriteAllText($ConfigPath, $MergedJson + [Environment]::NewLine, $Utf8)
    foreach ($File in $Files) {
        $Target = Join-Path $Destination $File.Relative
        Backup-File $Target $File.Relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $Target) -Force | Out-Null
        Copy-Item -LiteralPath $File.Source -Destination $Target -Force
    }
    Write-Output "Installed harness in $Destination"
    if (Test-Path -LiteralPath $BackupRoot) {
        Write-Output "Previous files backed up in $BackupRoot"
    }
    Write-Output 'Quit and restart OpenCode to reload configuration and skills.'
}
