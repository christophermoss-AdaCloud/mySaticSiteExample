// Game variables
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game state
let gameRunning = false;
let gamePaused = false;
let score = 0;
let lives = 3;

// Player object
const player = {
    x: canvas.width / 2 - 25,
    y: canvas.height - 80,
    width: 50,
    height: 50,
    speed: 5,
    color: '#00ff00'
};

// Arrays for game objects
let bullets = [];
let enemies = [];
let powerUps = [];

// Input handling
const keys = {};

// Event listeners
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    
    if (e.key === ' ' && gameRunning && !gamePaused) {
        e.preventDefault();
        shootBullet();
    }
    
    if (e.key === 'Escape') {
        togglePause();
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

document.getElementById('startBtn').addEventListener('click', startGame);
document.getElementById('pauseBtn').addEventListener('click', togglePause);
document.getElementById('resetBtn').addEventListener('click', resetGame);

// Game functions
function startGame() {
    if (!gameRunning) {
        gameRunning = true;
        gamePaused = false;
        gameLoop();
    }
}

function togglePause() {
    if (gameRunning) {
        gamePaused = !gamePaused;
        if (!gamePaused) {
            gameLoop();
        }
    }
}

function resetGame() {
    gameRunning = false;
    gamePaused = false;
    score = 0;
    lives = 3;
    bullets = [];
    enemies = [];
    powerUps = [];
    player.x = canvas.width / 2 - 25;
    player.y = canvas.height - 80;
    updateDisplay();
    clearCanvas();
}

function updateDisplay() {
    document.getElementById('score').textContent = score;
    document.getElementById('lives').textContent = lives;
}

function clearCanvas() {
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawPlayer() {
    ctx.fillStyle = player.color;
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    // Draw ship details
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.moveTo(player.x + player.width / 2, player.y);
    ctx.lineTo(player.x, player.y + player.height);
    ctx.lineTo(player.x + player.width, player.y + player.height);
    ctx.closePath();
    ctx.fill();
}

function movePlayer() {
    if (keys['ArrowLeft'] && player.x > 0) {
        player.x -= player.speed;
    }
    if (keys['ArrowRight'] && player.x < canvas.width - player.width) {
        player.x += player.speed;
    }
    if (keys['ArrowUp'] && player.y > 0) {
        player.y -= player.speed;
    }
    if (keys['ArrowDown'] && player.y < canvas.height - player.height) {
        player.y += player.speed;
    }
}

function shootBullet() {
    bullets.push({
        x: player.x + player.width / 2 - 2,
        y: player.y,
        width: 4,
        height: 15,
        speed: 7,
        color: '#ffff00'
    });
}

function updateBullets() {
    bullets = bullets.filter(bullet => bullet.y > 0);
    
    bullets.forEach(bullet => {
        bullet.y -= bullet.speed;
        ctx.fillStyle = bullet.color;
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
}

function createEnemy() {
    enemies.push({
        x: Math.random() * (canvas.width - 40),
        y: -40,
        width: 40,
        height: 40,
        speed: 2 + Math.random() * 2,
        color: '#ff0000'
    });
}

function updateEnemies() {
    // Spawn new enemies
    if (Math.random() < 0.02) {
        createEnemy();
    }
    
    enemies = enemies.filter(enemy => enemy.y < canvas.height);
    
    enemies.forEach((enemy, enemyIndex) => {
        enemy.y += enemy.speed;
        
        // Draw enemy
        ctx.fillStyle = enemy.color;
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
        
        // Check collision with bullets
        bullets.forEach((bullet, bulletIndex) => {
            if (checkCollision(bullet, enemy)) {
                bullets.splice(bulletIndex, 1);
                enemies.splice(enemyIndex, 1);
                score += 10;
                updateDisplay();
            }
        });
        
        // Check collision with player
        if (checkCollision(player, enemy)) {
            enemies.splice(enemyIndex, 1);
            lives--;
            updateDisplay();
            
            if (lives <= 0) {
                gameOver();
            }
        }
    });
}

function checkCollision(obj1, obj2) {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
}

function gameOver() {
    gameRunning = false;
    ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = '48px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2 - 30);
    
    ctx.font = '24px Arial';
    ctx.fillText(`Final Score: ${score}`, canvas.width / 2, canvas.height / 2 + 20);
    ctx.fillText('Click Reset to play again', canvas.width / 2, canvas.height / 2 + 60);
}

function gameLoop() {
    if (!gameRunning || gamePaused) return;
    
    clearCanvas();
    movePlayer();
    drawPlayer();
    updateBullets();
    updateEnemies();
    
    requestAnimationFrame(gameLoop);
}

// Initialize
clearCanvas();
updateDisplay();

// Draw initial message
ctx.fillStyle = '#ffffff';
ctx.font = '32px Arial';
ctx.textAlign = 'center';
ctx.fillText('Click Start to Begin!', canvas.width / 2, canvas.height / 2);
