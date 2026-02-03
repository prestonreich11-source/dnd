"""Enemy and monster classes for the D&D-style game."""

import random
from dice import DiceRoller

class Enemy:
    """Base enemy class."""
    
    def __init__(self, name, level, base_stats):
        self.name = name
        self.level = level
        
        # Stats
        self.strength = base_stats.get('strength', 10)
        self.dexterity = base_stats.get('dexterity', 10)
        self.constitution = base_stats.get('constitution', 10)
        self.intelligence = base_stats.get('intelligence', 10)
        self.wisdom = base_stats.get('wisdom', 10)
        self.charisma = base_stats.get('charisma', 10)
        
        # Combat stats
        self.max_hp = base_stats.get('hp', 10)
        self.current_hp = self.max_hp
        self.armor_class = base_stats.get('ac', 10)
        self.damage_dice = base_stats.get('damage', '1d6')
        self.xp_value = base_stats.get('xp', level * 100)
        self.gold_drop = base_stats.get('gold', level * 10)
    
    def get_modifier(self, stat_name):
        """Calculate ability modifier from stat."""
        stat_value = getattr(self, stat_name)
        return (stat_value - 10) // 2
    
    def take_damage(self, damage):
        """Apply damage to enemy."""
        actual_damage = max(0, damage)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
    
    def is_alive(self):
        """Check if enemy is still alive."""
        return self.current_hp > 0
    
    def get_attack_bonus(self):
        """Calculate attack bonus."""
        return self.get_modifier('strength')
    
    def get_attack_damage(self):
        """Get attack damage dice."""
        return self.damage_dice
    
    def __str__(self):
        return f"{self.name} (Level {self.level}) - HP: {self.current_hp}/{self.max_hp}, AC: {self.armor_class}"

# Enemy templates
ENEMY_TEMPLATES = {
    'demobat': {
        'name': 'Demobat',
        'strength': 8,
        'dexterity': 14,
        'constitution': 10,
        'intelligence': 10,
        'wisdom': 8,
        'charisma': 8,
        'hp': 15,
        'ac': 13,
        'damage': '1d4',
        'xp': 50,
        'gold': 10,
    },
    'demodog': {
        'name': 'Demodog',
        'strength': 16,
        'dexterity': 12,
        'constitution': 16,
        'intelligence': 7,
        'wisdom': 11,
        'charisma': 10,
        'hp': 30,
        'ac': 13,
        'damage': '1d6+2',
        'xp': 100,
        'gold': 25,
    },
    'flayed': {
        'name': 'Flayed Human',
        'strength': 10,
        'dexterity': 14,
        'constitution': 15,
        'intelligence': 6,
        'wisdom': 8,
        'charisma': 5,
        'hp': 20,
        'ac': 13,
        'damage': '1d4+1',
        'xp': 75,
        'gold': 5,
    },
    'vine': {
        'name': 'Vine Creature',
        'strength': 12,
        'dexterity': 15,
        'constitution': 12,
        'intelligence': 3,
        'wisdom': 12,
        'charisma': 6,
        'hp': 18,
        'ac': 13,
        'damage': '1d4+1',
        'xp': 50,
        'gold': 0,
    },
    'soldier': {
        'name': 'Russian Soldier',
        'strength': 11,
        'dexterity': 12,
        'constitution': 12,
        'intelligence': 10,
        'wisdom': 10,
        'charisma': 10,
        'hp': 22,
        'ac': 12,
        'damage': '1d4+1',
        'xp': 75,
        'gold': 30,
    },
    'demogorgon': {
        'name': 'Demogorgon',
        'strength': 18,
        'dexterity': 13,
        'constitution': 20,
        'intelligence': 7,
        'wisdom': 9,
        'charisma': 7,
        'hp': 60,
        'ac': 15,
        'damage': '1d8+2',
        'xp': 300,
        'gold': 50,
    },
    'mindflayer': {
        'name': 'Mind Flayer',
        'strength': 19,
        'dexterity': 8,
        'constitution': 16,
        'intelligence': 5,
        'wisdom': 7,
        'charisma': 7,
        'hp': 50,
        'ac': 11,
        'damage': '1d8+2',
        'xp': 250,
        'gold': 40,
    },
    'shadow_monster': {
        'name': 'Shadow Monster',
        'strength': 21,
        'dexterity': 14,
        'constitution': 19,
        'intelligence': 14,
        'wisdom': 13,
        'charisma': 17,
        'hp': 100,
        'ac': 18,
        'damage': '1d10+3',
        'xp': 1000,
        'gold': 500,
    },
    'demogorgon_creature': {
        'name': 'Demogorgon',
        'strength': 20,
        'dexterity': 16,
        'constitution': 18,
        'intelligence': 4,
        'wisdom': 10,
        'charisma': 6,
        'hp': 80,
        'ac': 16,
        'damage': '2d8+5',
        'xp': 400,
        'gold': 100,
    },
    'vecna': {
        'name': 'Vecna - Mind Flayer Lord',
        'strength': 18,
        'dexterity': 17,
        'constitution': 17,
        'intelligence': 20,
        'wisdom': 18,
        'charisma': 19,
        'hp': 150,
        'ac': 19,
        'damage': '1d10+4',
        'xp': 2000,
        'gold': 1000,
    },
    'mind_flayer': {
        'name': 'Mind Flayer',
        'strength': 15,
        'dexterity': 14,
        'constitution': 15,
        'intelligence': 17,
        'wisdom': 14,
        'charisma': 12,
        'hp': 55,
        'ac': 15,
        'damage': '1d8+4',
        'xp': 200,
        'gold': 50,
    },
    'shadow_creature': {
        'name': 'Shadow Creature',
        'strength': 14,
        'dexterity': 16,
        'constitution': 12,
        'intelligence': 6,
        'wisdom': 8,
        'charisma': 4,
        'hp': 35,
        'ac': 14,
        'damage': '1d6+2',
        'xp': 100,
        'gold': 20,
    },
}

def create_enemy(enemy_type, level=None):
    """Create an enemy from a template."""
    if enemy_type not in ENEMY_TEMPLATES:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
    
    template = ENEMY_TEMPLATES[enemy_type].copy()
    
    # Scale enemy stats by level if provided
    if level and level > 1:
        template['hp'] = int(template['hp'] * (1 + (level - 1) * 0.3))
        template['ac'] = template['ac'] + ((level - 1) // 2)
        template['xp'] = int(template['xp'] * level)
        template['gold'] = int(template['gold'] * level)
        
        # Increase damage dice for higher levels
        if level >= 3:
            original_damage = template['damage']
            # Simple damage increase
            if '1d' in original_damage:
                template['damage'] = original_damage.replace('1d', '2d')
    
    enemy_level = level if level else 1
    return Enemy(template['name'], enemy_level, template)

def generate_random_encounter(player_level, player_gear_level=0):
    """Generate a random encounter based on player level and gear.
    
    Args:
        player_level: Player's character level
        player_gear_level: Average item level of player's equipped gear (0-5)
    """
    # Determine number of enemies
    num_enemies = random.randint(1, min(3, player_level + 1))
    
    # Calculate effective encounter level based on gear
    # Higher gear = higher chance of stronger enemies
    gear_bonus = player_gear_level * 0.3  # Each gear level adds 30% to encounter level
    encounter_level = player_level + int(player_level * gear_bonus)
    
    # Select appropriate enemy types based on encounter level
    if encounter_level <= 2:
        enemy_types = ['demobat', 'vine', 'flayed', 'soldier']
    elif encounter_level <= 4:
        enemy_types = ['demodog', 'flayed', 'soldier', 'vine']
    elif encounter_level <= 6:
        enemy_types = ['demodog', 'demogorgon', 'mindflayer', 'soldier']
    else:
        enemy_types = ['demogorgon', 'mindflayer', 'shadow_monster']
    
    enemies = []
    for _ in range(num_enemies):
        enemy_type = random.choice(enemy_types)
        enemy = create_enemy(enemy_type, encounter_level)
        enemies.append(enemy)
    
    return enemies

def get_boss_encounter(boss_type='shadow_monster'):
    """Create a boss encounter."""
    boss = create_enemy(boss_type, level=5)
    boss.name = f"The {boss.name}"
    boss.max_hp = int(boss.max_hp * 1.5)
    boss.current_hp = boss.max_hp
    boss.xp_value = int(boss.xp_value * 2)
    boss.gold_drop = int(boss.gold_drop * 2)
    return [boss]
