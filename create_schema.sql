-- Banelo Coffee POS Database Schema
-- This script creates all necessary tables for the inventory management system

-- =================================================
-- PRODUCTS TABLE (Main inventory items)
-- =================================================
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    firebase_id TEXT UNIQUE,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price FLOAT DEFAULT 0,
    inventory_a FLOAT DEFAULT 0,  -- Main warehouse stock
    inventory_b FLOAT DEFAULT 0,  -- Expendable/display stock
    cost_per_unit FLOAT DEFAULT 0,
    unit VARCHAR(50) DEFAULT 'pcs',
    image_uri TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_products_firebase ON products(firebase_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- =================================================
-- RECIPES TABLE (Links products to their recipes)
-- =================================================
CREATE TABLE IF NOT EXISTS recipes (
    id TEXT PRIMARY KEY,
    firebase_id TEXT UNIQUE,
    product_firebase_id TEXT,  -- References products.firebase_id
    product_name VARCHAR(255),
    product_number INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_recipes_product ON recipes(product_firebase_id);

-- =================================================
-- RECIPE INGREDIENTS TABLE (Ingredients needed for each recipe)
-- =================================================
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id TEXT PRIMARY KEY,
    firebase_id TEXT,
    recipe_id TEXT,  -- References recipes.id
    recipe_firebase_id TEXT,  -- References recipes.firebase_id
    ingredient_firebase_id TEXT,  -- References products.firebase_id
    ingredient_name VARCHAR(255),
    quantity_needed FLOAT,  -- Amount needed per serving
    unit VARCHAR(50) DEFAULT 'g',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_firebase_id);

-- =================================================
-- SALES TABLE (Transaction history)
-- =================================================
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_firebase_id VARCHAR(255),
    product_name VARCHAR(255),
    quantity FLOAT,
    unit_price FLOAT,
    total_price FLOAT,
    order_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_sales_product ON sales(product_firebase_id);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date);

-- =================================================
-- WASTE LOGS TABLE (Track spoilage and waste)
-- =================================================
CREATE TABLE IF NOT EXISTS waste_logs (
    id SERIAL PRIMARY KEY,
    product_firebase_id VARCHAR(255),
    product_name VARCHAR(255),
    quantity FLOAT,
    reason VARCHAR(255),
    category VARCHAR(100),
    waste_date TIMESTAMP,
    recorded_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =================================================
-- AUDIT TRAIL TABLE (Track user actions)
-- =================================================
CREATE TABLE IF NOT EXISTS audit_trail (
    id SERIAL PRIMARY KEY,
    action VARCHAR(255),
    details TEXT,
    user_id VARCHAR(255),
    user_name VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_trail(timestamp);

-- =================================================
-- ML PREDICTIONS TABLE (Forecasting data)
-- =================================================
CREATE TABLE IF NOT EXISTS ml_predictions (
    id SERIAL PRIMARY KEY,
    product_firebase_id VARCHAR(255),
    product_name VARCHAR(255),
    predicted_daily_usage FLOAT,
    avg_daily_usage FLOAT,
    trend FLOAT,
    confidence_score FLOAT,
    data_points INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =================================================
-- ML MODELS TABLE (Model training history)
-- =================================================
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    is_trained BOOLEAN DEFAULT FALSE,
    last_trained TIMESTAMP,
    total_records INTEGER,
    products_analyzed INTEGER,
    predictions_generated INTEGER,
    accuracy INTEGER,
    model_type VARCHAR(200),
    training_period_days INTEGER
);

-- =================================================
-- Insert some sample data for testing
-- =================================================

-- Sample Ingredients
INSERT INTO products (id, firebase_id, name, category, price, inventory_a, inventory_b, cost_per_unit, unit) VALUES
('ing001', 'ing001', 'Espresso Beans', 'Ingredients', 0, 5000, 500, 0.5, 'g'),
('ing002', 'ing002', 'Milk', 'Ingredients', 0, 10000, 1000, 0.1, 'ml'),
('ing003', 'ing003', 'Sugar', 'Ingredients', 0, 3000, 300, 0.05, 'g'),
('ing004', 'ing004', 'Chocolate Syrup', 'Ingredients', 0, 2000, 200, 0.2, 'ml'),
('ing005', 'ing005', 'Vanilla Extract', 'Ingredients', 0, 1000, 100, 0.3, 'ml'),
('ing006', 'ing006', 'Whipped Cream', 'Ingredients', 0, 1500, 150, 0.25, 'g'),
('ing007', 'ing007', 'Croissant Dough', 'Ingredients', 0, 2000, 200, 1.0, 'g'),
('ing008', 'ing008', 'Almonds', 'Ingredients', 0, 1000, 100, 0.8, 'g'),
('ing009', 'ing009', 'Flour', 'Ingredients', 0, 5000, 500, 0.03, 'g'),
('ing010', 'ing010', 'Butter', 'Ingredients', 0, 3000, 300, 0.4, 'g')
ON CONFLICT (id) DO NOTHING;

-- Sample Beverages
INSERT INTO products (id, firebase_id, name, category, price, inventory_a, inventory_b, cost_per_unit, unit) VALUES
('bev001', 'bev001', 'Americano', 'Beverage', 6.27, 0, 0, 0, 'pcs'),
('bev002', 'bev002', 'Cappuccino', 'Beverage', 5.39, 0, 0, 0, 'pcs'),
('bev003', 'bev003', 'Chai Latte', 'Beverage', 5.43, 0, 0, 0, 'pcs'),
('bev004', 'bev004', 'Chocolate', 'Beverage', 2.89, 0, 0, 0, 'pcs')
ON CONFLICT (id) DO NOTHING;

-- Sample Pastries
INSERT INTO products (id, firebase_id, name, category, price, inventory_a, inventory_b, cost_per_unit, unit) VALUES
('pas001', 'pas001', 'Almond Croissant', 'Pastries', 8.42, 0, 0, 0, 'pcs'),
('pas002', 'pas002', 'Blueberry Muffin', 'Pastries', 7.86, 0, 0, 0, 'pcs'),
('pas003', 'pas003', 'Brownie', 'Pastries', 3.93, 0, 0, 0, 'pcs'),
('pas004', 'pas004', 'Cheesecake', 'Pastries', 2.79, 0, 0, 0, 'pcs')
ON CONFLICT (id) DO NOTHING;

-- Sample Recipes for Beverages
-- Americano Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec001', 'rec001', 'bev001', 'Americano')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem001', 'rec001', 'rec001', 'ing001', 'Espresso Beans', 18, 'g')
ON CONFLICT (id) DO NOTHING;

-- Cappuccino Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec002', 'rec002', 'bev002', 'Cappuccino')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem002', 'rec002', 'rec002', 'ing001', 'Espresso Beans', 18, 'g'),
('recitem003', 'rec002', 'rec002', 'ing002', 'Milk', 120, 'ml')
ON CONFLICT (id) DO NOTHING;

-- Chai Latte Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec003', 'rec003', 'bev003', 'Chai Latte')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem004', 'rec003', 'rec003', 'ing002', 'Milk', 200, 'ml'),
('recitem005', 'rec003', 'rec003', 'ing003', 'Sugar', 10, 'g')
ON CONFLICT (id) DO NOTHING;

-- Chocolate Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec004', 'rec004', 'bev004', 'Chocolate')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem006', 'rec004', 'rec004', 'ing002', 'Milk', 150, 'ml'),
('recitem007', 'rec004', 'rec004', 'ing004', 'Chocolate Syrup', 30, 'ml'),
('recitem008', 'rec004', 'rec004', 'ing006', 'Whipped Cream', 20, 'g')
ON CONFLICT (id) DO NOTHING;

-- Sample Recipes for Pastries
-- Almond Croissant Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec005', 'rec005', 'pas001', 'Almond Croissant')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem009', 'rec005', 'rec005', 'ing007', 'Croissant Dough', 80, 'g'),
('recitem010', 'rec005', 'rec005', 'ing008', 'Almonds', 15, 'g'),
('recitem011', 'rec005', 'rec005', 'ing010', 'Butter', 10, 'g')
ON CONFLICT (id) DO NOTHING;

-- Blueberry Muffin Recipe
INSERT INTO recipes (id, firebase_id, product_firebase_id, product_name) VALUES
('rec006', 'rec006', 'pas002', 'Blueberry Muffin')
ON CONFLICT (id) DO NOTHING;

INSERT INTO recipe_ingredients (id, recipe_id, recipe_firebase_id, ingredient_firebase_id, ingredient_name, quantity_needed, unit) VALUES
('recitem012', 'rec006', 'rec006', 'ing009', 'Flour', 50, 'g'),
('recitem013', 'rec006', 'rec006', 'ing003', 'Sugar', 20, 'g'),
('recitem014', 'rec006', 'rec006', 'ing010', 'Butter', 15, 'g')
ON CONFLICT (id) DO NOTHING;

-- Print success message
SELECT 'Database schema created successfully!' AS status;
SELECT 'Sample data inserted!' AS status;
SELECT COUNT(*) AS total_products FROM products;
SELECT COUNT(*) AS total_recipes FROM recipes;
SELECT COUNT(*) AS total_recipe_ingredients FROM recipe_ingredients;
