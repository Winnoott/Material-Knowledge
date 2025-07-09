#!/usr/bin/env python3
"""
Clear database and add fresh sample data
"""
from app import app, db
from app.models import Material, MaterialSupplier, MaterialTest

def clear_and_add_data():
    """Clear existing data and add fresh sample data"""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        MaterialTest.query.delete()
        MaterialSupplier.query.delete()
        Material.query.delete()
        db.session.commit()
        
        print("Adding fresh sample data...")
        
        # Import the add_sample_data function
        import add_sample_data
        add_sample_data.add_sample_data()

if __name__ == '__main__':
    clear_and_add_data()
