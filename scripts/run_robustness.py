from neurocodec.data.generator import make_dataset
from neurocodec.translation.custom_adapter import CustomFormatAdapter
from neurocodec.validation.adversarial import run_adversarial_suite
from neurocodec.validation.robustness import benchmark_model

def main():
    adapter=CustomFormatAdapter()
    records=make_dataset(32,77)
    results,summary=run_adversarial_suite()
    valid={"name":"novel-valid","field_separator":"~","key_value":"=>","strings":"plain","numbers":"plain"}
    benchmark=benchmark_model(adapter,records,valid)
    print({"phase":"7-robustness","summary":summary,"cases":[r.__dict__ for r in results],"benchmark":benchmark})
if __name__=="__main__":main()
