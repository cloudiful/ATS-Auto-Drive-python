from time import time
import cv2 as cv
import numpy as np
import win32con
import win32gui
import win32ui
from ultralytics import YOLO


# class for capture windows
class WindowsCapture:
    # monitor resolution
    w = 0
    h = 0

    # game windows
    hwnd = None

    # crop to game windows size
    cropped_x = 0
    cropped_y = 0

    # game windows position
    offset_x = 0
    offset_y = 0

    def __init__(self, windows_name):
        # find game window and get position, size
        self.hwnd = win32gui.FindWindow(None, windows_name)
        if not self.hwnd:
            raise Exception('Windows not found: {}'.format(windows_name))

        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = -window_rect[0]
        self.offset_y = -window_rect[1]

        # after getting all the position and size data
        # get desktop screenshot cause pywin32 can't grab game footage
        self.hwnd = win32gui.GetDesktopWindow()

    def get_screenshot(self):
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((self.offset_x, self.offset_y), (self.w - self.offset_x, self.h - self.offset_y), dcObj,
                   (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signed_ints_array = dataBitMap.GetBitmapBits(True)
        img = np.frombuffer(signed_ints_array, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[..., :3]

        img = np.ascontiguousarray(img)

        return img


def show_info(cv_image, info):
    cv.putText(cv_image,
               'Speed {}'.format(str(info)),
               (10, 30),
               cv.FONT_HERSHEY_COMPLEX,
               1,
               (250, 250, 250), 3)

    cv.putText(cv_image,
               'Speed {}'.format(str(info)),
               (10, 30),
               cv.FONT_HERSHEY_COMPLEX,
               1,
               (10, 10, 10), 2)


if __name__ == "__main__":
    # capture ATS
    capture = WindowsCapture('American Truck Simulator')

    # load YOLO model for object detection
    model = YOLO('yolov8s.pt')

    loop_time = time()

    while True:
        # update screenshot
        screenshot = capture.get_screenshot()

        # crop image to save cpu
        velocity_area = screenshot[int(capture.h * 124 / 190):int(capture.h * 129 / 190),
                        int(capture.w * 261 / 340):int(capture.w * 278 / 340), :]

        # get object result from YOLO
        object_result = model(screenshot)

        # get text result from easyocr
        velocity = 12

        # plot result
        object_result_plotted = object_result[0].plot()

        # add FPS on the top left of screen
        show_info(object_result_plotted, int(1 / (time() - loop_time)))

        # final display
        cv.imshow('detect', object_result_plotted)

        loop_time = time()

        if cv.waitKey(1) == ord('q') or cv.getWindowProperty('detect', cv.WND_PROP_VISIBLE) < 1:
            cv.destroyAllWindows()
            break
