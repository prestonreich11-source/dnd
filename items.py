"""Items and inventory management for the D&D-style game."""

class Item:
    """Base class for items."""
    
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

class Weapon(Item):
    """Weapon item with damage dice."""
    
    def __init__(self, name, description, value, damage, finesse=False):
        super().__init__(name, description, value)
        self.damage = damage
        self.finesse = finesse
    
    def to_dict(self):
        """Convert to dictionary for compatibility."""
        return {
            'name': self.name,
            'damage': self.damage,
            'finesse': self.finesse,
            'value': self.value,
            'description': self.description
        }

class Armor(Item):
    """Armor item with AC bonus."""
    
    def __init__(self, name, description, value, ac_bonus):
        super().__init__(name, description, value)
        self.ac_bonus = ac_bonus
    
    def to_dict(self):
        """Convert to dictionary for compatibility."""
        return {
            'name': self.name,
            'ac_bonus': self.ac_bonus,
            'value': self.value,
            'description': self.description
        }

class Consumable(Item):
    """Consumable item like potions."""
    
    def __init__(self, name, description, value, effect_type, effect_value):
        super().__init__(name, description, value)
        self.effect_type = effect_type
        self.effect_value = effect_value
    
    def to_dict(self):
        """Convert to dictionary for compatibility."""
        return {
            'name': self.name,
            self.effect_type: self.effect_value,
            'value': self.value,
            'description': self.description
        }

# Available items in the game
WEAPONS = {
    'dagger': Weapon('Dagger', 'A small, sharp blade', 20, '1d4', finesse=True),
    'shortsword': Weapon('Shortsword', 'A light, versatile blade', 100, '1d6', finesse=True),
    'longsword': Weapon('Longsword', 'A classic knightly weapon', 150, '1d8', finesse=False),
    'greatsword': Weapon('Greatsword', 'A massive two-handed blade', 500, '2d6', finesse=False),
    'mace': Weapon('Mace', 'A heavy bludgeoning weapon', 50, '1d6', finesse=False),
    'staff': Weapon('Staff', 'A wooden walking staff', 10, '1d6', finesse=False),
    'warhammer': Weapon('Warhammer', 'A heavy war hammer', 150, '1d10', finesse=False),
}

ARMOR = {
    'leather': Armor('Leather Armor', 'Light, flexible armor', 50, 1),
    'chainmail': Armor('Chainmail', 'Metal rings woven together', 750, 3),
    'plate': Armor('Plate Armor', 'Heavy, full-body protection', 1500, 5),
    'shield': Armor('Shield', 'A wooden shield', 100, 2),
}

CONSUMABLES = {
    'health_potion': Consumable('Health Potion', 'Restores 20 HP', 50, 'healing', 20),
    'greater_health_potion': Consumable('Greater Health Potion', 'Restores 50 HP', 150, 'healing', 50),
    'antidote': Consumable('Antidote', 'Cures poison', 25, 'cure_poison', True),
}

class Shop:
    """Shop for buying and selling items."""
    
    def __init__(self):
        self.inventory = self._create_shop_inventory()
    
    def _create_shop_inventory(self):
        """Create shop inventory with all available items."""
        inventory = []
        
        for weapon in WEAPONS.values():
            inventory.append(weapon)
        
        for armor in ARMOR.values():
            inventory.append(armor)
        
        for consumable in CONSUMABLES.values():
            inventory.append(consumable)
        
        return inventory
    
    def display_items(self):
        """Display all items available for purchase."""
        print("\n=== SHOP ===")
        print("\nWeapons:")
        for item in self.inventory:
            if isinstance(item, Weapon):
                print(f"  {item.name} - {item.damage} damage - {item.value} gold")
        
        print("\nArmor:")
        for item in self.inventory:
            if isinstance(item, Armor):
                print(f"  {item.name} - +{item.ac_bonus} AC - {item.value} gold")
        
        print("\nConsumables:")
        for item in self.inventory:
            if isinstance(item, Consumable):
                print(f"  {item.name} - {item.description} - {item.value} gold")
    
    def buy_item(self, player, item_name):
        """Player buys an item."""
        item_name_lower = item_name.lower()
        
        # Find item
        item = None
        for shop_item in self.inventory:
            if shop_item.name.lower() == item_name_lower:
                item = shop_item
                break
        
        if not item:
            print(f"Item '{item_name}' not found.")
            return False
        
        # Check if player has enough gold
        if player.gold < item.value:
            print(f"Not enough gold! You need {item.value} but only have {player.gold}.")
            return False
        
        # Purchase item
        player.gold -= item.value
        player.add_item(item.to_dict())
        print(f"Purchased {item.name} for {item.value} gold!")
        return True
    
    def sell_item(self, player, item):
        """Player sells an item for half its value."""
        if isinstance(item, dict):
            # Get value from dict
            value = item.get('value', 10)
            sell_price = value // 2
            item_name = item.get('name', 'Unknown Item')
        else:
            sell_price = item.value // 2
            item_name = item.name
        
        player.gold += sell_price
        player.remove_item(item)
        print(f"Sold {item_name} for {sell_price} gold!")
        return True

def display_inventory(player):
    """Display player's inventory."""
    print("\n=== INVENTORY ===")
    print(f"Gold: {player.gold}")
    
    if not player.inventory:
        print("Your inventory is empty.")
        return
    
    print("\nItems:")
    for i, item in enumerate(player.inventory):
        if isinstance(item, dict):
            name = item.get('name', 'Unknown')
            if 'damage' in item:
                print(f"{i+1}. {name} (Weapon - {item['damage']} damage)")
            elif 'ac_bonus' in item:
                print(f"{i+1}. {name} (Armor - +{item['ac_bonus']} AC)")
            elif 'healing' in item:
                print(f"{i+1}. {name} (Potion - Heals {item['healing']} HP)")
            else:
                print(f"{i+1}. {name}")
        else:
            print(f"{i+1}. {item}")
