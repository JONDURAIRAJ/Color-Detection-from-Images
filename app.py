import cv2
import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np

# Load CSV of colors
@st.cache_data
def load_colors():
    return pd.read_csv('colors.csv')

colors_df = load_colors()

def get_color_name(R, G, B):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(colors_df)):
        d = abs(R - int(colors_df.loc[i, 'R'])) + abs(G - int(colors_df.loc[i, 'G'])) + abs(B - int(colors_df.loc[i, 'B']))
        if d <= minimum:
            minimum = d
            cname = colors_df.loc[i, 'color_name']
    return cname

st.title("🎨 Color Detection from Image")
st.write("Upload an image and click on any part to detect the color.")

uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    st.image(image, caption='Uploaded Image', use_column_width=True)

    click = st.experimental_data_editor({"x": 0, "y": 0}, key="coords", use_container_width=True)
    x, y = int(click["x"]), int(click["y"])

    if 0 <= y < image_np.shape[0] and 0 <= x < image_np.shape[1]:
        b, g, r = image_np[y, x]
        color_name = get_color_name(r, g, b)

        st.markdown(f"**Color Name:** {color_name}")
        st.markdown(f"**RGB:** ({r}, {g}, {b})")

        st.markdown(
            f"<div style='width:150px;height:50px;background-color:rgb({r},{g},{b});border:1px solid #000;'></div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Click within image bounds!")