import streamlit as st
import os
import time

# Set the path to the folder containing the images
path = "pages/items"
st.title('Items Found')

itemsfound = st.empty()

with open("ItemsFound.txt", "r") as f:
    steps = f.read()
    itemsfound.text(steps)
    time.sleep(1)

# Get a list of all image file names in the folder
image_files = [f for f in os.listdir(path) if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png")]

# Display the images in a gallery format
for image_file in image_files:
    image_path = os.path.join(path, image_file)
    st.image(image_path, use_column_width=True)

    # Add a hyperlink to the image to open it in a new tab
    image_url = f"{os.getcwd()}/{image_path}"
    st.markdown(f'<a href="{image_url}" target="_blank">{image_file}</a>', unsafe_allow_html=True)
