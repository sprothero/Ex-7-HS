
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
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus


# ////////////////////////////////////////////////////////////////////////////////
# ///                                Setup                                     ///
# ////////////////////////////////////////////////////////////////////////////////

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

spi = spidev.SpiDev()

s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
# Init a 200 steps per revolution stepper on Port 0

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN = 'main'
SCREEN1 = 'screen1'
PRO_SCREEN = 'program'
SCREEN2 = 'screen2'
SCREEN3 = 'screen3'
TRANSITION = 'transition'


Builder.load_file('main.kv')
Window.clearcolor = (0.75, 0.75, 0.75, 1)
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

    @staticmethod
    def go_to_screen(screen_num):
        global snum
        snum = screen_num
        SCREEN_MANAGER.current = TRANSITION


# ////////////////////////////////////////////////////////////////////////////////
# ///                   Transition Screen Initialization                       ///
# ////////////////////////////////////////////////////////////////////////////////

class TransitionScreen(Screen):
    button_state = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('transition.kv')

        super(TransitionScreen, self).__init__(**kwargs)

    def send_to_screen(self):
        global snum
        if snum == 1:
            self.setupLabel.font_size = 150
            self.setupLabel.text = "Stepper Motor in port 0"
        elif snum == 2:
            self.setupLabel.font_size = 100
            self.setupLabel.text = "Servo Motor in P4, Limit Switch in P6"
        elif snum == 3:
            self.setupLabel.font_size = 100
            self.setupLabel.text = "Talon Motor in P4, Limit Switch in P6"
        elif snum == 4:
            self.setupLabel.font_size = 65
            self.setupLabel.text = "Cytron controller and DC motor in P5, Proximity sensor in P7"

    def screen_go(self):
        self.setupLabel.text = " "
        if snum == 1:
            SCREEN_MANAGER.current = SCREEN1
        elif snum == 2:
            SCREEN_MANAGER.current = SCREEN2
        elif snum == 3:
            SCREEN_MANAGER.current = SCREEN3
        elif snum == 4:
            SCREEN_MANAGER.current = SCREEN3


# ////////////////////////////////////////////////////////////////////////////////
# ///                     Stepper Screen Initialization                        ///
# ////////////////////////////////////////////////////////////////////////////////

class Part1Screen(Screen):
    button_state = ObjectProperty(None)
    global direct
    direct = 1

    def __init__(self, **kwargs):
        Builder.load_file('screen1.kv')

        super(Part1Screen, self).__init__(**kwargs)

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
    def screen_transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN


# ////////////////////////////////////////////////////////////////////////////////
# ///                 Stepper Program Screen Initialization                    ///
# ////////////////////////////////////////////////////////////////////////////////

class ProgramScreen(Screen):
    button_state = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('ProgramScreen.kv')

        super(ProgramScreen, self).__init__(**kwargs)

    def start_program(self):
        s0.free()
        Clock.schedule_once(lambda dt: self.part0(), 0.01)
        Clock.schedule_once(lambda dt: self.part1(), 0.03)
        Clock.schedule_once(lambda dt: self.part2(), 15)
        Clock.schedule_once(lambda dt: self.part3(), 25)
        Clock.schedule_once(lambda dt: self.part4(), 25.01)
        Clock.schedule_once(lambda dt: self.part5(), 27.01)
        Clock.schedule_once(lambda dt: self.part6(), 35)
        Clock.schedule_once(lambda dt: self.part7(), 35.01)
        Clock.schedule_once(lambda dt: self.part8(), 40.25)
        Clock.schedule_once(lambda dt: self.part9(), 70.25)
        Clock.schedule_once(lambda dt: self.part10(), 70.26)
        Clock.schedule_once(lambda dt: self.part11(), 90.25)
        Clock.schedule_once(lambda dt: self.part12(), 100.25)
        Clock.schedule_once(lambda dt: self.part13(), 100.26)
        Clock.schedule_once(lambda dt: self.part14(), 125.25)

    def part0(self):
        self.proLabel.text = "15 turns at 1 turn/second"
        s0.free()
    # update label

    def part1(self):
        self.move_in_rotations(1, 15)
        self.posLabel.text = "Position: 15.0"
    # turn motor

    def part2(self):
        self.proLabel.text = "rest for 10 seconds"
        s0.free()
    # update label and rest

    def part3(self):
        self.proLabel.text = "10 turns at 5 turns/second"
        s0.free()
    # update label

    def part4(self):
        self.move_in_rotations(5, 10)
        self.posLabel.text = "Position: 25.0"
    # turn motor

    def part5(self):
        self.proLabel.text = "rest for 8 seconds"
        s0.free()
    # update label and rest

    def part6(self):
        self.proLabel.text = "go home"
    # update label

    def part7(self):
        self.move_home()
        self.posLabel.text = "Position: 0.0"
    # go home

    def part8(self):
        self.proLabel.text = "rest for 30 seconds"
        s0.free()
    # update label and rest

    def part9(self):
        self.proLabel.text = "100 turns backwards at 8 turns/second"
    # update label

    def part10(self):
        self.move_in_rotations(-4, 100)
        self.posLabel.text = "Position: -100.0"
    # turn motor

    def part11(self):
        self.proLabel.text = "rest for 10 seconds"
    # update label and rest

    def part12(self):
        self.proLabel.text = "go home"
        s0.free()
    # update label

    def part13(self):
        self.move_home()
        self.posLabel.text = "Position: 0.0"
    # go home

    def part14(self):
        self.proLabel.text = "Ready"
        s0.free()
    # update label

    @staticmethod
    def move_in_rotations(speed, rotations):
        s0.set_speed(speed)
        s0.relative_move(rotations)

    @staticmethod
    def move_home():
        s0.set_speed(4)
        s0.go_to_position(0.0)

    @staticmethod
    def screen_transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN


# ////////////////////////////////////////////////////////////////////////////////
# ///                      Servo Screen Initialization                         ///
# ////////////////////////////////////////////////////////////////////////////////

class Part2Screen(Screen):
    button_state = ObjectProperty(None)
    global p4_state
    p4_state = 0

    def __init__(self, **kwargs):
        Builder.load_file('screen2.kv')
        super(Part2Screen, self).__init__(**kwargs)

    def cyprus_setup(self):
        global p4_state
        p4_state = 0
        cyprus.initialize()
        cyprus.setup_servo(1)
        cyprus.set_servo_position(1, 0)
        sleep(0.2)
        self.start_cyprus_thread()

    def start_cyprus_thread(self):
        Thread(target=self.trigger_button_update).start()

    def trigger_button_update(self):
        while 1:
            if self.get_trigger_button_state() == 'up':
                pass
            else:
                self.button_down()

    @staticmethod
    def get_trigger_button_state():
        if cyprus.read_gpio() & 0b0001:
            return 'up'

    def button_down(self):
        self.goSwitch.color = 0, 0.588, 0.637, 1
        sleep(0.05)
        if cyprus.read_gpio() & 0b0001:
            self.goSwitch.color = 0.0, 0.84, 0.91, 1
            self.p4_change()

    @staticmethod
    def get_p4_state():
        if p4_state == 0:
            return 1
        elif p4_state == 1:
            return 0

    def p4_change(self):
        if self.get_p4_state() == 0:
            global p4_state
            p4_state = 0
            cyprus.set_servo_position(1, 0)
            sleep(0.2)
        elif self.get_p4_state() == 1:
            global p4_state
            p4_state = 1
            cyprus.set_servo_position(1, 1)
            sleep(0.2)

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN
        cyprus.close()


# ////////////////////////////////////////////////////////////////////////////////
# ///                      Talon Screen Initialization                         ///
# ////////////////////////////////////////////////////////////////////////////////

class Part3Screen(Screen):
    button_state = ObjectProperty(None)

    def __init__(self, **kwargs):
        Builder.load_file('screen3.kv')
        super(Part3Screen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN


# ////////////////////////////////////////////////////////////////////////////////
# ///                           Screen Declarations                            ///
# ////////////////////////////////////////////////////////////////////////////////

Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN))
SCREEN_MANAGER.add_widget(ProgramScreen(name=PRO_SCREEN))
SCREEN_MANAGER.add_widget(Part2Screen(name=SCREEN2))
SCREEN_MANAGER.add_widget(Part1Screen(name=SCREEN1))
SCREEN_MANAGER.add_widget(Part3Screen(name=SCREEN3))
SCREEN_MANAGER.add_widget(TransitionScreen(name=TRANSITION))


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
