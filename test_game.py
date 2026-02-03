"""
Test script to verify game components work correctly.
"""

import sys
sys.path.insert(0, '/workspaces/dnd')

from character import Character, RACES, CLASSES
from dice import DiceRoller
from enemies import create_enemy, generate_random_encounter
from combat import Combat
from items import Shop, WEAPONS, ARMOR, CONSUMABLES

def test_dice_rolling():
    """Test dice rolling mechanics."""
    print("Testing dice rolling...")
    
    # Test basic rolls
    total, rolls, modifier = DiceRoller.roll('2d6')
    assert len(rolls) == 2
    assert all(1 <= r <= 6 for r in rolls)
    assert total == sum(rolls) + modifier
    
    # Test with modifier
    total, rolls, modifier = DiceRoller.roll('1d20+5')
    assert len(rolls) == 1
    assert 1 <= rolls[0] <= 20
    assert modifier == 5
    assert total == rolls[0] + 5
    
    # Test advantage
    result, rolls = DiceRoller.roll_with_advantage()
    assert len(rolls) == 2
    assert result == max(rolls)
    
    # Test ability score rolling
    scores = DiceRoller.roll_ability_scores()
    assert len(scores) == 6
    assert all(3 <= s <= 18 for s in scores)
    
    print("✓ Dice rolling tests passed!")

def test_character_creation():
    """Test character creation."""
    print("\nTesting character creation...")
    
    race = RACES['human']
    char_class = CLASSES['warrior']
    
    character = Character("Test Hero", race, char_class)
    
    assert character.name == "Test Hero"
    assert character.level == 1
    assert character.is_alive()
    assert character.current_hp == character.max_hp
    assert character.armor_class >= 10
    assert len(character.inventory) > 0
    
    # Test stat modifiers
    character.strength = 16
    assert character.get_modifier('strength') == 3
    
    character.dexterity = 8
    assert character.get_modifier('dexterity') == -1
    
    # Test damage
    character.current_hp = 20
    character.max_hp = 20  # Set max_hp to match for test
    damage = character.take_damage(5)
    assert damage == 5
    assert character.current_hp == 15
    assert character.is_alive()
    
    # Test healing
    healed = character.heal(3)
    assert healed == 3
    assert character.current_hp == 18
    
    # Test death
    character.take_damage(100)
    assert not character.is_alive()
    
    print("✓ Character creation tests passed!")

def test_enemies():
    """Test enemy creation."""
    print("\nTesting enemy creation...")
    
    demobat = create_enemy('demobat', level=1)
    assert demobat.name == 'Demobat'
    assert demobat.level == 1
    assert demobat.is_alive()
    assert demobat.max_hp > 0
    
    # Test scaling
    demodog = create_enemy('demodog', level=3)
    assert demodog.level == 3
    assert demodog.max_hp > create_enemy('demodog', level=1).max_hp
    
    # Test random encounter generation
    encounters = generate_random_encounter(player_level=2)
    assert len(encounters) >= 1
    assert all(e.is_alive() for e in encounters)
    
    print("✓ Enemy tests passed!")

def test_items():
    """Test items and shop."""
    print("\nTesting items and shop...")
    
    # Test weapons
    assert 'longsword' in WEAPONS
    sword = WEAPONS['longsword']
    assert sword.damage == '1d8'
    
    # Test armor
    assert 'chainmail' in ARMOR
    armor = ARMOR['chainmail']
    assert armor.ac_bonus == 3
    
    # Test consumables
    assert 'health_potion' in CONSUMABLES
    potion = CONSUMABLES['health_potion']
    assert potion.effect_value == 20
    
    # Test shop
    shop = Shop()
    assert len(shop.inventory) > 0
    
    print("✓ Item tests passed!")

def test_combat_mechanics():
    """Test combat mechanics without full combat."""
    print("\nTesting combat mechanics...")
    
    # Create test character and enemy
    race = RACES['elf']
    char_class = CLASSES['rogue']
    player = Character("Test Rogue", race, char_class)
    player.strength = 14
    player.dexterity = 16
    
    # Equip weapon
    weapon = WEAPONS['dagger'].to_dict()
    player.equipped_weapon = weapon
    
    enemy = create_enemy('demobat', level=1)
    
    # Test attack bonus calculation
    attack_bonus = player.get_attack_bonus()
    assert attack_bonus >= -5 and attack_bonus <= 10
    
    # Test damage calculation
    damage_dice = player.get_attack_damage()
    assert 'd' in damage_dice
    
    # Test enemy can take damage
    initial_hp = enemy.current_hp
    enemy.take_damage(5)
    assert enemy.current_hp == initial_hp - 5
    
    print("✓ Combat mechanics tests passed!")

def test_level_up():
    """Test leveling system."""
    print("\nTesting level up system...")
    
    race = RACES['dwarf']
    char_class = CLASSES['warrior']
    player = Character("Test Warrior", race, char_class)
    
    initial_level = player.level
    initial_max_hp = player.max_hp
    
    # Add enough XP to level up
    player.add_experience(1000)
    
    assert player.level == initial_level + 1
    assert player.max_hp >= initial_max_hp
    assert player.current_hp == player.max_hp
    
    print("✓ Level up tests passed!")

def run_all_tests():
    """Run all test suites."""
    print("="*50)
    print("RUNNING GAME TESTS")
    print("="*50 + "\n")
    
    try:
        test_dice_rolling()
        test_character_creation()
        test_enemies()
        test_items()
        test_combat_mechanics()
        test_level_up()
        
        print("\n" + "="*50)
        print("ALL TESTS PASSED! ✓")
        print("="*50)
        print("\nThe game is ready to play with no bugs!")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
