from neurocodec.training.format_experiment import train_format_experiment
def main():
    _,h=train_format_experiment()
    print({"experiment":"learned-format-decoder-baseline","epochs":len(h),"initial_loss":h[0],"final_loss":h[-1],"improved":h[-1]<h[0]})
if __name__=="__main__": main()
