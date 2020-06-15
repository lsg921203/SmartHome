import cv2


def videoPlay(file):
    capture = cv2.VideoCapture(file)

    while True:
        if(capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT)):
            break
            

        ret, frame = capture.read()
        cv2.imshow("VideoFrame", frame)

        if cv2.waitKey(33) > 0: break

    capture.release()
    cv2.destroyAllWindows()
    
#videoPlay("goodMorning.mp4")
