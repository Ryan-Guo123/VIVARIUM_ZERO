# 🌱 VIVARIUM ZERO

**Artificial Life Simulation Through Genetic Programming**

An evolutionary artificial life system where creatures don't just evolve parameters - they evolve **code logic** itself. Running 24/7 on a Mac mini Home Lab, organisms self-modify their behavioral instructions in a virtual assembly environment, emerging survival strategies never conceived by humans.

---

## 🎯 Project Vision

VIVARIUM ZERO is a **Genetic Programming** based artificial life simulator where:
- 🧬 Creatures evolve their **instruction code**, not just neural network weights
- ⚡ A virtual machine (VM) executes genetic "assembly code" for each organism
- 🔄 Users have "God Mode" with time travel capabilities - rewind evolution at any moment
- 🏠 Designed for 24/7 operation on **Mac mini (ARM64) + Ubuntu Server**

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** installed
- **Mac mini (ARM64)** or any ARM64/x86_64 Linux system
- At least **2GB RAM** and **1GB disk space**

### Installation

1. **Clone the repository:**
   ```bash
   cd /home/home/VIVARIUM_ZERO
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the simulation:**
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

   You should see the VIVARIUM interface with creatures (colored dots) moving around and eating food (green dots).

---

## 📋 Current Status: **Phase 1 - Genesis** ✅

### Implemented Features

✅ **Basic World Simulation**
- 2D bounded universe (800x600 petri dish)
- Wall collision with bounce physics
- Spatial grid optimization for collision detection

✅ **Energy Economy**
- Photosynthesis: +0.5 energy/second (passive income)
- Existence tax: -0.2 energy/second (metabolism)
- Food spawning: Random food particles worth +20 energy
- Death when energy ≤ 0 (corpse becomes food)

✅ **Reproduction**
- Creatures split when energy ≥ 80
- Parent and child each get 50% of energy
- Generation counter tracks evolutionary progress

✅ **Visualization (p5.js)**
- Real-time rendering at 60 FPS
- Energy bars above creatures
- Trail visualization
- Color-coded creatures and food

✅ **God Mode Controls**
- ⏸ Pause/Resume simulation
- ⏭ Single-step execution (debugging)
- 🔄 Reset world
- 📊 Real-time statistics dashboard

✅ **WebSocket Real-time Communication**
- Bidirectional client-server updates
- Automatic reconnection on disconnect
- Command system for control

---

## 🏗️ Project Structure

```
VIVARIUM_ZERO/
├── backend/                    # Python/FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Configuration management
│   │   ├── core/              # Simulation core
│   │   │   ├── world.py       # Main world container
│   │   │   ├── entity.py      # Creature entity
│   │   │   ├── physics.py     # Physics engine
│   │   │   ├── spatial_grid.py # Spatial partitioning
│   │   │   ├── food_spawner.py # Food generation
│   │   │   └── vm/            # Virtual machine (Phase 2)
│   │   ├── evolution/         # Evolution system (Phase 2)
│   │   ├── persistence/       # Database & snapshots (Phase 3)
│   │   └── api/
│   │       └── websocket.py   # WebSocket handler
│   ├── requirements.txt
│   └── tests/
├── frontend/                  # Web client
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── websocket.js       # WebSocket client
│       ├── visualizer.js      # p5.js rendering
│       └── dashboard.js       # Control panel
├── data/                      # Persistent data (SQLite, snapshots)
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🎮 How to Use

### Control Panel

- **⏸ Pause**: Freeze the simulation
- **▶️ Resume**: Continue simulation
- **⏭ Step**: Execute one simulation tick (for debugging)
- **🔄 Reset**: Restart with new random population

### Understanding the Visualization

| Color | Meaning |
|-------|---------|
| 🟢 Green | Food particles (+20 energy) |
| 🔴 Red/Colored | Living creatures (color = family lineage) |
| 🟤 Brown | Corpse (dead creature, provides +10 energy) |

**Energy Bar Colors:**
- 🟢 Green: Healthy (>60% energy)
- 🟡 Yellow: Low (30-60% energy)
- 🔴 Red: Critical (<30% energy)

---

## 🧬 Evolutionary Mechanics (Phase 1)

### Current Behavior
- **Random Walk**: Creatures move in a direction, occasionally turning randomly
- **Food Seeking**: Passive - creatures that happen to encounter food survive better
- **Natural Selection**: Low-energy creatures die, successful ones reproduce

### Energy Flow
```
Photosynthesis: +0.5/s (baseline survival)
Existence Tax:  -0.2/s (cost of living)
Food:           +20    (scavenging reward)
Death:          →  Becomes food (+10 energy)
```

### Population Dynamics
- **Carrying Capacity**: Max 500 creatures
- **Environmental Pressure**: When overcrowded, random culling occurs
- **Reproduction Threshold**: 80 energy required to split

---

## 🔮 Roadmap

### ✅ Phase 1: Genesis (CURRENT)
**Status**: Complete
- Basic physics simulation
- Energy economy
- Simple hardcoded behavior (random walk)
- Real-time visualization
- Debug controls

### 🚧 Phase 2: Cambrian Explosion (NEXT)
**Target**: 3-4 weeks
- [ ] Stack-based Virtual Machine (VM)
- [ ] Instruction set: Sensors, Logic, Actions
- [ ] Genetic Programming: Creatures evolve code
- [ ] Mutation engine (4 types: flip, insert, delete, duplicate)
- [ ] Phenotype visualization (attack spikes, sensor halos)
- [ ] Behavior diversity emergence

**Instruction Set Preview:**
```assembly
SEE_FOOD        ; Sensor: Find nearest food
SEE_WALL        ; Sensor: Distance to wall
MY_ENERGY       ; Sensor: Self energy level
PUSH 10         ; Logic: Push constant
CMP             ; Logic: Compare stack values
JUMP_IF label   ; Logic: Conditional jump
MOVE_FWD        ; Action: Move forward
ROTATE 45       ; Action: Turn
ATTACK          ; Action: Harm nearby creature
SPLIT           ; Action: Reproduce
```

### 🔮 Phase 3: Time Lord
**Target**: 2-3 weeks
- [ ] SQLite database integration
- [ ] Automatic world snapshots (every 5 minutes)
- [ ] Time travel UI (timeline scrubber)
- [ ] Hot reload from historical state
- [ ] Export/import functionality
- [ ] Disaster system (environmental challenges)

---

## ⚙️ Configuration

Edit `.env` or pass environment variables to Docker:

```bash
# World Settings
WORLD_WIDTH=800
WORLD_HEIGHT=600
INITIAL_POPULATION=20
MAX_POPULATION=500

# Energy Economy
PHOTOSYNTHESIS_RATE=0.5
EXISTENCE_TAX=0.2
FOOD_ENERGY=20
FOOD_SPAWN_INTERVAL=2.0
FOOD_SPAWN_COUNT=3

# Evolution
MUTATION_RATE=0.01           # Phase 2
REPRODUCTION_ENERGY=80

# Performance
TARGET_FPS=60
MAX_GAS_PER_TICK=50          # Phase 2: VM instruction limit
```

---

## 🧪 Development

### Run without Docker (Local Development)

1. **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend:**
   Open `frontend/index.html` in browser or use a local server:
   ```bash
   python -m http.server 8080 --directory frontend
   ```

### Run Tests
```bash
cd backend
pytest tests/
```

---

## 🐛 Troubleshooting

### WebSocket Connection Failed
- Ensure backend is running: `docker-compose ps`
- Check logs: `docker-compose logs -f backend`
- Verify port 8000 is not in use: `lsof -i :8000`

### Simulation Running Slow
- Reduce population: Set `MAX_POPULATION=100` in `.env`
- Lower FPS: Set `TARGET_FPS=30`
- Check CPU usage: Phase 1 should use ~10-20% on Mac mini

### Docker Build Failed on ARM64
- Ensure using ARM64-compatible base image
- Current `Dockerfile` uses `python:3.11-slim-bookworm` (multi-arch)

---

## 📊 Performance Benchmarks

**Target (Mac mini M1):**
- 500 creatures @ 60 FPS
- <20% CPU usage
- <500MB RAM

**Phase 1 Actual:**
- 50 creatures @ 60 FPS
- ~10% CPU usage
- ~200MB RAM

---

## 🤝 Contributing

This is a learning/research project. Contributions welcome!

### Development Principles
1. **Simplicity First**: Phase 1 uses hardcoded behavior intentionally
2. **Incremental Complexity**: Each phase builds on previous
3. **Performance Matters**: Use Numba/JIT for hot paths (Phase 2+)
4. **Debuggability**: Always include pause/step/inspect tools

---

## 📜 License

MIT License - Free for research and educational use

---

## 🙏 Acknowledgments

- Inspired by **Avida**, **Tierra**, and **Polyworld**
- Built with **FastAPI**, **p5.js**, **Numba**
- Designed for **Mac mini Home Lab** enthusiasts

---

## 📞 Contact

**Project Owner**: Ryan (Founder)  
**CTO**: AI Assistant  
**Target Platform**: Mac mini (ARM64/Ubuntu) + Web Client

---

**Current Phase**: 1 (Genesis) ✅  
**Next Milestone**: Virtual Machine Implementation (Phase 2)  
**Ultimate Goal**: Emergent intelligence through code evolution 🧬🤖
