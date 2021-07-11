import sqlite3
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from face_recog2 import face
from datetime import datetime as dt


class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        frame = frame.to_ndarray(format="bgr24")

        face_data = face(frame)

        name, rno = face_data[1].split("_")

        
        conn = sqlite3.connect('attendance_data.db',  check_same_thread=False )
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO attendance VALUES (?, ?, ?)", (name, rno, dt.now() ))
        c.execute("select * from attendance")
        print(c.fetchall())
        
        conn.commit()
        conn.close()
        return face_data[0]





webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)

