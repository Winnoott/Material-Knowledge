#!/usr/bin/env python3
"""
Script to add sample material data for testing
"""
from app import app, db
from app.models import Material, MaterialSupplier, MaterialTest
from decimal import Decimal

def add_sample_data():
    """Add sample material data to the database"""
    
    with app.app_context():
        # Check if data already exists
        if Material.query.count() > 0:
            print("Sample data already exists. Skipping...")
            return
            
        print("Adding sample material data...")
        
        # Add Barium Sulfat (BaSO₄)
        barium_sulfat = Material(
            name='Barium Sulfat (BaSO₄)',
            description='High-quality barium sulfate powder used as an additive material in battery manufacturing.',
            material_type='Additive Active Material',
            usage_on='Negative Plate',
            monthly_usage='600 kg/month',
            battery_types='AMB, MCB',
            function_description='Prevents excessive lead sulfate formation. Reduces the coating effect and crystal formation.',
            image_url='barium_sulfat.jpg'
        )
        
        db.session.add(barium_sulfat)
        db.session.flush()
        
        # Add suppliers for Barium Sulfat
        supplier_a = MaterialSupplier(
            material_id=barium_sulfat.id,
            supplier_name='Supplier A',
            origin='Indonesia',
            price_per_kg=Decimal('121723'),
            currency='Rp',
            monthly_allocation=300,
            is_primary=True
        )
        
        supplier_b = MaterialSupplier(
            material_id=barium_sulfat.id,
            supplier_name='Supplier B',
            origin='Indonesia',
            price_per_kg=Decimal('120000'),
            currency='Rp',
            monthly_allocation=300,
            is_primary=False
        )
        
        db.session.add(supplier_a)
        db.session.add(supplier_b)
        
        # Add test data for Barium Sulfat
        porosity_test = MaterialTest(
            material_id=barium_sulfat.id,
            test_type='Porosity Test',
            test_value=15.2,
            test_unit='%',
            notes='Standard porosity test results within acceptable range'
        )
        
        xrd_test = MaterialTest(
            material_id=barium_sulfat.id,
            test_type='XRD Test',
            test_value=98.5,
            test_unit='% purity',
            notes='X-ray diffraction analysis showing high purity'
        )
        
        db.session.add(porosity_test)
        db.session.add(xrd_test)
        
        # Add SUSA / Fiber Flock
        susa_fiber = Material(
            name='SUSA / Fiber Flock',
            description='Specialized fiber material used as powder additive in battery manufacturing processes.',
            material_type='Additive Active Material',
            usage_on='Both Plates',
            monthly_usage='400 kg/month',
            battery_types='AMB, MCB, AGM',
            function_description='Improves paste cohesion and prevents active material shedding.',
            image_url='susa_fiber.jpg'
        )
        
        db.session.add(susa_fiber)
        db.session.flush()
        
        # Add supplier for SUSA Fiber
        susa_supplier = MaterialSupplier(
            material_id=susa_fiber.id,
            supplier_name='Fiber Solutions Ltd',
            origin='Germany',
            price_per_kg=Decimal('85000'),
            currency='Rp',
            monthly_allocation=400,
            is_primary=True
        )
        
        db.session.add(susa_supplier)
        
        # Add Carbon Powder
        carbon_powder = Material(
            name='Carbon Powder',
            description='High-grade carbon powder used as an active additive material in battery electrodes.',
            material_type='Active Additive Material',
            usage_on='Negative Plate',
            monthly_usage='800 kg/month',
            battery_types='Li-ion, AMB',
            function_description='Enhances electrical conductivity and improves charge-discharge efficiency.',
            image_url='carbon_powder.jpg'
        )
        
        db.session.add(carbon_powder)
        db.session.flush()
        
        # Add suppliers for Carbon Powder
        carbon_supplier1 = MaterialSupplier(
            material_id=carbon_powder.id,
            supplier_name='Carbon Tech Co',
            origin='China',
            price_per_kg=Decimal('95000'),
            currency='Rp',
            monthly_allocation=500,
            is_primary=True
        )
        
        carbon_supplier2 = MaterialSupplier(
            material_id=carbon_powder.id,
            supplier_name='Advanced Carbon Materials',
            origin='Japan',
            price_per_kg=Decimal('110000'),
            currency='Rp',
            monthly_allocation=300,
            is_primary=False
        )
        
        db.session.add(carbon_supplier1)
        db.session.add(carbon_supplier2)
        
        # Add Lignin
        lignin = Material(
            name='Lignin',
            description='Natural polymer material used as an active additive in battery manufacturing.',
            material_type='Active Additive Material',
            usage_on='Positive Plate',
            monthly_usage='200 kg/month',
            battery_types='AMB, AGM',
            function_description='Acts as a natural binder and improves paste consistency.',
            image_url='lignin.jpg'
        )
        
        db.session.add(lignin)
        db.session.flush()
        
        # Add supplier for Lignin
        lignin_supplier = MaterialSupplier(
            material_id=lignin.id,
            supplier_name='BioMaterials Inc',
            origin='Finland',
            price_per_kg=Decimal('75000'),
            currency='Rp',
            monthly_allocation=200,
            is_primary=True
        )
        
        db.session.add(lignin_supplier)
        
        # Add Natrium Sulfat (Na₂SO₄)
        natrium_sulfat = Material(
            name='Natrium Sulfat (Na₂SO₄)',
            description='Sodium sulfate powder used as electrolyte additive in battery systems.',
            material_type='Electrolyte Additive',
            usage_on='Electrolyte',
            monthly_usage='150 kg/month',
            battery_types='AMB, Flooded',
            function_description='Improves electrolyte conductivity and prevents sulfation.',
            image_url='natrium_sulfat.jpg'
        )
        
        db.session.add(natrium_sulfat)
        db.session.flush()
        
        # Add supplier for Natrium Sulfat
        natrium_supplier = MaterialSupplier(
            material_id=natrium_sulfat.id,
            supplier_name='Chemical Solutions Ltd',
            origin='Indonesia',
            price_per_kg=Decimal('45000'),
            currency='Rp',
            monthly_allocation=150,
            is_primary=True
        )
        
        db.session.add(natrium_supplier)
        
        # Add some test data for other materials
        carbon_test = MaterialTest(
            material_id=carbon_powder.id,
            test_type='Particle Size',
            test_value=2.5,
            test_unit='μm',
            notes='Average particle size measurement'
        )
        
        lignin_test = MaterialTest(
            material_id=lignin.id,
            test_type='Chemical Analysis',
            test_value=92.0,
            test_unit='% purity',
            notes='Chemical composition analysis'
        )
        
        db.session.add(carbon_test)
        db.session.add(lignin_test)
        
        # Commit all changes
        db.session.commit()
        print("Sample data added successfully!")
        
        # Print summary
        print(f"\nAdded {Material.query.count()} materials:")
        for material in Material.query.all():
            print(f"- {material.name} ({len(material.suppliers)} suppliers, {len(material.tests)} tests)")

if __name__ == '__main__':
    add_sample_data()
