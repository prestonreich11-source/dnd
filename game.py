#!/usr/bin/env python3
"""
D&D-Style Text Adventure Game
A complete role-playing game with character creation, combat, and adventure.
"""

import sys
from character import Character, RACES, CLASSES
from dice import DiceRoller
from adventure import Adventure
from vecna_adventure import VecnaAdventure

def print_banner():
    """Print game banner."""
    print("\n" + "="*50)
    print("  DUNGEONS & ADVENTURES")
    print("  A D&D-Style Text Adventure Game")
    print("="*50 + "\n")

def character_creation():
    """Create a new character."""
    print("=== CHARACTER CREATION ===\n")
    
    # Get character name
    while True:
        name = input("Enter your character's name: ").strip()
        if name:
            break
        print("Name cannot be empty.")
    
    # Choose race
    print("\nAvailable Races:")
    for key, race in RACES.items():
        print(f"  {key.capitalize()}: {race.special_ability}")
    
    while True:
        race_choice = input("\nChoose your race: ").strip().lower()
        if race_choice in RACES:
            race = RACES[race_choice]
            break
        print("Invalid race. Try again.")
    
    # Choose class
    print("\nAvailable Classes:")
    for key, char_class in CLASSES.items():
        print(f"  {key.capitalize()}: Hit Die d{char_class.hit_die}, "
              f"Primary Stats: {', '.join(char_class.primary_stats)}")
    
    while True:
        class_choice = input("\nChoose your class: ").strip().lower()
        if class_choice in CLASSES:
            char_class = CLASSES[class_choice]
            break
        print("Invalid class. Try again.")
    
    # Roll ability scores
    print("\nRolling ability scores...")
    scores = DiceRoller.roll_ability_scores()
    
    print("\nYour rolled scores (before racial bonuses):")
    stat_names = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
    for stat, score in zip(stat_names, scores):
        print(f"  {stat}: {score}")
    
    # Create character
    character = Character(name, race, char_class)
    
    # Assign rolled scores
    character.strength = scores[0]
    character.dexterity = scores[1]
    character.constitution = scores[2]
    character.intelligence = scores[3]
    character.wisdom = scores[4]
    character.charisma = scores[5]
    
    # Apply racial bonuses
    for stat, bonus in race.stat_bonuses.items():
        current = getattr(character, stat)
        setattr(character, stat, current + bonus)
    
    # Recalculate HP and AC
    character.max_hp = character.calculate_max_hp()
    character.current_hp = character.max_hp
    character.armor_class = 10 + character.get_modifier('dexterity')
    
    # Equip starting weapon
    weapons = [item for item in character.inventory if isinstance(item, dict) and 'damage' in item]
    if weapons:
        character.equipped_weapon = weapons[0]
    
    print("\n" + "="*50)
    print("CHARACTER CREATED!")
    print("="*50)
    print(f"\n{character}\n")
    
    input("Press Enter to begin your adventure...")
    
    return character

def main_menu():
    """Display main menu."""
    print_banner()
    print("1. New Game")
    print("2. How to Play")
    print("3. Exit")
    
    while True:
        choice = input("\nChoice: ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Try again.")

def show_instructions():
    """Show game instructions."""
    print("\n" + "="*50)
    print("HOW TO PLAY")
    print("="*50)
    print("""
This is a turn-based D&D-style adventure game.

GOAL:
Complete 5 wilderness encounters, then defeat the final boss!

STATS:
- STR (Strength): Melee attack damage
- DEX (Dexterity): Initiative, AC, finesse weapons
- CON (Constitution): Hit points
- INT (Intelligence): Spell power (not yet implemented)
- WIS (Wisdom): Perception and will saves
- CHA (Charisma): Social interactions

COMBAT:
- Combat is turn-based with initiative order
- Roll d20 + attack bonus vs enemy AC to hit
- Natural 20 = Critical Hit (double damage)
- Natural 1 = Critical Miss
- You can attack, use items, or flee

TOWN:
- Visit the shop to buy/sell items
- Rest at the inn to restore HP
- Equip better weapons and armor
- Prepare for the next adventure

TIPS:
- Buy health potions before venturing out
- Better equipment improves your chances
- Level up by gaining experience from combat
- Save gold for powerful items
    """)
    input("\nPress Enter to return to menu...")

def game_loop():
    """Main game loop."""
    # Choose adventure type
    print("\n" + "="*50)
    print("CHOOSE YOUR PATH")
    print("="*50)
    print("\n1. Play as a Hero (Normal Adventure)")
    print("2. Play as Vecna (Villain Mode)")
    
    while True:
        adventure_choice = input("\nChoice: ").strip()
        if adventure_choice in ['1', '2']:
            break
        print("Invalid choice. Try again.")
    
    # Character creation
    player = character_creation()
    
    # Start appropriate adventure
    if adventure_choice == '1':
        adventure = Adventure(player)
        location = 'town'
        
        while True:
            if location == 'town':
                location = adventure.town()
            elif location == 'wilderness':
                location = adventure.wilderness()
            elif location == 'final_dungeon':
                location = adventure.final_dungeon()
            elif location == 'game_over':
                print("\n" + "="*50)
                print("GAME OVER")
                print("="*50)
                print("\nYou have been defeated...")
                print(f"Final level: {player.level}")
                print(f"Encounters completed: {adventure.encounters_completed}")
                break
            elif location == 'game_won':
                break
            elif location == 'quit':
                print("\nThanks for playing!")
                break
    else:  # Vecna adventure
        adventure = VecnaAdventure(player)
        location = 'dark_citadel'
        
        while True:
            if location == 'dark_citadel':
                location = adventure.dark_citadel()
            elif location == 'open_gate':
                location = adventure.open_gate()
            elif location == 'attack_hawkins':
                location = adventure.attack_hawkins()
            elif location == 'corrupt_town':
                location = adventure.corrupt_town()
            elif location == 'recruit_flayers':
                location = adventure.recruit_flayers()
            elif location == 'train':
                location = adventure.train()
            elif location == 'final_conquest':
                location = adventure.final_conquest()
            elif location == 'game_over':
                print("\n" + "="*50)
                print("GAME OVER")
                print("="*50)
                print("\nYou have been defeated...")
                print(f"Final level: {player.level}")
                print(f"Missions completed: {adventure.missions_completed}")
                break
            elif location == 'game_won':
                break
            elif location == 'quit':
                print("\nThanks for playing!")
                break

def main():
    """Main entry point."""
    try:
        while True:
            choice = main_menu()
            
            if choice == '1':
                game_loop()
                input("\nPress Enter to return to main menu...")
            elif choice == '2':
                show_instructions()
            elif choice == '3':
                print("\nGoodbye!")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        print("Please report this bug!")
        sys.exit(1)

if __name__ == '__main__':
    main()
