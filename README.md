# GatorHoldEm

Github Repo: https://github.com/y0sh12/GatorHoldEm

Description:
GatorHoldEm is a desktop poker application which allows users to play one another or with an Artificial Intelligence robot. In order to play, users just have to open the application and play on a room of their choice. The first person to join a room becomes the 'VIP' and has the ability to add and remove players and AI bots as well as start the game. In order to start the game, you must have atleast two people in the room (including AI bots) and a maximum of 6 people. Once in the game, use the start game button to start the game. At the end of the game you will be returned to the main menu. 

Artificial Intelligence Implementation:
* The AI bots in this game are programmed to make a calculated choice depending on its own hand of cards.
* It uses the Two Plus Two evaluator which consists of a large lookup table containing some thirty-two million entries (32,487,834 to be precise).
* It considers all possible 7 card hands that can be held by the other players to determine its own hand strength which is turn used to perform a Call, Fold or Raise.
* It also includes a method of decision when it comes to the bluffing of certain actions.
* A game cannot be played with ONLY two AI bots playing against each other.

Installation: 
1. Use `pip install GatorHoldEm` to install the library dependencies
2. Run the command `gatorholdemserver` to start the server.
3. Run the command `gatorholdem` to run a client*.
4. If you want to play with multiple real players, run `gatorholdem` in another terminal to start a new client.

    *If using WSL, you will need an X server to support graphical display

Members of the group:

- Yaswanth Potluri

- Azharullah Baig

- Sean O'Reilly

- Bharat Samineni

- Adriel Mohammed

CONTRIBUTIONS:
- Backend Game Logic (Bharat and Adriel)
- Server and Client creation and communication (Yaswanth)
- AI Bot (Sean and Bharat)
- Front end UI (Sean, Azhar and Adriel)
(Important Note)
- Sean and Bharat have worked together on the Visual Studio Code's LiveShare for the AI, which is a tool platform that lets multiple individuals work together on the same code simulataneously. 
    Therefore, most of the commits of Bharat's git is a reflection of both Bharat AND Sean's work. Please consider this when evaluating the contributions. 

CITED SOURCES:
> https://github.com/chenosaurus/poker-evaluator/blob/master/lib/PokerEvaluator.js (For the AI)

> https://github.com/christophschmalhofer/poker/blob/master/XPokerEval/XPokerEval.TwoPlusTwo/HandRanks.dat (For the AI)

> https://en.wikipedia.org/wiki/Poker_Effective_Hand_Strength_(EHS)_algorithm (For the AI)

> https://www.codingthewheel.com/archives/poker-hand-evaluator-roundup/#2p2 (For the AI)

Attributions for Art: 
wordart.com, Chips image(poker_chips.png) from vector stock
Poker Chip (tablebet.png) by Linh Nguyen from the Noun Project


