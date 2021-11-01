import cv2
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

polygon1 = Polygon([[250, 300], [400, 300], [400, 200], [280, 200]])  # Khung đo vận tốc
width_min = 80  # Chiều rộng tối thiểu
height_min = 80  # Chiều cao tối thiểu
offset = 3
dist = 5  # độ dài quãng đường để đo vận tốc
line_down = 300  # tọa độ Y của dòng đo vận tốc
line_count = 225  # tọa độ Y của dòng đếm xe
speed_now = 0  # sử dụng để lưu file
delay = 55  # FPS
time = 0  # đếm frame
frame_list = []  # lưu frame
detect = []  # Lưu xe
count = 0  # đếm xe
speed = 0


# Lưu dữ liệu
def save(time_begin, speed_car):
    f = open("data.txt", 'a')
    f.write('\ntime = ' + str(time_begin))
    f.write(', speed car: ' + str(speed_car))
    f.close()


# lấy tọa độ trung tâm
def coordinates_central(coordinate_x, coordinate_y, width, height):
    x1 = int(width / 2)
    y1 = int(height / 2)
    cx = coordinate_x + x1
    cy = coordinate_y + y1
    return cx, cy


cap = cv2.VideoCapture('video11.mp4')
subtract = cv2.createBackgroundSubtractorMOG2()

while cap.isOpened():
    control_key = cv2.waitKey(15)
    ret, frame1 = cap.read()
    if ret:
        time = time + 1
        # Vẽ Hình chữ nhật để đo vận tốc
        pts1 = np.array([[250, 300], [400, 300], [400, 200], [280, 200]], np.int32)
        pts1 = pts1.reshape((-1, 1, 2))
        cv2.polylines(frame1, [pts1], 1, (0, 255, 255))

        # tracking
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (3, 3), 5)
        img_sub = subtract.apply(blur)
        dilate = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        morphology = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
        contour, h = cv2.findContours(morphology, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # vẽ đường kẻ
        cv2.line(frame1, (25, line_count), (450, line_count), (255, 127, 0), 3)

        for (i, c) in enumerate(contour):
            (x, y, w, h) = cv2.boundingRect(c)
            # xác định viền
            valid_contour = (w >= width_min) and (h >= height_min)
            if not valid_contour:
                continue

            # xác định vị trí xe
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = coordinates_central(x, y, w, h)
            detect.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)

            for (x, y) in detect:
                if (line_count + offset) > y > (line_count - offset):
                    count += 1
                    cv2.line(frame1, (25, line_count), (1200, line_count), (0, 127, 255), 3)
                # thêm frame vào list khi xe ở trong hình vẽ
                if polygon1.contains(Point(x, y)):
                    frame_list.append(time)
                detect.remove((x, y))
            # tính vận tốc
            if len(frame_list) > 1:
                if time - max(frame_list) > 1:
                    speed = ((dist * delay) * 3.6 / (max(frame_list) - min(frame_list)))
                    print(frame_list, speed)
                    frame_list = []

        s = "SPEED=" + str(round(speed, 3)) + 'KM/H'
        # Nếu V > 40 lưu lại thông tin
        if speed > 40:
            cv2.putText(frame1, s, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            if speed != speed_now:
                save(time, speed)
                speed_now = speed
        else:
            cv2.putText(frame1, s, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame1, "VEHICLE COUNT: " + str(count), (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    2)
        cv2.imshow("Video Original", frame1)
        cv2.imshow("Detector", morphology)
    else:
        break
    if control_key == ord('q'):
        break

# Lưu thông tin video
file = open('data.txt', 'a')
file.write("\ncar: " + str(count) + ', q (car/s) = ' + str(count / (time / delay)))
file.close()
cv2.destroyAllWindows()
cap.release()
