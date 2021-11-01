import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

polygon1 = Polygon([[250, 300], [400, 300], [400, 200], [280, 200]])
cars_cascade = cv2.CascadeClassifier('cars1.xml')


def detect_cars(frame):
    cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    return frame


def Simulator():
    speed = 0
    a = []
    count = 0
    fcount = 5
    offset = 2
    CarVideo = cv2.VideoCapture(
        'video11.mp4')
    while CarVideo.isOpened():
        ret, frame = CarVideo.read()
        pts1 = np.array([[250, 300], [400, 300], [400, 200], [280, 200]], np.int32)
        pts1 = pts1.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts1], 1, (0, 255, 255))
        controlkey = cv2.waitKey(1)
        if ret:
            cv2.line(frame, (25, 100), (400, 100), (255, 127, 0), 3)
            fcount = fcount + 1
            cars = cars_cascade.detectMultiScale(frame, 1.15, 4)
            for (x, y, w, h) in cars:
                cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
                print(y)
                if (75 + offset) > y > (75 - offset) and x < 400:
                    count += 1
                    cv2.line(frame, (25, 100), (450, 100), (0, 127, 255), 3)
                if polygon1.contains(Point(int(x + w / 2), int(y + h / 2))):
                    # print('yes')
                    a.append(fcount)
                else:
                    pass
                    # print('NO')
            dist = 5
            fps = 45
            if len(a) > 1:
                if fcount - max(a) > 1:
                    speed = (dist * fps) / ((max(a) - min(a)) * 1.5) * 3 / 2
                    if speed > 100:
                        speed = speed / 10
                    a = []
            s = "SPEED=" + str(round(speed, 2))
            st = 'vehicle count: ' + str(count)
            """
            cv2.putText(frame, s, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, st, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)"""
            cv2.imshow('frame', frame)
        else:
            break
        if controlkey == ord('q'):
            break

    CarVideo.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    Simulator()
