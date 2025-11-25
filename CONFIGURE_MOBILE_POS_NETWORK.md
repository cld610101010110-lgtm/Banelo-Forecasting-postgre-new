# Configure Mobile POS PostgreSQL for Network Access

## Overview
This guide will help you configure PostgreSQL on your Mobile POS laptop (192.168.254.176) to accept connections from your website server.

**IMPORTANT**: Both devices must be connected to the same WiFi network (192.168.254.x subnet).

---

## Step 1: Verify PostgreSQL is Running

1. Press `Win + R` and type `services.msc`, press Enter
2. Scroll down and find **postgresql-x64-16** (or similar)
3. Check the Status column - it should say **Running**
4. If not running:
   - Right-click → Start
   - Right-click → Properties
   - Set "Startup type" to **Automatic**
   - Click Apply → OK

---

## Step 2: Configure PostgreSQL to Listen on Network

1. Open File Explorer and navigate to:
   ```
   C:\Program Files\PostgreSQL\16\data
   ```

2. Find and open `postgresql.conf` with Notepad (Run as Administrator)

3. Press `Ctrl + F` and search for: `listen_addresses`

4. You'll find a line like:
   ```
   #listen_addresses = 'localhost'
   ```

5. Change it to:
   ```
   listen_addresses = '*'
   ```

   **Remove the # at the beginning!**

6. Save the file (Ctrl + S)

---

## Step 3: Configure PostgreSQL to Accept Network Connections

1. In the same folder (`C:\Program Files\PostgreSQL\16\data`)

2. Find and open `pg_hba.conf` with Notepad (Run as Administrator)

3. Scroll to the bottom of the file

4. Add this line at the end:
   ```
   host    all    all    192.168.254.0/24    md5
   ```

5. Your pg_hba.conf should now look like this at the bottom:
   ```
   # IPv4 local connections:
   host    all             all             127.0.0.1/32            md5
   # NEW LINE - allows connections from 192.168.254.x network
   host    all             all             192.168.254.0/24        md5
   ```

6. Save the file (Ctrl + S)

---

## Step 4: Configure Windows Firewall

### Option A: Using PowerShell (Recommended - Quick)

1. Press `Win + X` and select **Windows PowerShell (Admin)**
2. Run this command:
   ```powershell
   New-NetFirewallRule -DisplayName "PostgreSQL" -Direction Inbound -Protocol TCP -LocalPort 5432 -Action Allow
   ```
3. You should see a success message

### Option B: Using Windows Firewall GUI

1. Press `Win + R` and type `wf.msc`, press Enter
2. Click **Inbound Rules** on the left
3. Click **New Rule...** on the right
4. Select **Port** → Next
5. Select **TCP**, enter **5432** in "Specific local ports" → Next
6. Select **Allow the connection** → Next
7. Check all three: Domain, Private, Public → Next
8. Name: **PostgreSQL** → Finish

---

## Step 5: Restart PostgreSQL Service

1. Press `Win + R` and type `services.msc`, press Enter
2. Find **postgresql-x64-16**
3. Right-click → **Restart**
4. Wait for it to show "Running" status

---

## Step 6: Verify Network Configuration

Open Command Prompt and run:
```cmd
netstat -an | findstr 5432
```

You should see:
```
TCP    0.0.0.0:5432           0.0.0.0:0              LISTENING
```

If you see `127.0.0.1:5432` instead of `0.0.0.0:5432`, go back to Step 2 and verify postgresql.conf was saved correctly.

---

## Step 7: Test Connection from Website Server

After completing the above steps, run this command on your website server:

```bash
cd /home/user/Banelo-Forecasting-postgre-new/api-server
node test-connection.js
```

You should see:
```
✅ Successfully connected to PostgreSQL!
```

---

## Troubleshooting

### Connection Still Fails?

1. **Check both devices are on same network:**
   ```cmd
   ipconfig
   ```
   Both should show IP addresses like 192.168.254.x

2. **Ping test from website server to Mobile POS:**
   ```bash
   ping 192.168.254.176
   ```
   Should receive replies. If "Request timed out", check your WiFi connection.

3. **Test PostgreSQL port is open:**
   From website server:
   ```bash
   telnet 192.168.254.176 5432
   ```
   If it connects, PostgreSQL is accessible.

4. **Check PostgreSQL logs:**
   ```
   C:\Program Files\PostgreSQL\16\data\log\
   ```
   Look at the latest .log file for connection errors.

5. **Verify password:**
   On Mobile POS laptop, open pgAdmin 4
   - Try connecting with:
     - User: postgres
     - Password: admin123
   - If it fails, the password might be different

### Common Issues

| Issue | Solution |
|-------|----------|
| "Connection refused" | PostgreSQL service not running |
| "Connection timeout" | Firewall blocking port 5432 |
| "Authentication failed" | Wrong password in .env file |
| "Database does not exist" | Need to create banelo_db database |

---

## Security Note

This configuration allows any device on your local network (192.168.254.x) to connect to PostgreSQL. This is safe for local/private networks but:

- ❌ Do NOT use this configuration on public WiFi
- ❌ Do NOT expose port 5432 to the internet
- ✅ Only use on your private home/business network

---

## Next Steps

After successful connection, you can:

1. Start the API server:
   ```bash
   cd /home/user/Banelo-Forecasting-postgre-new/api-server
   npm start
   ```

2. Access the API at `http://localhost:3000/api/health`

3. Your website will now read/write data to the Mobile POS PostgreSQL database in real-time!
