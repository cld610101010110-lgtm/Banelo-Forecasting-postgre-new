# Configure Website to Connect to Mobile POS PostgreSQL Database

## Summary

This PR configures the Django website to connect to the same PostgreSQL database (`banelo_db`) that the mobile POS application uses, enabling seamless data synchronization between the mobile app and website.

## Problem Solved

Previously, the website was hardcoded to connect to `localhost` for the PostgreSQL database. Since the mobile POS and website run on **different laptops**, the website couldn't access the database and showed no data. This prevented:

- Viewing products from the mobile POS database
- Displaying sales data
- Managing recipes
- Editing or adding products

## Changes Made

### 1. Environment Variables Configuration (`.env`)
- Added `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` variables
- Allows easy switching between localhost and remote database connections
- Includes commented examples for network access

### 2. Settings Configuration (`settings.py`)
- Updated `DATABASES` configuration to use environment variables
- Changed from hardcoded values to `os.getenv()` calls
- Maintains backward compatibility with defaults

### 3. Documentation (`CONNECT_TO_MOBILE_POS_DATABASE.md`)
- Comprehensive step-by-step setup guide
- PostgreSQL remote connection configuration instructions
- Windows Firewall setup instructions
- Troubleshooting section
- Security notes

## How It Works

### Current Setup (Different Laptops)

**Mobile POS Laptop:**
- Runs PostgreSQL with `banelo_db` database
- Contains all products, sales, recipes, and ingredients
- Mobile app connects directly to localhost

**Website Laptop:**
- Runs Django website
- Connects to Mobile POS laptop's PostgreSQL via network IP
- Reads and writes to the same database

### Configuration Required

1. **On Mobile POS Laptop:**
   - Configure PostgreSQL to accept remote connections
   - Allow port 5432 through Windows Firewall
   - Restart PostgreSQL service

2. **On Website Laptop:**
   - Update `.env` file with Mobile POS laptop IP address
   - Example: `DB_HOST=192.168.254.176`

## Features Enabled

Once configured, the website can:

✅ **Display Data:**
- View all products from mobile POS database
- Show sales history
- Display recipes and ingredients
- View inventory levels (Inventory A & B)

✅ **Manage Data:**
- Add new products
- Edit existing products
- Delete products
- Create/update/delete recipes
- Transfer inventory (A → B)
- Record waste

✅ **Advanced Features:**
- Recipe management with ingredient calculations
- Max servings calculations based on available ingredients
- Inventory forecasting using ML
- Sales analytics and reporting
- Audit trail tracking

## Database Schema Compatibility

The Django models use `managed = False` for tables created by the mobile app, ensuring:
- Django won't modify the mobile app's table structure
- No migration conflicts
- Full read/write access to mobile POS data
- Safe concurrent access from both mobile app and website

## Testing Instructions

### 1. Find Mobile POS Laptop IP
```bash
ipconfig
# Look for IPv4 Address: 192.168.x.x
```

### 2. Configure PostgreSQL (Mobile POS Laptop)

**Edit `postgresql.conf`:**
```
listen_addresses = '*'
```

**Edit `pg_hba.conf`:**
```
host    banelo_db    postgres    192.168.254.0/24    md5
```

**Restart PostgreSQL:**
- Services → postgresql → Restart

### 3. Update Website Configuration

**Edit `.env`:**
```env
DB_HOST=192.168.254.176  # Your Mobile POS laptop IP
```

### 4. Test Connection
```bash
cd Banelo-Forecasting-main/baneloforecasting
python manage.py check
python manage.py runserver
```

### 5. Verify Data
- Open browser: http://localhost:8000
- Login to website
- Check inventory page shows products
- Check sales page shows transactions
- Check recipes page shows recipes
- Try editing a product
- Verify changes appear in mobile POS

## Security Considerations

- Database credentials stored in `.env` (not committed to git)
- `.env` file already in `.gitignore`
- Firewall configuration restricts access to local network only
- Connection requires authentication (username/password)

## Backward Compatibility

- Defaults to `localhost` if environment variables not set
- Existing local development setups continue to work
- No breaking changes to database schema

## Related Files

- `Banelo-Forecasting-main/baneloforecasting/.env`
- `Banelo-Forecasting-main/baneloforecasting/baneloforecasting/settings.py`
- `CONNECT_TO_MOBILE_POS_DATABASE.md`

## Documentation

Complete setup guide available in: `CONNECT_TO_MOBILE_POS_DATABASE.md`

Includes:
- Step-by-step instructions
- PostgreSQL configuration
- Firewall setup
- Network troubleshooting
- Common issues and solutions

## Notes

- Both laptops must be on the same WiFi network
- Mobile POS laptop IP may change if network changes
- PostgreSQL port 5432 must be accessible
- Database user is `postgres` with password `admin123`

## Checklist

- [x] Updated `.env` with database configuration variables
- [x] Modified `settings.py` to use environment variables
- [x] Created comprehensive setup documentation
- [x] Tested configuration compatibility
- [x] Verified backward compatibility with localhost
- [x] Added security considerations
- [x] Documented troubleshooting steps

---

**After this PR is merged**, users need to:
1. Follow the setup guide in `CONNECT_TO_MOBILE_POS_DATABASE.md`
2. Configure their Mobile POS laptop to allow remote connections
3. Update the `.env` file with their Mobile POS laptop IP
4. Test the connection and verify data appears
