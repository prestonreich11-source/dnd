"""Character classes and races for the D&D-style game."""

class Race:
    """Base class for character races."""
    
    def __init__(self, name, stat_bonuses, special_ability):
        self.name = name
        self.stat_bonuses = stat_bonuses
        self.special_ability = special_ability

class CharacterClass:
    """Base class for character classes."""
    
    def __init__(self, name, hit_die, primary_stats, starting_equipment):
        self.name = name
        self.hit_die = hit_die
        self.primary_stats = primary_stats
        self.starting_equipment = starting_equipment

class Character:
    """Player character with stats, inventory, and abilities."""
    
    def __init__(self, name, race, char_class):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = 1
        self.experience = 0
        
        # Base stats - improved starting stats
        self.strength = 14
        self.dexterity = 14
        self.constitution = 14
        self.intelligence = 10
        self.wisdom = 10
        self.charisma = 10
        
        # Apply race bonuses
        for stat, bonus in race.stat_bonuses.items():
            setattr(self, stat, getattr(self, stat) + bonus)
        
        # Combat stats
        self.max_hp = self.calculate_max_hp()
        
        # Add race bonus HP if available
        if hasattr(race, 'bonus_hp'):
            self.max_hp += race.bonus_hp
        
        self.current_hp = self.max_hp
        self.armor_class = 10 + self.get_modifier('dexterity')
        
        # Inventory
        self.inventory = char_class.starting_equipment.copy()
        self.gold = 100
        self.equipped_weapon = None
        self.equipped_armor = None
        
    def calculate_max_hp(self):
        """Calculate maximum hit points."""
        con_modifier = self.get_modifier('constitution')
        base_hp = self.char_class.hit_die + con_modifier
        return max(1, base_hp)
    
    def get_modifier(self, stat_name):
        """Calculate ability modifier from stat."""
        stat_value = getattr(self, stat_name)
        return (stat_value - 10) // 2
    
    def take_damage(self, damage):
        """Apply damage to character."""
        actual_damage = max(0, damage)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
    
    def heal(self, amount):
        """Heal the character."""
        actual_healing = min(amount, max(0, self.max_hp - self.current_hp))
        self.current_hp = min(self.max_hp, self.current_hp + actual_healing)
        return actual_healing
    
    def is_alive(self):
        """Check if character is still alive."""
        return self.current_hp > 0
    
    def add_experience(self, xp):
        """Add experience and check for level up."""
        self.experience += xp
        xp_needed = self.level * 1000
        
        if self.experience >= xp_needed:
            self.level_up()
    
    def level_up(self):
        """Level up the character."""
        self.level += 1
        hp_increase = self.char_class.hit_die // 2 + self.get_modifier('constitution')
        hp_increase = max(1, hp_increase)
        self.max_hp += hp_increase
        self.current_hp = self.max_hp
        return hp_increase
    
    def add_item(self, item):
        """Add item to inventory."""
        self.inventory.append(item)
    
    def remove_item(self, item):
        """Remove item from inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
    
    def get_attack_bonus(self):
        """Calculate attack bonus."""
        if self.equipped_weapon and self.equipped_weapon.get('finesse', False):
            return max(self.get_modifier('strength'), self.get_modifier('dexterity'))
        return self.get_modifier('strength')
    
    def get_attack_damage(self):
        """Calculate attack damage."""
        if self.equipped_weapon:
            return self.equipped_weapon['damage']
        return '1d4'  # Unarmed strike
    
    def get_gear_level(self):
        """Calculate average gear level from equipped items."""
        total_level = 0
        num_items = 0
        
        if self.equipped_weapon:
            total_level += self.equipped_weapon.get('level', 1)
            num_items += 1
        
        if self.equipped_armor:
            total_level += self.equipped_armor.get('level', 1)
            num_items += 1
        
        # Return average gear level (0-5 scale)
        if num_items == 0:
            return 0
        return min(5, total_level // num_items)
    
    def __str__(self):
        return (f"{self.name} - Level {self.level} {self.race.name} {self.char_class.name}\n"
                f"HP: {self.current_hp}/{self.max_hp} | AC: {self.armor_class} | Gold: {self.gold}\n"
                f"STR: {self.strength} ({self.get_modifier('strength'):+d}) | "
                f"DEX: {self.dexterity} ({self.get_modifier('dexterity'):+d}) | "
                f"CON: {self.constitution} ({self.get_modifier('constitution'):+d})\n"
                f"INT: {self.intelligence} ({self.get_modifier('intelligence'):+d}) | "
                f"WIS: {self.wisdom} ({self.get_modifier('wisdom'):+d}) | "
                f"CHA: {self.charisma} ({self.get_modifier('charisma'):+d})")

# Define available races
# Special races have bonus HP based on show survival:
# - Vecna: 150 HP (nearly indestructible, survived multiple seasons)
# - Eleven: 80 HP (powerful psychic, survived entire series)
# - Dustin: 50 HP (survived entire series, clever survivor)
# - Demogorgon: 60 HP (killed but left lasting impact, season 1 monster)
class RaceWithHP(Race):
    """Race with bonus HP."""
    def __init__(self, name, stat_bonuses, special_ability, bonus_hp=0):
        super().__init__(name, stat_bonuses, special_ability)
        self.bonus_hp = bonus_hp

RACES = {
    'human': Race('Human', {'strength': 1, 'dexterity': 1, 'constitution': 1, 
                            'intelligence': 1, 'wisdom': 1, 'charisma': 1}, 
                  'Versatile: +1 to all stats'),
    'elf': Race('Elf', {'dexterity': 2, 'intelligence': 1}, 
                'Keen Senses: Advantage on perception checks'),
    'dwarf': Race('Dwarf', {'constitution': 2, 'strength': 1}, 
                  'Tough: Extra hit points'),
    'halfling': Race('Halfling', {'dexterity': 2, 'charisma': 1}, 
                     'Lucky: Can reroll 1s'),
    'vecna': RaceWithHP('Vecna', {'intelligence': 3, 'charisma': 2, 'constitution': 2},
                  'Mind Flayer Lord: Control minds and cast dark magic', 150),
    'eleven': RaceWithHP('Eleven', {'intelligence': 3, 'wisdom': 2, 'constitution': 1},
                   'Telekinesis: Move objects with your mind and close gates', 80),
    'dustin': RaceWithHP('Dustin', {'intelligence': 2, 'constitution': 2, 'wisdom': 1},
                   'Strategic Mind: Understand complex systems and survive', 50),
    'demogorgon': RaceWithHP('Demogorgon', {'strength': 3, 'constitution': 3, 'intelligence': -2},
                       'Creature of the Upside Down: Regenerate health in battle', 60),
}

# Define available classes
CLASSES = {
    'warrior': CharacterClass('Warrior', 10, ['strength', 'constitution'], 
                             [{'name': 'Longsword', 'damage': '1d8', 'finesse': False},
                              {'name': 'Shield', 'ac_bonus': 2},
                              {'name': 'Health Potion', 'healing': 20}]),
    'rogue': CharacterClass('Rogue', 8, ['dexterity', 'charisma'],
                           [{'name': 'Dagger', 'damage': '1d6', 'finesse': True},
                            {'name': 'Lockpicks'},
                            {'name': 'Health Potion', 'healing': 20}]),
    'wizard': CharacterClass('Wizard', 6, ['intelligence', 'wisdom'],
                            [{'name': 'Staff', 'damage': '1d6', 'finesse': False},
                             {'name': 'Spellbook'},
                             {'name': 'Health Potion', 'healing': 20}]),
    'cleric': CharacterClass('Cleric', 8, ['wisdom', 'constitution'],
                            [{'name': 'Mace', 'damage': '1d6', 'finesse': False},
                             {'name': 'Holy Symbol'},
                             {'name': 'Health Potion', 'healing': 20}]),
    'psychic': CharacterClass('Psychic', 7, ['intelligence', 'wisdom'],
                             [{'name': 'Telekinesis', 'damage': '2d6', 'type': 'psychic'},
                              {'name': 'Mind Flayer Sensory', 'type': 'ability'},
                              {'name': 'Restoration Serum', 'healing': 30}]),
    'scientist': CharacterClass('Scientist', 8, ['intelligence', 'charisma'],
                               [{'name': 'Walkie-Talkie', 'type': 'communication'},
                                {'name': 'Scientific Instruments', 'type': 'tool'},
                                {'name': 'Makeshift Bomb', 'damage': '2d4'},
                                {'name': 'Health Potion', 'healing': 20}]),
    'creature': CharacterClass('Creature', 12, ['strength', 'constitution'],
                              [{'name': 'Tentacle Strike', 'damage': '3d6', 'type': 'melee'},
                               {'name': 'Upside Down Armor', 'ac_bonus': 3},
                               {'name': 'Creature Essence', 'healing': 50, 'type': 'power'}]),
}

# Map special races to their required classes
RACE_CLASS_MAPPING = {
    'eleven': ['psychic'],
    'dustin': ['scientist'],
    'demogorgon': ['creature'],
}
