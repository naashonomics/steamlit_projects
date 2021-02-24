from PyPDF2 import PdfFileReader
import os
from gtts import gTTS
import streamlit as st
import streamlit.components.v1 as components


def pypdf2(py_pdf_file):
	pdfReader = PdfFileReader(py_pdf_file)
	numOfPages = pdfReader.getNumPages()
	text = "PDF File name : " + str(pdfReader.getDocumentInfo().title) + ' \n'
	text_lst = list()
	for i in range(0, numOfPages):
		pageObj = pdfReader.getPage(i)
		try:
			data = pageObj.extractText()
		except:
			pass
		text_lst.append('\n' + data + '\n')
	py_pdf_file.close()
	text_temp = " ".join(text_lst)
	return text + text_temp

def text_to_speech(text, file_name):
    speech = gTTS(text = text, slow = False)
    audio_file = f'{file_name}.mp3'
    speech.save(audio_file)
    return audio_file


def main():
    uploaded_file = st.file_uploader("Choose a Pdf file", type=["pdf"])
    text = audio_file_name = None
    if uploaded_file is not None:
        text = pypdf2(uploaded_file)
        audio_file_name = text_to_speech(text, uploaded_file.name)
        audio_file = open(audio_file_name, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        
        with st.beta_expander("View PDF Text"):
            st.write(text)   
        audio_file.close()
        os.remove(audio_file_name)
    
if __name__ == '__main__':
	main()
	