#!/bin/bash
# Stop VIVARIUM ZERO

echo "🛑 Stopping VIVARIUM ZERO..."

docker-compose down

echo "✅ VIVARIUM ZERO stopped"
echo ""
echo "💾 Data preserved in ./data directory"
echo ""
echo "To start again, run: ./start.sh"
