import time
#gesture deteksi
last_swipe_time = 0
SWIPE_COOLDOWN = 0.3

def deteksi_pinch(keypoint, threshold = 30):
    if keypoint is None:
        return False
    x1, y1 = keypoint[4]
    x2, y2 = keypoint[8]
    distance = ((x2 - x1)**2 + (y2 - y1) **2)**0.5
    
    return distance < threshold

def deteksi_genggam(keypoints, threshold = 50):
    if keypoints is None:
        return False
    wrist_x, wrist_y = keypoints[0]
    finger_tips = [keypoints[i] for i in [4, 8, 12, 16, 20]]

    distances = []

    for idx in finger_tips :
        x_tip, y_tip = idx
        dist = ((x_tip-wrist_x)**2 + (y_tip - wrist_y)**2)**0.5
        distances.append(dist)
    all_closed = all(dist < threshold for dist in distances)

    return all_closed

def deteksi_swipe(current_y , past_y, threshold = 50):
    global last_swipe_time
    
    curr_time = time.time()
    if curr_time - last_swipe_time < SWIPE_COOLDOWN:
        return 0
    
    delta_y = current_y - past_y

    if delta_y < -threshold:
        last_swipe_time = curr_time
        return 1
    elif delta_y > threshold:
        last_swipe_time = curr_time
        return -1
    return 0
    
