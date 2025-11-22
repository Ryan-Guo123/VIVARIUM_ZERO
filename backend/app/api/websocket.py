"""
WebSocket handler for real-time simulation data streaming
"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import asyncio
import json


class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        """Send message to all connected clients"""
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception:
            self.disconnect(websocket)


# Global connection manager instance
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, world):
    """WebSocket endpoint for simulation data"""
    await manager.connect(websocket)
    
    try:
        # Send initial world state
        await websocket.send_json({
            'type': 'world_state',
            **world.get_state()
        })
        
        # Listen for client commands
        while True:
            try:
                # Receive with timeout to allow periodic state updates
                data = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=0.1
                )
                
                # Handle commands
                if data.get('type') == 'command':
                    command = data.get('command')
                    
                    if command == 'pause':
                        world.pause()
                        await manager.broadcast({
                            'type': 'status',
                            'message': 'Simulation paused',
                            'paused': True
                        })
                    
                    elif command == 'resume':
                        world.resume()
                        await manager.broadcast({
                            'type': 'status',
                            'message': 'Simulation resumed',
                            'paused': False
                        })
                    
                    elif command == 'step':
                        world.step()
                        await manager.broadcast({
                            'type': 'status',
                            'message': 'Executed one step'
                        })
                    
                    elif command == 'reset':
                        world.reset()
                        await manager.broadcast({
                            'type': 'status',
                            'message': 'World reset',
                            'paused': False
                        })
                    
                    elif command == 'get_statistics':
                        stats = world.get_statistics()
                        await websocket.send_json({
                            'type': 'statistics',
                            'stats': stats
                        })
            
            except asyncio.TimeoutError:
                # No message received, continue
                pass
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def broadcast_world_state(world):
    """Broadcast current world state to all clients"""
    state = world.get_state()
    await manager.broadcast({
        'type': 'world_state',
        **state
    })
