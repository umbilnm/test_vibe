import streamlit as st
from api_call import ocr_yandex
import base64
from img_handler import process_img
from model import get_label
st.title("Naive OCR Classifier")
file = st.file_uploader("Загрузите файл", type=["png", "jpg"])


if file is not None:
    st.write("Вы загрузили файл:", file.name)
    data = file.getvalue()
    data_encoded = base64.b64encode(data).decode('utf-8')
    ocr_output = ocr_yandex(data_encoded)
    features = process_img(ocr_output)
    label = get_label(features)
    st.write("Label: ", label)