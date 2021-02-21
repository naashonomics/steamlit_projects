import streamlit as st
import numpy as np
from PIL import Image
import cv2
import base64
from io import BytesIO
def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = BytesIO()
	img.save(buffered, format="JPEG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a href="data:file/jpg;base64,{img_str}">Download Your Converted Image </a>'
	return href



def dodgeV2(x, y):
    return cv2.divide(x, 255 - y, scale=256)

def pencilsketch(inp_img):
    img_gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21),sigmaX=0, sigmaY=0)
    final_img = dodgeV2(img_gray, img_smoothing)
    return(final_img)





def main():

    st.title("Image Filter  App")
    st.write("Streamlit App   to  convert your photos to realistic Pencil Sketches")

    file_image = st.sidebar.file_uploader("Upload your Photos", type=['jpeg','jpg','png'])
    option = st.sidebar.selectbox( 'How would your your images to be converted ?',
       ('pencilsketch', 'pencilsketch', 'pencilsketch'))
    if file_image is None:
        st.write("You haven't uploaded any image file")

    else:
        input_img = Image.open(file_image)
        final_sketch = pencilsketch(np.array(input_img))
        st.write("**Input Photo**")
        st.image(input_img, use_column_width=True)
        st.write("**Output Pencil Sketch**")
        st.image(final_sketch, use_column_width=True)
        result = Image.fromarray(final_sketch)
        st.markdown(get_image_download_link(result), unsafe_allow_html=True)
        
if __name__ == '__main__':
	main()