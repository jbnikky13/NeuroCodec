from neurocodec.training.format_experiment import train_format_experiment
def main():
    model,history=train_format_experiment()
    print({"experiment":"learned-format-decoder-baseline","epochs":len(history),"initial_loss":history[0],"final_loss":history[-1],"improved":history[-1]<history[0]})
if __name__=="__main__": main()
