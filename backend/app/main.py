"""
FastAPI main application entry point
VIVARIUM ZERO - Artificial Life Simulation System
"""
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import asyncio
from contextlib import asynccontextmanager

from .core.world import World
from .api.websocket import websocket_endpoint, broadcast_world_state
from .config import settings


# Global world instance
world = World()

# Background task for simulation loop
simulation_task = None


async def simulation_loop():
    """Main simulation loop running in background"""
    while True:
        try:
            # Update world
            world.update()
            
            # Broadcast state to all connected clients (every 2 frames to reduce bandwidth)
            if world.tick % 2 == 0:
                await broadcast_world_state(world)
            
            # Sleep to maintain target FPS
            await asyncio.sleep(1.0 / settings.target_fps)
        
        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(1.0)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global simulation_task
    
    # Startup
    print("🌱 VIVARIUM ZERO starting...")
    print(f"   World size: {settings.world_width}x{settings.world_height}")
    print(f"   Initial population: {settings.initial_population}")
    print(f"   Target FPS: {settings.target_fps}")
    
    # Start simulation loop
    simulation_task = asyncio.create_task(simulation_loop())
    
    yield
    
    # Shutdown
    print("🛑 VIVARIUM ZERO shutting down...")
    if simulation_task:
        simulation_task.cancel()
        try:
            await simulation_task
        except asyncio.CancelledError:
            pass


# Create FastAPI app
app = FastAPI(
    title="VIVARIUM ZERO",
    description="Artificial Life Simulation with Genetic Programming",
    version="1.0.0",
    lifespan=lifespan
)


# Mount static files (frontend)
import os
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
async def root():
    """Serve main HTML page"""
    index_path = os.path.join(frontend_dir, "index.html")
    with open(index_path, "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    """WebSocket endpoint for real-time simulation data"""
    await websocket_endpoint(websocket, world)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "tick": world.tick,
        "population": len(world.entities),
        "generation": world.generation
    }


@app.get("/api/statistics")
async def get_statistics():
    """Get current simulation statistics"""
    return world.get_statistics()


@app.post("/api/control/pause")
async def pause_simulation():
    """Pause the simulation"""
    world.pause()
    return {"status": "paused"}


@app.post("/api/control/resume")
async def resume_simulation():
    """Resume the simulation"""
    world.resume()
    return {"status": "resumed"}


@app.post("/api/control/step")
async def step_simulation():
    """Execute single simulation step"""
    world.step()
    return {"status": "stepped", "tick": world.tick}


@app.post("/api/control/reset")
async def reset_simulation():
    """Reset the simulation"""
    world.reset()
    return {"status": "reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
