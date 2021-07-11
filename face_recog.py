import face_recognition
import cv2
import numpy as np
import os
import sqlite3

conn = sqlite3.connect('student_data.db', check_same_thread=False)
c = conn.cursor()

def face( frame ):
    img_path = '.\\img\\'
    known_face_encodings = []

    for input_img in os.listdir(img_path):    
        
        print(input_img)
        img = face_recognition.load_image_file(img_path + input_img)
        img_face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(img_face_encoding)

    known_face_names = []
    
    c.execute("select * from student;")
    for stu in c.fetchall():
        known_face_names.append( stu[0] + "_" + str(stu[1]) )
    
    conn.commit()
    conn.close()

    known_face_names = ['Sahaj', 'abc', 'mom']
    known_face_names = sorted(known_face_names, key=str.lower)

    face_locations = []  
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            return frame, name
