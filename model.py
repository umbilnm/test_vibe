import re
import io
from PIL import Image

from loader import cv_model, idx_to_class, transformations
def inference_cv_model(data:bytes) -> str:
    '''Function for inference finetuned Resnet model'''    
    buffer = io.BytesIO(data)
    pil_image = Image.open(buffer)
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    tensor_data = transformations(pil_image).unsqueeze(0).float()
    label = cv_model(tensor_data).argmax().item()
    return idx_to_class[label]


