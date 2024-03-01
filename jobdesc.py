from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="JJD")

st.header("JJD")
input=st.text_input("Input Prompt: ",key="input")



# List of all jobs (replace with your complete list)
all_jobs = [
    'Software Engineer',
    'Data Scientist',
    'Graphic Designer',
    # Add more jobs here
]


selected_job = st.selectbox('Select a job:', all_jobs)
uploaded_file = st.file_uploader("Upload your resume", type=['jpg', 'pdf', 'png'])


image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Check the Resume")

input_prompt=f"""
You are an expert in Job descriptery u should check the uploaded resume from user and """  {selected_job}  """ u have to analyze the resume and say how much it has been 
matched with the selected job description , u have to mach the skill sets of resume and other u need to predic the percenage and if he is not
 having that skill set u have to give him eha skills he need to develop
               ----
               ----


"""

print(input_prompt)

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The mattched job Description is ")
    st.write(response)
