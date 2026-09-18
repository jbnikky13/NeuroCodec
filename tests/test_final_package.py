from pathlib import Path
def test_final_benchmark_script_exists():
    assert Path("scripts/run_final_benchmark.py").exists()
def test_submission_docs_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "submission.md").is_file()
