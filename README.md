**PYTHON VERSION** 3.10.10
**PYGAME VERSION** 2.1.2
**WINDOWS EDITION** Windows 10 Pro
**WINDOWS VERSION** 21H2
**WINDOWS OS BUILD** 19044.2604



***INSTRUCTIONS***
- The game will begin as soon as the program is launched
- Move with the arrow keys
- Dodge the Nautilus
    the Nautilus will move across the screen and gradually increase speed (up to a limit)
- Avoid seaweed
    seaweed will limit player speed when touched; more seaweed will gradually appear
- The 'dodge count' will increment every time the Nautilus exits the left side of the screen, after this the Nautilus will reappear from the right side of the screen



***HOW TO LOSE***
- If you touch the Nautilus: GAME OVER
***HOW TO WIN***
- If you dodge the Nautilus 30 times: YOU WIN
***MOTIVATION***
I have become fascinated with the geologic timescale recently and have been studying the different periods of the Paleozoic Era. I wanted my game setting to be related to this. I chose for the protagonist to by a Trilobite, one of the primary arthropods of the Paleozoic Era. I decided for the enemy to be a Nautilus, a cool looking cephalopod. Cephalopods were the primary predators of the Ordivician Period. While the Nautilus size may be exaggerated and Trilobites may not have been direct prey I thought they were both cool organisms to work with.
I wanted the game to be related to surviving "stages".
***REASONING***
I used classes to distinguish the sprites/entities in my game. It made it much easier to organize, identify, and manipulate each relative entity. The gameplay gets tougher by "activating" more obstacle entities or increasing the enemy speed as the score increases.
The sprites all have 1-2 rects. The seaweed obstacle sprite has a single rect with the image placed over it. The animated sprites have 2 rects: 1 to lay the animation over and identify its borders and 1 other to act as a "hitbox" for detecting collisions. I used a separate rect for a hitbox because the rect outlining the animation does not account for "blank space" well.
***FUTURE WORK***
I could invest more time in the images for smoother and more detailed animation.
I could develop more precise collision detection.
I could include a better user interface, including a menu, more detailed instructions, and play again button as well as storing high scores.
I could add changing stages or levels with different backgrounds/settings, obstacles, and enemies.
Lastly, there is a lot of conditional code in the game loop that could be consolidated into functions outside the game loop. This would support a cleaner and more organized look/function.

Similar to any basic survival game with progressing stages where difficulty gradually increases.



**GAME DOCUMENT**
***MAIN GAME SCRIPT***
main.py is my main game script. I decided not to separate code into different py files although I plan to in the future. The reason I did not separate them was simply because I have never worked with python to this level and was not prepared to isolate too much code. I did have spritesheet.py which includes functions that are used to extract individual images from sprite sheets for animation purposes (spritesheet.py is code taken from a YouTube channel reference in the top of the file).
***GAME LOOP***
The game loop handles all blits or drawing on the screen, although, some code related to drawing is outside the loop and in functions that are called in the game loop.
The game loop also handles input events related to keys. However, the player class also using key detectiong to track certain mechanics.
***MODEL***
The majority of the 'model' component of my game are in the sprite classes or in constants stored outside them.
***VIEW***
There are several different sections of code that blit/draw on the screen and update different conditions of the game. The view is not well comprised to a single place in the file. However, some of the blits must be separated to ensure the proper layout of images on the screen.
***CONTROLLER***
The game logic and controls are handled within the game loop and the sprites classes. I am unfamaliar with event queues.
***ENTITIES***
The game includes a player entity, enemy entity, obstacle entities, and decorative entities. The 'decorative entities' are less necessary to be destinguished with a class but it was the easiest to implement at the time.
Player class is the *player character*.