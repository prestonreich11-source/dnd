"""Combat system for the D&D-style game."""

from dice import DiceRoller
import time

class Combat:
    """Manage combat encounters between player and enemies."""
    
    def __init__(self, player, enemies):
        self.player = player
        self.enemies = enemies
        self.turn_order = []
        self.current_turn = 0
        self.combat_log = []
        
    def start_combat(self):
        """Initialize combat and determine turn order."""
        self.log(f"\n{'='*50}")
        self.log("COMBAT BEGINS!")
        self.log(f"{'='*50}\n")
        
        # Roll initiative
        combatants = [(self.player, DiceRoller.roll_d20() + self.player.get_modifier('dexterity'), 'player')]
        
        for i, enemy in enumerate(self.enemies):
            initiative = DiceRoller.roll_d20() + enemy.get_modifier('dexterity')
            combatants.append((enemy, initiative, f'enemy_{i}'))
        
        # Sort by initiative (highest first)
        combatants.sort(key=lambda x: x[1], reverse=True)
        self.turn_order = combatants
        
        # Display initiative order
        self.log("Initiative Order:")
        for combatant, initiative, _ in self.turn_order:
            name = combatant.name
            self.log(f"  {name}: {initiative}")
        self.log("")
        
    def run_combat(self):
        """Execute combat rounds until one side is defeated."""
        self.start_combat()
        
        round_num = 1
        
        while self.player.is_alive() and any(e.is_alive() for e in self.enemies):
            self.log(f"\n--- Round {round_num} ---")
            
            for combatant, _, combatant_type in self.turn_order:
                if not combatant.is_alive():
                    continue
                
                if not self.player.is_alive() or not any(e.is_alive() for e in self.enemies):
                    break
                
                if combatant == self.player:
                    action = self.player_turn()
                    if action == 'flee':
                        return 'fled'
                else:
                    self.enemy_turn(combatant)
                
                time.sleep(0.5)  # Pause for readability
            
            round_num += 1
        
        # Combat ended
        if self.player.is_alive():
            self.log("\n" + "="*50)
            self.log("VICTORY!")
            self.log("="*50 + "\n")
            return 'victory'
        else:
            self.log("\n" + "="*50)
            self.log("DEFEAT!")
            self.log("="*50 + "\n")
            return 'defeat'
    
    def player_turn(self):
        """Handle player's turn in combat."""
        self.log(f"\n{self.player.name}'s turn!")
        self.log(f"HP: {self.player.current_hp}/{self.player.max_hp}")
        
        while True:
            print("\nWhat do you want to do?")
            print("1. Attack")
            print("2. Use Item")
            print("3. Flee")
            
            choice = input("Choose an action: ").strip()
            
            if choice == '1':
                return self.player_attack()
            elif choice == '2':
                used = self.player_use_item()
                if used:
                    return 'item_used'
            elif choice == '3':
                if self.attempt_flee():
                    return 'flee'
            else:
                print("Invalid choice. Try again.")
    
    def player_attack(self):
        """Player attacks an enemy."""
        # Choose target
        alive_enemies = [e for e in self.enemies if e.is_alive()]
        
        if len(alive_enemies) == 1:
            target = alive_enemies[0]
        else:
            print("\nChoose a target:")
            for i, enemy in enumerate(alive_enemies):
                print(f"{i+1}. {enemy.name} (HP: {enemy.current_hp}/{enemy.max_hp})")
            
            while True:
                try:
                    choice = int(input("Target: ").strip())
                    if 1 <= choice <= len(alive_enemies):
                        target = alive_enemies[choice - 1]
                        break
                    else:
                        print("Invalid target.")
                except (ValueError, IndexError):
                    print("Invalid input.")
        
        # Roll attack
        attack_roll = DiceRoller.roll_d20()
        attack_bonus = self.player.get_attack_bonus()
        total_attack = attack_roll + attack_bonus
        
        self.log(f"{self.player.name} attacks {target.name}!")
        self.log(f"  Attack roll: {attack_roll} + {attack_bonus} = {total_attack} vs AC {target.armor_class}")
        
        # Check if hit
        if DiceRoller.is_critical_hit(attack_roll):
            # Critical hit - double damage dice
            damage_dice = self.player.get_attack_damage()
            damage = DiceRoller.roll_simple(damage_dice) + DiceRoller.roll_simple(damage_dice)
            damage += attack_bonus
            actual_damage = target.take_damage(damage)
            self.log(f"  CRITICAL HIT! {actual_damage} damage!")
        elif DiceRoller.is_critical_miss(attack_roll):
            self.log(f"  CRITICAL MISS! The attack goes wide!")
        elif total_attack >= target.armor_class:
            # Normal hit
            damage_dice = self.player.get_attack_damage()
            damage = DiceRoller.roll_simple(damage_dice) + attack_bonus
            actual_damage = target.take_damage(damage)
            self.log(f"  Hit! {actual_damage} damage!")
        else:
            self.log(f"  Miss!")
        
        if not target.is_alive():
            self.log(f"  {target.name} has been defeated!")
        
        return 'attacked'
    
    def player_use_item(self):
        """Player uses an item from inventory."""
        # Find usable items (potions, etc.)
        usable_items = [item for item in self.player.inventory 
                       if isinstance(item, dict) and 'healing' in item]
        
        if not usable_items:
            print("No usable items in inventory!")
            return False
        
        print("\nUsable Items:")
        for i, item in enumerate(usable_items):
            print(f"{i+1}. {item['name']} (Heals {item['healing']} HP)")
        print(f"{len(usable_items)+1}. Cancel")
        
        try:
            choice = int(input("Choose item: ").strip())
            if choice == len(usable_items) + 1:
                return False
            if 1 <= choice <= len(usable_items):
                item = usable_items[choice - 1]
                healing = self.player.heal(item['healing'])
                self.log(f"{self.player.name} uses {item['name']} and heals {healing} HP!")
                self.player.remove_item(item)
                return True
        except (ValueError, IndexError):
            print("Invalid choice.")
        
        return False
    
    def attempt_flee(self):
        """Attempt to flee from combat."""
        flee_roll = DiceRoller.roll_d20()
        if flee_roll >= 10:
            self.log(f"{self.player.name} successfully flees from combat!")
            return True
        else:
            self.log(f"{self.player.name} fails to escape!")
            return False
    
    def enemy_turn(self, enemy):
        """Handle enemy's turn in combat."""
        self.log(f"\n{enemy.name}'s turn!")
        
        # Simple AI - always attack player
        attack_roll = DiceRoller.roll_d20()
        attack_bonus = enemy.get_attack_bonus()
        total_attack = attack_roll + attack_bonus
        
        self.log(f"{enemy.name} attacks {self.player.name}!")
        self.log(f"  Attack roll: {attack_roll} + {attack_bonus} = {total_attack} vs AC {self.player.armor_class}")
        
        # Check if hit
        if DiceRoller.is_critical_hit(attack_roll):
            # Critical hit
            damage_dice = enemy.get_attack_damage()
            damage = DiceRoller.roll_simple(damage_dice) + DiceRoller.roll_simple(damage_dice)
            damage += attack_bonus
            actual_damage = self.player.take_damage(damage)
            self.log(f"  CRITICAL HIT! {actual_damage} damage!")
        elif DiceRoller.is_critical_miss(attack_roll):
            self.log(f"  CRITICAL MISS! The attack goes wide!")
        elif total_attack >= self.player.armor_class:
            # Normal hit
            damage_dice = enemy.get_attack_damage()
            damage = DiceRoller.roll_simple(damage_dice) + attack_bonus
            actual_damage = self.player.take_damage(damage)
            self.log(f"  Hit! {actual_damage} damage!")
        else:
            self.log(f"  Miss!")
        
        if not self.player.is_alive():
            self.log(f"  {self.player.name} has been defeated!")
    
    def log(self, message):
        """Add message to combat log and print it."""
        self.combat_log.append(message)
        print(message)
    
    def get_combat_log(self):
        """Return the full combat log."""
        return '\n'.join(self.combat_log)
