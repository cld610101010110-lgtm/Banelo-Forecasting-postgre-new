const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Database connection
const { Pool } = require('pg');
const pool = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 5432,
  database: process.env.DB_NAME || 'banelo_db',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD,
});

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('❌ Database connection error:', err);
  } else {
    console.log('✅ Connected to PostgreSQL database');
  }
});

// ============================================
// HEALTH CHECK
// ============================================
app.get('/api/health', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({
      success: true,
      status: 'healthy',
      database: 'connected',
      timestamp: result.rows[0].now
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      status: 'unhealthy',
      error: error.message
    });
  }
});

// ============================================
// PRODUCTS ENDPOINTS
// ============================================

// Get all products
app.get('/api/products', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        id,
        firebase_id,
        name,
        category,
        price,
        quantity,
        inventory_a,
        inventory_b,
        cost_per_unit,
        unit,
        image_uri,
        created_at,
        updated_at
      FROM products
      ORDER BY name
    `);

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching products:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// Get single product
app.get('/api/products/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'SELECT * FROM products WHERE id = $1 OR firebase_id = $1',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }

    res.json({
      success: true,
      data: result.rows[0]
    });
  } catch (error) {
    console.error('Error fetching product:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Add new product
app.post('/api/products', async (req, res) => {
  try {
    const {
      firebase_id,
      name,
      category,
      price,
      quantity,
      inventory_a,
      inventory_b,
      cost_per_unit,
      unit,
      image_uri
    } = req.body;

    const result = await pool.query(`
      INSERT INTO products (
        firebase_id, name, category, price, quantity,
        inventory_a, inventory_b, cost_per_unit, unit, image_uri
      )
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
      RETURNING *
    `, [
      firebase_id, name, category, price, quantity || 0,
      inventory_a || 0, inventory_b || 0, cost_per_unit || 0,
      unit || 'pcs', image_uri
    ]);

    res.status(201).json({
      success: true,
      data: result.rows[0]
    });
  } catch (error) {
    console.error('Error adding product:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Update product
app.put('/api/products/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;

    const fields = [];
    const values = [];
    let paramCount = 1;

    Object.keys(updates).forEach(key => {
      if (key !== 'id') {
        fields.push(`${key} = $${paramCount}`);
        values.push(updates[key]);
        paramCount++;
      }
    });

    if (fields.length === 0) {
      return res.status(400).json({
        success: false,
        error: 'No fields to update'
      });
    }

    values.push(id);
    const query = `
      UPDATE products
      SET ${fields.join(', ')}, updated_at = NOW()
      WHERE id = $${paramCount} OR firebase_id = $${paramCount}
      RETURNING *
    `;

    const result = await pool.query(query, values);

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }

    res.json({
      success: true,
      data: result.rows[0]
    });
  } catch (error) {
    console.error('Error updating product:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Delete product
app.delete('/api/products/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'DELETE FROM products WHERE id = $1 OR firebase_id = $1 RETURNING *',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Product not found'
      });
    }

    res.json({
      success: true,
      message: 'Product deleted successfully'
    });
  } catch (error) {
    console.error('Error deleting product:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// ============================================
// RECIPES ENDPOINTS
// ============================================

// Get all recipes with ingredients
app.get('/api/recipes', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT
        r.id,
        r.firebase_id,
        r.product_firebase_id,
        r.product_name,
        r.created_at,
        r.updated_at
      FROM recipes r
      ORDER BY r.product_name
    `);

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching recipes:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// Get single recipe with ingredients
app.get('/api/recipes/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const recipeResult = await pool.query(
      'SELECT * FROM recipes WHERE id = $1 OR firebase_id = $1',
      [id]
    );

    if (recipeResult.rows.length === 0) {
      return res.status(404).json({
        success: false,
        error: 'Recipe not found'
      });
    }

    const recipe = recipeResult.rows[0];

    // Get ingredients
    const ingredientsResult = await pool.query(
      'SELECT * FROM recipe_ingredients WHERE recipe_id = $1 OR recipe_firebase_id = $2',
      [recipe.id, recipe.firebase_id]
    );

    recipe.ingredients = ingredientsResult.rows;

    res.json({
      success: true,
      data: recipe
    });
  } catch (error) {
    console.error('Error fetching recipe:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get recipe ingredients
app.get('/api/recipes/:id/ingredients', async (req, res) => {
  try {
    const { id } = req.params;
    const result = await pool.query(
      'SELECT * FROM recipe_ingredients WHERE recipe_id = $1 OR recipe_firebase_id = $1',
      [id]
    );

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching recipe ingredients:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// ============================================
// SALES ENDPOINTS
// ============================================

// Get sales data
app.get('/api/sales', async (req, res) => {
  try {
    const { limit = 1000, date_from, date_to } = req.query;

    let query = `
      SELECT
        id,
        firebase_id,
        product_firebase_id,
        product_name,
        quantity,
        unit_price,
        total_price,
        order_date,
        created_at
      FROM sales
    `;

    const conditions = [];
    const values = [];
    let paramCount = 1;

    if (date_from) {
      conditions.push(`order_date >= $${paramCount}`);
      values.push(date_from);
      paramCount++;
    }

    if (date_to) {
      conditions.push(`order_date <= $${paramCount}`);
      values.push(date_to);
      paramCount++;
    }

    if (conditions.length > 0) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ` ORDER BY order_date DESC LIMIT $${paramCount}`;
    values.push(limit);

    const result = await pool.query(query, values);

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching sales:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// ============================================
// AUDIT LOGS ENDPOINTS
// ============================================

app.get('/api/audit-logs', async (req, res) => {
  try {
    const { limit = 1000 } = req.query;

    const result = await pool.query(`
      SELECT * FROM audit_logs
      ORDER BY timestamp DESC
      LIMIT $1
    `, [limit]);

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching audit logs:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// ============================================
// WASTE LOGS ENDPOINTS
// ============================================

app.get('/api/waste-logs', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT * FROM waste_logs
      ORDER BY waste_date DESC
    `);

    res.json({
      success: true,
      data: result.rows
    });
  } catch (error) {
    console.error('Error fetching waste logs:', error);
    res.status(500).json({
      success: false,
      error: error.message,
      data: []
    });
  }
});

// ============================================
// START SERVER
// ============================================

app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════╗
║   Banelo API Server                       ║
║   Running on http://localhost:${PORT}     ║
║   PostgreSQL Connected                    ║
╚═══════════════════════════════════════════╝
  `);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server...');
  pool.end();
  process.exit(0);
});
