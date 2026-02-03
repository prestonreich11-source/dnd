"""Dice rolling mechanics for the D&D-style game."""

import random
import re

class DiceRoller:
    """Handle all dice rolling operations."""
    
    @staticmethod
    def roll(dice_string):
        """
        Roll dice based on standard notation (e.g., '2d6', '1d20+5', '3d8-2').
        Returns the total result.
        """
        # Parse dice notation
        pattern = r'(\d+)d(\d+)([\+\-]\d+)?'
        match = re.match(pattern, dice_string.lower().replace(' ', ''))
        
        if not match:
            raise ValueError(f"Invalid dice notation: {dice_string}")
        
        num_dice = int(match.group(1))
        die_size = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        # Validate inputs
        if num_dice < 1 or num_dice > 100:
            raise ValueError("Number of dice must be between 1 and 100")
        if die_size < 2 or die_size > 100:
            raise ValueError("Die size must be between 2 and 100")
        
        # Roll the dice
        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        
        return total, rolls, modifier
    
    @staticmethod
    def roll_simple(dice_string):
        """Roll dice and return only the total."""
        total, _, _ = DiceRoller.roll(dice_string)
        return total
    
    @staticmethod
    def roll_with_advantage():
        """Roll 2d20 and take the higher result."""
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        return max(roll1, roll2), [roll1, roll2]
    
    @staticmethod
    def roll_with_disadvantage():
        """Roll 2d20 and take the lower result."""
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        return min(roll1, roll2), [roll1, roll2]
    
    @staticmethod
    def roll_ability_scores():
        """Roll ability scores using 4d6 drop lowest method."""
        scores = []
        for _ in range(6):
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.sort()
            score = sum(rolls[1:])  # Drop the lowest
            scores.append(score)
        return scores
    
    @staticmethod
    def roll_d20():
        """Roll a single d20."""
        return random.randint(1, 20)
    
    @staticmethod
    def roll_d6():
        """Roll a single d6."""
        return random.randint(1, 6)
    
    @staticmethod
    def roll_d4():
        """Roll a single d4."""
        return random.randint(1, 4)
    
    @staticmethod
    def roll_d8():
        """Roll a single d8."""
        return random.randint(1, 8)
    
    @staticmethod
    def roll_d10():
        """Roll a single d10."""
        return random.randint(1, 10)
    
    @staticmethod
    def roll_d12():
        """Roll a single d12."""
        return random.randint(1, 12)
    
    @staticmethod
    def is_critical_hit(roll):
        """Check if a d20 roll is a critical hit (natural 20)."""
        return roll == 20
    
    @staticmethod
    def is_critical_miss(roll):
        """Check if a d20 roll is a critical miss (natural 1)."""
        return roll == 1
