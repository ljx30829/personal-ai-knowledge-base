param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectPath,
    [string]$Command,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$runner = Join-Path $scriptRoot "run_project_smoke_test.py"
$arguments = @($runner, "--project-path", $ProjectPath)
if ($Command) { $arguments += @("--command", $Command) }

try {
    & $Python @arguments
    exit $LASTEXITCODE
} catch {
    [Console]::Error.WriteLine("smoke test could not start Python: {0}" -f $_.Exception.Message)
    [Console]::Out.WriteLine('{"schema_version":1,"status":"FAIL","reason":"python-unavailable"}')
    exit 2
}
