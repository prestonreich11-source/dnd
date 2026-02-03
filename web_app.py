#!/usr/bin/env python3
"""
Flask web server for D&D-Style Text Adventure Game
Access at http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, session
from functools import wraps
import json
import os
from character import Character, RACES, CLASSES, RACE_CLASS_MAPPING
from adventure import Adventure, UpsideDownAdventure
from vecna_adventure import VecnaAdventure

app = Flask(__name__)
app.secret_key = 'dnd_adventure_secret_key_' + os.urandom(16).hex()

# Store game instances per session
games = {}

def get_game():
    """Get or create game instance for current session."""
    session_id = request.sid if hasattr(request, 'sid') else session.get('session_id', 'default')
    if session_id not in games:
        games[session_id] = None
    return games[session_id]

def set_game(game):
    """Set game instance for current session."""
    session_id = request.sid if hasattr(request, 'sid') else session.get('session_id', 'default')
    games[session_id] = game

@app.route('/')
def index():
    """Main game page."""
    game = get_game()
    if game is None:
        return render_template('index.html', page='start')
    else:
        return render_template('index.html', page='game')

@app.route('/api/character-creation', methods=['GET'])
def character_creation_data():
    """Get character creation options."""
    races = {k: {'name': k.capitalize(), 'ability': v.special_ability} for k, v in RACES.items()}
    classes = {k: {'name': k.capitalize(), 'hit_die': v.hit_die, 'primary_stats': v.primary_stats} 
               for k, v in CLASSES.items()}
    return jsonify({
        'races': races, 
        'classes': classes,
        'race_class_mapping': RACE_CLASS_MAPPING
    })

@app.route('/api/create-character', methods=['POST'])
def create_character():
    """Create a new character."""
    data = request.json
    name = data.get('name', '').strip()
    race = data.get('race', '').lower()
    char_class = data.get('class', '').lower()
    adventure_type = data.get('adventure_type', 'normal')
    
    if not name:
        return jsonify({'error': 'Name cannot be empty'}), 400
    if race not in RACES:
        return jsonify({'error': 'Invalid race'}), 400
    if char_class not in CLASSES:
        return jsonify({'error': 'Invalid class'}), 400
    
    # Create character and game
    character = Character(name, RACES[race], CLASSES[char_class])
    
    if adventure_type == 'upside_down':
        adventure = UpsideDownAdventure(character)
    else:
        adventure = Adventure(character)
    
    set_game(adventure)
    
    return jsonify({
        'success': True,
        'adventure_type': adventure_type,
        'character': {
            'name': character.name,
            'race': race,
            'class': char_class,
            'hp': character.current_hp,
            'max_hp': character.max_hp,
            'stats': {
                'strength': character.strength,
                'dexterity': character.dexterity,
                'constitution': character.constitution,
                'intelligence': character.intelligence,
                'wisdom': character.wisdom,
                'charisma': character.charisma
            }
        }
    })

@app.route('/api/game-state', methods=['GET'])
def game_state():
    """Get current game state."""
    game = get_game()
    if game is None:
        return jsonify({'error': 'No active game'}), 400
    
    character = game.player
    inventory_list = []
    
    # Handle inventory - items might be dicts or objects
    for item in character.inventory:
        if isinstance(item, dict):
            inventory_list.append({
                'name': item.get('name', 'Unknown'),
                'type': item.get('type', 'misc'),
                'value': item.get('value', 0)
            })
        else:
            inventory_list.append({
                'name': getattr(item, 'name', 'Unknown'),
                'type': getattr(item, 'type', 'misc'),
                'value': getattr(item, 'value', 0)
            })
    
    status = {}
    if hasattr(game, 'get_status'):
        status = game.get_status()
    
    return jsonify({
        'character': {
            'name': character.name,
            'level': character.level,
            'experience': character.experience,
            'hp': character.current_hp,
            'max_hp': character.max_hp,
            'gold': character.gold,
            'stats': {
                'strength': character.strength,
                'dexterity': character.dexterity,
                'constitution': character.constitution,
                'intelligence': character.intelligence,
                'wisdom': character.wisdom,
                'charisma': character.charisma
            }
        },
        'inventory': inventory_list,
        'encounters_completed': getattr(game, 'encounters_completed', 0),
        'encounters_remaining': 5 - getattr(game, 'encounters_completed', 0),
        'status': status
    })

@app.route('/api/start-encounter', methods=['POST'])
def start_encounter():
    """Start a new encounter."""
    game = get_game()
    if game is None:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        from enemies import generate_random_encounter
        enemies = generate_random_encounter(game.player.level, game.player.get_gear_level())
        enemy = enemies[0]
        
        # Store enemy in game session for combat
        if not hasattr(game, 'current_enemy'):
            game.current_enemy = None
        game.current_enemy = enemy
        
        return jsonify({
            'enemy': {
                'name': enemy.name,
                'hp': enemy.current_hp,
                'max_hp': enemy.max_hp,
                'ac': enemy.armor_class,
                'level': enemy.level
            },
            'message': f"A wild {enemy.name} appears!"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/combat-action', methods=['POST'])
def combat_action():
    """Execute a combat action."""
    game = get_game()
    if game is None:
        return jsonify({'error': 'No active game'}), 400
    
    data = request.json
    action = data.get('action', 'attack').lower()
    
    try:
        if not hasattr(game, 'current_enemy') or game.current_enemy is None:
            return jsonify({'error': 'No active combat'}), 400
        
        enemy = game.current_enemy
        character = game.player
        
        # Resolve combat action
        message = ""
        combat_over = False
        victory = False
        
        if action == 'attack':
            # Roll attack
            from dice import DiceRoller
            roller = DiceRoller()
            attack_roll = roller.roll_d20() + character.get_attack_bonus()
            
            if attack_roll >= enemy.armor_class:
                # Hit!
                damage_dice = character.get_attack_damage()
                damage = roller.roll_simple(damage_dice) + character.get_attack_bonus()
                enemy.take_damage(damage)
                message = f"You hit {enemy.name} for {damage} damage! ({enemy.current_hp}/{enemy.max_hp} HP left)"
                
                if not enemy.is_alive():
                    combat_over = True
                    victory = True
                    xp_gain = enemy.xp_value
                    gold_gain = enemy.gold_drop
                    character.add_experience(xp_gain)
                    character.gold += gold_gain
                    game.encounters_completed += 1
                    message = f"Victory! {enemy.name} defeated! Gained {xp_gain} XP and {gold_gain} gold!"
                else:
                    # Enemy attacks back
                    enemy_attack = roller.roll_d20() + enemy.get_attack_bonus()
                    if enemy_attack >= character.armor_class:
                        enemy_damage = roller.roll_simple(enemy.get_attack_damage()) + enemy.get_attack_bonus()
                        character.take_damage(enemy_damage)
                        message += f"\n{enemy.name} hits you for {enemy_damage} damage! ({character.current_hp}/{character.max_hp} HP left)"
                    else:
                        message += f"\n{enemy.name}'s attack misses!"
            else:
                # Miss
                message = f"Your attack misses!"
                # Enemy attacks back
                from dice import DiceRoller
                roller = DiceRoller()
                enemy_attack = roller.roll_d20() + enemy.get_attack_bonus()
                if enemy_attack >= character.armor_class:
                    enemy_damage = roller.roll_simple(enemy.get_attack_damage()) + enemy.get_attack_bonus()
                    character.take_damage(enemy_damage)
                    message += f"\n{enemy.name} hits you for {enemy_damage} damage! ({character.current_hp}/{character.max_hp} HP left)"
                else:
                    message += f"\n{enemy.name}'s attack misses!"
        
        elif action == 'defend':
            message = "You brace for impact, raising your defense!"
            # Enemy attacks with disadvantage (lower damage)
            from dice import DiceRoller
            roller = DiceRoller()
            enemy_attack = roller.roll_d20() + enemy.get_attack_bonus() - 5
            if enemy_attack >= character.armor_class:
                enemy_damage = max(1, roller.roll_simple(enemy.get_attack_damage()) + enemy.get_attack_bonus() - 3)
                character.take_damage(enemy_damage)
                message += f"\n{enemy.name} hits you for {enemy_damage} damage! ({character.current_hp}/{character.max_hp} HP left)"
            else:
                message += f"\n{enemy.name}'s attack bounces off your defense!"
        
        elif action == 'flee':
            message = f"You fled from {enemy.name}!"
            combat_over = True
        
        elif action == 'useitem':
            # Use healing item if available
            healed = False
            for item in character.inventory:
                if isinstance(item, dict) and item.get('healing'):
                    healing = item.get('healing', 20)
                    character.heal(healing)
                    character.inventory.remove(item)
                    message = f"You used {item.get('name', 'potion')} and healed {healing} HP!"
                    healed = True
                    break
            
            if not healed:
                message = "You have no items to use!"
            else:
                # Enemy attacks back
                from dice import DiceRoller
                roller = DiceRoller()
                enemy_attack = roller.roll_d20() + enemy.get_attack_bonus()
                if enemy_attack >= character.armor_class:
                    enemy_damage = roller.roll_simple(enemy.get_attack_damage()) + enemy.get_attack_bonus()
                    character.take_damage(enemy_damage)
                    message += f"\n{enemy.name} attacks for {enemy_damage} damage! ({character.current_hp}/{character.max_hp} HP left)"
        
        # Check if player died
        if character.current_hp <= 0:
            combat_over = True
            victory = False
            message = "You have been defeated!"
        
        return jsonify({
            'message': message,
            'combat_over': combat_over,
            'victory': victory,
            'reward_xp': enemy.xp_value if victory else 0,
            'reward_gold': enemy.gold_drop if victory else 0,
            'player_hp': character.current_hp,
            'player_max_hp': character.max_hp,
            'enemy_hp': enemy.current_hp if not victory else 0,
            'enemy_max_hp': enemy.max_hp
        })
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 400

@app.route('/api/visit-shop', methods=['POST'])
def visit_shop():
    """Get shop inventory."""
    game = get_game()
    if game is None:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        # Get shop items from the shop
        shop_items = []
        for item in game.shop.inventory:
            if hasattr(item, 'to_dict'):
                shop_items.append(item.to_dict())
            else:
                shop_items.append({
                    'name': getattr(item, 'name', 'Unknown'),
                    'type': getattr(item, 'type', 'misc'),
                    'value': getattr(item, 'value', 0)
                })
        
        return jsonify({
            'items': shop_items,
            'gold': game.player.gold
        })
    except Exception as e:
        # Find the item in shop
        item_to_buy = None
        for item in game.shop.inventory:
            if item.name.lower() == item_name.lower():
                item_to_buy = item
                break
        
        if not item_to_buy:
            return jsonify({'success': False, 'error': 'Item not found'}), 400
        
        # Check if player has enough gold
        if game.player.gold >= item_to_buy.value:
            game.player.gold -= item_to_buy.value
            if hasattr(item_to_buy, 'to_dict'):
                game.player.add_item(item_to_buy.to_dict())
            else:
                game.player.add_item(item_to_buy)
            return jsonify({'success': True, 'gold': game.player.gold})
        else:
            return jsonify({'success': False, 'error': 'Not enough gold'}), 400
@app.route('/api/buy-item/<item_name>', methods=['POST'])
def buy_item(item_name):
    """Buy an item from shop."""
    game = get_game()
    if game is Nplayer.gold >= cost:
            game.player.gold -= cost
            game.player.current_hp = game.player.max_hp
            return jsonify({
                'success': True,
                'hp': game.player.current_hp,
                'max_hp': game.player.max_hp,
                'gold': game.play(e)}), 400

@app.route('/api/rest', methods=['POST'])
def rest():
    """Rest at inn."""
    game = get_game()
    if game is None:
        return jsonify({'error': 'No active game'}), 400
    
    try:
        cost = 20
        if game.character.gold >= cost:
            game.character.gold -= cost
            game.character.current_hp = game.character.max_hp
            return jsonify({
                'success': True,
                'hp': game.character.current_hp,
                'max_hp': game.character.max_hp,
                'gold': game.character.gold,
                'message': f'You rested and restored all HP! (-{cost} gold)'
            })
        else:
            return jsonify({
                'success': False,
                'message': f'You need {cost} gold to rest'
            }), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/new-game', methods=['POST'])
def new_game():
    """Start a new game."""
    session_id = request.sid if hasattr(request, 'sid') else session.get('session_id', 'default')
    if session_id in games:
        games[session_id] = None
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 50)
    print("  DUNGEONS & ADVENTURES - Web Server")
    print("  Access at http://localhost:5000")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
