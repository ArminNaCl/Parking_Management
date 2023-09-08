from deep_utils import CRNNInferenceTorch

def crnn_helper(image_path):
    model_path= "src/CRNN/best.ckpt"
    model = CRNNInferenceTorch(model_path)
    prediction = model.infer(image_path)
    prediction = "".join(prediction)
    return prediction
