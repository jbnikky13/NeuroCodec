from neurocodec.training.spec_experiment import train_spec_conditioned
def main():
    r=train_spec_conditioned(epochs=80)
    print({"experiment":"spec-conditioned-decoder","formats":list(r["formats"]),"initial_loss":r["history"][0],"final_loss":r["history"][-1],"improved":r["history"][-1]<r["history"][0]})
if __name__=="__main__":main()
