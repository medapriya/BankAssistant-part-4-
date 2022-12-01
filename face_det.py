import cv2
import time
import pickle
import imutils
import face_recognition


class Face:
    def __init__(self):
        self.exit_threads = False
        self.advt = cv2.imread('advt.jpeg')
        self.name = 'No face detected'
        self.name_prev = 'No face to recognize'
        self.face_detected_flag = False
        self.face_not_det_count = 0
        self.face_rec_flag = False
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.cap = cv2.VideoCapture(0)

    def start_stream(self):
        print('I am on face')
        while not self.exit_threads:
            ret, img = self.cap.read()
            if self.face_det(img) or self.face_not_det_count < 20 :
                self.face_detected_flag = True
                cv2.imshow('img', imutils.resize(img, width=480))
            elif self.face_not_det_count > 20:
                self.face_detected_flag = False
                self.face_rec_flag = False
                cv2.imshow('img1', imutils.resize(img, width=480))
                cv2.imshow('img', imutils.resize(self.advt, width=480))
            else:
                self.face_not_det_count = self.face_not_det_count + 1
                time.sleep(0.05)

            if cv2.waitKey(10) == 27:
                break

        print('Exiting Stream')
        cv2.destroyAllWindows()
        self.exit_threads = True

    def face_det(self, img):
        # pass
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            self.face_not_det_count = 0
            return True
        else:
            self.face_not_det_count = self.face_not_det_count + 1
            return False

    def face_rec(self):
        print('I am on face recognition')
        data = pickle.loads(open('faces_dump', 'rb').read())
        face_encodings = data["face_data"]
        encoded_names = data["face_name"]
        while not self.exit_threads:
            ret, img = self.cap.read()
            if self.face_detected_flag:
                # print('Face rec method')
                encodings = face_recognition.face_encodings(img)
                self.name = self.rec_face(face_encodings, encoded_names, encodings)
                # print('I am in self name : ', self.name)
                self.face_rec_flag = True

                if not self.name == 'Unknown':
                    time.sleep(20)

        print('Exiting face rec')

    def rec_face(self, face_encodings, encoded_names, encodings):
        name = 'Unknown'
        for encoding in encodings:
            matches = face_recognition.compare_faces(face_encodings, encoding, 0.4)

            if True in matches:
                matched_idxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matched_idxs:
                    name = encoded_names[i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
        # print(name)
        return name

    def get_name(self):
        return self.name