"""Vecna Adventure Mode - Play as the villain."""

import random
from dice import DiceRoller
from enemies import generate_random_encounter, create_enemy
from combat import Combat
from items import Shop

class VecnaAdventure:
    """Play as Vecna trying to conquer both worlds."""
    
    def __init__(self, player):
        self.player = player
        self.current_location = 'dark_citadel'
        self.missions_completed = 0
        self.power_level = 0  # Power level: 0-100
        self.gates_opened = 0
        self.hawkins_controlled = 0  # Percentage of Hawkins under control
        self.mind_flayers_recruited = 0
        self.final_conquest_available = False
        self.shop = Shop()
    
    def get_status(self):
        """Get current game status."""
        return {
            'missions_completed': self.missions_completed,
            'power_level': self.power_level,
            'gates_opened': self.gates_opened,
            'hawkins_controlled': self.hawkins_controlled,
            'mind_flayers': self.mind_flayers_recruited
        }
    
    def dark_citadel(self):
        """Vecna's base in the Upside Down."""
        while True:
            print("\n" + "="*50)
            print("VECNA'S DARK CITADEL")
            print("The Upside Down")
            print("="*50)
            print(f"\n{self.player}")
            print(f"\nPower Level: {self.power_level}/100")
            print(f"Gates Opened: {self.gates_opened}")
            print(f"Hawkins Controlled: {self.hawkins_controlled}%")
            print(f"Mind Flayers Recruited: {self.mind_flayers_recruited}")
            
            print("\nWhat dark deed will you perform?")
            print("1. Open a Gate to Hawkins")
            print("2. Send Creatures to Attack")
            print("3. Corrupt the Town")
            print("4. Recruit Mind Flayers")
            print("5. Train in Dark Arts")
            print("6. View Stats")
            print("7. Attempt Final Conquest (requires 70% control)")
            print("8. Save and Quit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                return 'open_gate'
            elif choice == '2':
                return 'attack_hawkins'
            elif choice == '3':
                return 'corrupt_town'
            elif choice == '4':
                return 'recruit_flayers'
            elif choice == '5':
                return 'train'
            elif choice == '6':
                print(f"\n{self.player}")
            elif choice == '7':
                if self.hawkins_controlled >= 70:
                    return 'final_conquest'
                else:
                    print(f"\nYou need more control! Current: {self.hawkins_controlled}%/70%")
            elif choice == '8':
                return 'quit'
            else:
                print("Invalid choice.")
    
    def open_gate(self):
        """Open a gate between worlds."""
        print("\n" + "="*50)
        print("OPENING A GATE")
        print("="*50)
        print("\nYou focus your dark energy on tearing the fabric between worlds...")
        
        input("\nPress Enter to channel your power...")
        
        # Need to fight off resistance
        defenders = []
        if self.gates_opened > 2:
            # Stronger resistance
            defenders = generate_random_encounter(self.player.level + 1, self.player.get_gear_level())
            print("\nHawkins fighters try to stop you!")
        else:
            defenders = generate_random_encounter(max(1, self.player.level - 1), 0)
            print("\nSome townspeople try to interfere!")
        
        for enemy in defenders:
            print(f"  - {enemy}")
        print()
        
        input("Press Enter to begin combat...")
        
        combat = Combat(self.player, defenders)
        result = combat.run_combat()
        
        if result == 'victory':
            self.gates_opened += 1
            self.power_level += 15
            self.hawkins_controlled += 10
            print("\n✓ Gate opened successfully!")
            print(f"Power gained: +15 (Total: {self.power_level})")
            print(f"Control of Hawkins: +10% (Total: {self.hawkins_controlled}%)")
            self.missions_completed += 1
        elif result == 'fled':
            print("\nYou retreated before opening the gate.")
        
        input("\nPress Enter to return to the citadel...")
        return 'dark_citadel'
    
    def attack_hawkins(self):
        """Send creatures to attack Hawkins."""
        print("\n" + "="*50)
        print("ATTACK HAWKINS")
        print("="*50)
        
        if self.gates_opened < 1:
            print("\nYou need at least 1 gate open to send creatures!")
            input("\nPress Enter to continue...")
            return 'dark_citadel'
        
        print("\nYou send your creatures through the gates...")
        print("Leading them personally, you terrorize the town!")
        
        input("\nPress Enter to lead the attack...")
        
        # Multiple waves of combat
        for wave in range(2):
            print(f"\n--- Wave {wave + 1} ---")
            enemies = generate_random_encounter(self.player.level, self.player.get_gear_level())
            
            # These are actually defenders
            print("\nHawkins defenders appear!")
            for enemy in enemies:
                print(f"  - {enemy}")
            print()
            
            input("Press Enter to begin combat...")
            
            combat = Combat(self.player, enemies)
            result = combat.run_combat()
            
            if result != 'victory':
                print("\nThe attack failed!")
                input("\nPress Enter to return to the citadel...")
                return 'dark_citadel'
        
        # Success
        self.power_level += 20
        self.hawkins_controlled += 15
        self.player.gold += 200
        print("\n✓ Attack successful! Hawkins is terrorized!")
        print(f"Power gained: +20 (Total: {self.power_level})")
        print(f"Control increased: +15% (Total: {self.hawkins_controlled}%)")
        print(f"Loot gained: +200 gold")
        self.missions_completed += 1
        
        input("\nPress Enter to return to the citadel...")
        return 'dark_citadel'
    
    def corrupt_town(self):
        """Spread corruption through Hawkins."""
        print("\n" + "="*50)
        print("CORRUPT THE TOWN")
        print("="*50)
        print("\nYou use your psychic powers to corrupt the minds of Hawkins...")
        
        cost = 50
        if self.player.gold < cost:
            print(f"\nYou need {cost} gold to perform this ritual!")
            input("\nPress Enter to continue...")
            return 'dark_citadel'
        
        self.player.gold -= cost
        
        input("\nPress Enter to perform the ritual...")
        
        success_roll = random.randint(1, 100)
        intelligence_bonus = self.player.get_modifier('intelligence') * 5
        
        if success_roll + intelligence_bonus > 40:
            corruption = random.randint(10, 20)
            self.hawkins_controlled += corruption
            self.power_level += 10
            print(f"\n✓ Success! You corrupted {corruption}% of the town!")
            print(f"Control: {self.hawkins_controlled}%")
            print(f"Power gained: +10 (Total: {self.power_level})")
            self.missions_completed += 1
        else:
            print("\n✗ The ritual failed! Your gold is wasted.")
        
        input("\nPress Enter to return to the citadel...")
        return 'dark_citadel'
    
    def recruit_flayers(self):
        """Recruit mind flayers to your cause."""
        print("\n" + "="*50)
        print("RECRUIT MIND FLAYERS")
        print("="*50)
        print("\nYou venture into the depths to recruit more mind flayers...")
        
        input("\nPress Enter to seek them out...")
        
        # Challenge to prove yourself
        flayer = create_enemy('mindflayer', self.player.level)
        print(f"\nA {flayer.name} challenges you!")
        print("You must prove your dominance!")
        print(f"{flayer}")
        print()
        
        input("Press Enter to begin combat...")
        
        combat = Combat(self.player, [flayer])
        result = combat.run_combat()
        
        if result == 'victory':
            recruited = random.randint(1, 3)
            self.mind_flayers_recruited += recruited
            self.power_level += 12
            print(f"\n✓ You recruited {recruited} mind flayer(s)!")
            print(f"Total mind flayers: {self.mind_flayers_recruited}")
            print(f"Power gained: +12 (Total: {self.power_level})")
            self.missions_completed += 1
        elif result == 'fled':
            print("\nYou fled from the challenge.")
        
        input("\nPress Enter to return to the citadel...")
        return 'dark_citadel'
    
    def train(self):
        """Train and increase power."""
        print("\n" + "="*50)
        print("TRAIN IN DARK ARTS")
        print("="*50)
        print("\nYou meditate on dark energies and hone your powers...")
        
        power_gain = random.randint(8, 15)
        self.power_level += power_gain
        
        # Heal
        healing = random.randint(15, 30)
        self.player.heal(healing)
        
        print(f"\nPower gained: +{power_gain} (Total: {self.power_level})")
        print(f"HP restored: +{healing}")
        
        # Small chance to gain gold
        if random.randint(1, 100) <= 25:
            gold = random.randint(30, 80)
            self.player.gold += gold
            print(f"\nYou found dark treasures worth {gold} gold!")
        
        input("\nPress Enter to return to the citadel...")
        return 'dark_citadel'
    
    def final_conquest(self):
        """Attempt to fully conquer Hawkins and the real world."""
        print("\n" + "="*50)
        print("FINAL CONQUEST")
        print("="*50)
        print("\nYou have gained enough control to attempt total domination!")
        print("The heroes of Hawkins gather for one last stand...")
        print("You face Eleven, the only one powerful enough to stop you!")
        
        input("\nPress Enter to face your final challenge...")
        
        # Create Eleven as the final boss
        eleven_boss = create_enemy('shadow_monster', self.player.level + 2)
        eleven_boss.name = "Eleven - Psychic Hero"
        eleven_boss.max_hp = 120 + (self.player.level * 10)
        eleven_boss.current_hp = eleven_boss.max_hp
        eleven_boss.damage_dice = '2d8+4'
        
        print(f"\n*** FINAL BATTLE! ***")
        print(f"You face {eleven_boss.name}!")
        print(f"{eleven_boss}")
        print()
        
        input("Press Enter to begin combat...")
        
        combat = Combat(self.player, [eleven_boss])
        result = combat.run_combat()
        
        if result == 'victory':
            print("\n" + "="*50)
            print("DARK VICTORY!")
            print("="*50)
            print("\nEleven falls before your might!")
            print("The gate between worlds fully opens!")
            print("The Upside Down consumes Hawkins, then spreads...")
            print("\nYou have conquered both worlds as Vecna, the supreme power!")
            print(f"\nFinal Stats:")
            print(f"Level: {self.player.level}")
            print(f"Power: {self.power_level}")
            print(f"Control: {self.hawkins_controlled}%")
            print(f"Mind Flayers: {self.mind_flayers_recruited}")
            print(f"Gates: {self.gates_opened}")
            return 'game_won'
        elif result == 'fled':
            print("\nYou retreated from Eleven!")
            print("The conquest is delayed...")
            input("\nPress Enter to return to the citadel...")
            return 'dark_citadel'
        else:
            print("\n" + "="*50)
            print("DEFEAT")
            print("="*50)
            print("\nEleven has defeated you!")
            print("The gates close and the Upside Down recedes...")
            return 'game_over'
