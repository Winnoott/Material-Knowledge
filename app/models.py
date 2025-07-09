from app import db
from datetime import datetime

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    material_type = db.Column(db.String(100))  # e.g., "Additive Active Material"
    usage_on = db.Column(db.String(100))  # e.g., "Negative Plate"
    monthly_usage = db.Column(db.String(100))  # Monthly consumption characteristics
    battery_types = db.Column(db.String(255))  # e.g., "AMB, MCB"
    function_description = db.Column(db.Text)  # Material function description
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    suppliers = db.relationship('MaterialSupplier', backref='material', lazy=True, cascade='all, delete-orphan')
    tests = db.relationship('MaterialTest', backref='material', lazy=True, cascade='all, delete-orphan')

class MaterialSupplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    supplier_name = db.Column(db.String(255), nullable=False)
    origin = db.Column(db.String(255))
    price_per_kg = db.Column(db.Numeric(10, 2))
    currency = db.Column(db.String(10), default='Rp')
    monthly_allocation = db.Column(db.Integer)  # in kg
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MaterialTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    test_type = db.Column(db.String(100), nullable=False)  # e.g., "Porosity Test", "XRD Test"
    test_date = db.Column(db.Date)
    test_value = db.Column(db.Float)
    test_unit = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
