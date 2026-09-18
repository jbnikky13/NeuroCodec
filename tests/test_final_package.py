from pathlib import Path
def test_final_benchmark_script_exists():
    assert Path("scripts/run_final_benchmark.py").exists()
def test_submission_docs_exist():
    root=Path(__file__).resolve().parents[1]
    assert (root/"docs"/"submission.md").is_file()
def test_robustness_report_has_case_details():
    from neurocodec.validation.robustness import aggregate,RobustnessResult
    report=aggregate([RobustnessResult("ok",True,None,1.0),RobustnessResult("bad",False,"x",2.0)])
    assert report["passed"]==1.0 and report["failed"]==1.0
    assert len(report["cases_detail"])==2
