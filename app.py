import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv() # Load environment variables from .env file
from PIL import Image

#model configure
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt,image):
    model= genai.GenerativeModel("gemini-2.0-flash")
    response=model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_set(uploaded_file):
    #check if a file has been uploaded
    if uploaded_file is not None:
        # Read the image file
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("Please upload an image file.")
    
    #intialize the Streamlit app

st.set_page_config(page_title="Gemini Pro Visios")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

submit= st.button("Tell me about the calories in this image")

input_prompt = """"
You are aexpert in nutritionist and you need to see the food items from the image and calculate the total calories,also provide the details
 of every food items with caloried intake in below formate

 1.item 1 - no of calories
 2.item 2 - no of calories
 ---
 ---
 Finally you can also mention wheter the food is healthy or not based on the total calories intake.
 percenatage split of the ratio of carbohydrates, proteins and fats in the food items and other important things required in our diet.
"""

if submit:
    image_data= input_image_set(uploaded_file)
    reponse= get_gemini_response(input_prompt, image_data)
    st.header("The Response")
    st.write(reponse) 
