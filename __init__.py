import os
import time
import random

colors = [
     "\033[91m",
     "\033[92m",
     "\033[93m",
     "\033[94m",
     "\033[95m",
     "\033[96m",
     "\033[0m"
]

def show_colored_ascii_art(color_choice="blue"):
    # Color chosen from the dictionary or defaults to blue
    color1 =  colors[random.randint(0,6)]
    color2 =  colors[random.randint(0,6)]
    color3 =  colors[random.randint(0,6)]
    color4 =  colors[random.randint(0,6)]
    color5 =  colors[random.randint(0,6)]
    color6 =  colors[random.randint(0,6)]
    color7 =  colors[random.randint(0,6)]
    
    reset = "\033[0m"
    art = [
        f"{color1}        ___            ___            ___       {reset}",
        f"{color2}       /   \          / - \          /   \      {reset}",
        f"{color3}     -|  o  |-      -| x x |-      -|  o  |-    {reset}",
        f"{color4}       \___/          \ - /          \___/      {reset}",
        f"{color5}         |              |              |        {reset}",
        f"{color6}        / \            /|\            / \       {reset}",
        f"{color7}       /___\          /_Y_\          /___\      {reset}",
    ]

    # Clear the terminal screen
    clear_screen()

    # Print the ASCII art with color
    for line in art:
        print(line)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__=='__main__':
    clear_screen()
    show_colored_ascii_art()

    


