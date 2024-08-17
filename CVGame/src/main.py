import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280*2)
cap.set(4, 720*2)
detector = HandDetector(detectionCon=1)
colorR = 255, 0, 255
width = cap.get(3)
height = cap.get(4)
print(width, height)

class DragRect():
    def __init__(self, posCenter, size = [80,80]):
        self.posCenter = posCenter
        self.size = size 
        
    def update(self, cursor):

        cx, cy = self.posCenter
        w, h = self.size

        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            self.posCenter = cursor

rectList = []          
for x in range(4):
    rectList.append(DragRect([x*160+90, 150]))

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    #img = cv2.resize(img, (0, 0), fx=1.9, fy=1.9)
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)
    colorR = 255, 0, 255

    if lmList:

        l, _, _ = detector.findDistance(8, 4, img)


        if l<30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)
            
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx-w//2,cy-h//2), (cx+w//2,cy+h//2), colorR, cv2.FILLED)

    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord('q'):
        break
