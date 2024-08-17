import cv2

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=1, fy=1, interpolation=cv2.INTER_LINEAR)
    frame = cv2.flip(frame, 1)

    bframe = cv2.GaussianBlur(frame, (15,15), 3)

    cv2.imshow("Video", frame)
    cv2.imshow("Blurred_video", bframe)


    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
