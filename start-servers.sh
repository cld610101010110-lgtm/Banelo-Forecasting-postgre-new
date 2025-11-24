#!/bin/bash

# Banelo Inventory & Sales Admin Interface Startup Script
# This script starts both the Mobile POS API and the Admin Website

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Banelo Inventory & Sales Admin Interface               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if PostgreSQL is running
echo -e "${BLUE}[1/4] Checking PostgreSQL connection...${NC}"
if pg_isready -q 2>/dev/null; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not running. Please start PostgreSQL first.${NC}"
    echo "  Try: sudo service postgresql start"
    exit 1
fi

# Check Node.js
echo -e "${BLUE}[2/4] Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    echo -e "${GREEN}✓ Node.js $(node --version) found${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js first.${NC}"
    exit 1
fi

# Check Python
echo -e "${BLUE}[3/4] Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python $(python3 --version) found${NC}"
else
    echo -e "${RED}✗ Python3 not found. Please install Python3 first.${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[4/4] Starting servers...${NC}"
echo ""

# Start Mobile POS API (Node.js on port 3000)
echo -e "${GREEN}Starting Mobile POS API on port 3000...${NC}"
cd api-server
node server.js &
API_PID=$!
cd ..

# Wait a moment for API to start
sleep 3

# Check if API started successfully
if ps -p $API_PID > /dev/null; then
    echo -e "${GREEN}✓ Mobile POS API started (PID: $API_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start Mobile POS API${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Starting Django Admin Interface on port 8000...${NC}"
cd Banelo-Forecasting-main/baneloforecasting

# Run Django server
python3 manage.py runserver 0.0.0.0:8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Check if Django started successfully
if ps -p $DJANGO_PID > /dev/null; then
    echo -e "${GREEN}✓ Django Admin Interface started (PID: $DJANGO_PID)${NC}"
else
    echo -e "${RED}✗ Failed to start Django Admin Interface${NC}"
    kill $API_PID 2>/dev/null
    exit 1
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   SERVERS RUNNING                                         ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║                                                           ║"
echo "║   📱 Mobile POS API:                                      ║"
echo "║      http://localhost:3000                                ║"
echo "║      http://192.168.254.176:3000                          ║"
echo "║                                                           ║"
echo "║   🌐 Admin Website:                                       ║"
echo "║      http://localhost:8000                                ║"
echo "║      http://192.168.254.176:8000                          ║"
echo "║                                                           ║"
echo "║   Press Ctrl+C to stop both servers                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Trap Ctrl+C and cleanup
trap "echo ''; echo 'Stopping servers...'; kill $API_PID $DJANGO_PID 2>/dev/null; echo 'Servers stopped.'; exit 0" INT

# Wait for both processes
wait $API_PID $DJANGO_PID
