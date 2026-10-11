param(
    [string]$Root = "D:\AIWorkspace",
    [string]$CodexHome = "$env:USERPROFILE\.codex",
    [switch]$Execute
)

$ErrorActionPreference = "Stop"
$vaultRoot = Split-Path -Parent $PSScriptRoot
$projectsRoot = Join-Path $Root "projects"
$repositories = @(
    [ordered]@{
        name = "account-knowledge-distiller"
        url = "https://github.com/ljx30829/account-knowledge-distiller.git"
        smoke = "scripts\setup.ps1"
    },
    [ordered]@{
        name = "independent-site-research-vault"
        url = "https://github.com/ljx30829/independent-site-research-vault.git"
        smoke = $null
    }
)

function Test-CommandAvailable([string]$Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

$report = [ordered]@{
    schema_version = 1
    status = "DRY_RUN"
    root = $Root
    codex_home = $CodexHome
    git_available = Test-CommandAvailable "git"
    python_available = Test-CommandAvailable "python"
    vault_bundle = Test-Path (Join-Path $vaultRoot "portable-skills\portable-skills-manifest.json")
    repositories = @()
    actions = @()
}

foreach ($repo in $repositories) {
    $destination = Join-Path $projectsRoot $repo.name
    $report.repositories += [ordered]@{
        name = $repo.name
        url = $repo.url
        destination = $destination
        already_present = Test-Path $destination
    }
}

if (-not $Execute) {
    $report.actions = @(
        "Create workspace directories",
        "Clone two private repositories using existing GitHub authentication",
        "Audit and install reviewed user and plugin skills without overwriting existing files",
        "Run the source project's local test suite"
    )
    $report | ConvertTo-Json -Depth 6
    exit 0
}

if (-not $report.git_available) { throw "Git is required" }
if (-not $report.python_available) { throw "Python 3.11 or newer is required" }
if (-not $report.vault_bundle) { throw "portable-skills manifest is missing from the knowledge vault" }

New-Item -ItemType Directory -Path $projectsRoot -Force | Out-Null
foreach ($repo in $repositories) {
    $destination = Join-Path $projectsRoot $repo.name
    if (-not (Test-Path $destination)) {
        & git clone $repo.url $destination
        if ($LASTEXITCODE -ne 0) { throw "Clone failed: $($repo.name)" }
    }
}

& python (Join-Path $PSScriptRoot "audit_portable_skills.py") `
    --bundle (Join-Path $vaultRoot "portable-skills")
if ($LASTEXITCODE -ne 0) { throw "Portable skill compatibility audit failed" }

& python (Join-Path $PSScriptRoot "install_portable_skills.py") `
    --bundle (Join-Path $vaultRoot "portable-skills") `
    --target-codex-home $CodexHome `
    --include-plugin-cache `
    --execute
if ($LASTEXITCODE -ne 0) { throw "Portable skill installation failed" }

$sourceProject = Join-Path $projectsRoot "account-knowledge-distiller"
& (Join-Path $sourceProject "scripts\setup.ps1")
if ($LASTEXITCODE -ne 0) { throw "Source project verification failed" }

$report.status = "PASS_LOCAL_RESTORE"
$report.actions = @("repositories-restored", "skills-audited", "user-and-plugin-skills-restored", "source-tests-passed")
$report | ConvertTo-Json -Depth 6
