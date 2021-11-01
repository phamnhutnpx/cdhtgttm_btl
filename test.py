import cv2

car_cascade = cv2.CascadeClassifier('cars.xml')


def car_tracking(frames):
    cars = car_cascade.detectMultiScale(frames, 1.15, 4)
    for (x, y, w, h) in cars:
        cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 0, 0), 2)
    return frames


car_video = cv2.VideoCapture('video13.mp4')
count = 0
while car_video.isOpened():
    ret, frames = car_video.read()
    count +=1
    controlkey = cv2.waitKey(1)
    if ret:
        car_frame = car_tracking(frames)
        cv2.imshow("Nhom BLNS", car_frame)
    else:
        break
    if controlkey == ord('q'):
        break
print(count)
car_video.release()
cv2.destroyAllWindows()