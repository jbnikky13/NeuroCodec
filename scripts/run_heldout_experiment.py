from neurocodec.training.heldout import train_heldout_experiment
from neurocodec.validation.format_metrics import vector_metrics,cosine_similarity
def main():
    r=train_heldout_experiment(held_out="pipe",epochs=80)
    print({"experiment":"held-out-format","held_out":r["held_out"],"final_training_loss":r["history"][-1],"train_decoder_errors":r["train_errors"]})
    print("A held-out target is prepared for evaluation; no pipe decoder was trained.")
if __name__=="__main__": main()
