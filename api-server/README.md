# Banelo API Server

Node.js Express API server for Banelo Forecasting system with PostgreSQL database.

## Setup

### 1. Install Dependencies

```bash
cd api-server
npm install
```

### 2. Configure Database

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=banelo_db
DB_USER=postgres
DB_PASSWORD=your_password_here
PORT=3000
```

### 3. Ensure PostgreSQL Database Exists

Make sure your PostgreSQL database is created and has the required tables:

- products
- recipes
- recipe_ingredients
- sales
- audit_logs
- waste_logs

### 4. Start the Server

Development mode (with auto-reload):
```bash
npm run dev
```

Production mode:
```bash
npm start
```

The server will run on `http://localhost:3000`

## API Endpoints

### Health Check
- `GET /api/health` - Check server and database status

### Products
- `GET /api/products` - Get all products
- `GET /api/products/:id` - Get single product
- `POST /api/products` - Create new product
- `PUT /api/products/:id` - Update product
- `DELETE /api/products/:id` - Delete product

### Recipes
- `GET /api/recipes` - Get all recipes
- `GET /api/recipes/:id` - Get single recipe with ingredients
- `GET /api/recipes/:id/ingredients` - Get recipe ingredients

### Sales
- `GET /api/sales` - Get sales data (supports date_from, date_to, limit params)

### Audit Logs
- `GET /api/audit-logs` - Get audit logs

### Waste Logs
- `GET /api/waste-logs` - Get waste logs

## Testing

Test the API health:
```bash
curl http://localhost:3000/api/health
```

Test getting products:
```bash
curl http://localhost:3000/api/products
```

## Connecting Django Website

The Django website in `Banelo-Forecasting-main/baneloforecasting/` is already configured to use this API.

Make sure the API server is running before starting Django:

```bash
# Terminal 1 - Start API Server
cd api-server
npm start

# Terminal 2 - Start Django
cd Banelo-Forecasting-main/baneloforecasting
python manage.py runserver
```

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check if port 3000 is available: `lsof -i :3000`

### Database Errors
- Verify database exists: `psql -U postgres -l`
- Check credentials in `.env` file
- Ensure tables are created in PostgreSQL

### CORS Errors
- CORS is enabled by default for all origins
- Adjust cors configuration in `server.js` if needed
