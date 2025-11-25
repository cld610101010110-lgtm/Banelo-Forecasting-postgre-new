# Firebase ID Verification & Management Scripts

## Quick Start

### 1. Verify Your Database

Check if your `firebase_id` values are consistent and properly set:

```bash
cd /home/user/Banelo-Forecasting-postgre-new/Banelo-Forecasting-main/baneloforecasting
python verify_firebase_ids.py
```

**This will check:**
- ✅ All products have `firebase_id`
- ✅ No duplicate `firebase_id` values
- ✅ Proper ID format (20+ characters)
- ✅ Sales reference valid products
- ✅ Recipes reference valid products
- ✅ Recipe ingredients reference valid products

### 2. Fix Any Issues (If Found)

First, do a dry run to see what would be fixed:

```bash
python fix_firebase_ids.py
```

Then, if the fixes look correct, apply them:

```bash
python fix_firebase_ids.py --live
```

### 3. Verify Again

After fixing, verify everything is correct:

```bash
python verify_firebase_ids.py
```

## What These Scripts Do

### `verify_firebase_ids.py`
- **Safe**: Read-only, makes no changes
- **Purpose**: Identifies issues with `firebase_id` fields
- **Reports**: Missing IDs, duplicates, invalid references

### `fix_firebase_ids.py`
- **Default Mode**: Dry run (shows what would be fixed, makes no changes)
- **Live Mode**: Applies fixes to database (use `--live` flag)
- **Fixes**: Generates missing IDs, resolves duplicates, updates references

### `FIREBASE_ID_GUIDE.md`
- Complete documentation
- Explains `firebase_id` purpose and structure
- Troubleshooting guide
- Best practices
- SQL queries for manual checks

## Your Database Status (From Screenshot)

Your database appears to have proper Firebase IDs:

| Column | Format | Example |
|--------|--------|---------|
| `id` | UUID (36 chars) | `05755b4b-fc48-41f6-8e96-fc782c22a5...` |
| `firebase_id` | Firebase ID (20 chars) | `54Nmuu1uaJ3R2CzlboB4` |
| `name` | Product name | `Lemonade` |
| `category` | Category | `Pastries`, `Beverage` |

**This is the correct format!** ✅

However, it's recommended to run the verification script to ensure:
1. All 71 products have `firebase_id`
2. No duplicates exist
3. All sales and recipes properly reference these IDs

## When to Run These Scripts

Run verification:
- ✅ After data imports
- ✅ After database migrations
- ✅ Monthly maintenance
- ✅ When debugging cross-reference issues
- ✅ After mobile app syncs

Run fixes:
- ⚠️ Only when verification reports issues
- ⚠️ Always test with dry run first
- ⚠️ Backup database before running `--live`

## Expected Output

### ✅ Healthy Database
```
🔍 VERIFYING PRODUCT FIREBASE IDs
══════════════════════════════════════════════════════════════════
📊 Total Products: 71

✅ Products WITHOUT firebase_id: 0
✅ Duplicate firebase_id values: 0

📋 Firebase ID Format Check:
   ✅ Valid format: 71

══════════════════════════════════════════════════════════════════
📊 VERIFICATION SUMMARY
══════════════════════════════════════════════════════════════════
   Products: ✅ PASSED
   Recipes: ✅ PASSED
   Sales: ✅ PASSED
   Recipe Ingredients: ✅ PASSED

══════════════════════════════════════════════════════════════════
✅ ALL CHECKS PASSED! Firebase IDs are consistent.
══════════════════════════════════════════════════════════════════
```

### ⚠️ Issues Found
```
🔍 VERIFYING PRODUCT FIREBASE IDs
══════════════════════════════════════════════════════════════════
📊 Total Products: 71

⚠️ Products WITHOUT firebase_id: 5
   Products missing firebase_id:
      - Espresso (id: abc123...)
      - Cappuccino (id: def456...)
      ...

❌ Duplicate firebase_id values: 2
   Duplicate firebase_ids found:
      - firebase_id 'XYZ123ABC' used by 2 products:
         • Latte (id: ghi789...)
         • Latte Copy (id: jkl012...)

══════════════════════════════════════════════════════════════════
⚠️ SOME CHECKS FAILED! Please review the issues above.
══════════════════════════════════════════════════════════════════
```

## Files Created

1. **verify_firebase_ids.py** - Verification script (safe, read-only)
2. **fix_firebase_ids.py** - Fix script (with dry-run mode)
3. **FIREBASE_ID_GUIDE.md** - Complete documentation
4. **FIREBASE_ID_README.md** - This quick reference

## Next Steps

1. **Start your PostgreSQL database** (if not running):
   ```bash
   # Check database status
   systemctl status postgresql

   # Or check with pg_isready
   pg_isready -h localhost -p 5432
   ```

2. **Run verification**:
   ```bash
   python verify_firebase_ids.py
   ```

3. **If issues found, review and fix**:
   ```bash
   # Dry run first
   python fix_firebase_ids.py

   # If fixes look good, apply them
   python fix_firebase_ids.py --live
   ```

4. **Verify again to confirm**:
   ```bash
   python verify_firebase_ids.py
   ```

## Support

For detailed information, see: `FIREBASE_ID_GUIDE.md`

For questions about:
- Database schema → See `FIREBASE_ID_GUIDE.md` section "Database Schema"
- Common issues → See `FIREBASE_ID_GUIDE.md` section "Common Issues"
- SQL queries → See `FIREBASE_ID_GUIDE.md` section "Manual Verification via SQL"
- Best practices → See `FIREBASE_ID_GUIDE.md` section "Best Practices"
