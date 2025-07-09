#!/usr/bin/env python3
"""
Database recreation script to create new schema
"""
import sqlite3
from datetime import datetime
import os

def recreate_database():
    """Recreate the database with new schema"""
    db_path = 'instance/material_knowledge.db'
    backup_path = 'instance/material_knowledge_backup.db'
    
    try:
        # Backup existing database if it exists
        if os.path.exists(db_path):
            print("Backing up existing database...")
            import shutil
            shutil.copy2(db_path, backup_path)
            
            # Read existing data
            conn_old = sqlite3.connect(db_path)
            cursor_old = conn_old.cursor()
            
            # Get existing materials
            try:
                cursor_old.execute("SELECT * FROM material")
                existing_materials = cursor_old.fetchall()
                
                # Get column names
                cursor_old.execute("PRAGMA table_info(material)")
                old_columns = [row[1] for row in cursor_old.fetchall()]
                print(f"Found {len(existing_materials)} existing materials")
            except:
                existing_materials = []
                old_columns = []
                
            conn_old.close()
        else:
            existing_materials = []
            old_columns = []
        
        # Remove old database
        if os.path.exists(db_path):
            os.remove(db_path)
        
        print("Creating new database with updated schema...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create material table with new structure
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create material_supplier table
        cursor.execute('''
        CREATE TABLE material_supplier (
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
        
        # Create material_test table
        cursor.execute('''
        CREATE TABLE material_test (
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
        
        # Migrate existing data if any
        if existing_materials and old_columns:
            print("Migrating existing data...")
            for material_data in existing_materials:
                # Create mapping of old columns to new
                material_dict = dict(zip(old_columns, material_data))
                
                # Insert material with new structure
                cursor.execute('''
                INSERT INTO material (name, description, material_type, usage_on, monthly_usage, 
                                    battery_types, function_description, image_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    material_dict.get('name', ''),
                    material_dict.get('description', ''),
                    material_dict.get('material_type', ''),
                    material_dict.get('usage_on', ''),
                    material_dict.get('monthly_usage', ''),
                    material_dict.get('battery_types', material_dict.get('battery_type', '')),
                    material_dict.get('function_description', ''),
                    material_dict.get('image_url', ''),
                    datetime.now().isoformat()
                ))
                
                material_id = cursor.lastrowid
                
                # Migrate supplier data if exists
                if material_dict.get('supplier'):
                    cursor.execute('''
                    INSERT INTO material_supplier (material_id, supplier_name, price_per_kg, origin, is_primary)
                    VALUES (?, ?, ?, ?, 1)
                    ''', (
                        material_id,
                        material_dict.get('supplier', ''),
                        material_dict.get('price_per_kg', 0),
                        material_dict.get('origin', '')
                    ))
        
        conn.commit()
        print("Database recreation completed successfully!")
        
        # Show new table structure
        print("\nNew Material table structure:")
        cursor.execute("PRAGMA table_info(material)")
        for row in cursor.fetchall():
            print(f"  {row[1]} ({row[2]})")
            
        print("\nMaterialSupplier table structure:")
        cursor.execute("PRAGMA table_info(material_supplier)")
        for row in cursor.fetchall():
            print(f"  {row[1]} ({row[2]})")
            
        print("\nMaterialTest table structure:")
        cursor.execute("PRAGMA table_info(material_test)")
        for row in cursor.fetchall():
            print(f"  {row[1]} ({row[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Database recreation failed: {e}")

if __name__ == '__main__':
    recreate_database()
