#!/usr/bin/env python

import time
import cv2
import numpy as np
import threading
import PySimpleGUI as sg
from pathlib import Path
from configparser import ConfigParser


class SimpleGui():
    def __init__(self, config):
        self.config = config
        self.height = self.config.getint('DISPLAY_HEIGHT')
        self.width = self.config.getint('DISPLAY_WIDTH')

        # Prepare a blank image
        self.frame = np.zeros((self.height, self.width, 3), np.uint8)

        # sg.theme('Black')

        self.button_name = 'Close'

        self.layout = [
            # [sg.Text('PySimpleGUI', size=(10, 1), justification='center', font='Helvetica 20')],
            [sg.Image(filename='', key='image_box', size=(self.height, self.width))],
            [sg.Button(self.button_name, size=(10, 1), font='Helvetica 14')]
        ]

        self.window = sg.Window('PySimpleGUI', self.layout, location=(200, 200))

        self.started = False
        self.thread = threading.Thread(target=self.update, name='WorkerThread', args=())
        self.read_lock = threading.Lock()

    def show(self, frame_np_array: np.array) -> None:
        self.read_lock.acquire()
        self.frame = frame_np_array
        self.read_lock.release()

    def start(self):
        if self.started:
            return

        self.started = True
        self.thread.start()

    def stop(self):
        if self.started:
            self.started = False

            self.thread.join()

    def update(self):
        while self.started:
            self.read_lock.acquire()
            frame = self.frame
            self.read_lock.release()

            # Timeout = milliseconds to wait until the Read will return
            event, values = self.window.read(timeout=10)

            if event == self.button_name or event == sg.WIN_CLOSED:
                self.started = False
                break
            
            some_text = f"this is a text"
            font = cv2.FONT_HERSHEY_DUPLEX

            cv2.putText(frame, some_text, (10, 20), font, 0.4, (255, 255, 255), 1)

            img_bytes = cv2.imencode(".png", frame)[1].tobytes()
            self.window["image_box"].update(data=img_bytes)

        self.window.close()


def main():
    config_object = ConfigParser()
    config_object.read(Path("config.ini"))
    config = config_object["DEFAULT"]

    display = SimpleGui(config)
    display.start()

    frame = cv2.imread("ImagesClock/IMG20231003125035.jpg")
    while display.started:
        
        display.show(frame)

    display.stop()


if __name__ == '__main__':
    main()
