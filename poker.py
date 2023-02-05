'''
3 Card Poker
poker.py
Theresa Rumoro and Caroline Canfield

This program runs a 3 card poker game and uses a cheat algorithm that uses the
cost of relationships to determine whether it should cheat.

Resources that we used:
    -We used these resources to import the pydealer, which makes the deck.
    -It was also informational to help us through the methods that the pydealer provides.
https://pypi.org/project/pydealer/
https://pydealer.readthedocs.io/en/latest/usage.html#import-specific-classes-functions
'''

'''
Import needed libraries
'''
from array import array
from ast import Index
from tkinter import FIRST
from tokenize import PseudoToken
import pydealer
import string
import math

'''
Create global functions, wins and total_rounds, to use throughout program
'''
wins = int(0)
total_rounds = int(0)
# check_deck = pydealer.Deck()

'''
Establish the rules of the game
'''
def rules():
    # Print the rules of the game
    print ('\n', "The rules of the game are as follows: ")
    print ('\t', " - The user will be asked to start the game")
    print ('\t', " - The user will place the first bet to start the game")
    print ('\t', " - The tokens for both players will be displayed")
    print ('\t', " - The user can then bet or fold based on the card")
    print ('\t', " - If the user folds, the computer wins the round and the round ends")
    print ('\t', " - The computer will then either match, raise, or fold")
    print ('\t', " - If the computer folds, the user wins the round and the round ends")
    print ('\t', " - If the computer matches or raises, the user will then be asked if they want to match or fold")
    print ('\t', " - If the user folds, the computer wins the round and the round ends")
    print ('\t', " - If the user matches, the cards are compared and whoever has: ")
    print ('\t\t', " - Hand relationships such as: straight flush, straight, flush, three of a kind, or two of a kind")
    print ('\t\t', " - If there is no relationship, the winning hand will be chosen by who has the highest card")
    print ('\t', " - The winner is declared and the user is asked if they want to continue")
    print ('\t', " - The stats are shown after each round", '\n')
    return


'''
Prompts the user to see if they want to continue or end the game. The parameter is continue_prompt
'''
def continue_game(continue_prompt):

    # Print statement
    continue_prompt = input("Want to continue (or start) playing? Y for yes, N for no.")
    print(" ")

    # Assign variables to determine the user response
    yes = int(1)
    no = int(0)

    # If the user wants to continue, return yes
    if (continue_prompt == 'Y' or continue_prompt == 'y'):
        return yes

    # If the user does not want to continue, return no
    elif (continue_prompt == 'N' or continue_prompt == 'n'):
        return no

    # If the input is a digit, prompt the user to try again and call this function again
    elif (continue_prompt.isdigit() == True):
        print('Not a valid response. Please try again.')
        return continue_game(continue_prompt)

    # Else there is not a valid response, prompt the user to try again and call this function again
    else:
        print('Not a valid response. Please try again.')
        return continue_game(continue_prompt)


'''
create_decks has no parameters and creates the decks and the hands.
It also deals 3 cards to each hand from the shuffled deck.
This function returns both hands.
'''
def create_decks():

    # Use library to create a deck of cards and to shuffle the deck so that it is random
    poker_deck = pydealer.Deck()
    poker_deck.shuffle()

    # Create two hands using the Stack() method, one for the computer and user
    computer_hand = pydealer.Stack()
    user_hand = pydealer.Stack()
    
    # Deal 3 cards to each of the hands: computer and user
    computer_cards = poker_deck.deal(3)
    user_cards = poker_deck.deal(3)

    # Add the dealt cards to the hands
    computer_hand.add(computer_cards)
    user_hand.add(user_cards)

    # Return both hands
    return computer_hand, user_hand


'''
create_tokens create the currency for the game. No parameters are taken in.
'''
def create_tokens():

    # The computer and the user start with 2000
    computer_tokens = 2000
    user_tokens = 2000

    # Return the computer_tokens and the user_tokens
    return computer_tokens, user_tokens


'''
display_tokens has the parameter values of the computer and user tokens and it prints the values.
'''
def display_tokens(new_computer_tokens, new_user_tokens):

    # Print the value for the user tokens and the computer tokens
    print ('The user has: ', new_user_tokens, ' tokens.')
    print ('The computer has: ', new_computer_tokens, ' tokens.', '\n')


'''
betting takes in the user_tokens, computer_tokens, computer_hand, and user_hand parameters. This function controls all of the
betting and checks for errors. This function also calls other functions to split up the work.
'''
def betting(user_tokens, computer_tokens, new_computer_hand, new_user_hand):

    # Create the lists for the computer and user hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Call global variables so we can use them later
    global wins
    global total_rounds

    # Create a variable total_bet with the value of 0
    total_bet = int(0)

    # Call first_bet with the parameter user_tokens and turn it into an integer and then set it equal to starting_bet
    starting_bet = int(first_bet(user_tokens))

    # Add the starting_bet to the total_bet
    total_bet += starting_bet
    # Subtract the total_bet from the user_tokens
    user_tokens -= total_bet

    # Call show_two_cards function with computer_hand and user_hand functions to print the first two cards
    show_two_cards(computer_hand, user_hand)

    # Call user_bet with the parameter user_tokens and turn it into an integer and then set it equal to bet
    bet = int(user_bet(user_tokens))

    # If bet equals zero, the user decided to fold
    if (bet == 0):
        # Incremenet the wins for the computer
        wins += 1
        # Increment the rounds
        total_rounds += 1
        # Add the total_bet to the computer_tokens
        computer_tokens += total_bet
        # Return user_tokens, computer_tokens, computer_hand, and user_hand
        return user_tokens, computer_tokens, computer_hand, user_hand

    # Else, the user decided to place a bet
    else:
        # Add the bet to the total_bet
        total_bet += bet
        # Subtract the bet from the user_tokens
        user_tokens -= bet

        # Call computer_bet with the computer_tokens, user_tokens, bet, user_hand, computer_hand
        comp_bet = computer_bet(computer_tokens, user_tokens, bet, user_hand, computer_hand)

        # If the comp_bet is 0, the computer will fold and return user_tokens and computer_tokens
        if (comp_bet == 0):
            # Add the total_bet to the user_tokens
            user_tokens += total_bet
            # Increment the rounds
            total_rounds += 1
            # Print that user won
            print("Congrats user! You won!")
            # Return user_tokens, computer_tokens, computer_hand, and user_hand
            return user_tokens, computer_tokens, computer_hand, user_hand

        # Else, the computer placed a bet
        else:
            # Add comp_bet to total_bet
            total_bet += comp_bet
            # Subtract comp_bet from computer_tokens
            computer_tokens -= comp_bet

        # If the computer should cheat
        if (check_comp_should_cheat(user_hand, computer_hand)):
            # Call highest_possible_relationship to find the new hands with the new relationship
            new_computer_hand, new_user_hand = highest_possible_relationship(computer_hand, user_hand)
            # Set new_computer_hand equal to computer_hand
            computer_hand = new_computer_hand
            # Set new_user_hand equal to user_hand
            user_hand = new_user_hand
            # Add the comp_bet to the total_bet
            total_bet += comp_bet
            # Subtract the comp_bet from the computer_tokens
            computer_tokens -= comp_bet
            #
            last_decision = user_last_bet(user_tokens)
            # If user_last_bet with the paramter user_tokens is True, meaning the user wants to match
            if (last_decision == 1):
                # Set the last_bet equal to the comp_bet to match
                last_bet = comp_bet
                # Add the last_bet to the total_bet
                total_bet += last_bet
                user_tokens -= last_bet

                # If the user has the winning hand
                if (winning_hand(user_hand, computer_hand)):
                    # Add the total_bet to the user_tokens
                    user_tokens += total_bet
                    # Print that the user won
                    print("Congrats user! You won!")
                    # Increment total_rounds
                    total_rounds += 1
                    # Return user_tokens, computer_tokens, computer_hand, and user_hand
                    return user_tokens, computer_tokens, computer_hand, user_hand

                # Else, the computer had the winning hand
                else:
                    # Add the total_bet to the computer_tokens
                    computer_tokens += total_bet
                    # Print that the user lost
                    print("Better luck next time!")
                    # Increment wins and total_rounds
                    wins += 1
                    total_rounds += 1
                    # Return user_tokens, computer_tokens, computer_hand, and user_hand
                    return user_tokens, computer_tokens, computer_hand, user_hand

            # Else, the user wants to fold
            else:
                # Increment wins and total_rounds
                wins += 1
                total_rounds += 1
                # Add the total_bet to the computer_tokens
                computer_tokens += total_bet
                # Print that the user lost
                print("Better luck next time!")
                # Return user_tokens, computer_tokens, computer_hand, and user_hand
                return user_tokens, computer_tokens, computer_hand, user_hand
        
        # If the computer should not cheat
        else:
            # Add the comp_bet to the total_bet
            total_bet += comp_bet
            # Subtract the comp_bet from the computer_tokens
            computer_tokens -= comp_bet
            # Assign the user's last betting decision to last_decision
            last_decision = user_last_bet(user_tokens)

            # If the user wants to match
            if (last_decision == 1):
                # Set the last_bet equal to the comp_bet to match the value
                last_bet = comp_bet
                # Add the last_bet to the total_bet
                total_bet += last_bet
                # Subtract the last_bet from the user_tokens
                user_tokens -= last_bet

                # If the user has a better hand cost
                if (winning_hand(user_hand, computer_hand)):
                    # Add the total_bet to the user_tokens
                    user_tokens += total_bet
                    # Print that the user won
                    print("Congrats user! You won!")
                    # Increment the total_rounds
                    total_rounds += 1
                    # Return user_tokens, computer_tokens, computer_hand, and user_hand
                    return user_tokens, computer_tokens, computer_hand, user_hand
                
                # If the computer has a better hand cost
                else:
                    # Add the total_bet to the computer_tokens
                    computer_tokens += total_bet
                    # Print that the user lost
                    print("Better luck next time!")
                    # Increment the wins and total_rounds
                    wins += 1
                    total_rounds += 1
                    # Return user_tokens, computer_tokens, computer_hand, and user_hand
                    return user_tokens, computer_tokens, computer_hand, user_hand

            # Else, the user wants to fold
            else:
                # Increment the wins and total_rounds
                wins += 1
                total_rounds += 1
                # Add the total_bet to the computer_tokens
                computer_tokens += total_bet
                # Print that the user lost
                print("Better luck next time!")
                # Return user_tokens, computer_tokens, computer_hand, and user_hand
                return user_tokens, computer_tokens, computer_hand, user_hand


'''
first_bet with the parameter user_tokens lets the user place the first bet to start the game
'''
def first_bet(user_tokens):

    # Let the user place and bet and set it equal to bet
    bet = input("User: Please place your first bet: ")

    # If the bet is a digit, which is the goal
    if (bet.isdigit() == True):
        # Turn the bet variable into an integer from a string
        bet = int(bet)

        # If the bet is greater than the user_tokens
        if (bet > user_tokens):
            # Prompt user to try again because they do not have that much money
            print("You don't have that much money! Try again.")
            # Call this function, first_bet with the paramter user_tokens, again for the user
            return first_bet(user_tokens)

        # If the bet is 0
        elif (bet == 0):
            # Prompt user to try again because they need to bet more than zero
            print("Please bet more than 0. Try again.")
            # Call this function, first_bet with the parameter user_tokens, again for the user
            return first_bet(user_tokens)
        
        # Else, the bet is good
        else:
            # Return bet
            return bet

    # Else the user inputted another character other than a digit
    else:
        # Prompr user to try again because they need to input a digit
        print("Not a valid response. Please try again.")
        # Call this function, first_bet with the parameter user_tokens, again for the user
        return first_bet(user_tokens)


'''
show_two_cards takes in the computer_hand and user_hand parameters. This function is used to show the first two cards in each hand.
'''
def show_two_cards(new_computer_hand, new_user_hand):

    # Create lists for the computer and user hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1]]
    user_hand = [new_user_hand[0], new_user_hand[1]]

    # Print the first and second card of each hand and include ___ for the third card
    print ('\n', "Computer's hand: ", computer_hand[0], ' ', computer_hand[1], ' ', "___")
    print ('\n', "User's hand: ", user_hand[0], ' ', user_hand[1], ' ', "___", "\n")


'''
user_bet with the parameter user_tokens lets the user place a bet
'''
def user_bet(user_tokens):

    # Prompt the user to enter a bet or zero to fold and set it equal to bet
    bet = input("User: Place a bet or enter 0 to fold: ")

    # If the bet is a digit, which is the goal    
    if (bet.isdigit() == True):
        # Turn the bet variable into an integer from a string
        bet = int(bet)

        # If the bet is greater than the user_tokens
        if (bet > user_tokens):
            # Prompt user to try again because they do not have that much money
            print("You don't have that much money! Try again.")
            # Call this function, user_bet with the paramter user_tokens, again for the user
            return user_bet(user_tokens)

        # Else, the bet is good or is equal to zero, which means the user will fold
        else:
            # Return bet
            return bet

    # Else the user inputted another character other than a digit
    else:
        # Prompr user to try again because they need to input a digit        
        print("Not a valid response. Please try again.")
        # Call this function, user_bet with the parameter user_tokens, again for the user        
        return user_bet(user_tokens)


'''
This function determines whether the computer should cheat, place a bet, or fold. The parameters are
computer_tokens, user_tokens, bet, new_user_hand, new_computer_hand. It returns the bet.
'''
def computer_bet(computer_tokens, user_tokens, bet, new_user_hand, new_computer_hand):

    # Create lists with values
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]

    # If the computer should cheat, call the function
    if (check_comp_should_cheat(user_hand, computer_hand)):
        # Find the cost of the first 
        cost = int(find_cost_card(computer_hand[1]))
        # If the number is even
        if ((cost % 2) == 0):
            # Call raise_bet function and set it equal to new_bet, return new_bet
            new_bet = int(raise_bet(computer_tokens, user_tokens, bet))
            return new_bet

        # Else the number is odd
        else:
            # Match the bet by setting the bet equal to comp_bet
            comp_bet = int(bet)
            # Let the user know the computer is matching, return comp_bet
            print("Computer: Place bet, raise, or fold: Match ", comp_bet)
            return comp_bet

    else:
        # If the hand relationship is below 21 and the user has the highest card, the computer will raise the bet, and return new_bet
        if ((int(hand_relationship_cost(computer_hand)) <= 21) and (check_computer_highest_two_card(user_hand, computer_hand))):
            # Call raise_bet and set it equal to new_bet and return the new bet
            new_bet = raise_bet(computer_tokens, user_tokens, bet)
            return new_bet

        # If the hand relationship is above 22, the computer will fold and return comp_bet
        elif ((int(hand_relationship_cost(computer_hand)) >= 22)):
            # Set comp_bet equal to 0
            comp_bet = 0
            # Print that computer will fold
            print("Computer: Place bet, raise, or fold: Fold")
            return comp_bet

        # Else, raise bet and return new_bet
        else:
            # Call raise_bet and set it equal to new_bet and return the new bet
            new_bet = raise_bet(computer_tokens, user_tokens, bet)
            return new_bet


'''
checks if the computer should cheat or not by going through all possible relationships
'''
def check_comp_should_cheat(user_hand, computer_hand):

    # Create a list of the computer hand and the user hand
    computer_list = [computer_hand[0], computer_hand[1], computer_hand[2]]
    user_list = [user_hand[0], user_hand[1], user_hand[2]]
    
    # If the computer is winning over 60% of the time, return false
    if game_statistics() >= 60:
        return False

    # Else the computer is losing
    else:
        #Find the cost of the relationship for the user hand
        user_cost = hand_relationship_cost(user_list)
        # Find the cost of the relationship for the computer hand
        comp_cost = hand_relationship_cost(computer_list)

        # If the compuer cost is greater than the user_cost, return false
        if (comp_cost > user_cost):
            return False
        # If the costs are the same
        elif (comp_cost == user_cost):

            # If the user has a better high card, return true
            if ((better_high_card(user_list, computer_list))):
                return True
            # If the user has a better hand has a better hand, return true
            elif (check_computer_better_hand(user_list, computer_list) == False):
                return True
            # Else, return false
            else:
                return False
        
        # Else, return true
        else:
            return True


'''
This function has the parameter specific_card and assigns a value to the card, it returns the integer.
'''
def find_cost_card(specific_card):

    # Assign the variable value to 0
    value = int(0)

    # Create a string of the card
    specific_card = str(specific_card)

    # If the card starts with 2, assign value to 2
    if str(specific_card).startswith('2'):
        value = int(2)

    # If the card starts with 3, assign value to 3
    elif str(specific_card).startswith('3'):
        value = int(3)

    # If the card starts with 4, assign value to 4
    elif str(specific_card).startswith('4'):
        value = int(4)

    # If the card starts with 5, assign value to 5
    elif str(specific_card).startswith('5'):
        value = int(5)

    # If the card starts with 6, assign value to 6
    elif str(specific_card).startswith('6'):
        value = int(6)

    # If the card starts with 7, assign value to 7
    elif str(specific_card).startswith('7'):
        value = int(7)

    # If the card starts with 8, assign value to 8
    elif str(specific_card).startswith('8'):
        value = int(8)

    # If the card starts with 9, assign value to 9
    elif str(specific_card).startswith('9'):
        value = int(9)

    # If the card starts with 10, assign value to 10
    elif str(specific_card).startswith('10'):
        value = int(10)

    # If the card starts with J, assign value to 11
    elif str(specific_card).startswith('J'):
        value = int(11)

    # If the card starts with Q, assign value to 12
    elif str(specific_card).startswith('Q'):
        value = int(12)

    # If the card starts with K, assign value to 13
    elif str(specific_card).startswith('K'):
        value = int(13)

    # Else, assign the value to 14
    else:
        value = int(14)

    # Return the value
    return value


'''
This function lets the computer raise the bet. It has the parameters computer_tokens, user_tokens, and bet.
It returns the value of the bet.
'''
def raise_bet(computer_tokens, user_tokens, bet):

    # Assign the bet value to the new bet
    new_bet = int(bet)

    # If the computer has more tokens than the user
    if (computer_tokens > user_tokens):
        # Assign the value to 0
        value = 0
        # Subtract the uuser_tokens from the computer_tokens
        value = computer_tokens - user_tokens
        # Divide the value by 20 for a random bet
        value = value / 20
        # Add the bet raise to the value
        value += new_bet
        # Round value up
        new_value = math.ceil(value)
        # Print that computer will raise bet by value and return value
        print("Computer: Place bet, raise, or fold: Raise ", new_value)
        return new_value

    # If the computer tokens equal the user_tokens
    elif (computer_tokens == user_tokens):
        # Assign the value to 0
        value = 0
        # Add 10 to the new bet for a random bet
        value = new_bet + 10
        # Add the bet raise to the value
        value += new_bet
        # Print that computer will raise bet by value and return value
        print("Computer: Place bet, raise, or fold: Raise ", value)        
        return value

    # Else the computer has less tokens than the user
    else:
        # Assign the value to 0
        value = 0
        # Subtract the computer_tokens from the user_tokens
        value = user_tokens - computer_tokens
        # Divide the value by 20 for a random bet
        value = value / 20
        # Add the bet raise to the value
        value += new_bet
        # Round value up
        new_value = math.ceil(value)
        # Print that computer will raise bet by value and return value
        print("Computer: Place bet, raise, or fold: Raise ", new_value)
        return new_value


'''
Determines the cost of a users hand. The parameter is a specific had and it returns an int value
'''
def hand_relationship_cost(specific_hand):

    # Assign 0 to value
    value = int(0)

    # If there is a straight flush, assign 24 to value and return value
    if straight_flush(specific_hand):
        value = int(24)
        return value

    # If there is a flush, assign 23 to value and return value
    elif flush(specific_hand):
        value = int(23)
        return value

    # If there is a straight, assign 22 to value and return value
    elif straight(specific_hand):
        value = int(22)
        return value

    # If there is three of a kind, assign 21 to value and return value
    elif three_of_a_kind(specific_hand):
        value = int(21)
        return value

    # If there is a pair, assign 20 to value and return value
    elif pair(specific_hand):
        value = int(20)
        return value

    # Else no relationship, assign 0 to value and return value
    else:
        return value


'''
This function finds the statistics of the two players. It returns the computer stats and has no parameters.
'''
def print_game_statistics():

    # Call global variables
    global wins
    global total_rounds

    # Set the comp_stats variable equal to 0
    comp_stats = 0

    # If there were no rounds played
    if (total_rounds == 0):
        # Print that no games were played yet and return comp_stats
        print ("No games played yet!", '\n')
        return comp_stats
    
    # If the rounds and wins equal 1
    elif (total_rounds == 1 and wins == 1):
        # Set the comp_stats equal to 100 and user_stats equal to 0
        comp_stats = 100
        user_stats = 0

        # Print the stats for the computer and user and return comp_stats
        print("Computer: ", comp_stats)
        print("User: ", user_stats, '\n')
        return comp_stats
    
    # Else, there are stats to find
    else:
        # Evaluate wins divided by total rounds and set that equal to comp_stats
        new_comp_stats = wins/total_rounds
        # Multiply comp_stats by 100 to find the percentage
        new_comp_stats *= 100
        # Find the user percentage by subtracting comp_stats from 100
        user_stats = 100 - new_comp_stats

        # Print the computer and user stats and return comp_stats
        print("Computer: ", new_comp_stats)
        print("User: ", user_stats, '\n')
        return new_comp_stats



'''
This function finds the statistics of the two players. It returns the computer stats and has no parameters.
'''
def game_statistics():

    # Call global variables
    global wins
    global total_rounds

    # Set the comp_stats variable equal to 0
    comp_stats = 0

    # If there were no rounds played, return computer stats
    if (total_rounds == 0):
        return comp_stats
    
    # If the rounds and wins equal 1
    elif (total_rounds == 1 and wins == 1):
        # Set the comp_stats equal to 100
        comp_stats = 100
        # Return computer stats
        return comp_stats
    
    # Else, there are stats to find
    else:
        # Evaluate wins divided by total rounds and set that equal to comp_stats
        new_comp_stats = wins/total_rounds

        # Multiply comp_stats by 100 to find the percentage
        new_comp_stats *= 100

        # Return computer stats
        return new_comp_stats


'''
Determines which player has the highest card by taking in both the user and computer hands
and returns a boolean. The parameters are the user and computer hand.
'''
def better_high_card(user_hand, computer_hand):

    # Create a user and computer list with the hands
    user_card_list = [user_hand[0], user_hand[1], user_hand[2]]
    comp_card_list = [computer_hand[0], computer_hand[1], computer_hand[2]]

    # Create a list with the cost of each card
    user_card = [find_cost_card(user_card_list[0]), find_cost_card(user_card_list[1]), find_cost_card(user_card_list[2])]
    comp_card = [find_cost_card(comp_card_list[0]), find_cost_card(comp_card_list[1]), find_cost_card(comp_card_list[2])]

    # Sort both lists
    user_card.sort()
    comp_card.sort()

    # If the user's last card is equal to the computer's last card
    if (user_card[2] == comp_card[2]):

        # If the user's second card is equal to the computer's second card
        if (user_card[1] == comp_card[1]):

            # If the user's first card is equal to the computer's first card, return false
            if (user_card[0] == comp_card[0]):
                return False
            # If the user's first card is greater than the computer's first card, return true
            elif (user_card[0] > comp_card[0]):
                return True
            # Else, return false
            else:
                return False

        # If the user's second card is greater than the computer's second card, return true
        elif (user_card[1] > comp_card[1]):
            return True
        # Else, return false
        else:
            return False

    # If the user's last card is greater than the computer's last card, return true
    elif (user_card[2] > comp_card[2]):
        return True
    # Else, return False
    else:
        return False


'''
Determines if the computer's hand is better and returns a boolean. The parameters are both the hands.
'''
def check_computer_better_hand(user_hand, computer_hand):

    # Create a list with the computer and the user hand
    initial_comp_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]
    initial_user_hand_list = [user_hand[0], user_hand[1], user_hand[2]]

    # Find the cost of the relationship of the hand
    computer_relationship_cost = int(hand_relationship_cost(initial_comp_hand_list))
    user_relationship_cost = int(hand_relationship_cost(initial_user_hand_list))

    # Find the cost of each element in the computer list and then find the total sum of the hand
    computer_hand_list = find_cost(initial_comp_hand_list)
    computer_hand_cost = sum(computer_hand_list)

    # Find the cost of each element in the user list and then find the total sum of the hand
    user_hand_list = find_cost(initial_user_hand_list)
    user_hand_cost = sum(user_hand_list)

    # Find the total hand cost by adding the relationship cost to the hand cost
    computer_relationship = computer_relationship_cost + computer_hand_cost
    user_relationship = user_relationship_cost + user_hand_cost

    # If the computer relationship is lower than the user relationship, return false
    if computer_relationship < user_relationship:
        return False
    # Else, the computer relationship is higher than the user relationship
    else:
        # If the computer relationship is equal to the user relationship
        if (computer_relationship == user_relationship):
            # If the computer has the highest card, return true
            if (check_computer_highest_card(initial_user_hand_list, initial_comp_hand_list)):
                return True
            # Else, return false
            else:
                return False


'''
Checks to see if the computer has the second highest card. The parameters are user_hand and computer_hand. It returns a boolean.
'''
def check_computer_highest_two_card(new_user_hand, new_computer_hand):
    
    # Create lists with both hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Find the cost of each elements in the hand and put it into a list
    user_card = find_cost(user_hand)
    comp_card = find_cost(computer_hand)

    # Sort the list
    user_card.sort()
    comp_card.sort()

    # If the user's second card is higher than the computer's second card, return false
    if (user_card[1] > comp_card[1]):
        return False
    # Else, return true
    else:
        return True


'''
Determines the highest possible relationship a hand can have based off two cards and returns the new hands.
The parameters are the two hands.
'''
def highest_possible_relationship(new_computer_hand, new_user_hand):

    # Create lists with the hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # If there is a possible straight flush
    if check_possible_straight_flush(computer_hand):
        # Create the straight flush and return the new hands
        new_computer_hand, new_user_hand = list(create_straight_flush(computer_hand, user_hand))
        return new_computer_hand, new_user_hand

    # If there is a possible flush
    elif check_possible_flush(computer_hand):
        # Create the flush and return the new hands
        new_computer_hand, new_user_hand = list(create_flush(computer_hand, user_hand))
        return new_computer_hand, new_user_hand

    # If there is a possible straight
    elif check_possible_straight(computer_hand):
        # Create the straight and return the new hands
        new_computer_hand, new_user_hand = list(create_straight(computer_hand, user_hand))
        return new_computer_hand, new_user_hand

    # If there is a possible three of a kind
    elif check_possible_three_kind(computer_hand):
        # Create the three of a kind and return the new hands
        new_computer_hand, new_user_hand = list(create_three_of_a_kind(computer_hand, user_hand))
        return new_computer_hand, new_user_hand

    # Else, there is no relationship
    else:
        # Create a pair and return the new hands
        new_computer_hand, new_user_hand = list(create_pair(computer_hand, user_hand))
        return new_computer_hand, new_user_hand


'''
This function checks if the user wants to match or fold for the last betting round and returns the answer.
'''
def user_last_bet(user_tokens):

    # Prompt the user to input what they want to do, either match or fold
    bet = input("M for matching or f to fold: ")

    # Assign the user's answer to an int
    yes = int(1)
    no = int(0)

    # If the user wants to bet, return yes
    if (bet == 'm' or bet == 'M'):
        return yes
    # If the user wants to fold, return no
    elif (bet == "f" or bet == "F"):
        return no
    # Else, the user inputted an invalid answer
    else:
        # Print that their input is not a value answer and return this function for them to try again.
        print('Not a valid response. Please try again.')
        return user_last_bet(user_tokens)


'''
This function checks who has the winning hand and returns a boolean. The parameters are the two hands.
'''
def winning_hand(new_user_hand, new_computer_hand):

    # Create lists with the hands
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]

    # If the user and the computer have no hand relationship
    if (int(hand_relationship_cost(user_hand)) == 0 and int(hand_relationship_cost(computer_hand)) == 0):
        # If the user has a higher card, return true
        if (better_high_card(user_hand, computer_hand)):
            return True
        # Else, the computer has a higher card, return false
        else:
            return False

    # Else, there is a relationship in the hands
    else:
        # Find the relationship cost of both hands
        user_cost_relationship = int(hand_relationship_cost(user_hand))
        computer_hand_relationship = int(hand_relationship_cost(computer_hand))

        # If the cost of the user relationship is greater than the computer relationship, return true
        if (user_cost_relationship > computer_hand_relationship):
            return True

        # If the user relationship is less than the computer relationship, return false
        elif (user_cost_relationship < computer_hand_relationship):
            return False

        # Else, if the relationships are equal
        else:
            # Find the cost of each element in the user hand and put it in a list
            user_cost_card = find_cost(user_hand)
            # Find the sum of the list with the costs of the cards
            user_card_sum = sum(user_cost_card)

            # Find the cost of each element in the computer hand and put it in a list
            computer_cost_card = find_cost(computer_hand)
            # Find the sum of the list with the costs of the cards
            comp_card_sum = sum(computer_cost_card)

            # Add the card cost and the relationship cost of both hands into their own hand variables
            user_cost = user_cost_relationship + user_card_sum
            computer_cost = computer_hand_relationship + comp_card_sum

            # If the user cost is greater than the computer cost, return true
            if (user_cost > computer_cost):
                return True
            # Else, the computer cost is greater than the computer cost, return false
            else:
                return False


'''
find_cost with the parameter specific_hand assigns a cost to each card. This is done by creating lists,
using if elif else statements, using string methods, and appending values to the list. It then
returns the cost of the cards in a list.
'''
def find_cost(specific_hand):

    # Set the array_value to 0 to keep track of what card should be examined
    array_value = 0

    # Create a list with the hand cards
    hand_list = [specific_hand[0], specific_hand[1], specific_hand[2]]

    # Create an empty list to hold the cost of each card
    cost_card = []

    # Use while loop to iterate through each card and have it end when it reaches the end of the list, which is the length of 2
    while array_value <= 2:

        # If the card starts with 2, append the value of 2 to the cost of card list and increment the array_value
        if str(specific_hand[array_value]).startswith('2'):
            cost_card.append(2)
            array_value += 1

        # If the card starts with 3, append the value of 3 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('3'):
            cost_card.append(3)
            array_value += 1

        # If the card starts with 4, append the value of 4 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('4'):
            cost_card.append(4)
            array_value += 1

        # If the card starts with 5, append the value of 5 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('5'):
            cost_card.append(5)
            array_value += 1

        # If the card starts with 6, append the value of 6 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('6'):
            cost_card.append(6)
            array_value += 1

        # If the card starts with 7, append the value of 7 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('7'):
            cost_card.append(7)
            array_value += 1

        # If the card starts with 8, append the value of 8 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('8'):
            cost_card.append(8)
            array_value += 1

        # If the card starts with 9, append the value of 9 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('9'):
            cost_card.append(9)
            array_value += 1

        # If the card starts with 10, append the value of 10 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('10'):
            cost_card.append(10)
            array_value += 1

        # If the card starts with J, append the value of 11 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('J'):
            cost_card.append(11)
            array_value += 1

        # If the card starts with Q, append the value of 12 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('Q'):
            cost_card.append(12)
            array_value += 1

        # If the card starts with K, append the value of 13 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('K'):
            cost_card.append(13)
            array_value += 1

        # If the card starts with A, append the value of 14 to the cost of card list and increment the array_value
        elif str(specific_hand[array_value]).startswith('A'):
            cost_card.append(14)
            array_value += 1

        # Else statement fulfills the else requirement and breaks the cycle
        else:
            break

    # Return the list of the card costs
    return cost_card


'''
Takes in a hand to see if it is a straight flush and returns a boolean.
'''
def straight_flush(specific_hand):
    # Check if straight and flush are true and return true is they are both true
    if (straight(specific_hand) == True and flush(specific_hand) == True):
        return True
    # Else, return false
    else:
        return False


'''
This function checks to see if the hand given can be a straight flush. The parameter is the hand and it returns a boolean.
'''
def check_possible_straight_flush(computer_hand):

    # If hand can be a possible straight and a possible flush, return true
    if (check_possible_straight(computer_hand) and check_possible_flush(computer_hand)):
        return True

    # Else, return false
    else:
        return False


'''
Takes in both hands as parameters and creates a straight flush and returns the new hands.
'''
def create_straight_flush(new_computer_hand, new_user_hand):

    # Create the lists of the hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Create a list of the costs of the first two cards
    comp_hand = [int(find_cost_card(computer_hand[0])), int(find_cost_card(computer_hand[1]))]

    # Sort the list
    comp_hand.sort()

    # Find the low card by finding the value before the first card value
    low_card = int(comp_hand[0] - 1)
    # Find suit value and assign it to cost
    low_card_cost = int(assign_suit_value(computer_hand[0]))

    # Find the high card by finding the value after the second card value
    high_card = int(comp_hand[1] + 1)
    # Find suit value and assign it to cost
    high_card_cost = int(assign_suit_value(computer_hand[1]))

    # Create lists of the suit value in both hands
    user_hand_suit = [int(assign_suit_value(user_hand[0])), int(assign_suit_value(user_hand[1])), (int(assign_suit_value(user_hand[2])))]
    user_hand_card = [int(find_cost_card(user_hand[0])), int(find_cost_card(user_hand[0])), int(find_cost_card(user_hand[0]))]

    # Find the suit goal which would be either the first or second, here we choose the second
    suit_goal = int(assign_suit_value(computer_hand[1]))

    # If the high card is 15, meaning that the straight cannot work with the high card
    if (high_card == 15):
        # Set rounds equal to 0
        round = 0

        # While loop to iterate through each card
        while (round < 3):
            # If the low card cost equals the suit of the user hand card
            if (low_card_cost == int(assign_suit_value(user_hand_suit[round]))):
                # If the low card equals the cost of the user hand card
                if (low_card == find_cost_card(user_hand_card[round])):
                    # If it is the final round
                    if (round == 2):
                        # Save computer third card equal to save_card
                        save_card = computer_hand[2]
                        # Pop last card in computer hand
                        computer_hand.pop()
                        # Append last card in user hand to computer hand
                        computer_hand.append(user_hand[2])
                        # Pop last card in user hand
                        user_hand.pop()
                        # Append save card to user hand
                        user_hand.append(save_card)
                        # Return both hands
                        return computer_hand, user_hand
                # Else, increment round
                else:
                    round += 1
            # Else, increment round
            else:
                round += 1

    # If the low card is 2, meaning that the straight cannot work with the low card
    elif (low_card == 2):
        # Set round equal to 0
        round = 0

        # While loop to iterate through each card
        while (round < 3):
            # If the high card cost equals the suit of the user hand card
            if (high_card_cost == int(assign_suit_value(user_hand_suit[round]))):
                # If the high card equals the cost of the user hand card
                if (high_card == int(find_cost_card(user_hand_card[round]))):
                    # If it is the final round
                    if (round == 2):
                        # Save computer third card equal to save_card
                        save_card = computer_hand[2]
                        # Pop last card in computer hand
                        computer_hand.pop()
                        # Append last card in user hand to computer hand
                        computer_hand.append(user_hand[2])
                        # Pop last card in user hand
                        user_hand.pop()
                        # Append save card to user hand
                        user_hand.append(save_card)
                        # Return both hands                        
                        return computer_hand, user_hand
                # Else, increment round
                else:
                    round += 1
            # Else, increment round
            else:
                round += 1

    # Else the straight can happen in the middle
    else:
        # Set round equal to 0
        round = 0
        # While loop to iterate through each card
        while (round < 3):
            # If the user card suit equals the goal suit
            if (int(assign_suit_value(user_hand_suit[round])) == suit_goal):
                # If the user card cost equals the high card cost
                if (int(find_cost_card(user_hand_card[round])) == high_card):
                    # If it is the last round
                    if (round == 2):
                        # Save computer third card equal to save_card
                        save_card = computer_hand[2]
                        # Pop last card in computer hand
                        computer_hand.pop()
                        # Append last card in user hand to computer hand
                        computer_hand.append(user_hand[2])
                        # Pop last card in user hand
                        user_hand.pop()
                        # Append save card to user hand
                        user_hand.append(save_card)
                        # Return both hands
                        return computer_hand, user_hand 
                # Else, increment round
                else:
                    round += 1

            # If it is the last round
            elif (round == 2):
                # Find string of the cost and set it equal to start
                start = str(create_card_cost(high_card))
                # Find string of the suit and then set them all equal to create a new card
                card = start + " of " + str(find_suit_from_value(high_card_cost))
                # Pop last card from computer hand
                computer_hand.pop()
                # Append string to
                computer_hand.append(card)
                # Return the hands
                return computer_hand, user_hand

            # Else, increment round
            else:
                round += 1

        # Set round equal to 0
        round = 0

        # While loop to iterate through each card
        while (round < 3):
            # If the user card suit equals the goal suit
            if (int(assign_suit_value(user_hand_suit[round])) == suit_goal):
                # If the user card cost equalts the low card cost
                if (int(find_cost_card(user_hand_card[round])) == low_card):
                    # If it is the last round
                    if (round == 2):
                        # Save computer third card equal to save_card
                        save_card = computer_hand[2]
                        # Pop last card in computer hand
                        computer_hand.pop()
                        # Append last card in user hand to computer hand
                        computer_hand.append(user_hand[2])
                        # Pop last card in user hand
                        user_hand.pop()
                        # Append save card to user hand
                        user_hand.append(save_card)
                        # Return both hands
                        return computer_hand, user_hand

                # Else, increment round
                else:
                    round += 1

            # If it is the last round
            elif (round == 2):
                # Find string of the cost and set it equal to start
                start = str(create_card_cost(low_card))
                # Find string of the suit and then set them all equal to create a new card
                card = start + " of " + str(find_suit_from_value(low_card_cost))
                # Pop last card from computer hand
                computer_hand.pop()
                # Append string to end of computer hand
                computer_hand.append(card)
                # Return the hands
                return computer_hand, user_hand

            # Else, increment round
            else:
                round += 1

        # Return both hands
        return computer_hand, user_hand


'''
Takes in a hand to see if it is a straight and returns a boolean.
'''
def straight(specific_hand):

    # Put hand into a list
    hand_list = [specific_hand[0], specific_hand[1], specific_hand[2]]

    # Find the cost of each card and put it into a list
    sort_hand_values = list(find_cost(hand_list))

    # Sort the list
    sort_hand_values.sort()
    
    # If the costs of the cards are in one above each other, return true
    if (sort_hand_values == [find_cost_card(specific_hand[0]), find_cost_card(specific_hand[0])+1, find_cost_card(specific_hand[0])+2]):
        return True
    # Else, return false
    else:
        return False


'''
This function checks to see if the hand given can be a straight. The parameter is the hand and it returns a boolean.
'''
def check_possible_straight(computer_hand):

    # Create a list of the hand
    computer_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]

    # Find the costs of the first two cards and put them into a list
    sorted_user_list = [int(find_cost_card(computer_hand_list[0])), int(find_cost_card(computer_hand_list[1]))]
    
    # Sort the list
    sorted_user_list.sort()

    # Find the first card cost in the sorted list and assign it to first_card
    first_card = sorted_user_list[0]

    # Add one to the first card
    first_card += 1

    # Find the second card cost in the sorted list and assign it to second_card
    second_card = sorted_user_list[1]
    
    # If the first card equals the second card, the second is one value above the first, which is the goal of the straight, so return true
    if (first_card == second_card):
        return True
    # Else, there is no possible straight, return false
    else:
        return False


'''
Takes in both hands as parameters and creates a straight and returns the new hands.
'''
def create_straight(new_computer_hand, new_user_hand):

    # Create lists of possible suits to keep track of what suit is available
    possible_suits = [15, 16, 17, 18]
    possible_suits_high = [15, 16, 17, 18]
    possible_suits_low = [15, 16, 17, 18]

    # Create lists with the hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Find the cost of the first two cards in the computer hand
    comp_hand = [int(find_cost_card(computer_hand[0])), int(find_cost_card(computer_hand[1]))]
    
    # Sort the list
    comp_hand.sort()

    # Find the cost of the low card by subtracting one from the first card to find the card to make a straight
    low_card_cost = int(find_cost_card(comp_hand[0]) - 1)
    # Find the cost of the high card by adding one to the second card to find the card to make a straight
    high_card_cost = int(find_cost_card(comp_hand[1]) + 1)

    # If the cost of the high card is 15, the only card that can make it a straight is a Jack
    if (high_card_cost == 15):
        # Assign round equal to 0
        round = 0

        # While loop to iterate through each card
        while (round <= 2):
            # If the cost of the card is equal to the low card cost
            if (int(find_cost_card(user_hand[round])) == low_card_cost):
                # Remove it from the list of possible suits
                possible_suits.remove(int(assign_suit_value(user_hand[round])))
                # Increment round
                round +=1
            # Else the cost is not the wanted cost
            else:
                # Increment round
                round += 1
        
        # Find the available suit from the possible suit list by popping the last value
        new_suit = str(find_suit_from_value(possible_suits.pop()))
        # Assign the value of the card to start
        start = str(create_card_cost(high_card_cost))
        # Create a string of the card
        new_card = start + " of " + new_suit
        # Pop the last card in the computer hand
        computer_hand.pop()
        # Append the new card to the computer hand
        computer_hand.append(new_card)
        # Return the new hands
        return computer_hand, user_hand

    # If the cost of the low card is 1, the only card that can make it a straight is a 4
    elif (low_card_cost == 1):
        # Assign round to 0
        round = 0 

        # While loop to iterate through the cards
        while (round <= 2):
            # If the cost of the card is equal to the high card
            if (int(find_cost_card(user_hand[round])) == high_card_cost): 
                # Remove the suit of that card from the list of suits
                possible_suits.remove(int(assign_suit_value(user_hand[round])))
                # Increment round
                round +=1
            # Else the cost is not the high card cost
            else:
                # Increment round
                round += 1
        
        # Find the available suit from the possible suit list by popping the last value
        new_suit = str(find_suit_from_value(possible_suits.pop()))
        # Assign the value of the card to start        
        start = str(create_card_cost(low_card_cost))
        # Create a string of the card        
        new_card = start + " of " + new_suit
        # Pop the last card in the computer hand
        computer_hand.pop()
        # Append the new card to the computer hand        
        computer_hand.append(new_card)
        # Return the new hands        
        return computer_hand, user_hand
    
    # If the suit can happen anywhere in the middle of the hand
    else:
        # Assign round to 0
        round = 0 

        # While loop to iterate through the cards
        while (round <=2):
            # If the cost of the card is equal to the high card cost
            if (int(find_cost_card(user_hand[round])) == high_card_cost):
                # Remove the suit from the possible high card suit list
                possible_suits_high.remove(int(assign_suit_value(user_hand[round])))
                # Increment round
                round +=1
            # If the cost of the low card is equal to the low card cost
            if (int(find_cost_card(user_hand[round])) == low_card_cost):
                # Remove the suit from the possible low card suit list
                possible_suits_low.remove(int(assign_suit_value(user_hand[round])))
                # Increment round
                round +=1
        
        # If the length of the possible high suit list is not empty
        if len(possible_suits_high) != 0:
            # Find the available suit from the possible high suit list by popping the last value            
            new_suit = str(find_suit_from_value(possible_suits_high.pop()))
            # Assign the value of the card to start
            start = str(create_card_cost(high_card_cost))
            # Create a string of the card
            new_card = start + " of " + new_suit
            # Pop the last card in the computer hand
            computer_hand.pop()
            # Append the new card to the computer hand
            computer_hand.append(new_card)
            # Return the new hands
            return computer_hand, user_hand

        # If the length of the possible low suit list is not empty
        elif len(possible_suits_low) != 0 :
            # Find the available suit from the possible low suit list by popping the last value
            new_suit = str(find_suit_from_value(possible_suits_low.pop()))
            # Assign the value of the card to start
            start = str(create_card_cost(low_card_cost))
            # Create a string of the card
            new_card = start + " of " + new_suit
            # Pop the last card in the computer hand
            computer_hand.pop()
            # Append the new card to the computer hand
            computer_hand.append(new_card)
            # Return the new hands
            return computer_hand, user_hand
        
        # Else, the lists are empty, return both hands
        else: 
            return computer_hand, user_hand 


'''
Takes in a hand to see if it is a flush and returns a boolean.
'''
def flush(specific_hand):

    # Create a list from the hand
    hand_list = [specific_hand[0], specific_hand[1], specific_hand[2]]

    # Assign the suit value to each card in the list
    first_card = int(assign_suit_value(hand_list[0]))
    second_card = int(assign_suit_value(specific_hand[1]))
    third_card = int(assign_suit_value(specific_hand[2]))

    # If all cards have the same suit value, they are a flush, so return true
    if (first_card == second_card and first_card == third_card and second_card == third_card):
        return True
    # Else, return false
    else:
        return False


'''
This function checks to see if the hand given can be a flush. The parameter is the hand and it returns a boolean.
'''
def check_possible_flush(computer_hand):

    # Create a list with the computer hand
    computer_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]

    # Assign suit values of the first and second card to the separate variables
    first_suit = assign_suit_value(computer_hand_list[0])
    second_suit = assign_suit_value(computer_hand_list[1])

    # If the suits are the same, meaning a possible flush, return true
    if first_suit == second_suit:
        return True
    # Else, return false
    else:
        return False


'''
Takes in both hands as parameters and creates a flush and returns the new hands.
'''
def create_flush(computer_hand, user_hand):

    # Create potential value list to keep track of what costs are available
    potential_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # Create the lists using the hands
    computer_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]
    user_hand_list = [user_hand[0], user_hand[1], user_hand[2]]

    # Assign suit value to needed_suit
    needed_suit = int(assign_suit_value(computer_hand_list[0]))

    # Assign cost to first and second card
    cost_first = int(find_cost_card(computer_hand_list[0]))
    cost_second = int(find_cost_card(computer_hand_list[1]))

    # Remove cost from potential value list
    potential_values.remove(cost_first)
    potential_values.remove(cost_second)

    # Set round equal to 0
    round = 0

    # While loop to iterate through the hand
    while round <= 2:
        # Assign the suit value from the user hand to wanted_suit
        wanted_suit = int(assign_suit_value(user_hand_list[round]))

        # If the two suits are equal
        if (needed_suit == wanted_suit):
            # Find the cost of the user card
            current_cost = int(find_cost_card(user_hand_list[round]))
            # Remove the cost from the potential values list
            potential_values.remove(current_cost)
            # Increment round
            round += 1

        # Else, increment round
        else: 
            round += 1

    # Assign the cost of the user's highest card cost
    last_user_card = find_cost_card(user_hand_list[2])
    # Take the highest value from the highest potential list
    highest_potential = potential_values.pop()

    # If the suit value of the user's highest card equals the needed_suit
    if (int(assign_suit_value(user_hand_list[2])) == needed_suit):
        # If the last card cost is greater than the highest_potential
        if (last_user_card > highest_potential): 
            # Save computer third card equal to save_card
            save_card = computer_hand[2]
            # Pop last card in computer hand
            computer_hand_list.pop()
            # Append last card in user hand to computer hand
            computer_hand_list.append(user_hand[2])
            # Pop last card in user hand
            user_hand_list.pop()
            # Append save_card to user hand
            user_hand_list.append(save_card)
            # Return both hands
            return computer_hand_list, user_hand_list

        # Else the suit is available in the list
        else:
            # Find the suit from the needed_suit value
            suit_needed_string = str(find_suit_from_value(needed_suit))
            # Find the cost of the card from the highest potential list
            start = str(create_card_cost(highest_potential))
            # Create a string of the cost and suit
            final_card = start + " of " + suit_needed_string
            # Pop last card from computer hand list
            computer_hand_list.pop()
            # Append string to computer list
            computer_hand_list.append(final_card)
            # Return both hands
            return computer_hand_list, user_hand_list

    # Else the suit is available in the list
    else:
        # Find the suit from the needed_suit value
        suit_needed_string = str(find_suit_from_value(needed_suit))
        # Find the cost of the card from the highest potential list
        start = str(create_card_cost(highest_potential))
        # Create a string of the cost and suit
        final_card = start + " of " + suit_needed_string
        # Pop last card from computer hand list
        computer_hand_list.pop()
        # Append string to list
        computer_hand_list.append(final_card)
        # Return both hands
        return computer_hand_list, user_hand_list


'''
Takes in a hand to see if it is a three of a kind and returns a boolean.
'''
def three_of_a_kind(specific_hand):

    # Create a list with the hand
    specific_hand_list = [specific_hand[0], specific_hand[1], specific_hand[2]]

    # Find the cost of each card in the list and then save it as a int with another variable
    first_card = find_cost_card(specific_hand_list[0])
    first_card_value = int(first_card)
    second_card = find_cost_card(specific_hand_list[1])
    second_card_value = int(second_card)
    third_card = find_cost_card(specific_hand_list[2])
    third_card_value = int(third_card)

    # If all card costs are the same, there is three of a kind, so return true
    if first_card_value == second_card_value == third_card_value:
        return True
    # Else, return false
    else:
        return False


'''
This function checks to see if the hand given can be a three of a kind. The parameter is the hand and it returns a boolean.
'''
def check_possible_three_kind(computer_hand):

    # Create a list with the hand
    comp_card_list = [computer_hand[0], computer_hand[1], computer_hand[2]]

    # If the cost of the first card equals the cost of the second card, there is a possible three of a kind, so return true
    if (int(find_cost_card(comp_card_list[0])) == (int(find_cost_card(comp_card_list[1])))):
        return True
    # Else, return false
    else:
        return False


'''
Takes in both hands as parameters and creates a three of a kind and returns the new hands.
'''
def create_three_of_a_kind(new_computer_hand, new_user_hand):

    # Create a list with the computer hand
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Find the cost of the first computer card and set it equal to needed_value
    needed_value = int(find_cost_card(computer_hand[0]))

    # Create a list of the possible suits
    possible_suits = [15, 16, 17, 18]

    # Assign the suit value of the first two cards in the computer hand and save them to separate variables
    first_comp = int(assign_suit_value(computer_hand[0]))
    second_comp = int(assign_suit_value(computer_hand[1]))

    # Remove the suit from the possible suit list
    possible_suits.remove(first_comp)
    possible_suits.remove(second_comp)

    # Set round equal to 0
    round = 0

    # While loop to iterate through each card
    while (round <= 2):
        # If it is the final round, meaning the last card
        if (round == 2):
            # If the needed value cost equals the user's third card
            if (needed_value == int(find_cost_card(user_hand[round]))): 
                # Save computer third card equal to save_card
                save_card = computer_hand[2]
                # Pop last card in computer hand
                computer_hand.pop()
                # Append last card in user hand to computer hand
                computer_hand.append(user_hand[2])
                # Pop last card in user hand
                user_hand.pop()
                # Append save card to user hand
                user_hand.append(save_card)
                # Return both hands
                return computer_hand, user_hand
        # If it is not the final round and the needed value cost equals the user's card
        elif(needed_value == int(find_cost_card(user_hand[round]))):
            # Remove the suit value from the possible suit list
            possible_suits.remove(int(assign_suit_value(user_hand[round])))
            # Increment round
            round += 1
        # Else, there is no match to the needed value cost
        else:
            # Increment round
            round += 1

    # If the length of the possible suit list is not empty
    if len(possible_suits) != 0:
        # Save the suit value from the possible suit list to a variable
        swap_suit_num = possible_suits[0]
        # Find the cost of the variable to find the suit
        swap_suit = str(find_suit_from_value(swap_suit_num))
        # Find the cost of the needed value cost and save it as a string to a variable
        start = str(create_card_cost(needed_value))
        # Create a string of the wanted card
        card = start + " of " + swap_suit
        # Pop the last card from the computer hand
        computer_hand.pop()
        # Append the new card to the computer hand
        computer_hand.append(card)
        # Return both hands
        return computer_hand, user_hand

    # Else, if the list is empty, return both hands
    else:
        return computer_hand, user_hand 


'''
Takes in a hand to see if it is a pair and returns a boolean.
'''
def pair(new_specific_hand):
    
    # Create a list of the hand
    specific_hand = [new_specific_hand[0], new_specific_hand[1], new_specific_hand[2]]

    # Assign the cost of each card to a variable
    first_card = int(find_cost_card(specific_hand[0]))
    second_card = int(find_cost_card(specific_hand[1]))
    third_card = int(find_cost_card(specific_hand[2]))    

    # Checks to see if there is any match between two of the cards, if there is that is a pair, so return true
    if (first_card == second_card or first_card == third_card or second_card == third_card):
        return True
    # Else, there is no pair, return false
    else:
        return False


'''
Takes in both hands as parameters and creates a pair and returns the new hands.
'''
def create_pair(computer_hand, user_hand):

    # Create two lists of both hands
    computer_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]
    user_hand_list = [user_hand[0], user_hand[1], user_hand[2]]

    # Save the first and second card from the computer hand to two separate variables
    first_card = computer_hand_list[0]
    second_card = computer_hand_list[1]

    # Find the cost of the first and second card and set to two separate variables
    first_card_cost = int(find_cost_card(first_card))
    second_card_cost = int(find_cost_card(second_card))

    # Create two lists of possible suits for the low and high card
    possible_suits_high = [15, 16, 17, 18]
    possible_suits_low = [15, 16, 17, 18]

    # If the first card cost is greater than the second card cost
    if (first_card_cost > second_card_cost):
        # Assign the first card to the high_card variable
        high_card = first_card
        # Assign the second card to the low_card variable
        low_card = second_card
    # Else, the second card cost is greater than the first card cost
    else:
        # Assign the second card to the high_card variable
        high_card = second_card
        # Assign the first card to the low_card variable
        low_card = first_card

    # Set round equal to 0
    round = 0

    # While loop to iterate through the cards
    while (round < 3):
        # If the cost of the high card is equal to the user card
        if (int(find_cost_card(high_card)) == int(find_cost_card(user_hand_list[round]))):
            # Find the suit value of the user card and set it equal to the variable
            value = int(assign_suit_value(user_hand_list[round]))
            # Remove the suit value from the possible suit list
            possible_suits_high.remove(value)
            # Increment round
            round += 1
        # Else, the cost of the high card is not equal to the user card
        else:
            # Increment round
            round += 1

    # Set round equal to 0
    round = 0

    # While loop to iterate through the cards
    while (round < 3):
        # If the cost of the low card is equal to the user card
        if (int(find_cost_card(low_card)) == int(find_cost_card(user_hand_list[round]))):
            # Find the suit value of the user card and set it equal to the variable            
            value = int(assign_suit_value(user_hand_list[round]))
            # Remove the suit value from the possible suit list            
            possible_suits_low.remove(value)
            # Increment round
            round += 1
        # Else, the cost of the low card is not equal to the user card            
        else:
            # Increment round
            round += 1
    
    # Find the suit value from the high card
    high_suit = assign_suit_value(high_card)
    # Remove the suit value from the possible suit list
    possible_suits_high.remove(high_suit)

    # Find the suit value from the low card
    low_suit = assign_suit_value(low_card)
    # Remove the suit value from the possible suit list
    possible_suits_low.remove(low_suit)

    # If the length of the possible suit list is not empty
    if len(possible_suits_high) != 0:
        # Pop the value from the possible high suit list and set it equal to variable
        swap_suit_num = possible_suits_high.pop()
        # Find the suit value from the variable
        swap_suit = str(find_suit_from_value(swap_suit_num))
        # Find the cost of the high card and set it equal to variable
        value = find_cost_card(high_card)
        # Find the value of the card using the string and set it equal to the string
        start = str(create_card_cost(value))
        # Create the card
        card = start + " of " + swap_suit
        # Pop the card from the computer hand
        computer_hand_list.pop()
        # Append the new card
        computer_hand_list.append(card)
        # Return both hands
        return computer_hand_list, user_hand_list
    
    # Else, the length of the possible suit list is empty
    else:
        # Pop the value from the possible low suit list and set it equal to variable
        swap_suit_num = possible_suits_low.pop()
        # Find the suit value from the variable
        swap_suit = str(find_suit_from_value(swap_suit_num))
        # Find the cost of the low card and set it equal to the string
        value = str(find_cost_card(low_card))
        # Find the value of the card using the string and set it equal to variable
        start = create_card_cost(value)
        # Create the card
        card = start + " of " + swap_suit
        # Pop the card from the computer hand
        computer_hand_list.pop()
        # Append the new card
        computer_hand_list.append(card)
        # Return both hands
        return computer_hand_list, user_hand_list


'''
Checks to see if the computer has the highest high card. The parameters are both hands and returns a boolean.
'''
def check_computer_highest_card(user_hand, computer_hand):

    # Create lists of both hands
    user_hand_list = [user_hand[0], user_hand[1], user_hand[2]]
    comp_hand_list = [computer_hand[0], computer_hand[1], computer_hand[2]]

    # Find cost of each card in each hand and put the values in a list for each hand
    user_card = [find_cost_card(user_hand_list[0]), find_cost_card(user_hand_list[1]), find_cost_card(user_hand_list([2]))]
    comp_card = [find_cost_card(comp_hand_list[0]), find_cost_card(comp_hand_list[1]), find_cost_card(comp_hand_list[2])]
    
    # Sort both lists
    user_card.sort()
    comp_card.sort()

    # If the computer has the higher last card, return true
    if (find_cost_card(user_card[2]) < find_cost_card(comp_card[2])):
        return True
    # Else, the user has the higher last card, return false
    else:
        return False


'''
This function assigns an int value to the suit. It has the parameter of a card and returns the value
'''
def assign_suit_value(specific_suit):

    # Assign value to 0
    value = int(0)

    # Create the string of the card
    specific_card_string = str(specific_suit)
    # Split the string up by each individual word into a list
    specific_card_suit = specific_card_string.split()
    # Find the last value, last word, which would be the suit
    specific_suit_string = specific_card_suit[-1]

    # If it says "Clubs", assign the value of 15 and return the value
    if (specific_suit_string == "Clubs"):
        value = int(15)
        return value

    # If it says "Hearts", assign the value of 16 and return the value
    elif (specific_suit_string == "Hearts"):
        value = int(16)
        return value

    # If it says "Spades", assign the value of 17 and return the value
    elif (specific_suit_string == "Spades"):
        value = int(17)
        return value

    # Else, assign 18 to variable, which would be Diamonds, and return the value
    else:
        value = int(18)
        return value


'''
This function finds the string of the suit, has the parameter value, and returns the string of the suit.
'''
def find_suit_from_value(value):

    # Set suit equal to an empty string
    suit = ""

    # If value equals 15, assign "Clubs" to suit and return suit
    if (value == 15):
        suit = "Clubs"
        return suit

    # If value equals 16, assign "Hearts" to suit and return suit
    elif (value == 16):
        suit = "Hearts"
        return suit

    # If value equals 17, assign "Spades" to suit and return suit
    elif (value == 17):
        suit = "Spades"
        return suit

    # Else, assign "Diamonds" to suit and return suit
    else:
        suit = "Diamonds"
        return suit


'''
This function uses the cost of the card as the parameter and assigns it back to the string value and returns the string.
'''
def create_card_cost(value):

    # Assign string_value to an empty string
    string_value = str("")

    # If value equals 2, assign string of 2 and return the string
    if (value == 2):
        string_value = "2"
        return string_value

    # If value equals 3, assign string of 3 and return the string
    elif (value == 3):
        string_value = "3"
        return string_value

    # If value equals 4, assign string of 4 and return the string
    elif (value == 4):
        string_value = "4"
        return string_value

    # If value equals 5, assign string of 5 and return the string
    elif (value == 5):
        string_value = "5"
        return string_value

    # If value equals 6, assign string of 6 and return the string
    elif (value == 6):
        string_value = "6"
        return string_value

    # If value equals 7, assign string of 7 and return the string
    elif (value == 7):
        string_value = "7"
        return string_value

    # If value equals 8, assign string of 8 and return the string
    elif (value == 8):
        string_value = "8"
        return string_value

    # If value equals 9, assign string of 9 and return the string
    elif (value == 9):
        string_value = "9"
        return string_value

    # If value equals 10, assign string of 10 and return the string
    elif (value == 10):
        string_value = "10"
        return string_value

    # If value equals 11, assign string "Jack" and return the string
    elif (value == 11):
        string_value = "Jack"
        return string_value

    # If value equals 12, assign string "Queen" and return the string
    elif (value == 12):
        string_value = "Queen"
        return string_value

    # If value equals 13, assign string "King" and return the string
    elif (value == 13):
        string_value = "King"
        return string_value

    # Else, assign string "Ace" and return the string
    elif (value == 13):
        string_value = "Ace"
        return string_value

    # Else, assign string "Ace" and return the string
    else:
        return string_value


'''
This function shows all of the card to the user. The parameters are both hands and it prints the cards.
'''
def show_all_cards(new_computer_hand, new_user_hand):

    # Create lists for both hands
    computer_hand = [new_computer_hand[0], new_computer_hand[1], new_computer_hand[2]]
    user_hand = [new_user_hand[0], new_user_hand[1], new_user_hand[2]]

    # Print all three cards in each hand
    print ('\n', "Computer's hand: ", computer_hand[0], ' ', computer_hand[1], ' ', computer_hand[2])
    print ('\n', "User's hand: ", user_hand[0], ' ', user_hand[1], ' ', user_hand[2], "\n")


'''
This poker program is designed to let the user play against the computer. In the end the computer will cheat to win,
but it will not be obvious. Enjoy!
'''
def main():

    # Print rules
    rules()

    # Create tokens
    computer_tokens, user_tokens = create_tokens()

    # Call continue_game to prompt the user to let the program know when to end the game
    continue_or_end = int(-1)
    continue_or_end = int(continue_game(continue_or_end))

    # While loop if user wants to continue
    while (continue_or_end == 1):
        # Create both hands
        computer_hand, user_hand = create_decks()
        show_all_cards(computer_hand, user_hand)
        # Print tokens
        display_tokens(computer_tokens, user_tokens)

        # Call the betting function to start the game
        user_tokens, computer_tokens, computer_hand, user_hand = betting(user_tokens, computer_tokens, computer_hand, user_hand)

        # Show all cards to the user
        show_all_cards(computer_hand, user_hand)

        # Print the game statistics
        print_game_statistics()

        # Prompt the user to see if they want to continue playing
        continue_or_end = int(continue_game(continue_or_end))

    # If the user wants to end
    else:
        # Print end statement
        print ('We will miss you... Until next time!')

        # Print final game statistics
        print_game_statistics()


if __name__ == "__main__":
    main()