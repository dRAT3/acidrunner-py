import os
import time
import random

jumbled_code = """⠀⠀⠀⠀☁️☄️🌀🌙⠀⠀⠀⧉@staticmethod⧉⠀⠀⠀⠀🌙💫⚡🔥☁️
⠀⠀⠀⠀async def ☄️wait_for_token(bucket_name: str):⠀⠀☂️
🌪️ ⠀⠀⠀global ⭕corrosive_buckets⠀⠀⠀⠀💥
⠀⠀⠀⠀ bucket = corrosive_buckets.get(bucket_name)☠️
   ☢️⠀⠀⠀⠀if bucket:⠀⠀⠀⠀⠀⠀
⠀⠀⚡⠀⠀⠀⠀☄️☄️await bucket.wait_for_tokens()⠀⠀⠀⠀⚡☄️

🔮 def ✨funcinfo_to_pool(self, 🔥func_info: FunctionInfo🔥, sut_name):⠀⠀⠀
(•🌑•)⠀⠀⠀⠀⠀⠀⠀for file 🌿 in func_info.filenames:⠀⠀⠀⠀⠀
⛰️ with open(file, 'r') as file: 🌠☠️
⠀🎭yaml_data🎭 = yaml.safe_load(file)☄️
(👁️👄👁️)⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀for corro in 🧬yaml_data['corroz']:🧬
   🍄 task_data_immutable = 🦠CorrosiveTaskDataImmutable🦠(
⠀⠀⠀⠀⠀⠀🍥task_id = str(uuid4())🍥
⠀⠀⠀⠀⠀⠀👾name = corro['name']👾
⠀⠀⠀⠀⠀⠀🔗func=func_info🔗
    ⠀⠀⠀⛓️args = [corro['args'][arg] for arg in corro['args']]⛓️
⠀⠀⠀⠀⠀⠀s u t _ n a m e  = ☢️ sut_name☢️
⠀⠀⠀⠀⠀⠀⠀)
🌈task_data🌈 = 🧪CorrosiveTaskData🧪(
         🧠immutable = task_data_immutable🧠
         🔥meta_data = {},🔥
         🧯result = None🧯
        )
✨✨tc = 🌀copy.deepcopy🌀(task_data)✨
🔮🔮self.pool.append(tc)🔮🔮"""

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

def show_colored_ascii_art_flash(color_choice="blue"):
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
        f"{color1}        ___            ___            _-_       {reset}",
        f"{color2}       - - -          / - \          -   -      {reset}",
        f"{color3}     -|- - -|-      -| x - |-      -| -   |-    {reset}",
        f"{color4}       \_-_/          \ - /          \___/      {reset}",
        f"{color5}         |- -           |              |        {reset}",
        f"{color6}        / \-           /|\            / \       {reset}",
        f"{color7}       /\_/\          \_Y_\          /___\      {reset}",
    ]

    # Clear the terminal screen
    clear_screen()

    # Print the ASCII art with color
    for line in art:
        print(line)


def show_colored_ascii_artfinal(color_choice="blue"):
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
        f"{color2}       /   \          / - \          /-  \      {reset}",
        f"{color3}     0|)o-O)|-)     -| - - |-      -|- o -|-    {reset}",
        f"{color4}       \___/          \ - /          \_-_/      {reset}",
        f"{color5}         |              |              |        {reset}",
        f"{color6}        / \            /|\            / \       {reset}",
        f"{color7}       /___\          /_Y_\          /___\      {reset}",
    ]

    # Clear the terminal screen
    clear_screen()

    # Print the ASCII art with color
    for line in art:
        print(line)

def show_colored_ascii_art_glitch():
    color1 = colors[random.randint(0, 6)]
    color2 = colors[random.randint(0, 6)]
    reset = "\033[0m"
    
    art = [
        f"{color1}        ___       ___         ___      {reset}",
        f"{color2}      / x \     /   \       / -  \     {reset}",
        f"{color1}   --|  0  |-  -| o o |-   -|  x x |-  {reset}",
        f"{color2}      \___/     \_-_/       \ - /      {reset}",
        f"{color1}        |         |           |        {reset}",
        f"{color2}       / \       /|\         / \       {reset}",
        f"{color1}     /__ \     / _Y_\      /__  \      {reset}",
    ]

    clear_screen()
    for line in art:
        print(line)

def loop_between_normal_and_glitch(repeat_count=10):
    for i in range(repeat_count):
        if i % 2 == 0:
            show_colored_ascii_artfinal()  # Normal final version
        else:
            show_colored_ascii_art_glitch()  # Glitchy version
        
        # Random delay between frames to make the transitions unpredictable
        time.sleep(random.uniform(0.0, 0.3))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
lucky_scary = random.randint(0, 3333)

if __name__=='__main__':
    for i in range(0,33):
        clear_screen()
        show_colored_ascii_art()
        time.sleep(0.00033)
    for i in range(0, 6):
        clear_screen()
        int1 = random.randint(0, len(jumbled_code))
        int2 = random.randint(int1, len(jumbled_code))
        if lucky_scary == 0x0c:
            print(jumbled_code[int1:int2])
        show_colored_ascii_art_flash()
        time.sleep(0.00033)
    for i in range(0,33):
        if lucky_scary == 0x0c:
            int1 = random.randint(0, len(jumbled_code))
            int2 = random.randint(int1, len(jumbled_code))
            print(jumbled_code[int1:int2])
        clear_screen()
        show_colored_ascii_artfinal()
        int1 = random.randint(0, len(jumbled_code))
        int2 = random.randint(int1, len(jumbled_code))
        time.sleep(0.00033)
    # Initial flicker effect with variable speeds
    for i in range(0, 33):
        clear_screen()
        show_colored_ascii_art()
        time.sleep(random.uniform(0.0001, 0.001))  # More variable timing for effect

    loop_between_normal_and_glitch()

    # Flashing with occasional jumbled code printouts
    for i in range(0, 6):
        clear_screen()
        int1 = random.randint(0, len(jumbled_code))
        int2 = random.randint(int1, len(jumbled_code))
        
        # Slightly increased chance of printing jumbled code
        if lucky_scary % 13 == 0:
            print(jumbled_code[int1:int2])
        
        show_colored_ascii_art_flash()
        time.sleep(random.uniform(0.0001, 0.001))  # Variable timing

    # Final phase with a more intense flicker effect
    for i in range(0, 33):
        if lucky_scary % 42 == 0:
            int1 = random.randint(0, len(jumbled_code))
            int2 = random.randint(int1, len(jumbled_code))
            print(jumbled_code[int1:int2])
        
        clear_screen()
        show_colored_ascii_artfinal()
        time.sleep(random.uniform(0.0001, 0.001))  # Variable timing
