"""Synchronize source code and logs into the deliverables directory."""

from pathlib import Path
import shutil

CODE_MAPPINGS = {
    Path("minicoin/ledger.py"): Path("deliverables/code/ledger.py.txt"),
    Path("minicoin/server.py"): Path("deliverables/code/server.py.txt"),
    Path("clients/simulator.py"): Path("deliverables/code/simulator.py.txt"),
    Path("tests/test_ledger.py"): Path("deliverables/code/test_ledger.py.txt"),
}

DOCS_REPORT_DIR = Path("docs/report")
DOCS_DELIVERABLES_ROOT = DOCS_REPORT_DIR / "deliverables"


def sync_code() -> None:
    for src, dest in CODE_MAPPINGS.items():
        if not src.exists():
            raise FileNotFoundError(f"Missing source file: {src}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        print(f"Synced {src} -> {dest}")


def sync_logs() -> None:
    src_root = Path("logs")
    dest_root = Path("deliverables/logs")
    dest_root.mkdir(parents=True, exist_ok=True)

    if not src_root.exists():
        print("No logs/ directory found; skipping log sync.")
        return

    copied = 0
    for log_path in sorted(src_root.glob("*.log")):
        if log_path.is_file():
            target_path = dest_root / log_path.name
            shutil.copy2(log_path, target_path)
            copied += 1
            print(f"Copied log {log_path} -> {target_path}")

    if copied == 0:
        print("No .log files found under logs/; skipping log sync.")


def mirror_deliverables_to_docs() -> None:
    source_root = Path("deliverables")

    if not DOCS_REPORT_DIR.exists():
        print("docs/report directory not found; skipping docs mirror.")
        return

    if not source_root.exists():
        print("deliverables directory not found; skipping docs mirror.")
        return

    if DOCS_DELIVERABLES_ROOT.exists():
        shutil.rmtree(DOCS_DELIVERABLES_ROOT)

    shutil.copytree(source_root, DOCS_DELIVERABLES_ROOT)
    print(f"Mirrored {source_root} -> {DOCS_DELIVERABLES_ROOT}")


def main() -> None:
    sync_code()
    sync_logs()
    mirror_deliverables_to_docs()


if __name__ == "__main__":
    main()
