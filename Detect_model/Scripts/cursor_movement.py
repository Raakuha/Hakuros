import pyautogui

class CursorController:
    def __init__(self, smoothing_factor = 0.8):
        self.smoothing_factor = smoothing_factor
        self.past_x = 0
        self.past_y = 0
        self.inisiasi = False
    
    def smooth(self, new_x: float, new_y: float) :
        if not self.inisiasi:
            self.past_x = new_x
            self.past_y = new_y
            self.inisiasi = True
            return (new_x, new_y)
        alpha = self.smoothing_factor
        smooth_x = alpha * self.past_x + (1 - alpha) * new_x
        smooth_y = alpha * self.past_y + (1- alpha) * new_y
        self.past_x = smooth_x
        self.past_y = smooth_y
        return (smooth_x, smooth_y)
        
    def move_cursor(self, x, y ):
        x = int(x)
        y = int(y)
        pyautogui.moveTo(x,y)

    def reset(self):
        self.past_x = 0
        self.past_y = 0
        self.inisiasi = False

def get_screen_size():
    width, height = pyautogui.size()
    return width, height
    