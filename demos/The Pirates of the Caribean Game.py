"""
from:
https://code.google.com/p/piratesofthecaribbeangame/
"""
import sys

import easygui.boxes.button_box
import easygui.boxes.fillable_box

sys.path.append('..')
import easygui

import random

secret = random.randint(1,99)
guess = 0
tries = 0

name = easygui.boxes.fillable_box.enterbox("Arrg its me Davy Jones whats your name ye scallywab")
txt = "Do you fear DEATH {}? Lets play a game if ye win ye can go if ye lose"
txt += " then you are my a sailer on my ship the flying dutchman forever AHAAAA!"
easygui.boxes.button_box.msgbox(txt.format(name))
easygui.boxes.button_box.msgbox(
    "The game be simple ye get 15 chances to guess a number between 1 and 100. Ye be ready?")

while guess != secret and tries < 15:
    guess = easygui.boxes.fillable_box.integerbox("What's your guess " + name)
    if not guess: break
    if guess < secret:
        easygui.boxes.button_box.msgbox(str(guess) + " is too low " + name)
    elif guess > secret:
        easygui.boxes.button_box.msgbox(str(guess) + " is too high " + name)

    tries += 1
    
    if guess == secret:
        easygui.boxes.button_box.msgbox("Arrg ye got it in {}.  You can go.".format(tries))
    if tries == 15:
        easygui.boxes.button_box.msgbox(
            "NO more guesses for ye.  You're mine forever now {} !! AHAAHAA!!!".format(name))
        
