import os
from kivy.core.window import Window
import pygame
import spidev
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

# ------------------------- all imports -------------------------
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from pidev.MixPanel import MixPanel
from pidev.Joystick import Joystick
from pidev.kivy.PassCodeScreen import PassCodeScreen
from datetime import datetime
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from kivy.animation import AnimationTransition
from kivy.graphics import Color, Rectangle
from kivy.uix.slider import Slider
from threading import Thread
from time import sleep
# -----------------------------------------------------------------

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
# Init a 200 steps per revolution stepper on Port 0

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'

Builder.load_file('main.kv')
Window.clearcolor = (0.7, 0.7, 0.7, 1)
# Initial Window Color


class ProjectNameGUI(App):

    def build(self):
        return SCREEN_MANAGER
# Launches Window Manager
# -----------------------------------------------------------------


class MainScreen(Screen):
    button_state = ObjectProperty(None)

    def m_speed(self):
        print("slider")
        self.motor_move(self.get_direction(), self.get_speed())

    def start_motor(self):
        global direct
        global speedy
        direct = 1
        speedy = self.speedSlider.value

        if self.start_text() == "Start":
            self.startButton.text = "Stop"
            self.startButton.color = 1, 0.21, 0.13, 1
            s0.run(direct, speedy)

        elif self.start_text() == "Stop":
            self.startButton.text = "Start"
            self.startButton.color = 0.43, 0.68, 0.08, 1
            s0.softStop()

    def start_text(self):
        if self.startButton.text == "Start":
            return 'Off'

        elif self.startButton.text == "Stop":
            return 'On'

    def get_direction(self):
        if self.dirSwitch.text == "->":
            self.dirSwitch.text = "<-"
        elif self.dirSwitch.text == "<-":
            self.dirSwitch.text = "->"

    def direction_control(self):
        if self.get_direction() == 0:
            self.motor_move(1, self.get_speed())
            self.dirSwitch.text = "->"
        elif self.get_direction() == 1:
            self.motor_move(0, self.get_speed())
            self.dirSwitch.text = "<-"


# ----------------- Screen Declarations -----------------------
Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
# -------------------------------------------------------------


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()
# MixPanel Events


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
# Execute GUI
