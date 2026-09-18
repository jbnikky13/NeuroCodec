from neurocodec.training.baseline import train_autoencoder
from neurocodec.validation.metrics import reconstruction_metrics
from neurocodec.core.features import record_to_features
from neurocodec.data.generator import make_dataset
def main():
    model,history=train_autoencoder(epochs=50)
    records=make_dataset(16,123)
    import torch
    x=torch.tensor([record_to_features(r) for r in records],dtype=torch.float32)
    with torch.inference_mode(): pred,_=model(x)
    m=reconstruction_metrics(x[0].tolist(),pred[0].tolist())
    print({"final_loss":history[-1],"validation":m})
if __name__=="__main__": main()
