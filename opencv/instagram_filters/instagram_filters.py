import streamlit as st
import numpy as np
from PIL import Image
import cv2
import base64
from io import BytesIO
from pilgram import css
from pilgram import util


def valencia(im):
    """Applies Valencia filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [58, 3, 57])
    cs = css.blending.exclusion(cb, cs)
    cr = Image.blend(cb, cs, .5)  # opacity

    cr = css.contrast(cr, 1.08)
    cr = css.brightness(cr, 1.08)
    cr = css.sepia(cr, .08)

    return cr

def _1977(im):
    """Applies 1977 filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    """

    cb = util.or_convert(im, 'RGB')

    cs = util.fill(cb.size, [243, 106, 188, .3])
    cr = css.blending.screen(cb, cs)

    cr = css.contrast(cr, 1.1)
    cr = css.brightness(cr, 1.1)
    cr = css.saturate(cr, 1.3)

    return cr

def nashville(im):
    """Applies Nashville filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
     #source : https://github.com/akiomik/pilgram/blob/master/pilgram/nashville.py 
    """

    cb = util.or_convert(im, 'RGB')

    cs1 = util.fill(cb.size, [247, 176, 153, .56])
    cm1 = css.blending.darken(cb, cs1)

    cs2 = util.fill(cb.size, [0, 70, 150, .4])
    cr = css.blending.lighten(cm1, cs2)

    cr = css.sepia(cr, .2)
    cr = css.contrast(cr, 1.2)
    cr = css.brightness(cr, 1.05)
    cr = css.saturate(cr, 1.2)

    return cr


def xpro2(im):
    """Applies X-pro II filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    #source : https://github.com/akiomik/pilgram/blob/master/pilgram/nashville.py 
    """

    cb = util.or_convert(im, 'RGB')

    cs1 = util.fill(cb.size, [230, 231, 224])
    cs2 = util.fill(cb.size, [43, 42, 161])
    cs2 = Image.blend(cb, cs2, .6)

    gradient_mask = util.radial_gradient_mask(cb.size, length=.4, scale=1.1)
    cs = Image.composite(cs1, cs2, gradient_mask)

    # TODO: improve alpha blending
    cm1 = css.blending.color_burn(cb, cs)
    cm2 = cm1.copy()
    cm2 = Image.blend(cb, cm2, .6)
    cr = Image.composite(cm1, cm2, gradient_mask)

    cr = css.sepia(cr, .3)

    return cr

def brannan(im):
    """Applies Brannan filter.
    Arguments:
        im: An input image.
    Returns:
        The output image.
    ##source : https://github.com/akiomik/pilgram/blob/master/pilgram/nashville.py 
    """

    cb = util.or_convert(im, 'RGB')
    cs = util.fill(cb.size, [161, 44, 199, .31])
    cr = css.blending.lighten(cb, cs)

    cr = css.sepia(cr, .5)
    cr = css.contrast(cr, 1.4)

    return cr


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

    st.title("Image Filter App")
    st.write("Streamlit App   to  convert your photos to Filter of your choice ")
    file_image = st.sidebar.file_uploader("Upload your Photos", type=['jpeg','jpg','png'])
    option = st.sidebar.selectbox( 'How would your your images to be converted ?',
       ('pencilsketch', 'brannan','xpro2','nashville','_1977','valencia'))
    if file_image is None:
        st.write("You haven't uploaded any image file")

    else:
    
        if option == "pencilsketch":
            input_img = Image.open(file_image)
            final_sketch = pencilsketch(np.array(input_img))
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output Pencil Sketch**")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(final_sketch)
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)
        elif option == "brannan":
            input_img = Image.open(file_image)
            final_sketch = brannan(input_img)
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output Brannan Filter *")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(np.array(final_sketch))
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)
        elif option == "xpro2":
            input_img = Image.open(file_image)
            final_sketch = xpro2(input_img)
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output xpro2 Filter *")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(np.array(final_sketch))
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)            
        elif option == "nashville":
            input_img = Image.open(file_image)
            final_sketch = nashville(input_img)
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output nashville Filter *")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(np.array(final_sketch))
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)            
        elif option == "_1977":
            input_img = Image.open(file_image)
            final_sketch = _1977(input_img)
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output _1977 Filter *")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(np.array(final_sketch))
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)
        elif option == "valencia":
            input_img = Image.open(file_image)
            final_sketch = valencia(input_img)
            st.write("**Input Photo**")
            st.image(input_img, use_column_width=True)
            st.write("**Output valencia Filter *")
            st.image(final_sketch, use_column_width=True)
            result = Image.fromarray(np.array(final_sketch))
            st.markdown(get_image_download_link(result), unsafe_allow_html=True)            
if __name__ == '__main__':
	main()