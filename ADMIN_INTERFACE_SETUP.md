# Banelo Inventory & Sales Admin Interface

This admin interface allows you to manage your inventory and sales data from any device on your network. It connects to your Mobile POS API to read and write data.

## 🏗️ Architecture

```
┌─────────────────────┐         ┌──────────────────┐         ┌────────────────┐
│   Admin Website     │         │  Mobile POS API  │         │   PostgreSQL   │
│   (Django)          │────────>│  (Node.js)       │────────>│   Database     │
│   Port 8000         │         │  Port 3000       │         │                │
└─────────────────────┘         └──────────────────┘         └────────────────┘
     Read & Write                  REST API                    Data Storage
```

- **Admin Website (Django)**: Web interface for managing inventory and viewing sales
- **Mobile POS API (Node.js)**: Backend API that your mobile app and admin website both use
- **PostgreSQL Database**: Shared database for all data

## 📋 Prerequisites

1. **PostgreSQL** must be installed and running
2. **Node.js** (v14 or higher)
3. **Python 3** (v3.8 or higher)
4. **pip** (Python package manager)

## 🚀 Quick Start

### Step 1: Configure Database Connection

Edit `api-server/.env` and set your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banelo_db
DB_USER=postgres
DB_PASSWORD=your_actual_password
```

### Step 2: Install Dependencies

```bash
# Install Node.js dependencies for API
cd api-server
npm install
cd ..

# Install Python dependencies for Django
cd Banelo-Forecasting-main/baneloforecasting
pip3 install -r requirements.txt
cd ../..
```

### Step 3: Start Both Servers

```bash
./start-servers.sh
```

This will start:
- Mobile POS API on **port 3000**
- Admin Website on **port 8000**

### Step 4: Access Admin Interface

1. Open your browser and go to: `http://localhost:8000`
2. Or from another device: `http://192.168.254.176:8000`
3. Login with your Django admin credentials

## 🔧 Manual Startup (Alternative)

If you prefer to start servers manually:

### Terminal 1 - Start API Server
```bash
cd api-server
node server.js
```

### Terminal 2 - Start Django Admin
```bash
cd Banelo-Forecasting-main/baneloforecasting
python3 manage.py runserver 0.0.0.0:8000
```

## 📝 Creating Admin User

If you don't have an admin user yet:

```bash
cd Banelo-Forecasting-main/baneloforecasting
python3 manage.py createsuperuser
```

Follow the prompts to create your admin account.

## 🌐 Network Access

### Same Machine
- API: `http://localhost:3000`
- Admin: `http://localhost:8000`

### From Other Devices (on same network)
- API: `http://192.168.254.176:3000`
- Admin: `http://192.168.254.176:8000`

**Note**: Replace `192.168.254.176` with your actual machine IP address. Find it with:
```bash
ip addr show    # Linux
ipconfig        # Windows
ifconfig        # macOS
```

## 📱 Connecting Your Mobile POS

Update your mobile app's API configuration to point to:
```
http://192.168.254.176:3000
```

## ✨ Features

### Inventory Management
- ✅ View all products
- ✅ Add new products
- ✅ Edit product details (name, price, quantity, category)
- ✅ Delete products
- ✅ Track inventory levels (Inventory A & B)
- ✅ Transfer stock between inventories
- ✅ Calculate max servings for beverages

### Sales Management
- ✅ View all sales transactions
- ✅ Filter by date range
- ✅ Export sales data to CSV
- ✅ Sales analytics and charts

### Recipe Management
- ✅ Create recipes for beverages
- ✅ Add ingredients with quantities
- ✅ Edit existing recipes
- ✅ Calculate cost per serving

### Additional Features
- ✅ Waste tracking
- ✅ Audit trail
- ✅ ML-based inventory forecasting
- ✅ Dashboard with analytics

## 🔒 API Endpoints

Your Mobile POS API provides these endpoints:

### Products
- `GET /api/products` - List all products
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Add new product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Sales
- `GET /api/sales` - List sales (with filters)
- `GET /api/sales?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`

### Recipes
- `GET /api/recipes` - List all recipes
- `GET /api/recipes/:id` - Get recipe with ingredients
- `GET /api/recipes/:id/ingredients` - Get recipe ingredients

### Other
- `GET /api/health` - Health check
- `GET /api/audit-logs` - Audit trail
- `GET /api/waste-logs` - Waste logs

## 🐛 Troubleshooting

### "Cannot connect to API server"
- Make sure the API server is running on port 3000
- Check if PostgreSQL is running
- Verify `.env` file has correct database credentials

### "Connection refused"
- Check firewall settings
- Ensure both servers are running
- Verify the IP address is correct

### "Database error"
- Make sure PostgreSQL is running: `sudo service postgresql start`
- Check database name and credentials in `api-server/.env`
- Ensure database `banelo_db` exists

### Port already in use
```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9

# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

## 📞 Support

If you encounter issues:
1. Check the terminal output for error messages
2. Verify all prerequisites are installed
3. Ensure database connection is working
4. Check that no firewall is blocking the ports

## 🔄 Updating Data

Any changes you make in the admin interface will immediately be reflected in your mobile POS app, and vice versa, since they share the same database through the API.
