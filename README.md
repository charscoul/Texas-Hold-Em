The .py file in this repository is the code to run a player vs computer tournament of Texas Hold-em Poker. This is my Capstone project for Sigma Labs

The tournament is completely terminal based, using numerical inputs to provide set-up information for the game, navigate between actions, and set stakes for raising bets.
The computer-operated players within the tournament will have their actions displayed in plain text
The player's cards and the cards on the table are printed as basic playing cards, using plain text characters and emojis. The other players cards are only revealed at the point of of comparing hands to see who wins a given pot.

The code includes (to my understanding) accurate Texas hold-em betting mechanics, including:
- Burning cards before each game stage
- The moving of blinds
- Minimum raise amounts based on previous raises
- Broadly correct terminology to describe game stages and collections of cards
- The correct division of chips into separate pots when dealing with game-states where only some players are all-in

In its current state on the main branch, the opponent betting behavior is not sophisticated, instead randomising across the actions the player can take at a given point, randomising the raise amount within the possible range if that is the option selected
The behaviour branch is where I intend to improve these behaviors, but the main branch is fully playable

Explaining the code:

I have separated my code into sections to allow easier explanations and understanding for the functions within:
1. Section 1 - The cards
  - The functions in this section serve to establish the backbone of both the visual interface, and the scoring of poker hands - mainly revolving around the cards themselves
  - The cards are displayed using -, |, their numeric / letter value and the emoji for their suit, to construct the cards in the terminal, as I found this more engaging than just plain text descriptions of the cards. For this reason the code doesn't run well on a terminal that is set to dark-mode, as it removes the white backgrounds of the card and makes the club or spade suits harder to distinguish.
  - The dealing mechanic is something I intend to improve in a branch, changing it from the current system of randomly selecting a card by index form an ordered deck list for each dealt / burnt card, to a system that shuffles the deck as you would shuffle a real deck, and selects the first card from the deck each time
  - The scoring mechanics iterate over all possible hands that can be made with the cards in a player's pocket and the cards on the table, the type of each hand is then identified, and ranked against the global span dictionaries to allow comparisons across hands, deciding the player's best hand, or the winner between two players' hands
  - The nuts is the best possible hand that could be made using the cards shown on the table, supplemented by the ideal two cards from the deck. I created a function to identify the nuts which I haven't yet used, as I intend to use it to help inform the decision making of the computer-controlled opponents, by comparing the strength of their hand to the strength of the nuts, to assess how strong their hand is relative to other possible hands

2. Section 2 - The betting
  - The functions in this section serve to track player's chips throughout a hand, and more broadly a tournament. The backbone is a list of dictionaries that describe what position a player is in relative to the current hand, and allow betting to flow around the 'table' appropriately
  - A separate function exists for each of the action a player may take when it is their turn to act (check, call, fold, raise, re-raise, all-in), with raise and re-raise then asking for further input to determine raise amount.
  - The chips aren't taken from a player's balance until the end of a hand, though they are displayed to be within the terminal. Instead, at the end of a hand all chips that a player is "In For" (has bet) are collected into pots and removed from their Chip Total
  - In most cases, and always in the first hand of a tournament, there are no more than 1 pots. More pots are only made when a player has bet all-in, but their chip total is lower than the current bet, this means that if they have the winning hand they are only eligible to win chips in the main pot, and other players who bet higher can play for the remaining side pots
  - The actions available to a player are determined by their chip total, the amount they have bet so far, the current highest bet amount, the size of the previous raise, and the second-highest chip total among remaining players
  - Players are only able to take actions that are supported by their current position, avoiding any errors due to missing/ incorrect variable or calculations. two exceptions exist:
    1. I have not given the player the ability to fold if they are already in for the maximum bet, as this is an irresponsible decision, and a mistake that lots of beginners make
    2. In the pre-flop betting round, players who were not the big blind are presented with the re-raise option, despite no prior raise being made. This is due to the way my code distinguishes between raising and re-raising, and needs to be corrected
  - The player's actions are selected by inputing a printed numerical reference
  - The opponents actions are chosen at random, as explained before, I intend to provide more sophisticated decision making once I begin Section 3

3. Section 3 - Basic gameplay
  - The basic_play_hand function creates the gameplay experience, as it exists in a game of Texas Hold-em
  - The code in the basic_play_hand function could be simplified using sub functions, particularly for the often repeated tests, or for a betting stage, which I could pass the stage name into to achieve some of the minor differences between rounds. I intend to do this, and the only reason I did not do it earlier was that when building and testing the function I expected greater differences between each stage
  - The basic_play_tournament function contains the current gameplay experience, and tracks chip totals between hands, modifying the active player list accordingly.

4. Section 4 - Opponent behavior
  - This section doesn't currently exist, but the #notes provide the skeleton for what I hope to achieve.
  - The aggressiveness scores I intend to be randomly created within a range at the point of initiating the game. These would then be stored in a list of dictionaries, each describing a player's behaviours
  - Hand quality will be determined relative to the nuts
  - Pocket quality will be determined and used in the place of hand quality pre-flop, using a new global-span dictionary, ranking hands like pocket Aces very highly, and 7-2 off suit very poorly
  - I may attempt to create a vague "prediction" score, that infers strength of opponent's pockets based on betting behavior, and beliefs regarding bluffs using a 'skepticism' score, as this is a key part of poker, but I am not sure if it is something I am capable of at this stage
  - The opponent's action, and raise amount, will then be determined by getting a random number, weighting it based on hand score and player behaviors, then using a global span dictionary to determine what action / bet the corresponding score relates to.
  - This method should ensure variety among opponents, sufficient variety within an opponent to make it difficult for the player to accurately gauge their strategy, and as opposed to random actions it should reduce the likelihood of huge raises or going all-in pre flop
  - A player only chooses whether to reveal cards in Texas hold-em at the point where they win a hand based on all other players folding. A 'showmanship' score and random value would determine whether an opponent chooses to do this

5. Section 5 - tests and the main function
   - This section is where I have run code outside of function definitions to test functionality and allow debugging
   - The main function is the way in which the code is run

Other areas i wish to improve:


