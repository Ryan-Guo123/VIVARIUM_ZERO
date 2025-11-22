# Development Guide

## Phase 1 - Genesis (Current) ✅

### What's Implemented

1. **Backend Core (Python/FastAPI)**
   - `world.py`: Main simulation loop
   - `entity.py`: Creature entity with physics and energy
   - `physics.py`: Collision detection and interactions
   - `spatial_grid.py`: Spatial partitioning optimization
   - `food_spawner.py`: Random food generation
   - `websocket.py`: Real-time bidirectional communication

2. **Frontend (p5.js/Vanilla JS)**
   - `visualizer.js`: Canvas rendering at 60 FPS
   - `websocket.js`: WebSocket client with auto-reconnect
   - `dashboard.js`: Control panel (pause/resume/step/reset)
   - `main.js`: Application coordinator

3. **Infrastructure**
   - `Dockerfile`: ARM64-compatible Python container
   - `docker-compose.yml`: Single-service orchestration
   - `.env.example`: Configuration template
   - Unit tests for core components

### Development Workflow

#### Local Development (Without Docker)

```bash
# Terminal 1: Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend (optional, FastAPI serves it)
cd frontend
python -m http.server 8080
```

#### Docker Development

```bash
# Start
./start.sh

# View logs
docker-compose logs -f backend

# Restart after code changes
docker-compose restart backend

# Stop
./stop.sh
```

#### Running Tests

```bash
cd backend
pytest tests/ -v
```

### Key Files to Understand

1. **`backend/app/main.py`**
   - FastAPI app initialization
   - Background simulation loop (`simulation_loop()`)
   - WebSocket and REST endpoints

2. **`backend/app/core/world.py`**
   - Main `World` class
   - `update()` method runs each simulation tick
   - Phase 1: Calls `entity.simple_behavior()` (hardcoded)

3. **`frontend/js/visualizer.js`**
   - p5.js sketch definition
   - `drawEntity()` and `drawFood()` rendering
   - Receives state updates via WebSocket

### Debugging Tips

1. **Pause and Single-Step**
   - Click "⏸ Pause" in UI
   - Click "⏭ Step" to execute one frame
   - Inspect `worldState` in browser console

2. **Backend Logging**
   ```python
   # Add to world.py or entity.py
   print(f"Entity {entity.id[:8]} at ({entity.x}, {entity.y}), energy={entity.energy}")
   ```

3. **Frontend Logging**
   ```javascript
   // Add to visualizer.js
   console.log('Drawing', worldState.entities.length, 'entities');
   ```

4. **Check WebSocket Messages**
   - Open browser DevTools → Network → WS
   - Inspect JSON messages flowing between client and server

### Performance Monitoring

- **Backend**: Check CPU usage with `htop` or `docker stats`
- **Frontend**: p5.js shows FPS in top-left corner
- **Target**: 60 FPS with 50+ entities

---

## Phase 2 - Cambrian Explosion (Next) 🚧

### What to Build

1. **Virtual Machine (`backend/app/core/vm/`)**
   - `instructions.py`: Define instruction enum
   - `interpreter.py`: Execute instruction stack
   - `genome.py`: Encode/decode genetic sequences

2. **Evolution (`backend/app/evolution/`)**
   - `mutation.py`: 4 mutation types
   - `reproduction.py`: Genetic crossover (optional)

3. **Enhanced Visualization**
   - Attack spikes (if genome contains `ATTACK`)
   - Sensor halos (visual range)
   - Code complexity trail

### VM Design Decisions (Confirmed)

- **Architecture**: Stack-based (easier to mutate)
- **Gas Limit**: 50 instructions per tick
- **Instruction Format**: 1 byte opcode + optional 1-byte operand

Example genome:
```
[SEE_FOOD, PUSH, 100, CMP, JUMP_IF, 10, MOVE_FWD, JUMP, 0]
```

### Integration Points

1. Replace `entity.simple_behavior()` with:
   ```python
   def execute_genome(self):
       vm = VMInterpreter(self.genome)
       vm.execute(gas=50, entity=self)
   ```

2. Add genome to `Entity.__init__()`:
   ```python
   self.genome: List[Instruction] = initial_genome or random_genome()
   ```

3. Mutate genome in `entity.reproduce()`:
   ```python
   child.genome = mutate(self.genome, rate=settings.mutation_rate)
   ```

---

## Phase 3 - Time Lord (Future) 🔮

### Snapshot System

```python
# backend/app/persistence/snapshot.py
class SnapshotManager:
    def save_snapshot(self, world):
        state = {
            'tick': world.tick,
            'entities': [e.to_dict() for e in world.entities],
            'foods': [f.to_dict() for f in world.foods]
        }
        compressed = zlib.compress(json.dumps(state).encode())
        self.db.execute('INSERT INTO snapshots ...', compressed)
    
    def load_snapshot(self, snapshot_id):
        # Restore world state from DB
        pass
```

### Timeline UI

```javascript
// frontend/js/timeline.js
<div class="timeline">
  <input type="range" id="time-slider" min="0" max="1000">
</div>

document.getElementById('time-slider').addEventListener('change', (e) => {
    vivariumWS.sendCommand('load_snapshot', { snapshot_id: e.target.value });
});
```

---

## Common Issues & Solutions

### Issue: Docker build fails on Mac mini
**Solution**: Ensure Docker Desktop is set to use ARM64 architecture (should be automatic)

### Issue: WebSocket connection refused
**Solution**: 
- Check backend is running: `curl http://localhost:8000/api/health`
- Verify port 8000 is exposed in `docker-compose.yml`
- Check firewall settings

### Issue: Frontend shows "Disconnected"
**Solution**:
- Open browser console, check for errors
- Verify WebSocket URL in `websocket.js` matches your setup
- Try hard refresh (Ctrl+Shift+R)

### Issue: Simulation runs very slowly
**Solution**:
- Reduce `INITIAL_POPULATION` to 10-20
- Lower `TARGET_FPS` to 30
- Check if too many logs are being printed

### Issue: Entities all die immediately
**Solution**:
- Increase `PHOTOSYNTHESIS_RATE` (e.g., to 1.0)
- Decrease `EXISTENCE_TAX` (e.g., to 0.1)
- Increase `FOOD_SPAWN_COUNT` (e.g., to 5)

---

## Code Style Guide

### Python
- Follow PEP 8
- Use type hints: `def update(self, dt: float) -> None:`
- Docstrings for public methods
- Keep methods under 30 lines when possible

### JavaScript
- Use ES6+ syntax (const/let, arrow functions)
- CamelCase for classes, camelCase for functions
- Comment complex logic

### Naming Conventions
- Files: `snake_case.py`, `camelCase.js`
- Classes: `PascalCase`
- Functions/methods: `snake_case` (Python), `camelCase` (JS)
- Constants: `UPPER_SNAKE_CASE`

---

## Git Workflow (If Using Version Control)

```bash
# Feature branches
git checkout -b feature/vm-interpreter
git commit -am "Add stack-based VM interpreter"
git push origin feature/vm-interpreter

# Main branch
git checkout main
git merge feature/vm-interpreter
```

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **p5.js Reference**: https://p5js.org/reference/
- **Numba Tutorial**: https://numba.readthedocs.io/
- **WebSocket Guide**: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API

---

**Last Updated**: Phase 1 Complete
**Next Milestone**: VM Interpreter Implementation
