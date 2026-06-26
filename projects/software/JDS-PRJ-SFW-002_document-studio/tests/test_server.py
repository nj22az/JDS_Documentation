"""HTTP-route tests for the FastAPI layer, exercised with Starlette's TestClient.

Run:  python3 tests/test_server.py
If fastapi/httpx are not installed the suite skips cleanly (exit 0) rather than
failing — the pure core is covered by test_core.py regardless.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from fastapi.testclient import TestClient
except Exception:  # noqa: BLE001
    TestClient = None

import tests.test_core as core  # reuse the sandbox helpers + samples  # noqa: E402


def _client_and_sandbox():
    from studio import server, config
    sandbox, saved = core._sandbox()
    (config.REPO_ROOT / "jds" / "procedures").mkdir(parents=True, exist_ok=True)
    return server, config, sandbox, saved, TestClient(server.app)


def test_metadata_routes():
    server, config, sandbox, saved, client = _client_and_sandbox()
    try:
        assert client.get("/api/health").json()["ready"] in (True, False)
        assert "PRO" in client.get("/api/taxonomy").json()["categories"]
        assert isinstance(client.get("/api/templates").json(), list)
        nn = client.get("/api/next-number", params={"category": "PRO"}).json()
        assert nn["doc_no"] == "JDS-PRO-011"
        assert nn["target_dir"] == "jds/procedures"
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def test_create_and_revise_roundtrip():
    server, config, sandbox, saved, client = _client_and_sandbox()
    try:
        created = client.post("/api/documents", json={
            "template_rel_path": "jds/templates/reports/tmpl.md",
            "target_dir": "jds/procedures", "title": "Routine Check",
            "category": "PRO", "author": "N. J.",
        }).json()
        assert created["doc_no"] == "JDS-PRO-011"
        assert (sandbox / created["path"]).exists()

        # Revise a document that has a Revision History section.
        doc = sandbox / "jds" / "procedures" / "JDS-PRO-001_a.md"
        doc.write_text(core.DOC_SAMPLE)
        res = client.post("/api/revise", json={
            "path": "jds/procedures/JDS-PRO-001_a.md",
            "author": "N. J.", "description": "Tightened wording",
        }).json()
        assert res["new_rev"] == "B"
        assert "| **Revision** | B |" in doc.read_text()
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def test_bad_requests_are_rejected():
    server, config, sandbox, saved, client = _client_and_sandbox()
    try:
        # Out-of-repo path on read.
        assert client.get("/api/document", params={"path": "../../etc/passwd"}).status_code == 400
        # Unknown office kind.
        assert client.post("/api/office", params={"kind": "bogus"}).status_code == 400
        # Empty title on create.
        assert client.post("/api/documents", json={
            "template_rel_path": "jds/templates/reports/tmpl.md",
            "target_dir": "jds/procedures", "title": "  ",
            "category": "PRO", "author": "N. J.",
        }).status_code == 400
    finally:
        config.REPO_ROOT, config.REGISTRY_PATH, config.TEMPLATES_DIR = saved


def _main():
    if TestClient is None:
        print("  SKIP  fastapi/httpx not installed — server routes not exercised")
        return 0
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError as exc:
            failed += 1
            print(f"  FAIL  {test.__name__}: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_main())
