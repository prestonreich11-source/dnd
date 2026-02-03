# Dungeons & Adventures

A complete D&D-style text adventure game written in Python with no bugs!

## Features

- **Complete Character Creation**: Choose from 4 races (Human, Elf, Dwarf, Halfling) and 4 classes (Warrior, Rogue, Wizard, Cleric)
- **Ability Score Rolling**: Classic 4d6 drop lowest method for generating character stats
- **Turn-Based Combat**: Initiative-based combat with attack rolls, critical hits, and tactical choices
- **Inventory System**: Collect weapons, armor, and potions
- **Shop System**: Buy and sell items to improve your character
- **Level Progression**: Gain experience, level up, and become more powerful
- **Random Encounters**: Face various enemies including goblins, orcs, trolls, and more
- **Boss Fight**: Challenge the final dragon boss when you're ready!

## How to Play

### Starting the Game

```bash
python3 game.py
```

### Game Goal

1. Complete 5 wilderness encounters
2. Return to town to prepare
3. Challenge the final dungeon and defeat the boss!

### Character Stats

- **STR (Strength)**: Melee attack damage and athletics
- **DEX (Dexterity)**: Initiative order, AC, and finesse weapons
- **CON (Constitution)**: Hit points and endurance
- **INT (Intelligence)**: Spell power and investigation
- **WIS (Wisdom)**: Perception and insight
- **CHA (Charisma)**: Social interactions

### Combat System

- Turn-based combat with initiative rolls
- Roll d20 + attack bonus vs enemy AC to hit
- **Natural 20**: Critical hit (double damage!)
- **Natural 1**: Critical miss
- Choose to attack, use items, or flee each turn

### Town Activities

- **Shop**: Buy weapons, armor, and potions
- **Inn**: Rest and restore all HP for 20 gold
- **Inventory**: Equip better gear to improve your character
- **Wilderness**: Venture out for combat encounters and treasure

## Game Files

- `game.py` - Main game loop and menu system
- `character.py` - Character classes, races, and stats
- `dice.py` - Dice rolling mechanics
- `combat.py` - Combat system and turn management
- `enemies.py` - Enemy templates and encounter generation
- `items.py` - Items, weapons, armor, and shop
- `adventure.py` - Adventure locations and story progression
- `test_game.py` - Comprehensive test suite

## Testing

Run the test suite to verify everything works:

```bash
python3 test_game.py
```

All tests should pass with no errors!

## Tips for Success

- Buy health potions before venturing into the wilderness
- Better equipment significantly improves your chances in combat
- Level up by gaining experience from defeating enemies
- Save your gold for powerful items in the shop
- Rest at the inn between adventures to maintain full HP
- Equip the best weapon and armor you can afford

## Available Races

### Human
- +1 to all stats
- Versatile and balanced

### Elf
- +2 DEX, +1 INT
- Keen senses and agility

### Dwarf
- +2 CON, +1 STR
- Tough and resilient

### Halfling
- +2 DEX, +1 CHA
- Lucky and nimble

## Available Classes

### Warrior
- Hit Die: d10
- Primary Stats: Strength, Constitution
- Starting Equipment: Longsword, Shield, Health Potion
- Best for: Frontline combat, high damage

### Rogue
- Hit Die: d8
- Primary Stats: Dexterity, Charisma
- Starting Equipment: Dagger, Lockpicks, Health Potion
- Best for: Finesse attacks, critical hits

### Wizard
- Hit Die: d6
- Primary Stats: Intelligence, Wisdom
- Starting Equipment: Staff, Spellbook, Health Potion
- Best for: Versatile combat (future spell system)

### Cleric
- Hit Die: d8
- Primary Stats: Wisdom, Constitution
- Starting Equipment: Mace, Holy Symbol, Health Potion
- Best for: Balanced combat and support

## Enemies

- **Goblin**: Weak but numerous
- **Wolf**: Fast and agile
- **Skeleton**: Undead warriors
- **Bandit**: Human outlaws
- **Orc**: Strong and aggressive
- **Troll**: Regenerating brutes
- **Ogre**: Massive and powerful
- **Dragon**: The ultimate challenge!

## Requirements

- Python 3.6 or higher
- No external dependencies required!

## License

This game is free to play and modify. Enjoy your adventure!

---

**Have fun and may the dice roll in your favor!**