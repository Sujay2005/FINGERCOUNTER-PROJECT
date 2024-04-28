import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480  # Webcam frame size
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = r"C:\Users\sujay\PycharmProjects\handtracking\finger images"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(os.path.join(folderPath, imPath))
    if image is not None:
        # Resize image to match webcam frame size
        resized_image = cv2.resize(image, (wCam // 4, hCam // 4))  # Resize to 1/4th of webcam size
        overlayList.append(resized_image)
print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0.80)  # Or any float value between 0 and 1

tipIds =  [4,8,12,16,20]

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame")
        break

    detector.findHands(img)
    lmList= detector.findPosition(img,draw=False)
    #print(lmList)




    if len(lmList)!=0:
        fingers =[]

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

         #print(fingers)
            totalFingers=fingers.count(1)
            print(totalFingers)

        if overlayList:
            overlay = overlayList[totalFingers-1]  # Assuming you want to overlay the first image from the list

        # Overlay the image onto the webcam frame at the top-left corner
            if overlay is not None:  # Check if overlay image is loaded successfully
                 h_overlay, w_overlay, _ = overlay.shape
                 img[0:h_overlay, 0:w_overlay] = overlay  # Place overlay image at (0,0)
                 cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
                 cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (img.shape[1] - 220, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
