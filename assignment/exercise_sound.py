#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime
import _thread


# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))
speaker.duty_u16(32000)

done = False

def wait(duration: float) -> None:
    global done
    utime.sleep_ms(duration)
    done = True
    _thread.exit()


""" Travis Scott- FE!N """
while True:
    done = False
    utime.sleep_ms(1)
    _thread.start_new_thread(wait, (1500,))
    
    while not done:
        speaker.freq(311)
        speaker.freq(370)
        speaker.freq(466)
        
    done = False
    utime.sleep_ms(1)
    _thread.start_new_thread(wait, (2000,))
    
    while not done:
        speaker.freq(247)
        speaker.freq(311)
        speaker.freq(350)
        speaker.freq(466)

# Turn off the PWM
speaker.duty_u16(0)