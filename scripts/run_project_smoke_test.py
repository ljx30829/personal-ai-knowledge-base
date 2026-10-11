from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

try:
    from scripts.build_project_inventory import scan_project
except ModuleNotFoundError:  # Direct execution from the scripts directory.
    from build_project_inventory import scan_project


def run_smoke_test(path: Path, command: str | None = None) -> dict[str, Any]:
    project = scan_project(path)
    result: dict[str, Any] = {
        "schema_version": 1,
        "project_path": project["source_path"],
        "status": project["status"],
        "entrypoints": project["entrypoints"],
        "state_files": project["state_files"],
        "command_run": bool(command),
    }
    if project["status"] in {"MISSING", "EXCLUDED"}:
        return result
    if not command:
        result["status"] = "WATCH_NO_SMOKE_COMMAND"
        return result
    completed = subprocess.run(
        command,
        cwd=Path(project["source_path"]),
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )
    result["command_exit_code"] = completed.returncode
    result["status"] = "PASS" if completed.returncode == 0 else "FAIL"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an explicitly supplied project smoke command safely.")
    parser.add_argument("--project-path", required=True, type=Path)
    parser.add_argument("--command", help="Optional explicit project-local command; output is captured, not printed.")
    args = parser.parse_args(argv)
    result = run_smoke_test(args.project_path, args.command)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"PASS", "WATCH_NO_SMOKE_COMMAND", "ACTIVE", "PRESENT"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
