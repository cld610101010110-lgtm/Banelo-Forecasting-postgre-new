#!/usr/bin/env python3
"""
Verify Firebase ID consistency in PostgreSQL database
This script checks that firebase_id values are properly set and unique
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'baneloforecasting.settings')
django.setup()

from dashboard.models import Product, Recipe, RecipeIngredient, Sale
from django.db.models import Q, Count
from collections import defaultdict


def verify_product_firebase_ids():
    """Verify Product firebase_id consistency"""
    print("\n" + "=" * 70)
    print("🔍 VERIFYING PRODUCT FIREBASE IDs")
    print("=" * 70)

    all_products = Product.objects.all()
    total_count = all_products.count()

    print(f"\n📊 Total Products: {total_count}")

    # Check for missing firebase_id
    missing_firebase_id = all_products.filter(
        Q(firebase_id__isnull=True) | Q(firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n{'✅' if missing_count == 0 else '⚠️'} Products WITHOUT firebase_id: {missing_count}")
    if missing_count > 0:
        print("   Products missing firebase_id:")
        for product in missing_firebase_id[:10]:
            print(f"      - {product.name} (id: {product.id})")
        if missing_count > 10:
            print(f"      ... and {missing_count - 10} more")

    # Check for duplicate firebase_id
    products_with_firebase_id = all_products.exclude(
        Q(firebase_id__isnull=True) | Q(firebase_id='')
    )

    duplicates = (products_with_firebase_id
                  .values('firebase_id')
                  .annotate(count=Count('firebase_id'))
                  .filter(count__gt=1))

    duplicate_count = duplicates.count()

    print(f"\n{'✅' if duplicate_count == 0 else '❌'} Duplicate firebase_id values: {duplicate_count}")
    if duplicate_count > 0:
        print("   Duplicate firebase_ids found:")
        for dup in duplicates:
            firebase_id = dup['firebase_id']
            products = Product.objects.filter(firebase_id=firebase_id)
            print(f"      - firebase_id '{firebase_id}' used by {dup['count']} products:")
            for p in products:
                print(f"         • {p.name} (id: {p.id})")

    # Check firebase_id format
    print(f"\n📋 Firebase ID Format Check:")
    valid_format_count = 0
    invalid_format_products = []

    for product in products_with_firebase_id:
        firebase_id = product.firebase_id
        # Firebase IDs are typically 20-28 characters, alphanumeric
        if len(firebase_id) >= 15 and firebase_id.replace('_', '').isalnum():
            valid_format_count += 1
        else:
            invalid_format_products.append((product.name, firebase_id))

    print(f"   ✅ Valid format: {valid_format_count}")
    if invalid_format_products:
        print(f"   ⚠️  Unusual format: {len(invalid_format_products)}")
        for name, fid in invalid_format_products[:10]:
            print(f"      - {name}: '{fid}'")
        if len(invalid_format_products) > 10:
            print(f"      ... and {len(invalid_format_products) - 10} more")

    return missing_count == 0 and duplicate_count == 0


def verify_recipe_firebase_ids():
    """Verify Recipe firebase_id consistency"""
    print("\n" + "=" * 70)
    print("🍳 VERIFYING RECIPE FIREBASE IDs")
    print("=" * 70)

    all_recipes = Recipe.objects.all()
    total_count = all_recipes.count()

    print(f"\n📊 Total Recipes: {total_count}")

    # Check for missing firebase_id
    missing_firebase_id = all_recipes.filter(
        Q(firebase_id__isnull=True) | Q(firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n{'✅' if missing_count == 0 else '⚠️'} Recipes WITHOUT firebase_id: {missing_count}")
    if missing_count > 0:
        for recipe in missing_firebase_id[:5]:
            print(f"      - {recipe.product_name} (id: {recipe.id})")

    # Check if product_firebase_id matches actual products
    orphaned_recipes = []
    for recipe in all_recipes:
        if recipe.product_firebase_id:
            try:
                Product.objects.get(firebase_id=recipe.product_firebase_id)
            except Product.DoesNotExist:
                orphaned_recipes.append(recipe)

    print(f"\n{'✅' if len(orphaned_recipes) == 0 else '⚠️'} Recipes with invalid product_firebase_id: {len(orphaned_recipes)}")
    if orphaned_recipes:
        for recipe in orphaned_recipes[:5]:
            print(f"      - {recipe.product_name} → '{recipe.product_firebase_id}'")

    return missing_count == 0 and len(orphaned_recipes) == 0


def verify_sales_firebase_ids():
    """Verify Sales product_firebase_id consistency"""
    print("\n" + "=" * 70)
    print("💰 VERIFYING SALES FIREBASE IDs")
    print("=" * 70)

    all_sales = Sale.objects.all()
    total_count = all_sales.count()

    print(f"\n📊 Total Sales: {total_count}")

    # Check for missing product_firebase_id
    missing_firebase_id = all_sales.filter(
        Q(product_firebase_id__isnull=True) | Q(product_firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n{'✅' if missing_count == 0 else '⚠️'} Sales WITHOUT product_firebase_id: {missing_count}")
    if missing_count > 0:
        percentage = (missing_count / total_count * 100) if total_count > 0 else 0
        print(f"   ⚠️  {percentage:.1f}% of sales are missing product_firebase_id")
        print(f"   Sample sales missing firebase_id:")
        for sale in missing_firebase_id[:5]:
            print(f"      - {sale.product_name} on {sale.order_date}")

    # Check if product_firebase_id matches actual products
    sales_with_firebase_id = all_sales.exclude(
        Q(product_firebase_id__isnull=True) | Q(product_firebase_id='')
    )

    orphaned_count = 0
    product_cache = {}

    for sale in sales_with_firebase_id:
        firebase_id = sale.product_firebase_id
        if firebase_id not in product_cache:
            try:
                Product.objects.get(firebase_id=firebase_id)
                product_cache[firebase_id] = True
            except Product.DoesNotExist:
                product_cache[firebase_id] = False
                orphaned_count += 1

    print(f"\n{'✅' if orphaned_count == 0 else '⚠️'} Sales with invalid product_firebase_id: {orphaned_count}")
    if orphaned_count > 0:
        percentage = (orphaned_count / total_count * 100) if total_count > 0 else 0
        print(f"   ⚠️  {percentage:.1f}% of sales reference non-existent products")

    return missing_count == 0 and orphaned_count == 0


def verify_recipe_ingredients():
    """Verify RecipeIngredient firebase_id consistency"""
    print("\n" + "=" * 70)
    print("🥤 VERIFYING RECIPE INGREDIENT FIREBASE IDs")
    print("=" * 70)

    all_ingredients = RecipeIngredient.objects.all()
    total_count = all_ingredients.count()

    print(f"\n📊 Total Recipe Ingredients: {total_count}")

    # Check for missing ingredient_firebase_id
    missing_firebase_id = all_ingredients.filter(
        Q(ingredient_firebase_id__isnull=True) | Q(ingredient_firebase_id='')
    )
    missing_count = missing_firebase_id.count()

    print(f"\n{'✅' if missing_count == 0 else '⚠️'} Ingredients WITHOUT firebase_id: {missing_count}")

    # Check if ingredient_firebase_id matches actual products
    ingredients_with_firebase_id = all_ingredients.exclude(
        Q(ingredient_firebase_id__isnull=True) | Q(ingredient_firebase_id='')
    )

    orphaned_count = 0
    for ingredient in ingredients_with_firebase_id:
        try:
            Product.objects.get(firebase_id=ingredient.ingredient_firebase_id)
        except Product.DoesNotExist:
            orphaned_count += 1

    print(f"\n{'✅' if orphaned_count == 0 else '⚠️'} Ingredients with invalid firebase_id: {orphaned_count}")

    return missing_count == 0 and orphaned_count == 0


def print_summary(results):
    """Print final summary"""
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)

    all_passed = all(results.values())

    for entity, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {entity}: {status}")

    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL CHECKS PASSED! Firebase IDs are consistent.")
    else:
        print("⚠️  SOME CHECKS FAILED! Please review the issues above.")
    print("=" * 70 + "\n")


def main():
    """Main verification function"""
    print("\n" + "=" * 70)
    print("🔍 FIREBASE ID CONSISTENCY VERIFICATION")
    print("=" * 70)
    print("\nThis script verifies that firebase_id values are:")
    print("  1. Present in all records")
    print("  2. Unique (no duplicates)")
    print("  3. Properly formatted")
    print("  4. Reference valid products\n")

    results = {
        'Products': verify_product_firebase_ids(),
        'Recipes': verify_recipe_firebase_ids(),
        'Sales': verify_sales_firebase_ids(),
        'Recipe Ingredients': verify_recipe_ingredients(),
    }

    print_summary(results)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
