import streamlit as st 
from model import inference_cv_model
import time
st.title("Classifier")
file = st.file_uploader("Загрузите файл", type=["png", "jpg"])


if file is not None:
    start = time.time()
    st.write(f'Данное приложение классифицирует фотографии на три класса: анкета из дейтинг приложения, фотография, скрин переписки')
    st.write("Вы загрузили файл:", file.name)
    data = file.getvalue()
    label = inference_cv_model(data)
    end = time.time()
    st.write("Label: ", label)
    st.write(f"Время обработки запроса: {(end - start):.2f}с")
