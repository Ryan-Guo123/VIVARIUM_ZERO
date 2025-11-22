/**
 * Dashboard controls and statistics display
 */

class Dashboard {
    constructor() {
        this.initializeControls();
    }

    initializeControls() {
        // Pause button
        document.getElementById('btn-pause').addEventListener('click', () => {
            vivariumWS.sendCommand('pause');
        });

        // Resume button
        document.getElementById('btn-resume').addEventListener('click', () => {
            vivariumWS.sendCommand('resume');
        });

        // Step button
        document.getElementById('btn-step').addEventListener('click', () => {
            vivariumWS.sendCommand('step');
        });

        // Reset button
        document.getElementById('btn-reset').addEventListener('click', () => {
            if (confirm('Are you sure you want to reset the simulation? All progress will be lost.')) {
                vivariumWS.sendCommand('reset');
            }
        });
    }

    updateStatistics(data) {
        // Update tick counter
        if (data.tick !== undefined) {
            document.getElementById('stat-tick').textContent = data.tick.toLocaleString();
        }

        // Update generation
        if (data.generation !== undefined) {
            document.getElementById('stat-generation').textContent = data.generation;
        }

        // Update population
        if (data.population !== undefined) {
            document.getElementById('stat-population').textContent = data.population;
        }

        // Update food count
        if (data.food_count !== undefined) {
            document.getElementById('stat-food').textContent = data.food_count;
        }

        // Update average energy
        if (data.entities && data.entities.length > 0) {
            const avgEnergy = data.entities.reduce((sum, e) => sum + e.energy, 0) / data.entities.length;
            document.getElementById('stat-energy').textContent = avgEnergy.toFixed(1);
        } else {
            document.getElementById('stat-energy').textContent = '0.0';
        }

        // Update status
        const statusEl = document.getElementById('stat-status');
        if (data.paused !== undefined) {
            if (data.paused) {
                statusEl.textContent = 'Paused';
                statusEl.className = 'stat-value status-paused';
            } else {
                statusEl.textContent = 'Running';
                statusEl.className = 'stat-value status-running';
            }
        }
    }
}

// Global dashboard instance
const dashboard = new Dashboard();
