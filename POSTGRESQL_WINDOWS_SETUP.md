# PostgreSQL Setup Guide for Windows

This guide will help you install and configure PostgreSQL on Windows for the Banelo Forecasting application.

## Step 1: Install PostgreSQL

### Option A: Download Official PostgreSQL Installer (Recommended)

1. **Download PostgreSQL**:
   - Go to: https://www.postgresql.org/download/windows/
   - Click "Download the installer" from EnterpriseDB
   - Download PostgreSQL 15 or 16 (latest stable version)

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Click "Next" through the setup wizard
   - **IMPORTANT**: When asked for a password, set it to: `admin123`
     (This matches your Django settings.py configuration)
   - Keep the default port: `5432`
   - Keep the default locale
   - Complete the installation

3. **Verify Installation**:
   ```cmd
   # Open Command Prompt and run:
   psql --version
   ```

### Option B: Using Chocolatey (Alternative)

If you have Chocolatey package manager installed:
```cmd
choco install postgresql
```

## Step 2: Start PostgreSQL Service

PostgreSQL should start automatically after installation. If not:

### Method 1: Using Services (GUI)
1. Press `Win + R`
2. Type: `services.msc` and press Enter
3. Find "postgresql-x64-15" (or similar) in the list
4. Right-click and select "Start"
5. Right-click again and select "Properties"
6. Set "Startup type" to "Automatic"

### Method 2: Using Command Prompt (Run as Administrator)
```cmd
# Start the service
net start postgresql-x64-15

# Or if the service name is different, list all PostgreSQL services:
sc query | findstr postgresql
```

## Step 3: Create the Database

1. **Open Command Prompt**

2. **Connect to PostgreSQL**:
   ```cmd
   psql -U postgres
   ```
   - Enter the password: `admin123` when prompted

3. **Create the database**:
   ```sql
   CREATE DATABASE banelo_db;
   ```

4. **Verify the database was created**:
   ```sql
   \l
   ```
   You should see `banelo_db` in the list

5. **Exit psql**:
   ```sql
   \q
   ```

## Step 4: Run Django Migrations

Now that PostgreSQL is running and the database is created:

```cmd
# Navigate to your Django project
cd "C:\Users\USER\Downloads\Banelo-Forecasting-postgre-new-main (9)\Banelo-Forecasting-postgre-new-main\Banelo-Forecasting-main\baneloforecasting"

# Run migrations
python manage.py migrate
```

## Step 5: Create Django Superuser

```cmd
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

## Troubleshooting

### Issue: "psql: command not found"
**Solution**: Add PostgreSQL to your PATH
1. Find PostgreSQL bin directory (usually `C:\Program Files\PostgreSQL\15\bin`)
2. Add to System PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System Variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\PostgreSQL\15\bin`
   - Click OK on all dialogs
3. Restart Command Prompt

### Issue: "Connection refused" still occurs
**Solution**: Check if PostgreSQL is running
```cmd
# List running services
sc query | findstr postgresql

# Or check specific service status
sc query postgresql-x64-15
```

### Issue: Wrong password
**Solution**: Reset PostgreSQL password
1. Find `pg_hba.conf` file (usually in `C:\Program Files\PostgreSQL\15\data`)
2. Edit the file (as Administrator)
3. Change `md5` to `trust` for local connections
4. Restart PostgreSQL service
5. Connect without password and reset:
   ```sql
   ALTER USER postgres WITH PASSWORD 'admin123';
   ```
6. Change `trust` back to `md5` in `pg_hba.conf`
7. Restart PostgreSQL service again

### Issue: Port 5432 is already in use
**Solution**: Check what's using the port
```cmd
netstat -ano | findstr :5432
```
If another application is using it, either stop that application or change the PostgreSQL port in both PostgreSQL configuration and Django settings.

## Quick Reference

**Start PostgreSQL Service:**
```cmd
net start postgresql-x64-15
```

**Stop PostgreSQL Service:**
```cmd
net stop postgresql-x64-15
```

**Connect to PostgreSQL:**
```cmd
psql -U postgres -d banelo_db
```

**Check Database Connection from Python:**
```cmd
python manage.py dbshell
```

## Next Steps

After PostgreSQL is running and migrations are complete:

1. **Start the Django development server:**
   ```cmd
   python manage.py runserver
   ```

2. **Access the application:**
   - Website: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

3. **Start the Node.js API** (if needed):
   ```cmd
   cd path\to\api-server
   node server.js
   ```

## Database Configuration Summary

Your Django application is configured with:
- **Database Name**: `banelo_db`
- **Username**: `postgres`
- **Password**: `admin123`
- **Host**: `localhost`
- **Port**: `5432`

These settings are in: `baneloforecasting/settings.py`

## Alternative: Using SQLite for Development

If you want to quickly test the application without PostgreSQL, you can temporarily switch to SQLite:

1. Open `baneloforecasting/settings.py`
2. Comment out the PostgreSQL DATABASES configuration
3. Add this SQLite configuration:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```
4. Run migrations: `python manage.py migrate`

**Note**: SQLite is only for development. For production and to work with the Mobile POS system, you must use PostgreSQL.
