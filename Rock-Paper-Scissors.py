import random
import os

def clear_screen():
    """Clear the terminal screen for better UI"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_header():
    """Display the game header"""
    print("=" * 50)
    print("🎮  ROCK PAPER SCISSORS GAME  🎮")
    print("=" * 50)
    print()

def display_choices():
    """Display available choices"""
    print("Choose your weapon:")
    print("1. 🪨 Rock")
    print("2. 📄 Paper") 
    print("3. ✂️  Scissors")
    print("4. 📊 View Stats")
    print("5. 🔄 Reset Game")
    print("6. ❌ Quit")
    print("-" * 30)

def get_computer_choice():
    """Generate random computer choice"""
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def get_choice_emoji(choice):
    """Return emoji for the choice"""
    emojis = {
        'rock': '🪨',
        'paper': '📄',
        'scissors': '✂️'
    }
    return emojis.get(choice, '❓')

def determine_winner(player_choice, computer_choice):
    """Determine the winner of the round"""
    if player_choice == computer_choice:
        return 'tie'
    
    winning_combinations = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if winning_combinations[player_choice] == computer_choice:
        return 'win'
    else:
        return 'lose'

def display_round_result(player_choice, computer_choice, result):
    """Display the result of the current round"""
    print("\n" + "=" * 30)
    print("⚔️  BATTLE RESULT  ⚔️")
    print("=" * 30)
    
    # Show choices
    print(f"You chose:      {get_choice_emoji(player_choice)} {player_choice.capitalize()}")
    print(f"Computer chose: {get_choice_emoji(computer_choice)} {computer_choice.capitalize()}")
    print("-" * 30)
    
    # Show result
    if result == 'win':
        print("🎉 YOU WIN! 🎉")
        print("Great choice!")
    elif result == 'lose':
        print("💻 COMPUTER WINS! 💻") 
        print("Better luck next time!")
    else:
        print("🤝 IT'S A TIE! 🤝")
        print("Great minds think alike!")
    
    print("=" * 30)

def display_score(player_score, computer_score):
    """Display current scores"""
    total_games = player_score + computer_score
    print(f"\n📊 SCOREBOARD:")
    print(f"You: {player_score} | Computer: {computer_score}")
    
    if total_games > 0:
        win_rate = (player_score / total_games) * 100
        print(f"Your win rate: {win_rate:.1f}%")
    print()

def display_stats(player_score, computer_score, ties):
    """Display detailed game statistics"""
    clear_screen()
    display_header()
    
    total_games = player_score + computer_score + ties
    
    print("📊 DETAILED STATISTICS 📊")
    print("-" * 40)
    print(f"Total Games Played: {total_games}")
    print(f"Your Wins:          {player_score}")
    print(f"Computer Wins:      {computer_score}")
    print(f"Ties:               {ties}")
    
    if total_games > 0:
        win_rate = (player_score / total_games) * 100
        lose_rate = (computer_score / total_games) * 100
        tie_rate = (ties / total_games) * 100
        
        print(f"\nWin Rate:           {win_rate:.1f}%")
        print(f"Loss Rate:          {lose_rate:.1f}%")
        print(f"Tie Rate:           {tie_rate:.1f}%")
        
        if player_score > computer_score:
            print(f"\n🏆 You're ahead by {player_score - computer_score} wins!")
        elif computer_score > player_score:
            print(f"\n😅 Computer is ahead by {computer_score - player_score} wins!")
        else:
            print(f"\n⚖️  It's perfectly tied!")
    else:
        print("\nNo games played yet!")
    
    print("-" * 40)
    input("Press Enter to continue...")

def main():
    """Main game loop"""
    player_score = 0
    computer_score = 0
    ties = 0
    
    print("🎮 Welcome to Rock Paper Scissors!")
    print("Let's see if you can beat the computer!\n")
    input("Press Enter to start...")
    
    while True:
        clear_screen()
        display_header()
        display_score(player_score, computer_score)
        display_choices()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '6':
                clear_screen()
                display_header()
                print("Thanks for playing! 👋")
                display_score(player_score, computer_score)
                if ties > 0:
                    print(f"Ties: {ties}")
                print("See you next time!")
                break
            
            elif choice == '4':
                display_stats(player_score, computer_score, ties)
                continue
            
            elif choice == '5':
                player_score = 0
                computer_score = 0
                ties = 0
                clear_screen()
                print("🔄 Game reset! Starting fresh...")
                input("Press Enter to continue...")
                continue
            
            elif choice in ['1', '2', '3']:
                choice_map = {'1': 'rock', '2': 'paper', '3': 'scissors'}
                player_choice = choice_map[choice]
                computer_choice = get_computer_choice()
                
                result = determine_winner(player_choice, computer_choice)
                
                # Update scores
                if result == 'win':
                    player_score += 1
                elif result == 'lose':
                    computer_score += 1
                else:
                    ties += 1
                
                # Display result
                display_round_result(player_choice, computer_choice, result)
                
                input("\nPress Enter to continue...")
                
            else:
                print("❌ Invalid choice! Please enter 1-6.")
                input("Press Enter to try again...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for playing!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()