param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$checker = Join-Path $scriptRoot "check_project_dependencies.py"

try {
    & $Python $checker --project-path $ProjectPath
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine("doctor could not start Python: {0}" -f $_.Exception.Message)
    [Console]::Out.WriteLine('{"schema_version":1,"status":"FAIL","reason":"python-unavailable"}')
    exit 2
}
