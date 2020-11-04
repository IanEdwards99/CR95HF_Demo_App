# About: Additional module to assist in TestApp for nfcreader API for CR95HF.
# Authors: Ian Edwards and Agoritsa Spirakis
# Import libraries
import RPi.GPIO as GPIO
import random
import os
import time
import sys
import nfcreader as nfc
from RPLCD import CharLCD

# Constants: Pins used
LED_green = 11
LED_red = 13
buzzer = 15
HIGH = 1
LOW = 0
lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23], numbering_mode=GPIO.BOARD)

def setup():
    # Set pinout numbering on Pi to board numbering.
    GPIO.setmode(GPIO.BOARD)
    # Setup regular GPIO
    GPIO.setup(LED_green, GPIO.OUT)
    GPIO.setup(LED_red, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.output(LED_red, HIGH)

# Change status of green LED.
def toggle_green(value):
    if value:
        GPIO.output(LED_green, HIGH)
    else:
        GPIO.output(LED_green, LOW)

# Change status of red LED.
def toggle_red(value):
    if value:
        GPIO.output(LED_red, HIGH)
    else:
        GPIO.output(LED_red, LOW)

# Change status of buzzer.
def toggle_buzzer(value):
    if value:
        GPIO.output(buzzer, HIGH)
    else:
        GPIO.output(buzzer, LOW)

# buzz and flash green LED shortly.
def buzz_green(delay):
    GPIO.output(LED_red, LOW)
    GPIO.output(LED_green, HIGH)
    GPIO.output(buzzer, HIGH)
    time.sleep(delay)
    GPIO.output(buzzer, LOW)
    GPIO.output(LED_green, LOW)

# flash LEDs momentarily.
def flash(delay):
    clear()
    GPIO.output(LED_red, HIGH)
    GPIO.output(LED_green, HIGH)
    time.sleep(delay)
    clear()

# Failure: Shine red LED for a delay amount.
def failure(delay):
    clear()
    toggle_red(True)
    time.sleep(delay)
    toggle_red(False)

# Reset outputs.
def clear():
    GPIO.output(LED_red, LOW)
    GPIO.output(LED_green, LOW)
    GPIO.output(buzzer, LOW)

# Failure buzz.
def errorBuzz(delay):
    GPIO.output(LED_green, HIGH)
    GPIO.output(buzzer, HIGH)
    time.sleep(delay)
    GPIO.output(buzzer, LOW)
        

   