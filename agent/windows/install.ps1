<#
Install the SIEM agent (Fluent Bit 5.1.3) on Windows, shipping Security and Sysmon events.

  powershell -ExecutionPolicy Bypass -File .\install.ps1 -IngestHost <mac-ip> -Token <INGEST_TOKEN>

Run from an elevated PowerShell. Needs internet for the download, which is checked
against the SHA-256 published on docs.fluentbit.io. Re-running updates the config and restarts.
#>
param(
    [Parameter(Mandatory)] [ValidatePattern('^[A-Za-z0-9.:-]+$')] [string] $IngestHost,
    [Parameter(Mandatory)] [ValidatePattern('^[A-Za-z0-9]{16,}$')] [string] $Token,
    [ValidateRange(1, 65535)] [int] $IngestPort = 8000
)
$ErrorActionPreference = 'Stop'

$Version = '5.1.3'
# From https://docs.fluentbit.io/manual/installation/downloads/windows (read 2026-11-23).
$Builds = @{
    'ARM64' = @{ Name = "fluent-bit-$Version-winarm64.zip"; Sha256 = '0c0ea7aa79093491baf2d599826922e39b0b9f8abafad47ac18027a872d7fceb' }
    'AMD64' = @{ Name = "fluent-bit-$Version-win64.zip"; Sha256 = '2a06c1a3c0ecddc970f50486a94a775b54fa28bf2ebe42c57a325511d33c0bb5' }
}
$InstallDir = 'C:\Program Files\fluent-bit'
$DataDir = 'C:\ProgramData\fluent-bit'
$Conf = Join-Path $InstallDir 'conf\siem.conf'
$Exe = Join-Path $InstallDir 'bin\fluent-bit.exe'

$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
    ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { throw 'Run this from an elevated PowerShell (Run as administrator).' }
if (-not (Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational' -ErrorAction SilentlyContinue)) {
    throw 'Sysmon is not installed: install Sysmon64a.exe first (W2).'
}

Write-Host "== checking ingest at http://${IngestHost}:$IngestPort/health"
try { Invoke-RestMethod -TimeoutSec 5 "http://${IngestHost}:$IngestPort/health" | Out-Null }
catch { throw "Ingest not reachable: is 'docker compose up -d' running on the Mac? $_" }

$build = $Builds[$env:PROCESSOR_ARCHITECTURE]
if (-not $build) { throw "No Fluent Bit build listed for $env:PROCESSOR_ARCHITECTURE" }
$zip = Join-Path $env:TEMP $build.Name
Write-Host "== downloading $($build.Name)"
Invoke-WebRequest -UseBasicParsing "https://packages.fluentbit.io/windows/$($build.Name)" -OutFile $zip
$actual = (Get-FileHash -Algorithm SHA256 $zip).Hash.ToLower()
if ($actual -ne $build.Sha256) { Remove-Item $zip; throw "SHA-256 mismatch: got $actual" }

if (Get-Service fluent-bit -ErrorAction SilentlyContinue) { Stop-Service fluent-bit }
$unpack = Join-Path $env:TEMP "fluent-bit-$Version"
if (Test-Path $unpack) { Remove-Item -Recurse -Force $unpack }
Expand-Archive $zip $unpack
# The zip's top folder name is not documented; locate the binary instead.
$root = (Get-ChildItem -Recurse -Filter fluent-bit.exe $unpack | Select-Object -First 1).Directory.Parent.FullName
New-Item -ItemType Directory -Force $InstallDir, (Join-Path $DataDir 'buffer') | Out-Null
Copy-Item -Recurse -Force (Join-Path $root '*') $InstallDir

Write-Host '== config'
$template = Get-Content -Raw (Join-Path $PSScriptRoot 'fluent-bit.conf')
$config = $template.Replace('@INGEST_HOST@', $IngestHost).Replace('@INGEST_PORT@', "$IngestPort")
$config = $config.Replace('@INGEST_TOKEN@', $Token).Replace('@AGENT_HOST@', $env:COMPUTERNAME)
Set-Content -Path $Conf -Value $config -Encoding ascii
# The config holds the token: SYSTEM and Administrators only.
icacls $Conf /inheritance:r /grant:r 'SYSTEM:F' 'Administrators:F' | Out-Null
icacls $DataDir /inheritance:r /grant:r 'SYSTEM:(OI)(CI)F' 'Administrators:(OI)(CI)F' | Out-Null
& $Exe -c $Conf --dry-run
if ($LASTEXITCODE -ne 0) { throw 'Fluent Bit rejected the config (see above).' }

# Same paths on every run, so an existing service needs no change.
if (-not (Get-Service fluent-bit -ErrorAction SilentlyContinue)) {
    New-Service -Name fluent-bit -BinaryPathName "`"$Exe`" -c `"$Conf`"" -StartupType Automatic `
        -DisplayName 'Fluent Bit (SIEM agent)' | Out-Null
}
Start-Service fluent-bit
Start-Sleep 3
if ((Get-Service fluent-bit).Status -ne 'Running') { throw 'fluent-bit service did not start; check Event Viewer > Application.' }
Write-Host "== done: Fluent Bit $Version is shipping Security and Sysmon to ${IngestHost}:$IngestPort"
