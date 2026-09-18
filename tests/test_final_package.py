from pathlib import Path
def test_final_benchmark_script_exists():
    assert Path("scripts/run_final_benchmark.py").exists()
def test_submission_docs_exist():
    assert Path("docs/submission.md").exists()
