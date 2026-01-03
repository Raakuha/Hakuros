from inference import load_model, hand_keypoints, get_keypoint
from gesture import deteksi_pinch, deteksi_genggam, deteksi_swipe
from cursor_movement import CursorController, get_screen_size
from utils import map_to_screen, distance, clamp

import cv2
import time
import pyautogui

PATH = r"D:\Projek\Hakuros\Detect_model\best.pt"
SMOOTHING_FACTOR = 0.65
PINCH_THRESHOLD = 40
FIST_THRESHOLD = 45
SWIPE_THRESHOLD = 50
CLICK_COOLDOWN = 0.55


model = load_model(PATH)
cap = cv2.VideoCapture(0)
screen_w, screen_h = get_screen_size()
cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cursor = CursorController(smoothing_factor = SMOOTHING_FACTOR)

past_y = 0
last_left_click = 0
last_right_click = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera gak bisa dibuka jir")
        break

    has_hand, keypoint, conf = hand_keypoints(model, frame)

    if has_hand:
        index_tip = get_keypoint(keypoint, 8)

        if index_tip:
            cam_x, cam_y = index_tip

            screen_x, screen_y = map_to_screen(
                cam_x, cam_y, 
                cam_w, cam_h, 
                screen_w, screen_h, 
                flip_x = True           
                )
            smooth_x, smooth_y = cursor.smooth(screen_x, screen_y)
            cursor.move_cursor(smooth_x, smooth_y)

        nyubit = deteksi_pinch(keypoint, threshold = PINCH_THRESHOLD)

        if nyubit :
            curr_time = time.time()
            if curr_time - last_right_click > CLICK_COOLDOWN:
                pyautogui.rightClick()
                last_right_click = curr_time
                print("Klik kanan bisa nih !")

        genggam = deteksi_genggam(keypoint, threshold = FIST_THRESHOLD)

        if genggam:
            curr_time = time.time()
            if curr_time - last_left_click > CLICK_COOLDOWN:
                pyautogui.click()
                last_left_click = curr_time
                print("Klik kiri bisa nih !")

        wrist = get_keypoint(keypoint, 0)
        
        if wrist :
            curr_y = wrist[1]

            swipe_direction = deteksi_swipe(curr_y, past_y, threshold = SWIPE_THRESHOLD)

            if swipe_direction == 1:
                pyautogui.scroll(1)
                print("Scroll ke atas bisa nih !")
            elif swipe_direction == -1:
                pyautogui.scroll(-1)
                print("Scroll ke bawah bisa nih !")

            past_y = curr_y
    else:

        past_y = 0
        cursor.reset()


    cv2.imshow("Hakuros", frame)

    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
cap.release()
cv2.destroyAllWindows()
