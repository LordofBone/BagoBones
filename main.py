import _thread
import utime
from inventor import Inventor2040W, MOTOR_A
from machine import Pin

# LED Constants
SPEED = 5
BRIGHTNESS = 0.4
UPDATES = 50

# Motor Variables
offset = 0.0

pir = Pin(0, Pin.IN, Pin.PULL_DOWN)

TONES = {
    "B0": 31,
    "C1": 33,
    "CS1": 35,
    "D1": 37,
    "DS1": 39,
    "E1": 41,
    "F1": 44,
    "FS1": 46,
    "G1": 49,
    "GS1": 52,
    "A1": 55,
    "AS1": 58,
    "B1": 62,
    "C2": 65,
    "CS2": 69,
    "D2": 73,
    "DS2": 78,
    "E2": 82,
    "F2": 87,
    "FS2": 93,
    "G2": 98,
    "GS2": 104,
    "A2": 110,
    "AS2": 117,
    "B2": 123,
    "C3": 131,
    "CS3": 139,
    "D3": 147,
    "DS3": 156,
    "E3": 165,
    "F3": 175,
    "FS3": 185,
    "G3": 196,
    "GS3": 208,
    "A3": 220,
    "AS3": 233,
    "B3": 247,
    "C4": 262,
    "CS4": 277,
    "D4": 294,
    "DS4": 311,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "G4": 392,
    "GS4": 415,
    "A4": 440,
    "AS4": 466,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "DS5": 622,
    "E5": 659,
    "F5": 698,
    "FS5": 740,
    "G5": 784,
    "GS5": 831,
    "A5": 880,
    "AS5": 932,
    "B5": 988,
    "C6": 1047,
    "CS6": 1109,
    "D6": 1175,
    "DS6": 1245,
    "E6": 1319,
    "F6": 1397,
    "FS6": 1480,
    "G6": 1568,
    "GS6": 1661,
    "A6": 1760,
    "AS6": 1865,
    "B6": 1976,
    "C7": 2093,
    "CS7": 2217,
    "D7": 2349,
    "DS7": 2489,
    "E7": 2637,
    "F7": 2794,
    "FS7": 2960,
    "G7": 3136,
    "GS7": 3322,
    "A7": 3520,
    "AS7": 3729,
    "B7": 3951,
    "C8": 4186,
    "CS8": 4435,
    "D8": 4699,
    "DS8": 4978
}

# Trying and failing to recreate: https://www.youtube.com/watch?v=ho9rZjlsyYY
SONG = ("A1", "A2", "D2", "D5", "A5", "A2", "D1", "D2", "A2", "D2", "A2", "G1", "D2")

NOTE_DURATION = 1

board = Inventor2040W()

m = board.motors[MOTOR_A]
m.enable()


def play_song():
    """Play the song, split into another function to allow for multi-core use"""
    for i in range(len(SONG)):
        if SONG[i] == "P":
            board.play_silence()
        else:
            board.play_tone(TONES[SONG[i]])

        utime.sleep(NOTE_DURATION)

    board.stop_playing()


utime.sleep(3)
while True:
    """
    Main loop that waits for PIR detection, then plays the song and turns the motor, also turns on the LED
    """
    if pir.value() == 1:

        hue = float(1) / 1.0
        board.leds.set_hsv(1, hue + offset, 1.0, BRIGHTNESS)

        _thread.start_new_thread(play_song, ())

        offset += SPEED / 1000.0

        m = board.motors[MOTOR_A]
        m.enable()
        utime.sleep(2)

        m.full_positive()
        utime.sleep(2)

        m.stop()
        utime.sleep(2)

        m.full_negative()
        utime.sleep(2)

        m.stop()
        utime.sleep(2)

        m.full_positive()
        utime.sleep(2)

        m.stop()
        utime.sleep(2)

        m.full_negative()
        utime.sleep(2)
    else:
        m.coast()
        utime.sleep(2)

        hue = float(1) / 1.0
        board.leds.set_hsv(1, hue + offset, 1.0, 0.0)
