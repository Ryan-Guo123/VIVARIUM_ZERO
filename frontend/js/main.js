/**
 * Main application entry point
 * Coordinates WebSocket, visualizer, and dashboard
 */

// Initialize WebSocket connection
vivariumWS.connect();

// Register message handlers
vivariumWS.on('world_state', (data) => {
    // Update visualizer
    updateWorldState(data);
    
    // Update dashboard statistics
    dashboard.updateStatistics(data);
});

vivariumWS.on('status', (data) => {
    console.log('Status update:', data.message);
    
    // Update paused state if provided
    if (data.paused !== undefined) {
        worldState.paused = data.paused;
    }
});

vivariumWS.on('statistics', (data) => {
    console.log('Statistics:', data.stats);
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    vivariumWS.close();
});

// Log startup
console.log('🌱 VIVARIUM ZERO - Client initialized');
console.log('Phase 1: Genesis - Simple random walk behavior');
