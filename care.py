from dotenv import load_dotenv
from PIL import Image
load_dotenv()

import streamlit as st
import os

import google.generativeai as genai
import io

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("vit-base-patch16-224")
def get_gemini_response(input,image,prompt):
    if input !="":
        response=model.generate_content([input,image[0],prompt])
    else:
        response=model.generate_content(image)    
    return response.text

def input_image_setup(uploaded_file):
    #check if the file is uploaded
    if uploaded_file is not None:
        #read the file
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_file.type, #get the mime type of the uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
#intilze our streamlit page
st.set_page_config(page_title="Nutrionist App")
st.header("Nutrionist App")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file=st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png","wpeg"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit=st.button("Tell me about the calories")


input_prompt="""
You are an expert in nutrition analysis and  help  users understand the nutritional value of food items. 
Provide a detailed analysis of the food item based on the provided image. 
Include information about the calories, protein, carbs, fats, and other nutritional components present in the image.
calculate the total calories based on the information provided in the image
The format be like
1. Item 1 - no of calories
2. Item 2 - no of calories
------
------
"""

#if submit button is clicked
if submit:
   image_data=input_image_setup(uploaded_file)
   response=get_gemini_response(input, image_data, input_prompt)
   st.subheader("The Response is")
   st.write(response)
