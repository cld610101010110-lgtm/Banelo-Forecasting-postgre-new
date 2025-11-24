# Banelo Inventory & Sales Management System

A complete inventory and sales management system with:
- 📱 Mobile POS Application
- 🌐 Web Admin Interface
- 🔌 REST API Server
- 🗄️ PostgreSQL Database

## System Architecture

```
┌──────────────────────┐
│   Mobile POS App     │
│   (React Native)     │
└──────────┬───────────┘
           │
           │  HTTP Requests
           │
           ▼
┌──────────────────────┐         ┌────────────────────┐
│   Admin Website      │────────>│   Node.js API      │
│   (Django)           │         │   (Express.js)     │
│   Port 8000          │         │   Port 3000        │
└──────────────────────┘         └─────────┬──────────┘
                                           │
                                           │  SQL
                                           ▼
                                 ┌────────────────────┐
                                 │   PostgreSQL DB    │
                                 │   Port 5432        │
                                 └────────────────────┘
```

## Features

### Mobile POS App
- Point of Sale transactions
- Inventory tracking
- Recipe management
- Real-time sync with database

### Admin Website
- ✅ Product Management (Add/Edit/Delete)
- ✅ Inventory Control (Track stock levels, transfers)
- ✅ Sales Analytics & Reports
- ✅ Recipe Management for beverages
- ✅ Waste Tracking
- ✅ ML-based Inventory Forecasting
- ✅ Audit Trail
- ✅ Export to CSV

### REST API
- RESTful endpoints for all operations
- Shared by mobile app and admin interface
- Built with Express.js and PostgreSQL

## Quick Start

### Prerequisites
- PostgreSQL (running)
- Node.js v14+
- Python 3.8+
- npm and pip

### 1. Install Dependencies

```bash
# Install Node.js dependencies for API
cd api-server
npm install
cd ..

# Install Python dependencies for Admin Interface
cd Banelo-Forecasting-main/baneloforecasting
pip3 install -r requirements.txt
cd ../..
```

### 2. Configure Database

Edit `api-server/.env`:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banelo_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 3. Create Admin User

```bash
cd Banelo-Forecasting-main/baneloforecasting
python3 manage.py migrate
python3 manage.py createsuperuser
cd ../..
```

### 4. Start Servers

```bash
./start-servers.sh
```

This starts:
- **API Server**: http://localhost:3000
- **Admin Interface**: http://localhost:8000

## Access Points

### Local Machine
- Admin Interface: http://localhost:8000
- API Server: http://localhost:3000

### From Other Devices (same network)
- Admin Interface: http://192.168.254.176:8000
- API Server: http://192.168.254.176:3000

*Replace `192.168.254.176` with your machine's IP address*

## File Structure

```
.
├── api-server/              # Node.js REST API
│   ├── server.js           # Express server
│   ├── .env                # Database configuration
│   └── package.json
│
├── Banelo-Forecasting-main/
│   └── baneloforecasting/  # Django Admin Interface
│       ├── dashboard/      # Main app
│       ├── accounts/       # User management
│       ├── manage.py
│       └── .env           # API connection config
│
├── start-servers.sh        # Startup script
├── QUICK_START.txt         # Quick reference
└── ADMIN_INTERFACE_SETUP.md # Detailed documentation
```

## API Endpoints

### Products
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get product details
- `POST /api/products` - Create product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Sales
- `GET /api/sales?limit=1000&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`

### Recipes
- `GET /api/recipes`
- `GET /api/recipes/:id`
- `GET /api/recipes/:id/ingredients`

### Other
- `GET /api/health` - Health check
- `GET /api/audit-logs` - Audit trail
- `GET /api/waste-logs` - Waste tracking

## Configuration Files

### API Server (.env)
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banelo_db
DB_USER=postgres
DB_PASSWORD=your_password
PORT=3000
```

### Admin Interface (.env)
```env
API_BASE_URL=http://192.168.254.176:3000
API_TIMEOUT=30
```

## Mobile App Configuration

Update your mobile POS app to connect to:
```
http://192.168.254.176:3000
```

## Troubleshooting

### Cannot connect to database
- Ensure PostgreSQL is running: `sudo service postgresql start`
- Check credentials in `api-server/.env`
- Verify database exists: `psql -U postgres -l`

### Port already in use
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Module not found
```bash
# Reinstall Node.js dependencies
cd api-server
rm -rf node_modules package-lock.json
npm install

# Reinstall Python dependencies
cd Banelo-Forecasting-main/baneloforecasting
pip3 install -r requirements.txt
```

## Documentation

- **Quick Start**: See `QUICK_START.txt`
- **Detailed Setup**: See `ADMIN_INTERFACE_SETUP.md`
- **API Reference**: Check API endpoint comments in `api-server/server.js`

## Data Flow

1. **Mobile POS** → Makes transaction → **API Server** → Saves to **PostgreSQL**
2. **Admin Interface** → Views/Edits data → **API Server** → Updates **PostgreSQL**
3. All changes are synced in real-time through the shared database

## Support

For issues or questions, check the troubleshooting section in the documentation files.

---

**Last Updated**: November 2025
