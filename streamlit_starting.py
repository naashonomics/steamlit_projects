import streamlit as st

st.title("Streamlit Test App")

#add a sidebar
st.sidebar.subheader("Details about you")


first_name = st.sidebar.text_input(label="First Name")
last_name = st.sidebar.text_input(label="Last Name")
age = st.sidebar.number_input(label="Age", min_value=1, step=1)
gender = st.sidebar.radio(label="Gender", options=['Male', 'Female', 'NA'])
submit_button = st.sidebar.button(label="Submit")


if submit_button:
    st.write("first name is  "+first_name)
    st.write('Last Name is '+last_name)
    st.write("Age is "+ str(age))
    st.write('Gender is '+gender)
