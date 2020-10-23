#Import libraries
import RPi.GPIO as GPIO
import random
import os
import time
import sys
import nfcreader as nfc
from RPLCD import CharLCD

#Pins used
LED_green = 11
LED_red = 13
buzzer = 15
HIGH = 1
LOW = 0
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode=GPIO.BOARD)

def setup():
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_green, GPIO.OUT)
    GPIO.setup(LED_red, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    # GPIO.setup(btnStart, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # GPIO.setup(btnStop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(LED_red, HIGH)
    # Setup debouncing and callbacks
    #GPIO.add_event_detect(btnStart, GPIO.FALLING, callback=btnStart_pressed, bouncetime=300)
    #GPIO.add_event_detect(btnStop, GPIO.FALLING, callback=btnStop_pressed, bouncetime=300)

#def btnStart_pressed(channel)

def toggle_green(value):
    if value:
        GPIO.output(LED_green, HIGH)
    else:
        GPIO.output(LED_green, LOW)

def toggle_red(value):
    if value:
        GPIO.output(LED_red, HIGH)
    else:
        GPIO.output(LED_red, LOW)

def toggle_buzzer(value):
    if value:
        GPIO.output(buzzer, HIGH)
    else:
        GPIO.output(buzzer, LOW)

def buzz_green(delay):
    GPIO.output(LED_red, LOW)
    GPIO.output(LED_green, HIGH)
    GPIO.output(buzzer, HIGH)
    time.sleep(delay)
    GPIO.output(buzzer, LOW)
    #GPIO.output(LED_red, HIGH)
    GPIO.output(LED_green, LOW)

def flash(delay):
    clear()
    GPIO.output(LED_red, HIGH)
    GPIO.output(LED_green, HIGH)
    time.sleep(delay)
    clear()

def failure(delay):
    clear()
    toggle_red(True)
    time.sleep(delay)
    toggle_red(False)

def clear():
    GPIO.output(LED_red, LOW)
    GPIO.output(LED_green, LOW)
    GPIO.output(buzzer, LOW)

def errorBuzz(delay):
    GPIO.output(LED_green, HIGH)
    GPIO.output(buzzer, HIGH)
    time.sleep(delay)
    GPIO.output(buzzer, LOW)
        

   