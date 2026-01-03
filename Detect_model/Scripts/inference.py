import os
import numpy as np
from ultralytics import YOLO
# load model
path = r"D:\Projek\Hakuros\Detect_model\best.pt"

def load_model(path : str) -> YOLO:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model ga ketemu di path {path}")
    model = YOLO(path)
    return model


def hand_keypoints(model : YOLO, frame : np.ndarray) :
    results = model(
        frame,
        conf = 0.5,
        imgsz = 640,
        device = 0,
        verbose = False
    )
    
    if results[0].keypoints is None:
        return False, None, 0.0
    
    keypoints = results[0].keypoints.xy
    if len(keypoints) == 0:
        return False, None, 0.0
    
    conf = float(results[0].boxes.conf[0])
    return True, keypoints[0], conf

def get_keypoint(keypoints: np.ndarray, index: int):
    if keypoints is None or not (0 <= index < len(keypoints)):
        return None
    x, y = keypoints[index]
    return float(x), float(y)



