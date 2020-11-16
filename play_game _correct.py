import json, random
import time, os

def choose_from_list(Q, L):
    print(Q)
    i=1
    for element in L:
        print("  ",i,")", element)
        i=i+1
    choice= int(input(">"))
    if choice not in range(1,len(L)+1):
        return -1
    else:
        return choice-1

def main():
    # TODO: allow them to choose from multiple JSON files?
    Q="What game would you like to play?"
    jsonfiles=[]
    for x in os.listdir():
        if x.endswith(".json") ==True:
            jsonfiles.append(x)
    choice=choose_from_list(Q,jsonfiles)
    if choice >= 0:
        print("You chose", jsonfiles[choice])
        print("")
    else:
        print("That game doesn't exist. Try again later lol")
        return
    
    with open(jsonfiles[choice]) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)

def play(rooms):
    # Where are we? Look in __metadata__ for the room we should start in first.
    current_place = rooms['__metadata__']['start']
    # The things the player has collected.
    stuff = ['Dead Cell Phone', 'Wallet', 'Car Keys']
    visited = {}

    while True:
        print("")
        print("")
        # Figure out what room we're in -- current_place is a name.
        here = rooms[current_place]
        # Print the description.
        print(here["description"])
        
        move_cat(current_place, rooms, stuff)
        
        if current_place in visited: #searches dictionary to see if player has been there before
            print("~~~You've been here before~~~.")
        visited[current_place]=True #puts where the player has been into a dictionary
        
        
        # TODO: print any available items in the room...
        # e.g., There is a Mansion Key.
        if len(here["items"])>0:
            print("You see",','.join(here["items"]))

        # Is this a game-over?
        if here.get("ends_game", False):
            break

        # Allow the user to choose an exit:
        usable_exits = find_usable_exits(here, stuff)
        # Print out numbers for them to choose:
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        # See what they typed:
        action = input("> ").lower().strip()

        # If they type any variant of quit; exit the game.
        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break

        if action == "stuff":
            empty=[]
            if stuff==empty:
                print('You have nothing')
            else:
                print(",".join(stuff))
            continue
        
            #we want to stay where it is so go back to room where it was
        if action == "help":
            print_instructions()
            continue
        
        if action == "take":
            if len(here["items"])>0:
                for x in here["items"]:
                    stuff.append(x)
                print(stuff)
                here["items"]={}
            continue

        if action == "drop":
            if len(stuff)>0:
                print("Choose an item to drop:")
                for i, x in enumerate(stuff,1):
                    print("  {}.{}".format(i,x))
                pick=input("- ").lower().strip()
                try:
                    num = int(pick)
                    selected = stuff[num-1]
                    stuff.pop(num-1)
                    here["items"].append(selected)
                except:
                    print("I don't understand '{}'... please choose a number".format(pick))
            else:
                print("You have nothing to drop.")
            continue
        
        if action in ["search"]:
            for x in rooms[current_place]["exits"]:
                x["hidden"]=False
            #show hidden exits
                
        # TODO: if they type "take", grab any items in the room.
        # TODO: if they type "search", or "find", look through any exits in the room that might be hidden, and make them not hidden anymore!
        
        # Try to turn their action into an exit, by number.
        try:
            num = int(action) - 1
            selected = usable_exits[num]
            current_place = selected['destination']
            print("...")
            #move locked portion to here
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    print("=== GAME OVER ===")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        #move this portion up or make 2 separate functions where we have the key vs not or can see vs not
        if "required_key" in exit:
            if exit["required_key"] in stuff:
                usable.append(exit)
            continue
        usable.append(exit)
    return usable

def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

def move_cat(current_place, rooms, stuff):
    x=list(rooms)
    x.pop(0)
    place=random.choice(x)
    if place==current_place:
        print("You see a Cute Black Cat")
    if "Canned Tuna" in stuff:
        print("You see a Cute Black Cat.... It's purring and seems hungry")
        
#def deadends():
    #loop through to make a list of rooms
    #is there some way to check inside a function?
    

start=time.time()
if __name__ == '__main__':
    main()
end=time.time()
print("You played the game for about", (end-start)//1, "seconds.")