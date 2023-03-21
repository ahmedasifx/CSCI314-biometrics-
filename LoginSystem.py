import cv2
import face_recognition

class LoginSystem:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.user_face = None
        self.user_face_encoding = None

    def load_user_face(self, image_file):
        self.user_face = face_recognition.load_image_file(image_file)
        self.user_face_encoding = face_recognition.face_encodings(self.user_face)[0]

    def capture_user_face(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([self.user_face_encoding], face_encoding)

                if True in matches:
                    return True

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        return False

    def start_login(self, image_file):
        self.load_user_face(image_file)

        if self.capture_user_face():
            entered_username = input("Enter your username: ")
            entered_password = input("Enter your password: ")

            if entered_username == self.username and entered_password == self.password:
                print('Login successful')
            else:
                print('Incorrect username or password')
        else:
            print('Face not recognized')


login_system = LoginSystem('johndoe', 'password123')
login_system.start_login('p3.jpg')