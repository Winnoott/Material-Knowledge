#!/usr/bin/env python3
"""
Database migration script to update from old schema to new schema
"""
import sqlite3
from datetime import datetime

def migrate_database():
    """Migrate the existing database to new schema"""
    db_path = 'instance/material_knowledge.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting database migration...")
        
        # Create new tables
        print("Creating MaterialSupplier table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS material_supplier (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            supplier_name VARCHAR(255) NOT NULL,
            origin VARCHAR(255),
            price_per_kg DECIMAL(10, 2),
            currency VARCHAR(10) DEFAULT 'Rp',
            monthly_allocation INTEGER,
            is_primary BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES material (id)
        )
        ''')
        
        print("Creating MaterialTest table...")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS material_test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER NOT NULL,
            test_type VARCHAR(100) NOT NULL,
            test_date DATE,
            test_value REAL,
            test_unit VARCHAR(50),
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (material_id) REFERENCES material (id)
        )
        ''')
        
        # Check if old material table exists and migrate data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='material'")
        if cursor.fetchone():
            print("Updating material table structure...")
            
            # Get current table structure
            cursor.execute("PRAGMA table_info(material)")
            columns = [row[1] for row in cursor.fetchall()]
            
            # Add new columns to material table if they don't exist
            new_columns = [
                ('material_type', 'VARCHAR(100)'),
                ('usage_on', 'VARCHAR(100)'),
                ('monthly_usage', 'VARCHAR(100)'),
                ('battery_types', 'VARCHAR(255)'),
                ('function_description', 'TEXT'),
                ('created_at', 'DATETIME DEFAULT CURRENT_TIMESTAMP')
            ]
            
            for col_name, col_type in new_columns:
                if col_name not in columns:
                    try:
                        cursor.execute(f'ALTER TABLE material ADD COLUMN {col_name} {col_type}')
                        print(f"Added column: {col_name}")
                    except sqlite3.OperationalError as e:
                        print(f"Column {col_name} might already exist: {e}")
            
            # Update created_at for existing records if it's NULL
            cursor.execute("UPDATE material SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
            
            # Migrate supplier data from material table to material_supplier table
            cursor.execute('SELECT id, supplier, price_per_kg, origin FROM material WHERE supplier IS NOT NULL AND supplier != ""')
            materials = cursor.fetchall()
            
            for material_id, supplier, price, origin in materials:
                if supplier:
                    # Check if supplier already migrated
                    cursor.execute('SELECT COUNT(*) FROM material_supplier WHERE material_id = ?', (material_id,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute('''
                        INSERT INTO material_supplier (material_id, supplier_name, price_per_kg, origin, is_primary)
                        VALUES (?, ?, ?, ?, 1)
                        ''', (material_id, supplier, price, origin))
                        print(f"Migrated supplier data for material {material_id}")
            
            # Update battery_types from old battery_type column
            cursor.execute('SELECT id, battery_type FROM material WHERE battery_type IS NOT NULL AND battery_type != ""')
            battery_data = cursor.fetchall()
            
            for material_id, battery_type in battery_data:
                if battery_type:
                    cursor.execute('UPDATE material SET battery_types = ? WHERE id = ? AND (battery_types IS NULL OR battery_types = "")', (battery_type, material_id))
        
        else:
            print("Creating new material table...")
            cursor.execute('''
            CREATE TABLE material (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                material_type VARCHAR(100),
                usage_on VARCHAR(100),
                monthly_usage VARCHAR(100),
                battery_types VARCHAR(255),
                function_description TEXT,
                image_url VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                supplier VARCHAR(255),
                price_per_kg DECIMAL(10, 2),
                origin VARCHAR(255),
                brand VARCHAR(255),
                allocation VARCHAR(255),
                battery_type VARCHAR(255)
            )
            ''')
        
        conn.commit()
        print("Migration completed successfully!")
        
        # Show table structure
        print("\nMaterial table structure:")
        cursor.execute("PRAGMA table_info(material)")
        for row in cursor.fetchall():
            print(f"  {row[1]} ({row[2]})")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
