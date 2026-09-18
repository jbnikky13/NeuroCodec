from neurocodec.validation.adversarial import run_adversarial_suite
from neurocodec.validation.robustness import aggregate

def test_adversarial_suite_has_valid_and_invalid_cases():
    results,summary=run_adversarial_suite()
    assert len(results)>=5
    assert 0 < summary["pass_rate"] < 1

def test_aggregate_empty():
    assert aggregate({} if False else [])["cases"]==0
