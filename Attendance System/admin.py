import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from face_recog2 import face
import sqlite3 
import pandas as pd
from datetime import datetime as dt


def login_user(username,password):

    conn = sqlite3.connect('admin_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM admin WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    conn.close()
    return data


def main():

    st.title("Admin Page")

    st.sidebar.title('Login')

    #st.subheader("Login Section")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')

    if st.sidebar.checkbox("Login"):

        result = login_user(username, password)
        if result:

            st.success("Logged In as {}".format(username))
            
            st.subheader('Mark  Attendance')
            class VideoTransformer(VideoTransformerBase):
                def transform(self, frame):
                    frame = frame.to_ndarray(format="bgr24")

                    face_data = face(frame)

                    name, rno = face_data[1].split("_")

                    conn = sqlite3.connect('attendance_data.db',  check_same_thread=False )
                    c = conn.cursor()
                    
                    c.execute("INSERT OR IGNORE INTO attendance VALUES (?, ?, ?)", (name, rno, dt.now().date() ))
                    c.execute("select * from attendance")
                    print(c.fetchall())
                    
                    conn.commit()
                
                    return face_data[0]

            webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

            if st.checkbox("Show Attendance"):

                st.subheader('Attendance Database')
                date = st.date_input( "Enter the date to check attendance", dt.now().date())
                name = st.text_input("Enter Student Name")

                query_filter = st.multiselect( 'Filter Data:', ['Name', 'Date'])

                conn = sqlite3.connect('attendance_data.db',  check_same_thread=False )

                if len(query_filter) == 0:
                    query = 'select * from attendance'
                    df = pd.read_sql_query(query, conn)

                elif len(query_filter) == 1 and 'Date' in query_filter:
                    query = 'select * from attendance where date = "{}"'.format(date)
                    df = pd.read_sql_query(query, conn)
                
                elif len(query_filter) == 1 and 'Name' in query_filter:
                    query = 'select * from attendance where name = "{}"'.format(name)
                    df = pd.read_sql_query(query, conn) 
                
                else:
                    query = 'select * from attendance where date = "{}" and name = "{}"'.format(date, name)
                    df = pd.read_sql_query(query, conn) 

                st.write(df)
        else:
            st.warning("Incorrect Username/Password")


if __name__ == '__main__':
	main()