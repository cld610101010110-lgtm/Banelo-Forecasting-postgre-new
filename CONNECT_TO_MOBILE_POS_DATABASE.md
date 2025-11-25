# Connect Website to Mobile POS PostgreSQL Database

This guide helps you connect your Django website to the PostgreSQL database running on your Mobile POS laptop.

## Current Situation

- **Mobile POS Laptop**: Has PostgreSQL database with all your products, sales, and recipes
- **Website Laptop**: Needs to connect to the same database to show and edit data

## Step-by-Step Setup

### Step 1: Find Your Mobile POS Laptop IP Address

**On Windows (Mobile POS Laptop):**

1. Open Command Prompt (`Win + R`, type `cmd`, press Enter)
2. Type: `ipconfig`
3. Look for "IPv4 Address" under your network adapter (WiFi or Ethernet)
4. It will look like: `192.168.x.x` (example: `192.168.254.176`)

**On Mac/Linux:**

1. Open Terminal
2. Type: `ifconfig` or `ip addr show`
3. Look for `inet` address

**IMPORTANT:** Note down this IP address!

### Step 2: Configure PostgreSQL to Allow Remote Connections

On your **Mobile POS Laptop**, you need to allow PostgreSQL to accept connections from your website laptop.

#### 2.1 Find PostgreSQL Configuration Files

Default locations on Windows:
- `C:\Program Files\PostgreSQL\15\data\postgresql.conf`
- `C:\Program Files\PostgreSQL\15\data\pg_hba.conf`

(Change `15` to your PostgreSQL version number)

#### 2.2 Edit postgresql.conf

1. Open `postgresql.conf` in a text editor (as Administrator)
2. Find the line: `#listen_addresses = 'localhost'`
3. Change it to: `listen_addresses = '*'`
4. Save the file

#### 2.3 Edit pg_hba.conf

1. Open `pg_hba.conf` in a text editor (as Administrator)
2. Add this line at the end:

```
# Allow website laptop to connect
host    banelo_db    postgres    192.168.x.0/24    md5
```

Replace `192.168.x.0/24` with your network range. For example:
- If your Mobile POS IP is `192.168.254.176`
- Use: `192.168.254.0/24`

3. Save the file

#### 2.4 Restart PostgreSQL Service

**On Windows:**

1. Press `Win + R`, type `services.msc`, press Enter
2. Find `postgresql-x64-15` (or similar)
3. Right-click → Restart

**On Mac/Linux:**

```bash
sudo systemctl restart postgresql
```

#### 2.5 Allow PostgreSQL Through Windows Firewall

1. Open Windows Firewall Settings
2. Click "Advanced settings"
3. Click "Inbound Rules" → "New Rule"
4. Select "Port" → Next
5. Select "TCP" and enter port: `5432`
6. Select "Allow the connection" → Next
7. Check all profiles (Domain, Private, Public) → Next
8. Name it: "PostgreSQL" → Finish

### Step 3: Update Website Configuration

On your **Website Laptop**:

1. Open `.env` file in the Django project:
   ```
   Banelo-Forecasting-main/baneloforecasting/.env
   ```

2. Update the `DB_HOST` line with your Mobile POS laptop IP:

```env
# Change from:
DB_HOST=localhost

# To (use YOUR Mobile POS laptop IP):
DB_HOST=192.168.254.176
```

**Example .env file:**

```env
# PostgreSQL Database Configuration
DB_HOST=192.168.254.176          # ← Your Mobile POS laptop IP
DB_PORT=5432
DB_NAME=banelo_db
DB_USER=postgres
DB_PASSWORD=admin123
```

### Step 4: Test the Connection

On your **Website Laptop**, navigate to the project folder and test:

```bash
cd Banelo-Forecasting-main/baneloforecasting
python manage.py check
```

If successful, you should see:
```
System check identified no issues (0 silenced).
```

### Step 5: Test with Django Shell

```bash
python manage.py shell
```

Then type:

```python
from dashboard.models import Product
print(Product.objects.count())
```

You should see the number of products from your database!

### Step 6: Run the Website

```bash
python manage.py runserver 0.0.0.0:8000
```

Now open your browser and go to:
```
http://localhost:8000
```

You should see all your data from the Mobile POS database!

## Troubleshooting

### "Connection refused" Error

**Check:**
- Is PostgreSQL running on Mobile POS laptop?
- Are both laptops on the same WiFi network?
- Did you restart PostgreSQL after config changes?
- Is Windows Firewall allowing port 5432?

**Test connection from Website laptop:**

```bash
# Test if port 5432 is accessible
telnet 192.168.254.176 5432
```

Or use `psql`:

```bash
psql -h 192.168.254.176 -U postgres -d banelo_db
```

### "Password authentication failed"

Make sure the `DB_PASSWORD` in `.env` matches your PostgreSQL password.

### Website Shows No Data

**Check:**
1. Can you see data in pgAdmin on Mobile POS laptop?
2. Is the database name correct (`banelo_db`)?
3. Run the debug endpoint: http://localhost:8000/dashboard/debug-database-status/

### Network Changed

If you change WiFi networks or the Mobile POS laptop IP changes:

1. Find the new IP address (Step 1)
2. Update `.env` file with new IP
3. Restart Django server

## For Development on Same Laptop

If you're testing on the same laptop (not common for your setup):

```env
DB_HOST=localhost
```

## Security Notes

- The database password is in `.env` - don't share this file!
- Only allow connections from trusted networks
- Consider using a strong password for PostgreSQL user

## Need Help?

If you encounter issues:
1. Check PostgreSQL is running: `services.msc` on Windows
2. Verify IP address hasn't changed
3. Check firewall settings
4. Look at Django error messages in the terminal

---

**Summary:**
1. Find Mobile POS laptop IP (`ipconfig`)
2. Configure PostgreSQL to allow remote connections
3. Update `.env` with Mobile POS IP
4. Test connection
5. Run website and verify data appears
