import cv2  ## pip install opencv-contrib-python
from ursina import *     ## pip install ursina
import mediapipe as mp  ## pip install mediapipe


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,
                                     self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy, cz = float(lm.x*10), float(lm.y*10), float(lm.z*10)
                self.lmList.append([id, cx, cy, cz])
        return self.lmList


# Here Choose video (0 for webcam or choose Your own file):
# cap = cv2.VideoCapture("C://video//breakdance.mp4")
cap = cv2.VideoCapture(0)

spd = 10
app = Ursina()

nose = Entity(model='sphere', color=color.blue, scale_x=0.5, scale_y=0.5, scale_z=0.5)
left_shoulder = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_shoulder = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)

left_elbow = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_elbow = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)

left_wrist = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_wrist = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)

left_hip = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_hip = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)

left_knee = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_knee = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)

left_ankle = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)
right_ankle = Entity(model='sphere', color=color.red, scale_x=0.5, scale_y=0.5, scale_z=0.5)


EditorCamera()
Sky()

EditorCamera(rotation=(0,180,0))


detector = poseDetector()


def update():

    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw=False)
    #shows all body from opencv window (optional):
    # cv2.imshow('image', img)
    if success and len(lmList) != 0: #len(lmList) detect if there is an object
        #data of body!!!
        nose.setX(-lmList[0][1])
        nose.setY(-lmList[0][2])
        nose.setZ(-lmList[0][3])

        left_shoulder.setX(-lmList[11][1])
        left_shoulder.setY(-lmList[11][2])
        left_shoulder.setZ(-lmList[11][3])

        right_shoulder.setX(-lmList[12][1])
        right_shoulder.setY(-lmList[12][2])
        right_shoulder.setZ(-lmList[12][3])

        left_elbow.setX(-lmList[13][1])
        left_elbow.setY(-lmList[13][2])
        left_elbow.setZ(-lmList[13][3])

        right_elbow.setX(-lmList[14][1])
        right_elbow.setY(-lmList[14][2])
        right_elbow.setZ(-lmList[14][3])

        left_wrist.setX(-lmList[15][1])
        left_wrist.setY(-lmList[15][2])
        left_wrist.setZ(-lmList[15][3])

        right_wrist.setX(-lmList[16][1])
        right_wrist.setY(-lmList[16][2])
        right_wrist.setZ(-lmList[16][3])

        left_hip.setX(-lmList[23][1])
        left_hip.setY(-lmList[23][2])
        left_hip.setZ(-lmList[23][3])

        right_hip.setX(-lmList[24][1])
        right_hip.setY(-lmList[24][2])
        right_hip.setZ(-lmList[24][3])

        left_knee.setX(-lmList[25][1])
        left_knee.setY(-lmList[25][2])
        left_knee.setZ(-lmList[25][3])

        right_knee.setX(-lmList[26][1])
        right_knee.setY(-lmList[26][2])
        right_knee.setZ(-lmList[26][3])

        left_ankle.setX(-lmList[27][1])
        left_ankle.setY(-lmList[27][2])
        left_ankle.setZ(-lmList[27][3])

        right_ankle.setX(-lmList[28][1])
        right_ankle.setY(-lmList[28][2])
        right_ankle.setZ(-lmList[28][3])

    camera_control()

def camera_control():
    camera.z += held_keys["w"] * spd * time.dt
    camera.z -= held_keys["s"] * spd * time.dt
    camera.x += held_keys["d"] * spd * time.dt
    camera.x -= held_keys["a"] * spd * time.dt
    camera.y += held_keys["e"] * spd * time.dt
    camera.y -= held_keys["q"] * spd * time.dt

window.fullscreen_resolution = (640, 480)

window.screen_resolution = (300, 300)
window.center_on_screen = True
window.fullscreen = False
window.fps_counter.enabled = True

app.run()
