import face_recognition
import cv2
class LoginSystem:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password, image_file):
        user_face = face_recognition.load_image_file(image_file)
        user_face_encoding = face_recognition.face_encodings(user_face)[0]
        self.users[username] = {'password': password, 'face_encoding': user_face_encoding}

    def capture_user_face(self):
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding in face_encodings:
                for username, user_info in self.users.items():
                    matches = face_recognition.compare_faces([user_info['face_encoding']], face_encoding)

                    if True in matches:
                        return username

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        return None

    def start_login(self):
        username = self.capture_user_face()

        if username is not None:
            entered_password = input("Enter your password: ")

            if entered_password == self.users[username]['password']:
                print('Login successful')
            else:
                print('Incorrect password')
        else:
            print('Face not recognized')


login_system = LoginSystem()
login_system.add_user('johndoe', 'password123', 'p3.jpg')
login_system.add_user('janedoe', 'password456', 'p1.jpg')
login_system.start_login()