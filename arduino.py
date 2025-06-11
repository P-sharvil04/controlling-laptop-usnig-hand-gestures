import cv2
import mediapipe as mp
import pyautogui
import time


def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt


cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=2)

start_init = False

prev_right = -1
prev_left = -1

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        for hand_keyPoints in res.multi_hand_landmarks:
            # check which hand this is based on the position of the first landmark
            if hand_keyPoints.landmark[0].x < 0.5:  # left hand
                cnt_l = count_fingers(hand_keyPoints)

                if not (prev_left == cnt_l):
                    if not (start_init):
                        start_time = time.time()
                        start_init = True

                    elif (end_time - start_time) > 0.2:
                        if cnt_l == 1:
                            pyautogui.press("left")
                            print("Left hand: 1.left")
                        elif cnt_l == 2:
                            pyautogui.press("right")
                            print("Left hand: 2.right")
                        elif cnt_l == 3:
                            pyautogui.hotkey("ctrl", "shift", "esc")
                            print("Left hand: 3.task manager")
                        elif cnt_l == 4:
                            pyautogui.hotkey("win", "d")
                            print("Left hand: 4.show desktop")
                        elif cnt_l == 5:
                            pyautogui.hotkey("alt", "tab")
                            print("Left hand: 5.tab")
                        elif cnt_l == 0:
                            pyautogui.press("up")
                            print("Left hand: 0.up")
                        prev_left = cnt_l
                        start_init = False

                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

            else:  # right hand
                cnt_r = count_fingers(hand_keyPoints)

                if not (prev_right == cnt_r):
                    if not (start_init):
                        start_time = time.time()
                        start_init = True

                    elif (end_time - start_time) > 0.2:
                        if cnt_r == 1:
                            screenshot = pyautogui.screenshot()
                            screenshot.save("screenshot.png")
                            print("Right hand: 1.taken")
                        elif cnt_r == 2:
                            pyautogui.press("volumeup")
                            print("Right hand: 2.vol up")
                        elif cnt_r == 3:
                            pyautogui.hotkey("volumedown")
                            print("Right hand: 3.volume down")
                        elif cnt_r == 4:
                            pyautogui.hotkey("alt", "F4")
                            print("Right hand: 4.close")
                        elif cnt_r == 5:
                            pyautogui.hotkey("win", "tab")
                            print("Right hand: 5.windows tab")
                        elif cnt_r == 0:
                            pyautogui.press("down")
                            print("Right hand: 0.down")
                        prev_right = cnt_r
                        start_init = False

                drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
