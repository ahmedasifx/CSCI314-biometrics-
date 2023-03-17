import cv2
import face_recognition
import sqlite3

# Create a connection to the database
conn = sqlite3.connect("users.db")

# Prompt the user to enter their username and password
username = input("Username: ")
password = input("Password: ")

# Authenticate the user
cursor = conn.execute("SELECT FACE_ENCODING FROM USERS WHERE USERNAME = ? AND PASSWORD = ?", (username, password))
result = cursor.fetchone()

if result is not None:
    # Load the known face encoding from the database
    known_face_encoding = face_recognition.face_encoding(result[0])

    # Capture video from webcam
    video_capture = cv2.VideoCapture(0)

    # Loop over frames from the video stream
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        # If a face is detected, try to recognize it
        if len(face_locations) > 0:
            # Get the face encoding for the first detected face
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

            # Compare the detected face with the stored image of the user's face
            results = face_recognition.compare_faces([known_face_encoding], face_encoding)

            # If the detected face matches the stored image, authenticate the user
            if results[0]:
                print("Authenticated!")
                break

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Wait for user input (press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture device and close the window
    video_capture.release()
    cv2.destroyAllWindows()

else:
    print("Incorrect username or password. Please try again.")

# Close the connection to the database
conn.close()
