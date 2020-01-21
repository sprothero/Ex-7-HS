
# ////////////////////////////////////////////////////////////////////////////////
# ///                               All Imports                                ///
# ////////////////////////////////////////////////////////////////////////////////

import os
from kivy.core.window import Window
import pygame
import spidev
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers

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


# ////////////////////////////////////////////////////////////////////////////////
# ///                             Screen and Setup                             ///
# ////////////////////////////////////////////////////////////////////////////////

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
# Init a 200 steps per revolution stepper on Port 0

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
NEW_SCREEN_NAME = 'new'

Builder.load_file('main.kv')
Window.clearcolor = (0.7, 0.7, 0.7, 1)
# Initial Window Color


class ProjectNameGUI(App):

    def build(self):
        return SCREEN_MANAGER
# Launches Window Manager


# ////////////////////////////////////////////////////////////////////////////////
# ///                       Main Screen Initialization                         ///
# ////////////////////////////////////////////////////////////////////////////////

class MainScreen(Screen):
    button_state = ObjectProperty(None)
    global direct
    direct = 1

    def main_motor_control(self):
        s0.softFree()
        if self.start_text() == 'Off':
            pass

        elif self.start_text() == 'On':
            s0.run(direct, self.speedSlider.value)
    # updates speed value based on slider

    def start_motor(self):
        if self.start_text() == 'Off':
            self.startButton.text = "Stop"
            self.startButton.color = 1, 0.21, 0.13, 1
            s0.run(direct, self.speedSlider.value)
        elif self.start_text() == 'On':
            self.startButton.text = "Start"
            self.startButton.color = 0.43, 0.68, 0.08, 1
            s0.free()
    # changes motor 0 state

    def start_text(self):
        if self.startButton.text == "Start":
            return 'Off'
        elif self.startButton.text == "Stop":
            return 'On'
    # checks motor 0 state

    @staticmethod
    def change_direction():
        if direct == 0:
            return 1
        elif direct == 1:
            return 0
    # changes "direct" variable

    def direction_control(self):
        if self.start_text() == 'On':
            if self.change_direction() == 1:
                global direct
                direct = 1
                self.main_motor_control()
            elif self.change_direction() == 0:
                global direct
                direct = 0
                self.main_motor_control()
        elif self.start_text() == 'Off':
            pass
    # changes direction of motor 0

    @staticmethod
    def screen_transition():
        SCREEN_MANAGER.current = NEW_SCREEN_NAME


# ////////////////////////////////////////////////////////////////////////////////
# ///                     Second  Screen Initialization                        ///
# ////////////////////////////////////////////////////////////////////////////////

class AppScreen(Screen):
    button_state = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('appScreen.kv')

        super(AppScreen, self).__init__(**kwargs)

    def start_program(self):
        self.move_in_rotations(1, 15)

        self.sleep_seconds(10)

        self.move_in_rotations(5, 10)

        self.sleep_seconds(8)

        self.move_home()

        self.sleep_seconds(30)

        self.move_in_rotations(-5, 100)

        self.sleep_seconds(10)

        print("go home")
        s0.set_speed(3)
        s0.goHome()

    @staticmethod
    def sleep_seconds(seconds):
        print('rest for', seconds, 'seconds')
        sleep(seconds)

    @staticmethod
    def move_in_rotations(self, speed, rotations):
        s0.set_speed(speed)
        print(rotations, 'revolutions clockwise at', speed, 'revolutions/second')
        s0.relative_move(rotations)
        self.s0_text()

    @staticmethod
    def move_home(self):
        s0.set_speed(3)
        print('go home')
        s0.goHome()
        self.s0_text()

    def s0_text(self):
        self.positionLabel.text = str(s0.get_position_in_units())

    @staticmethod
    def screen_transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


# ////////////////////////////////////////////////////////////////////////////////
# ///                           Screen Declarations                            ///
# ////////////////////////////////////////////////////////////////////////////////

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(AppScreen(name=NEW_SCREEN_NAME))


# ////////////////////////////////////////////////////////////////////////////////
# ///                     GUI and MixPanel Initialization                      ///
# ////////////////////////////////////////////////////////////////////////////////

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
