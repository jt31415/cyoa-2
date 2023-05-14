import json, time, sys

DEBUG = False

with open('story.json',encoding="utf-8") as f:
    story = json.load(f)

world = {}

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def sprint(text):
    if DEBUG:
        print(text)
    else:
        for l in text:
            print(l,end='')
            sys.stdout.flush()
            time.sleep(0.01)
        print()

def check(conditional):
    conditional = conditional.split()
    for condition in range(0,len(conditional),2):
        if conditional[condition].startswith('!'):
            if conditional[condition][1:] in world.keys():
                if world[conditional[condition][1:]]:
                    return False
        else:
            if not conditional[condition] in world.keys():
                return False
            else:
                if not world[conditional[condition]]:
                    return False
    return True

def load_choice(c):
    global current, world
    
    # change current
    if c == None:
        sprint("That's not a valid choice.")
        print()
    elif c == "gameover":
        sprint("x_x You died. x_x\nWant to try again? (y/n)")
        inp = input()
        if inp.lower() == 'y':
            load_choice('begin')
        else:
            exit(0)
    elif c == "end":
        sprint("Congratulations! You've reached the end of the story (so far).\nThank you for playing! :D")
        input()
        exit(0)
    else:
        current = story[str(c)]

        # print story
        sprint(current['text'])
        print()
        
        # vars
        if 'vars' in current.keys():
            for var in current['vars']:
                world[var] = current['vars'][var]

def do_current():
    global current


    if 'fork' in current.keys():
        if current['fork']:
            for i, conditional in enumerate(current['choices']):
                if check(conditional):
                    load_choice(list(current['choices'].values())[i])

    else:
                        
        # print choices
        if len(current['choices']) > 1:
            for i, c in enumerate(current['choices']):
                sprint(f'{alphabet[i]}) {c}')
            print()
        else: # if there is only 1 choice
            load_choice(list(current['choices'].values())[0])
            return
    
        # get choice
        choice = None
        inp = input('-> ').lower()
        print()
    
        if not inp:
            load_choice(choice) # will result in "not a valid choice"
        # if it's a letter
        elif inp in alphabet and len(inp)==1:
            try:
                choice = list(current['choices'].values())[alphabet.index(inp)]
            except:
                pass
        # if it's a word
        else:
            for i, c in enumerate(current['choices']):
                if inp in c.lower():
                    choice = current['choices'][c]
                    break
    
        load_choice(choice)

load_choice('begin')

while True:

    do_current()