// Game State
let races = {};
let classes = {};
let raceClassMapping = {};
let currentGame = null;
let adventureType = 'normal';

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    loadCharacterCreationData();
    setupEventListeners();
    showStartScreen();
});

// Setup Event Listeners
function setupEventListeners() {
    // Start screen
    document.getElementById('btn-create').addEventListener('click', showCharacterCreation);

    // Character creation
    document.getElementById('creation-form').addEventListener('submit', createCharacter);
    document.getElementById('adventure-type').addEventListener('change', updateAdventureDescription);
    document.getElementById('char-race').addEventListener('change', updateRaceDescription);
    document.getElementById('char-class').addEventListener('change', updateClassDescription);
    document.getElementById('char-race').addEventListener('change', updateClassOptions);

    // Game actions
    document.getElementById('btn-encounter').addEventListener('click', startEncounter);
    document.getElementById('btn-shop').addEventListener('click', visitShop);
    document.getElementById('btn-rest').addEventListener('click', restAtInn);
    document.getElementById('btn-new-game').addEventListener('click', newGame);
}

// Load character creation data
async function loadCharacterCreationData() {
    try {
        const response = await fetch('/api/character-creation');
        const data = await response.json();
        races = data.races;
        classes = data.classes;
        raceClassMapping = data.race_class_mapping || {};
        populateSelects();
    } catch (error) {
        console.error('Error loading character data:', error);
    }
}

// Populate select dropdowns
function populateSelects() {
    const raceSelect = document.getElementById('char-race');
    const classSelect = document.getElementById('char-class');

    Object.keys(races).forEach(race => {
        const option = document.createElement('option');
        option.value = race;
        option.textContent = races[race].name;
        raceSelect.appendChild(option);
    });

    Object.keys(classes).forEach(cls => {
        const option = document.createElement('option');
        option.value = cls;
        option.textContent = classes[cls].name;
        classSelect.appendChild(option);
    });
}

// Update adventure description
function updateAdventureDescription() {
    const adventureSelect = document.getElementById('adventure-type').value;
    const description = document.getElementById('adventure-description');
    if (adventureSelect === 'upside_down') {
        description.textContent = 'Serve Vecna in the Upside Down and rise to power!';
    } else {
        description.textContent = 'Fight to save Hawkins from the Upside Down';
    }
}

// Update race description
function updateRaceDescription() {
    const raceSelect = document.getElementById('char-race').value;
    const description = document.getElementById('race-description');
    if (raceSelect && races[raceSelect]) {
        const desc = `Special Ability: ${races[raceSelect].ability}`;
        if (raceClassMapping[raceSelect]) {
            const requiredClass = raceClassMapping[raceSelect][0];
            const className = classes[requiredClass] ? classes[requiredClass].name : requiredClass;
            description.textContent = desc + ` (You must be a ${className})`;
        } else {
            description.textContent = desc;
        }
    } else {
        description.textContent = '';
    }
}

// Update class options based on selected race
function updateClassOptions() {
    const raceSelect = document.getElementById('char-race').value;
    const classSelect = document.getElementById('char-class');
    const currentClass = classSelect.value;
    
    // Clear existing options except first
    while (classSelect.options.length > 1) {
        classSelect.remove(1);
    }
    
    let availableClasses = [];
    
    if (raceSelect && raceClassMapping[raceSelect]) {
        // This race has restricted classes
        availableClasses = raceClassMapping[raceSelect];
    } else {
        // All classes available
        availableClasses = Object.keys(classes);
    }
    
    // Populate only available classes
    availableClasses.forEach(cls => {
        if (classes[cls]) {
            const option = document.createElement('option');
            option.value = cls;
            option.textContent = classes[cls].name;
            classSelect.appendChild(option);
        }
    });
    
    // If previous class is not available, clear selection
    if (!availableClasses.includes(currentClass)) {
        classSelect.value = '';
    }
}

// Update class description
function updateClassDescription() {
    const classSelect = document.getElementById('char-class').value;
    const description = document.getElementById('class-description');
    if (classSelect && classes[classSelect]) {
        const cls = classes[classSelect];
        description.textContent = `Hit Die: d${cls.hit_die}, Primary Stats: ${cls.primary_stats.join(', ')}`;
    } else {
        description.textContent = '';
    }
}

// Show start screen
function showStartScreen() {
    hideAllScreens();
    document.getElementById('start-screen').classList.remove('hidden');
}

// Show character creation
function showCharacterCreation() {
    hideAllScreens();
    document.getElementById('character-creation').classList.remove('hidden');
}

// Create character
async function createCharacter(e) {
    e.preventDefault();

    const name = document.getElementById('char-name').value;
    const race = document.getElementById('char-race').value;
    const charClass = document.getElementById('char-class').value;
    adventureType = document.getElementById('adventure-type').value;

    try {
        const response = await fetch('/api/create-character', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, race, class: charClass, adventure_type: adventureType })
        });

        const data = await response.json();
        if (data.success) {
            currentGame = data.character;
            showGameScreen();
            updateGameDisplay();
            if (adventureType === 'upside_down') {
                addMessage(`Welcome to the Upside Down, ${name}! Vecna awaits your service...`, 'info');
                showUpsideDownUI();
            } else {
                addMessage(`Welcome, ${name}! Your adventure begins!`);
            }
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error creating character:', error);
        alert('Error creating character');
    }
}

// Show game screen
function showGameScreen() {
    hideAllScreens();
    document.getElementById('game-screen').classList.remove('hidden');
    document.getElementById('btn-encounter').style.display = '';
    document.getElementById('btn-shop').style.display = '';
    document.getElementById('btn-rest').style.display = '';
}

// Hide all screens
function hideAllScreens() {
    document.getElementById('start-screen').classList.add('hidden');
    document.getElementById('character-creation').classList.add('hidden');
    document.getElementById('game-screen').classList.add('hidden');
}

// Update game display
async function updateGameDisplay() {
    try {
        const response = await fetch('/api/game-state');
        const data = await response.json();

        // Update character info
        document.getElementById('char-name-display').textContent = data.character.name;
        document.getElementById('level').textContent = data.character.level;
        document.getElementById('hp').textContent = data.character.hp;
        document.getElementById('max-hp').textContent = data.character.max_hp;
        document.getElementById('gold').textContent = data.character.gold;
        document.getElementById('experience').textContent = data.character.experience;

        // Update stats
        document.getElementById('str').textContent = data.character.stats.strength;
        document.getElementById('dex').textContent = data.character.stats.dexterity;
        document.getElementById('con').textContent = data.character.stats.constitution;
        document.getElementById('int').textContent = data.character.stats.intelligence;
        document.getElementById('wis').textContent = data.character.stats.wisdom;
        document.getElementById('cha').textContent = data.character.stats.charisma;

        // Update inventory
        const inventoryList = document.getElementById('inventory-list');
        inventoryList.innerHTML = '';
        data.inventory.forEach(item => {
            const div = document.createElement('div');
            div.className = 'inventory-item';
            div.textContent = `${item.name} (${item.type})`;
            inventoryList.appendChild(div);
        });

        // Update encounter status
        addMessage(`Encounters completed: ${data.encounters_completed}/5`);
    } catch (error) {
        console.error('Error updating game display:', error);
    }
}

// Start encounter
async function startEncounter() {
    try {
        const response = await fetch('/api/start-encounter', { method: 'POST' });
        const data = await response.json();

        if (data.error) {
            addMessage(`Error: ${data.error}`, 'info');
            return;
        }

        addMessage(data.message, 'info');
        showCombatUI(data.enemy);
    } catch (error) {
        console.error('Error starting encounter:', error);
        addMessage('Error starting encounter', 'combat');
    }
}

// Show combat UI
function showCombatUI(enemy) {
    document.getElementById('combat-section').classList.remove('hidden');
    document.getElementById('btn-encounter').disabled = true;
    document.getElementById('btn-shop').disabled = true;
    document.getElementById('btn-rest').disabled = true;

    const enemyInfo = document.getElementById('enemy-info');
    enemyInfo.innerHTML = `
        <h3>${enemy.name}</h3>
        <div class="stat">
            <span>HP:</span>
            <span id="enemy-hp">${enemy.hp}</span>/<span>${enemy.max_hp}</span>
        </div>
        <div class="stat">
            <span>AC:</span>
            <span>${enemy.ac}</span>
        </div>
        <div class="stat">
            <span>Level:</span>
            <span>${enemy.level}</span>
        </div>
    `;

    const combatActions = document.getElementById('combat-actions');
    combatActions.innerHTML = `
        <button class="combat-btn" onclick="executeCombatAction('attack')">⚔️ Attack</button>
        <button class="combat-btn" onclick="executeCombatAction('defend')">🛡️ Defend</button>
        <button class="combat-btn" onclick="executeCombatAction('useitem')">🧪 Use Item</button>
        <button class="combat-btn" onclick="executeCombatAction('flee')">🏃 Flee</button>
    `;
}

// Execute combat action
async function executeCombatAction(action) {
    try {
        const response = await fetch('/api/combat-action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });

        const data = await response.json();

        if (data.error) {
            addMessage(`Error: ${data.error}`, 'combat');
            return;
        }

        addMessage(data.message, 'combat');
        updateGameDisplay();

        if (data.combat_over) {
            document.getElementById('combat-section').classList.add('hidden');
            document.getElementById('btn-encounter').disabled = false;
            document.getElementById('btn-shop').disabled = false;
            document.getElementById('btn-rest').disabled = false;

            if (data.victory) {
                addMessage(`Victory! You earned ${data.reward_xp} XP and ${data.reward_gold} gold!`, 'success');
            } else {
                addMessage('You fled from combat!', 'info');
            }
        }
    } catch (error) {
        console.error('Error executing combat action:', error);
        addMessage('Error executing action', 'combat');
    }
}

// Visit shop
async function visitShop() {
    try {
        const response = await fetch('/api/visit-shop', { method: 'POST' });
        const data = await response.json();

        if (data.error) {
            addMessage(`Error: ${data.error}`, 'info');
            return;
        }

        addMessage(`Welcome to the shop! You have ${data.gold} gold.`);
        showShopUI(data.items);
    } catch (error) {
        console.error('Error visiting shop:', error);
        addMessage('Error visiting shop', 'info');
    }
}

// Show shop UI
function showShopUI(items) {
    document.getElementById('shop-section').classList.remove('hidden');
    document.getElementById('btn-encounter').disabled = true;
    document.getElementById('btn-rest').disabled = true;

    const shopItems = document.getElementById('shop-items');
    shopItems.innerHTML = '';

    items.forEach(item => {
        const div = document.createElement('div');
        div.className = 'shop-item';
        div.innerHTML = `
            <h4>${item.name}</h4>
            <p>${item.type}</p>
            <p style="color: #ffd700; font-weight: bold;">${item.value} gold</p>
            <button class="shop-btn" onclick="buyItem('${item.name}')">Buy</button>
        `;
        shopItems.appendChild(div);
    });

    const backBtn = document.createElement('button');
    backBtn.className = 'btn-action';
    backBtn.textContent = 'Back to Town';
    backBtn.onclick = closeShop;
    shopItems.parentElement.appendChild(backBtn);
}

// Buy item
async function buyItem(itemName) {
    try {
        const response = await fetch(`/api/buy-item/${itemName}`, { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            addMessage(`You bought ${itemName}!`, 'success');
            updateGameDisplay();
        } else {
            addMessage(`Error: ${data.error}`, 'info');
        }
    } catch (error) {
        console.error('Error buying item:', error);
    }
}

// Close shop
function closeShop() {
    document.getElementById('shop-section').classList.add('hidden');
    document.getElementById('btn-encounter').disabled = false;
    document.getElementById('btn-rest').disabled = false;
    addMessage('You left the shop.');
}

// Rest at inn
async function restAtInn() {
    try {
        const response = await fetch('/api/rest', { method: 'POST' });
        const data = await response.json();

        if (data.success) {
            addMessage(`You rested at the inn and restored all HP!`, 'success');
            addMessage(`Gold spent: 20g`, 'info');
            updateGameDisplay();
        } else {
            addMessage(`Error: ${data.message}`, 'info');
        }
    } catch (error) {
        console.error('Error resting:', error);
        addMessage('Error resting at inn', 'info');
    }
}

// New game
async function newGame() {
    if (confirm('Are you sure you want to start a new game?')) {
        try {
            await fetch('/api/new-game', { method: 'POST' });
            showStartScreen();
            document.getElementById('message-log').innerHTML = '<p>Welcome, adventurer! What would you like to do?</p>';
        } catch (error) {
            console.error('Error starting new game:', error);
        }
    }
}

// Add message to log
function addMessage(text, type = 'info') {
    const log = document.getElementById('message-log');
    const p = document.createElement('p');
    p.textContent = text;
    if (type) {
        p.className = `${type}-message`;
    }
    log.appendChild(p);
    log.scrollTop = log.scrollHeight;
}

// Show Upside Down UI
function showUpsideDownUI() {
    document.getElementById('btn-encounter').style.display = 'none';
    document.getElementById('btn-shop').style.display = 'none';
    document.getElementById('btn-rest').style.display = 'none';
    document.getElementById('upside-down-section').classList.remove('hidden');
    updateUpsideDownDisplay();
}

// Update Upside Down display
async function updateUpsideDownDisplay() {
    try {
        const response = await fetch('/api/game-state');
        const data = await response.json();

        if (data.status && data.status.vecna_power !== undefined) {
            document.getElementById('vecna-power').textContent = data.status.vecna_power;
            document.getElementById('vecna-favor').textContent = data.status.vecna_favor;
            document.getElementById('missions-completed').textContent = data.status.missions_completed;
            document.getElementById('captured-people').textContent = data.status.captured_people;
            document.getElementById('hawkins-resources').textContent = data.status.hawkins_resources;
        }
    } catch (error) {
        console.error('Error updating Upside Down display:', error);
    }
}
