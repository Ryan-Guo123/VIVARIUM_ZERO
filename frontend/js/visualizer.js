/**
 * p5.js visualizer for VIVARIUM ZERO
 * Renders creatures and food particles in real-time
 */

let worldState = {
    entities: [],
    foods: [],
    world_width: 800,
    world_height: 600,
    tick: 0,
    generation: 0,
    population: 0,
    food_count: 0,
    paused: false
};

// p5.js sketch
const sketch = (p) => {
    
    p.setup = () => {
        const canvas = p.createCanvas(800, 600);
        canvas.parent('canvas-container');
        p.frameRate(60);
    };
    
    p.draw = () => {
        // Background
        p.background(10, 10, 20);
        
        // Draw grid (subtle)
        drawGrid(p);
        
        // Draw foods
        worldState.foods.forEach(food => {
            drawFood(p, food);
        });
        
        // Draw entities
        worldState.entities.forEach(entity => {
            drawEntity(p, entity);
        });
        
        // Draw info overlay
        drawOverlay(p);
    };
};

function drawGrid(p) {
    p.stroke(30, 30, 40);
    p.strokeWeight(1);
    
    const gridSize = 50;
    
    // Vertical lines
    for (let x = 0; x < worldState.world_width; x += gridSize) {
        p.line(x, 0, x, worldState.world_height);
    }
    
    // Horizontal lines
    for (let y = 0; y < worldState.world_height; y += gridSize) {
        p.line(0, y, worldState.world_width, y);
    }
}

function drawFood(p, food) {
    const [r, g, b] = food.color;
    
    // Glow effect
    p.noStroke();
    p.fill(r, g, b, 30);
    p.circle(food.x, food.y, food.radius * 4);
    
    // Main body
    p.fill(r, g, b);
    p.circle(food.x, food.y, food.radius * 2);
    
    // Highlight
    p.fill(255, 255, 255, 150);
    p.circle(food.x - food.radius * 0.3, food.y - food.radius * 0.3, food.radius * 0.6);
}

function drawEntity(p, entity) {
    p.push();
    p.translate(entity.x, entity.y);
    p.rotate(entity.angle);
    
    const [r, g, b] = entity.color;
    
    // Draw trail
    if (entity.trail && entity.trail.length > 1) {
        p.noFill();
        p.stroke(r, g, b, 50);
        p.strokeWeight(2);
        p.beginShape();
        for (let point of entity.trail) {
            p.vertex(point[0] - entity.x, point[1] - entity.y);
        }
        p.endShape();
    }
    
    // Energy glow (opacity based on energy level)
    const energyRatio = entity.energy / entity.max_energy;
    const glowAlpha = Math.max(20, energyRatio * 80);
    p.noStroke();
    p.fill(r, g, b, glowAlpha);
    p.circle(0, 0, entity.radius * 3);
    
    // Main body
    p.fill(r, g, b);
    p.stroke(255, 255, 255, 100);
    p.strokeWeight(1);
    p.circle(0, 0, entity.radius * 2);
    
    // Direction indicator (small triangle)
    p.fill(255, 255, 255, 200);
    p.noStroke();
    p.triangle(
        entity.radius, 0,
        -entity.radius * 0.5, entity.radius * 0.5,
        -entity.radius * 0.5, -entity.radius * 0.5
    );
    
    // Energy bar
    const barWidth = entity.radius * 2.5;
    const barHeight = 3;
    const barY = -entity.radius - 8;
    
    // Background
    p.fill(50, 50, 50);
    p.noStroke();
    p.rect(-barWidth / 2, barY, barWidth, barHeight);
    
    // Energy level
    const energyWidth = barWidth * energyRatio;
    const energyColor = getEnergyColor(energyRatio);
    p.fill(energyColor);
    p.rect(-barWidth / 2, barY, energyWidth, barHeight);
    
    p.pop();
}

function getEnergyColor(ratio) {
    if (ratio > 0.6) return [0, 255, 100];      // Green - healthy
    if (ratio > 0.3) return [255, 200, 0];      // Yellow - low
    return [255, 50, 50];                        // Red - critical
}

function drawOverlay(p) {
    // Paused indicator
    if (worldState.paused) {
        p.fill(255, 100, 0, 150);
        p.noStroke();
        p.textSize(48);
        p.textAlign(p.CENTER, p.CENTER);
        p.text('⏸ PAUSED', worldState.world_width / 2, worldState.world_height / 2);
    }
    
    // FPS counter
    p.fill(255, 255, 255, 150);
    p.noStroke();
    p.textSize(12);
    p.textAlign(p.LEFT, p.TOP);
    p.text(`FPS: ${Math.round(p.frameRate())}`, 10, 10);
}

// Update world state from WebSocket
function updateWorldState(data) {
    worldState = {
        ...worldState,
        ...data
    };
    
    // Update canvas size if needed
    if (data.world_width && data.world_height) {
        const p = window.p5Instance;
        if (p && (p.width !== data.world_width || p.height !== data.world_height)) {
            p.resizeCanvas(data.world_width, data.world_height);
        }
    }
}

// Initialize p5.js
window.addEventListener('DOMContentLoaded', () => {
    window.p5Instance = new p5(sketch);
});
