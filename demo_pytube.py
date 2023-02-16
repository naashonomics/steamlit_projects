import streamlit as st
from pytube import YouTube
import base64
from io import BytesIO
import pickle
from pathlib import Path 
import streamlit_authenticator as stauth
def main():

	# User Auth
	users = ["Avinash","Udemy _learner"]
	usernames = ["anash","udmy"]

	#loading passwords which are hashed 
	file_path=Path(__file__).parent / "hashed_passwords.pkl"

	with file_path.open("rb") as file:
		hashed_passwords=pickle.load(file)

	#Create an Auth object 
	#  Authenticate( names,username,hashed_password,json_gen_token_cookie,random_key_to_hash_cokkie_signature,number_of_days_cokkie_can_be_used_for)
	authenticator = stauth.Authenticate(users, usernames, hashed_passwords,"demo_auth", "rkey1", cookie_expiry_days=10)

	# can be main or sidebar 
	name, authentication_status, username = authenticator.login("Login", "sidebar")

	if authentication_status == False:
		st.error("Username/password is incorrect")

	if authentication_status == None:
		st.warning("Please enter your username and password")

	if authentication_status:

		path = st.text_input('Enter URL of any youtube video')
		option = st.selectbox(
	     'Select type of download',
	     ('audio', 'highest_resolution', 'lowest_resolution'))
		
		if st.button("download"): 
			video_object =  YouTube(path)
			st.write("Title of Video: " + str(video_object.title))
			st.write("Number of Views: " + str(video_object.views))
			if option=='audio':
				video_object.streams.get_audio_only().download() 		#base64.b64encode(csv.encode()).decode()	
			elif option=='highest_resolution':
				video_object.streams.get_highest_resolution().download()
			elif option=='lowest_resolution':
				video_object.streams.get_lowest_resolution().download()
		if st.button("view"): 
			st.video(path) 

	# ---- Logout ----
	authenticator.logout("Logout", "sidebar")
if __name__ == '__main__':
	main()
	