from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from pathlib import PurePosixPath


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_source_files(
    bundle: Path, include_plugin_cache: bool
) -> list[tuple[str, Path, Path]]:
    mappings = [(bundle / "user-skills", Path("skills"))]
    if include_plugin_cache:
        mappings.append((bundle / "plugin-cache", Path("plugins") / "cache"))

    files: list[tuple[str, Path, Path]] = []
    for source_root, target_prefix in mappings:
        if not source_root.is_dir():
            continue
        for source in sorted(source_root.rglob("*")):
            if source.is_file() and not source.is_symlink():
                files.append(
                    (source_root.name, source, target_prefix / source.relative_to(source_root))
                )
    return files


def verify_bundle(bundle: Path, include_plugin_cache: bool) -> int:
    manifest_path = bundle / "portable-skills-manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Bundle manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    selected_sources = {"user-skills"}
    if include_plugin_cache:
        selected_sources.add("plugin-cache")

    expected: dict[tuple[str, str], str] = {}
    for item in manifest.get("files", []):
        source_label = item.get("source")
        if source_label not in selected_sources:
            continue
        raw_path = item.get("path")
        digest = item.get("sha256")
        if not isinstance(raw_path, str) or not isinstance(digest, str):
            raise ValueError("Bundle manifest contains an invalid file record.")
        relative = PurePosixPath(raw_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsafe path in bundle manifest: {raw_path}")
        key = (source_label, relative.as_posix())
        if key in expected:
            raise ValueError(f"Duplicate path in bundle manifest: {source_label}/{raw_path}")
        expected[key] = digest.lower()

    actual: dict[tuple[str, str], Path] = {}
    for source_label, source, _ in collect_source_files(bundle, include_plugin_cache):
        source_root = bundle / source_label
        key = (source_label, source.relative_to(source_root).as_posix())
        actual[key] = source

    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    if missing or extra:
        raise ValueError(
            f"Bundle contents do not match manifest: missing={len(missing)} extra={len(extra)}"
        )
    for key, source in actual.items():
        if sha256(source) != expected[key]:
            raise ValueError(f"Bundle hash mismatch: {key[0]}/{key[1]}")
    return len(actual)


def install_bundle(
    bundle: Path,
    target_codex_home: Path,
    include_plugin_cache: bool = False,
    execute: bool = False,
) -> dict[str, object]:
    bundle = bundle.resolve()
    target_codex_home = target_codex_home.resolve()
    if not bundle.is_dir():
        raise FileNotFoundError(f"Bundle directory not found: {bundle}")
    if bundle == target_codex_home or bundle in target_codex_home.parents:
        raise ValueError("Target Codex home must not be inside the bundle directory.")

    source_files = collect_source_files(bundle, include_plugin_cache)
    verified_files = verify_bundle(bundle, include_plugin_cache)
    conflicts = 0
    installable = 0
    total_bytes = 0
    for _, source, relative in source_files:
        destination = target_codex_home / relative
        if destination.exists():
            conflicts += 1
        else:
            installable += 1
            total_bytes += source.stat().st_size

    result: dict[str, object] = {
        "status": "DRY_RUN" if not execute else "INSTALLED",
        "source_files": len(source_files),
        "installable_files": installable,
        "conflicts_skipped": conflicts,
        "install_bytes": total_bytes,
        "plugin_cache_included": include_plugin_cache,
        "manifest_verified": True,
        "verified_files": verified_files,
    }
    if not execute:
        return result

    installed_manifest: list[dict[str, object]] = []
    for _, source, relative in source_files:
        destination = target_codex_home / relative
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        installed_manifest.append(
            {
                "path": relative.as_posix(),
                "bytes": source.stat().st_size,
                "sha256": sha256(destination),
            }
        )

    target_codex_home.mkdir(parents=True, exist_ok=True)
    (target_codex_home / "portable-skills-install-manifest.json").write_text(
        json.dumps({**result, "files": installed_manifest}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return result


def build_parser() -> argparse.ArgumentParser:
    user_profile = Path(os.environ.get("USERPROFILE", Path.home()))
    parser = argparse.ArgumentParser(
        description="Estimate or install a portable Codex skills tree without overwriting files."
    )
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument(
        "--target-codex-home",
        type=Path,
        default=user_profile / ".codex",
    )
    parser.add_argument("--include-plugin-cache", action="store_true")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Copy non-conflicting files. Without this flag the command is read-only.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = install_bundle(
        bundle=args.bundle,
        target_codex_home=args.target_codex_home,
        include_plugin_cache=args.include_plugin_cache,
        execute=args.execute,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
