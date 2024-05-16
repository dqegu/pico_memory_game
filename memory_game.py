import machine
from machine import Pin, PWM
import utime
import random

# Buzzer pin inspired by https://github.com/gevem119/ModelSolution_Part1and2/blob/main/model_solution.py
buzzer = PWM(Pin(18))

# Define button pins
button1 = Pin(20, Pin.IN, Pin.PULL_UP)
button2 = Pin(21, Pin.IN, Pin.PULL_UP)
button3 = Pin(22, Pin.IN, Pin.PULL_UP)

# Initialize game variables
sequence = [1, 2, 3]  # Sequence of notes to play
score = 0 # user score

# Function to activate buzzer at a given frequency
def activate_buzzer(freq):
    buzzer.freq(freq * 200)
    buzzer.duty_u16(500) #loudness
    utime.sleep(0.5)  # Play the note for 0.5 seconds
    buzzer.duty_u16(0)

# Function to play the sequence
def play_sequence():
    for freq in sequence:
        activate_buzzer(freq)
        utime.sleep(0.6)  # Wait 0.6 seconds between notes

# Function to verify user input
def verify_input():
    timeout_ms = 5000  
    for freq in sequence:
        start_time = utime.ticks_ms()  #used google to find out about timeouts
        button_pressed = False
        while utime.ticks_diff(utime.ticks_ms(), start_time) < timeout_ms:
            if freq == 1 and not button1.value():
                button_pressed = True
                break
            elif freq == 2 and not button2.value():
                button_pressed = True
                break
            elif freq == 3 and not button3.value():
                button_pressed = True
                break
            utime.sleep(0.1)  # check button state

        if not button_pressed:
            return False  # if more than 5 seconds has passed and correct button is not pressed

    return True

def error_buzzer():
    buzzer.freq(100)
    buzzer.duty_u16(500) #loudness
    utime.sleep(1)  
    buzzer.duty_u16(0)


# Main loop
while True:
    play_sequence()  
    if verify_input():
        score += 1
        print("Correct! Score:", score)
        sequence.append(random.randint(1, 3)) # add new note to sequence
    else:
        print("GAME OVER! Final score:", score)
        error_buzzer()
        break  # end the game

    utime.sleep(1) #pause
