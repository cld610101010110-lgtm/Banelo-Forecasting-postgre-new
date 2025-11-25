#!/usr/bin/env python3
"""
Fix Firebase ID issues in PostgreSQL database
This script will:
1. Generate firebase_id for products that don't have one
2. Fix duplicate firebase_id values
3. Update sales and recipes to reference correct firebase_ids
"""

import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baneloforecasting.settings')
django.setup()

from dashboard.models import Product, Recipe, RecipeIngredient, Sale
from django.db.models import Q, Count
from django.db import transaction


def generate_firebase_id():
    """Generate a Firebase-like ID (20 characters)"""
    # Firebase uses base64-like characters
    import random
    import string
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=20))


def fix_product_firebase_ids(dry_run=True):
    """Fix missing or duplicate firebase_id in products"""
    print("\n" + "=" * 70)
    print("🔧 FIXING PRODUCT FIREBASE IDs")
    print("=" * 70)

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")
    else:
        print("⚠️  LIVE MODE - Changes will be saved to database\n")

    # Fix missing firebase_id
    missing_firebase_id = Product.objects.filter(
        Q(firebase_id__isnull=True) | Q(firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n📦 Products without firebase_id: {missing_count}")

    if missing_count > 0:
        print("   Generating firebase_id for:")
        for product in missing_firebase_id:
            new_firebase_id = generate_firebase_id()
            print(f"      • {product.name} → {new_firebase_id}")

            if not dry_run:
                product.firebase_id = new_firebase_id
                product.save()

    # Fix duplicate firebase_id
    duplicates = (Product.objects
                  .exclude(Q(firebase_id__isnull=True) | Q(firebase_id=''))
                  .values('firebase_id')
                  .annotate(count=Count('firebase_id'))
                  .filter(count__gt=1))

    duplicate_count = duplicates.count()

    print(f"\n📦 Duplicate firebase_id values: {duplicate_count}")

    if duplicate_count > 0:
        print("   Fixing duplicates:")
        for dup in duplicates:
            firebase_id = dup['firebase_id']
            products = Product.objects.filter(firebase_id=firebase_id).order_by('id')
            print(f"\n   firebase_id '{firebase_id}' is duplicated:")

            # Keep the first one, regenerate for others
            for i, product in enumerate(products):
                if i == 0:
                    print(f"      ✅ KEEP: {product.name} (id: {product.id})")
                else:
                    new_firebase_id = generate_firebase_id()
                    print(f"      🔄 FIX:  {product.name} (id: {product.id}) → {new_firebase_id}")

                    if not dry_run:
                        # Update product
                        old_firebase_id = product.firebase_id
                        product.firebase_id = new_firebase_id
                        product.save()

                        # Update related records
                        Recipe.objects.filter(product_firebase_id=old_firebase_id).update(
                            product_firebase_id=new_firebase_id
                        )
                        Sale.objects.filter(product_firebase_id=old_firebase_id).update(
                            product_firebase_id=new_firebase_id
                        )
                        RecipeIngredient.objects.filter(ingredient_firebase_id=old_firebase_id).update(
                            ingredient_firebase_id=new_firebase_id
                        )

    return missing_count + duplicate_count


def fix_recipe_firebase_ids(dry_run=True):
    """Fix recipe firebase_ids and product references"""
    print("\n" + "=" * 70)
    print("🍳 FIXING RECIPE FIREBASE IDs")
    print("=" * 70)

    # Fix missing firebase_id
    missing_firebase_id = Recipe.objects.filter(
        Q(firebase_id__isnull=True) | Q(firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n📋 Recipes without firebase_id: {missing_count}")

    if missing_count > 0:
        for recipe in missing_firebase_id:
            new_firebase_id = generate_firebase_id()
            print(f"   • {recipe.product_name} → {new_firebase_id}")

            if not dry_run:
                recipe.firebase_id = new_firebase_id
                recipe.save()

    # Fix orphaned recipes (product_firebase_id doesn't exist)
    all_recipes = Recipe.objects.all()
    orphaned_recipes = []

    for recipe in all_recipes:
        if recipe.product_firebase_id:
            if not Product.objects.filter(firebase_id=recipe.product_firebase_id).exists():
                orphaned_recipes.append(recipe)

    print(f"\n📋 Recipes with invalid product_firebase_id: {len(orphaned_recipes)}")

    if orphaned_recipes:
        print("   Attempting to fix by matching product name:")
        for recipe in orphaned_recipes:
            # Try to find product by name
            try:
                product = Product.objects.get(name__iexact=recipe.product_name)
                print(f"   ✅ {recipe.product_name} → {product.firebase_id}")

                if not dry_run:
                    recipe.product_firebase_id = product.firebase_id
                    recipe.save()
            except Product.DoesNotExist:
                print(f"   ⚠️  {recipe.product_name} → Product not found")
            except Product.MultipleObjectsReturned:
                print(f"   ⚠️  {recipe.product_name} → Multiple products found")

    return missing_count + len(orphaned_recipes)


def fix_sales_firebase_ids(dry_run=True):
    """Fix sales product_firebase_id references"""
    print("\n" + "=" * 70)
    print("💰 FIXING SALES FIREBASE IDs")
    print("=" * 70)

    # Fix missing product_firebase_id
    missing_firebase_id = Sale.objects.filter(
        Q(product_firebase_id__isnull=True) | Q(product_firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n📊 Sales without product_firebase_id: {missing_count}")

    if missing_count > 0 and missing_count <= 1000:
        print("   Attempting to fix by matching product name:")
        fixed_count = 0
        not_found_count = 0

        for sale in missing_firebase_id:
            try:
                product = Product.objects.get(name__iexact=sale.product_name)
                if not dry_run:
                    sale.product_firebase_id = product.firebase_id
                    sale.save()
                fixed_count += 1
            except Product.DoesNotExist:
                not_found_count += 1
            except Product.MultipleObjectsReturned:
                not_found_count += 1

        print(f"   ✅ Can fix: {fixed_count}")
        print(f"   ⚠️  Cannot fix: {not_found_count}")
    elif missing_count > 1000:
        print(f"   ⚠️  Too many records ({missing_count}). Consider using bulk update.")

    # Fix orphaned sales
    sales_with_firebase_id = Sale.objects.exclude(
        Q(product_firebase_id__isnull=True) | Q(product_firebase_id='')
    )

    orphaned_count = 0
    orphaned_ids = set()

    print("\n📊 Checking for sales with invalid product_firebase_id...")

    # Sample check (check first 1000 or all if less)
    sample_size = min(1000, sales_with_firebase_id.count())
    print(f"   Checking {sample_size} sales records...")

    for sale in sales_with_firebase_id[:sample_size]:
        if sale.product_firebase_id not in orphaned_ids:
            if not Product.objects.filter(firebase_id=sale.product_firebase_id).exists():
                orphaned_ids.add(sale.product_firebase_id)
                orphaned_count += 1

    print(f"\n📊 Found {len(orphaned_ids)} unique invalid product_firebase_id values")

    if len(orphaned_ids) > 0:
        print("\n   Sample invalid IDs:")
        for invalid_id in list(orphaned_ids)[:10]:
            sales_with_invalid = Sale.objects.filter(product_firebase_id=invalid_id)
            count = sales_with_invalid.count()
            sample_sale = sales_with_invalid.first()
            print(f"      • '{invalid_id}' ({count} sales) - e.g., {sample_sale.product_name}")

    return missing_count


def main():
    """Main fix function"""
    import sys

    print("\n" + "=" * 70)
    print("🔧 FIREBASE ID FIX UTILITY")
    print("=" * 70)

    # Check if user wants to run in live mode
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == '--live':
        dry_run = False
        print("\n⚠️  WARNING: Running in LIVE mode!")
        print("⚠️  This will make changes to your database!")
        response = input("\n   Type 'yes' to continue: ")
        if response.lower() != 'yes':
            print("\n❌ Aborted by user")
            return
    else:
        print("\n🔍 Running in DRY RUN mode (no changes will be made)")
        print("   To make actual changes, run: python fix_firebase_ids.py --live\n")

    try:
        with transaction.atomic():
            # Fix products first
            product_issues = fix_product_firebase_ids(dry_run)

            # Fix recipes
            recipe_issues = fix_recipe_firebase_ids(dry_run)

            # Fix sales
            sales_issues = fix_sales_firebase_ids(dry_run)

            # Summary
            print("\n" + "=" * 70)
            print("📊 FIX SUMMARY")
            print("=" * 70)
            print(f"   Products fixed:  {product_issues}")
            print(f"   Recipes fixed:   {recipe_issues}")
            print(f"   Sales fixed:     {sales_issues}")
            print("=" * 70)

            if dry_run:
                print("\n🔍 DRY RUN complete - no changes were made")
                print("   To apply these fixes, run: python fix_firebase_ids.py --live\n")
                # Rollback transaction in dry run mode
                transaction.set_rollback(True)
            else:
                print("\n✅ Fixes applied successfully!\n")

    except Exception as e:
        print(f"\n❌ FIX FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
