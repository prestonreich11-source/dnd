"""Adventure and story content for the D&D-style game."""

import random
from dice import DiceRoller
from enemies import generate_random_encounter, get_boss_encounter, create_enemy
from combat import Combat
from items import Shop, display_inventory, CONSUMABLES

class Adventure:
    """Manage the game's adventure and story progression."""
    
    def __init__(self, player):
        self.player = player
        self.current_location = 'town'
        self.story_progress = 0
        self.encounters_completed = 0
        self.boss_defeated = False
        self.shop = Shop()
    
    def get_status(self):
        """Get current game status."""
        return {
            'encounters_completed': self.encounters_completed,
            'boss_defeated': self.boss_defeated,
            'location': self.current_location
        }
    
    def town(self):
        """Player is in town - safe zone with shop."""
        while True:
            print("\n" + "="*50)
            print("TOWN - Safe Haven")
            print("="*50)
            print(f"\n{self.player}")
            print("\nWhat would you like to do?")
            print("1. Visit the Shop")
            print("2. Rest at the Inn (Restore HP)")
            print("3. View Inventory")
            print("4. View Character Stats")
            print("5. Venture into the Wilderness")
            print("6. Attempt the Final Dungeon (Boss Fight)")
            print("7. Save and Quit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                self.visit_shop()
            elif choice == '2':
                self.rest_at_inn()
            elif choice == '3':
                display_inventory(self.player)
                self.manage_equipment()
            elif choice == '4':
                print(f"\n{self.player}")
            elif choice == '5':
                return 'wilderness'
            elif choice == '6':
                if self.encounters_completed >= 5:
                    return 'final_dungeon'
                else:
                    print("\nYou're not ready yet! Complete more adventures first.")
                    print(f"Encounters completed: {self.encounters_completed}/5")
            elif choice == '7':
                return 'quit'
            else:
                print("Invalid choice.")
    
    def visit_shop(self):
        """Visit the shop to buy/sell items."""
        while True:
            self.shop.display_items()
            print(f"\nYour gold: {self.player.gold}")
            print("\n1. Buy item")
            print("2. Sell item")
            print("3. Leave shop")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                item_name = input("Enter item name (or 'cancel'): ").strip()
                if item_name.lower() != 'cancel':
                    self.shop.buy_item(self.player, item_name)
            elif choice == '2':
                display_inventory(self.player)
                if self.player.inventory:
                    try:
                        item_num = int(input("Enter item number to sell (0 to cancel): ").strip())
                        if item_num > 0 and item_num <= len(self.player.inventory):
                            item = self.player.inventory[item_num - 1]
                            self.shop.sell_item(self.player, item)
                    except ValueError:
                        print("Invalid input.")
            elif choice == '3':
                break
            else:
                print("Invalid choice.")
    
    def rest_at_inn(self):
        """Rest at the inn to restore HP."""
        cost = 20
        if self.player.gold >= cost:
            self.player.gold -= cost
            self.player.current_hp = self.player.max_hp
            print(f"\nYou rest at the inn and restore all HP! (-{cost} gold)")
        else:
            print(f"\nYou don't have enough gold! (Need {cost} gold)")
    
    def manage_equipment(self):
        """Manage equipped items."""
        print("\n1. Equip weapon")
        print("2. Equip armor")
        print("3. Back")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            weapons = [item for item in self.player.inventory 
                      if isinstance(item, dict) and 'damage' in item]
            if weapons:
                print("\nWeapons:")
                for i, weapon in enumerate(weapons):
                    print(f"{i+1}. {weapon['name']} ({weapon['damage']} damage)")
                try:
                    weapon_num = int(input("Choose weapon to equip: ").strip())
                    if 1 <= weapon_num <= len(weapons):
                        self.player.equipped_weapon = weapons[weapon_num - 1]
                        print(f"Equipped {self.player.equipped_weapon['name']}!")
                except ValueError:
                    print("Invalid input.")
            else:
                print("No weapons in inventory.")
        
        elif choice == '2':
            armor = [item for item in self.player.inventory 
                    if isinstance(item, dict) and 'ac_bonus' in item]
            if armor:
                print("\nArmor:")
                for i, arm in enumerate(armor):
                    print(f"{i+1}. {arm['name']} (+{arm['ac_bonus']} AC)")
                try:
                    armor_num = int(input("Choose armor to equip: ").strip())
                    if 1 <= armor_num <= len(armor):
                        self.player.equipped_armor = armor[armor_num - 1]
                        # Update AC
                        base_ac = 10 + self.player.get_modifier('dexterity')
                        self.player.armor_class = base_ac + self.player.equipped_armor['ac_bonus']
                        print(f"Equipped {self.player.equipped_armor['name']}!")
                        print(f"New AC: {self.player.armor_class}")
                except ValueError:
                    print("Invalid input.")
            else:
                print("No armor in inventory.")
    
    def wilderness(self):
        """Explore the wilderness - random encounters."""
        print("\n" + "="*50)
        print("THE WILDERNESS")
        print("="*50)
        print("\nYou venture into the dangerous wilderness...")
        
        # Random event
        event = random.randint(1, 10)
        
        if event <= 6:
            # Combat encounter
            return self.combat_encounter()
        elif event <= 8:
            # Find treasure
            self.find_treasure()
            return 'town'
        else:
            # Safe travel
            print("\nYou travel safely through the wilderness.")
            print("Nothing eventful happens.")
            input("\nPress Enter to return to town...")
            return 'town'
    
    def combat_encounter(self):
        """Random combat encounter."""
        enemies = generate_random_encounter(self.player.level, self.player.get_gear_level())
        
        print("\n*** ENCOUNTER! ***")
        print("You are attacked by:")
        for enemy in enemies:
            print(f"  - {enemy}")
        print()
        
        input("Press Enter to begin combat...")
        
        combat = Combat(self.player, enemies)
        result = combat.run_combat()
        
        if result == 'victory':
            self.handle_victory(enemies)
            self.encounters_completed += 1
            input("\nPress Enter to return to town...")
            return 'town'
        elif result == 'fled':
            print("\nYou escaped safely!")
            input("\nPress Enter to return to town...")
            return 'town'
        else:  # defeat
            return 'game_over'
    
    def handle_victory(self, enemies):
        """Handle rewards after combat victory."""
        total_xp = 0
        total_gold = 0
        
        for enemy in enemies:
            total_xp += enemy.xp_value
            total_gold += enemy.gold_drop
        
        print(f"\n*** REWARDS ***")
        print(f"Experience: +{total_xp} XP")
        print(f"Gold: +{total_gold} gold")
        
        self.player.add_experience(total_xp)
        self.player.gold += total_gold
        
        # Check for level up
        xp_needed = self.player.level * 1000
        if self.player.experience >= xp_needed:
            print(f"\n*** LEVEL UP! ***")
            print(f"You are now level {self.player.level}!")
            print(f"HP increased to {self.player.max_hp}!")
        
        # Chance to find item
        if random.randint(1, 100) <= 30:
            item = CONSUMABLES['health_potion'].to_dict()
            self.player.add_item(item)
            print(f"\nYou found a {item['name']}!")
    
    def find_treasure(self):
        """Find random treasure."""
        print("\n*** TREASURE FOUND! ***")
        
        gold = random.randint(50, 200)
        self.player.gold += gold
        print(f"You found {gold} gold!")
        
        # Chance to find item
        if random.randint(1, 100) <= 50:
            items = [CONSUMABLES['health_potion'], CONSUMABLES['greater_health_potion']]
            item = random.choice(items).to_dict()
            self.player.add_item(item)
            print(f"You found a {item['name']}!")
        
        input("\nPress Enter to continue...")
    
    def final_dungeon(self):
        """Final boss fight."""
        print("\n" + "="*50)
        print("THE FINAL DUNGEON")
        print("="*50)
        print("\nYou enter the dark dungeon...")
        print("The air grows cold and heavy...")
        print("You sense a powerful presence ahead...")
        
        input("\nPress Enter to continue...")
        
        boss = get_boss_encounter('shadow_monster')
        
        print("\n*** BOSS FIGHT! ***")
        print(f"You face the {boss[0].name}!")
        print(f"{boss[0]}")
        print()
        
        input("Press Enter to begin combat...")
        
        combat = Combat(self.player, boss)
        result = combat.run_combat()
        
        if result == 'victory':
            self.boss_defeated = True
            print("\n" + "="*50)
            print("CONGRATULATIONS!")
            print("="*50)
            print("\nYou have defeated the boss and saved the realm!")
            print(f"Final level: {self.player.level}")
            print(f"Final gold: {self.player.gold}")
            print("\nThank you for playing!")
            return 'game_won'
        elif result == 'fled':
            print("\nYou fled from the boss fight!")
            input("\nPress Enter to return to town...")
            return 'town'
        else:
            return 'game_over'

class UpsideDownAdventure:
    """Upside Down adventure mode - Serve Vecna and rise to power."""
    
    def __init__(self, player):
        self.player = player
        self.current_location = 'upside_down'
        self.missions_completed = 0
        self.vecna_power = 0  # Power level: 0-100, reach 100 to surpass Vecna
        self.vecna_favor = 0  # Favor with Vecna: positive = loyal, negative = betrayal
        self.captured_people = 0
        self.hawkins_resources = 0
        self.boss_defeated = False
        self.shop = Shop()
    
    def get_status(self):
        """Get current game status."""
        return {
            'missions_completed': self.missions_completed,
            'vecna_power': self.vecna_power,
            'vecna_favor': self.vecna_favor,
            'captured_people': self.captured_people,
            'hawkins_resources': self.hawkins_resources
        }
    
    def upside_down_hub(self):
        """Vecna's realm - mission hub."""
        while True:
            print("\n" + "="*50)
            print("THE UPSIDE DOWN")
            print("Vecna's Dark Realm")
            print("="*50)
            print(f"\n{self.player}")
            print(f"\nVecna's Power: {self.vecna_power}/100")
            print(f"Vecna's Favor: {self.vecna_favor}")
            print(f"Missions Completed: {self.missions_completed}")
            print(f"People Captured: {self.captured_people}")
            print(f"Resources Gathered: {self.hawkins_resources}")
            
            print("\nWhat would you like to do?")
            print("1. Accept Mission from Vecna")
            print("2. Train and Gain Power")
            print("3. View Inventory")
            print("4. View Character Stats")
            print("5. Challenge Vecna (requires 80+ Power)")
            print("6. Save and Quit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == '1':
                return 'mission'
            elif choice == '2':
                return 'training'
            elif choice == '3':
                display_inventory(self.player)
            elif choice == '4':
                print(f"\n{self.player}")
            elif choice == '5':
                if self.vecna_power >= 80:
                    return 'challenge_vecna'
                else:
                    print(f"\nYou need more power! Current: {self.vecna_power}/80")
            elif choice == '6':
                return 'quit'
            else:
                print("Invalid choice.")
    
    def mission(self):
        """Accept a mission from Vecna."""
        missions = [
            {
                'name': 'Raid Hawkins Lab',
                'description': 'Infiltrate the lab and steal equipment for Vecna',
                'difficulty': 1,
                'rewards': {'power': 15, 'gold': 100, 'resources': 10}
            },
            {
                'name': 'Capture People from Town',
                'description': 'Kidnap townspeople to serve Vecna',
                'difficulty': 2,
                'rewards': {'power': 20, 'gold': 150, 'people': 3}
            },
            {
                'name': 'Destroy the Portal Hunters',
                'description': 'Eliminate those trying to close the gate',
                'difficulty': 3,
                'rewards': {'power': 30, 'gold': 200, 'favor': 10}
            },
            {
                'name': 'Spread the Upside Down',
                'description': 'Expand Vecna\'s influence into Hawkins',
                'difficulty': 2,
                'rewards': {'power': 25, 'gold': 120, 'resources': 15}
            },
            {
                'name': 'Corrupt a Local Leader',
                'description': 'Turn someone powerful to Vecna\'s side',
                'difficulty': 4,
                'rewards': {'power': 40, 'gold': 250, 'favor': 20}
            },
        ]
        
        print("\n" + "="*50)
        print("VECNA'S MISSIONS")
        print("="*50)
        
        for i, mission in enumerate(missions, 1):
            difficulty_stars = '★' * mission['difficulty']
            print(f"\n{i}. {mission['name']} ({difficulty_stars})")
            print(f"   {mission['description']}")
        
        print(f"\n{len(missions) + 1}. Back")
        
        try:
            choice = int(input("\nChoose mission: ").strip())
            if 1 <= choice <= len(missions):
                mission_data = missions[choice - 1]
                return self.execute_mission(mission_data)
            elif choice == len(missions) + 1:
                return 'upside_down'
        except ValueError:
            pass
        
        return 'upside_down'
    
    def execute_mission(self, mission):
        """Execute a mission."""
        print("\n" + "="*50)
        print(f"MISSION: {mission['name']}")
        print("="*50)
        print(f"\n{mission['description']}")
        
        # Random chance of success based on difficulty
        success_chance = max(30, 90 - (mission['difficulty'] * 15))
        roll = random.randint(1, 100)
        
        input("\nPress Enter to attempt the mission...")
        
        if roll <= success_chance:
            print(f"\n✓ SUCCESS!")
            self.missions_completed += 1
            
            # Award rewards
            self.vecna_power += mission['rewards'].get('power', 0)
            self.player.gold += mission['rewards'].get('gold', 0)
            self.captured_people += mission['rewards'].get('people', 0)
            self.hawkins_resources += mission['rewards'].get('resources', 0)
            self.vecna_favor += mission['rewards'].get('favor', 0)
            
            print(f"\nPower gained: +{mission['rewards'].get('power', 0)}")
            print(f"Gold gained: +{mission['rewards'].get('gold', 0)}")
            if mission['rewards'].get('people', 0):
                print(f"People captured: +{mission['rewards'].get('people', 0)}")
            if mission['rewards'].get('resources', 0):
                print(f"Resources gathered: +{mission['rewards'].get('resources', 0)}")
            if mission['rewards'].get('favor', 0):
                print(f"Vecna's favor: +{mission['rewards'].get('favor', 0)}")
        else:
            print(f"\n✗ FAILED!")
            print("The mission went awry. You barely escaped.")
            damage = random.randint(10, 30)
            self.player.take_damage(damage)
            print(f"You took {damage} damage!")
            self.vecna_favor -= 5
        
        input("\nPress Enter to return to the Upside Down...")
        return 'upside_down'
    
    def training(self):
        """Train to gain power."""
        print("\n" + "="*50)
        print("TRAINING IN THE UPSIDE DOWN")
        print("="*50)
        
        print("\nYou train in the dark energies of the Upside Down...")
        
        # Train and gain stats
        power_gain = random.randint(10, 25)
        self.vecna_power += power_gain
        
        # Heal while training
        healing = random.randint(20, 40)
        self.player.heal(healing)
        
        print(f"\nPower gained: +{power_gain}")
        print(f"HP restored: +{healing}")
        print(f"Current Power: {self.vecna_power}/100")
        
        # Chance to gain special item
        if random.randint(1, 100) <= 30:
            print("\nYou discovered a dark artifact!")
            self.player.gold += 50
        
        input("\nPress Enter to return to the Upside Down...")
        return 'upside_down'
    
    def challenge_vecna(self):
        """Challenge Vecna for control of the Upside Down."""
        print("\n" + "="*50)
        print("CHALLENGE TO VECNA")
        print("="*50)
        print("\nYou have grown powerful enough to challenge your master...")
        print("You stand before Vecna, mind flayer lord of the Upside Down...")
        
        input("\nPress Enter to begin the ultimate battle...")
        
        # Create Vecna as boss
        vecna_boss = create_enemy('vecna', self.player.level)
        
        # Adjust Vecna's stats based on player's power
        if self.vecna_power >= 100:
            print("\nYou are at equal power with Vecna!")
        else:
            print(f"\nVecna is still stronger! (Your power: {self.vecna_power}/100)")
            # Make Vecna stronger if player is weaker
            vecna_boss.max_hp += (100 - self.vecna_power)
            vecna_boss.current_hp = vecna_boss.max_hp
        
        print(f"\n*** FINAL BATTLE! ***")
        print(f"You face {vecna_boss.name}!")
        print(f"{vecna_boss}")
        
        combat = Combat(self.player, [vecna_boss])
        result = combat.run_combat()
        
        if result == 'victory':
            self.boss_defeated = True
            print("\n" + "="*50)
            print("VICTORY!")
            print("="*50)
            
            if self.vecna_favor > 0:
                print("\nVecna falls before your power!")
                print("You now rule the Upside Down with Vecna as your servant!")
                print("Together, you begin your conquest of both worlds...")
            else:
                print("\nVecna is defeated!")
                print("You take control of the Upside Down!")
                print("You now rule without him, your power absolute!")
            
            print(f"\nFinal level: {self.player.level}")
            print(f"Final gold: {self.player.gold}")
            print(f"Final Power: {self.vecna_power}")
            return 'game_won'
        elif result == 'fled':
            print("\nYou fled from Vecna!")
            print("Your challenge has failed... for now.")
            input("\nPress Enter to return to the Upside Down...")
            return 'upside_down'
        else:
            return 'game_over'