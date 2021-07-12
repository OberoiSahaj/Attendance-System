import streamlit as st
import cv2
from PIL import Image
import numpy as np
import sqlite3

conn = sqlite3.connect('student_data.db')

c = conn.cursor()

st.title('Student Sign up')

name_ip = st.text_input("Enter your Name")
rno_ip = st.text_input("Enter your Roll Number")

uploaded_file = st.file_uploader("Upload your image")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if st.button("Submit"):
        name = name_ip.title()
        rno = rno_ip.title()

        

        bytesData = uploaded_file.getvalue()
        nparr = np.frombuffer(bytesData, np.uint8)
        img_np = cv2.imdecode(nparr, 1  )

        image = img_np
        img_path = './img/{}.jpeg'.format(name+rno)

        c.execute("INSERT INTO STUDENT VALUES (?, ?, ?)", (name, rno, img_path ))

        cv2.imwrite( img_path, image  )
        conn.commit()
        st.success("Sign up Successful")

        
conn.close()