from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import Material, MaterialSupplier, MaterialTest
from decimal import Decimal
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    materials = Material.query.all()
    return render_template('index.html', materials=materials)

@app.route('/material/<int:id>')
def material_detail(id):
    material = Material.query.get_or_404(id)
    return render_template('material_detail.html', material=material)

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        material_type = request.form.get('material_type', '')
        usage_on = request.form.get('usage_on', '')
        monthly_usage = request.form.get('monthly_usage', '')
        battery_types = request.form.get('battery_types', '')
        function_description = request.form.get('function_description', '')

        # Validate required fields
        if not name or not description:
            flash('Name and description are required!', 'error')
            return redirect(url_for('add_material'))

        # Handle file upload
        image_url = ''
        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    # Create unique filename
                    filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                    
                    # Ensure upload directory exists
                    upload_folder = app.config['UPLOAD_FOLDER']
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    # Save file
                    file_path = os.path.join(upload_folder, filename)
                    file.save(file_path)
                    image_url = filename
                else:
                    flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files only.', 'error')
                    return redirect(url_for('add_material'))

        # Create new material
        new_material = Material(
            name=name,
            description=description,
            material_type=material_type,
            usage_on=usage_on,
            monthly_usage=monthly_usage,
            battery_types=battery_types,
            function_description=function_description,
            image_url=image_url
        )

        db.session.add(new_material)
        db.session.flush()  # Get the ID

        # Add suppliers
        supplier_names = request.form.getlist('supplier_name[]')
        supplier_origins = request.form.getlist('supplier_origin[]')
        supplier_prices = request.form.getlist('supplier_price[]')
        supplier_allocations = request.form.getlist('supplier_allocation[]')
        
        for i, supplier_name in enumerate(supplier_names):
            if supplier_name.strip():
                supplier = MaterialSupplier(
                    material_id=new_material.id,
                    supplier_name=supplier_name,
                    origin=supplier_origins[i] if i < len(supplier_origins) else '',
                    price_per_kg=Decimal(supplier_prices[i]) if i < len(supplier_prices) and supplier_prices[i] else None,
                    monthly_allocation=int(supplier_allocations[i]) if i < len(supplier_allocations) and supplier_allocations[i] else None,
                    is_primary=i == 0  # First supplier is primary
                )
                db.session.add(supplier)

        db.session.commit()
        flash('Material added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_material.html')

@app.route('/add_test/<int:material_id>', methods=['POST'])
def add_test(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        
        test_type = request.form.get('test_type', '').strip()
        test_value = request.form.get('test_value', '').strip()
        test_unit = request.form.get('test_unit', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validate required fields
        if not test_type:
            flash('Test type is required!', 'error')
            return redirect(url_for('material_detail', id=material_id))
        
        # Handle test_value conversion
        test_value_float = None
        if test_value:
            try:
                test_value_float = float(test_value)
                # Validate reasonable range
                if test_value_float < 0:
                    flash('Test value cannot be negative.', 'error')
                    return redirect(url_for('material_detail', id=material_id))
            except (ValueError, TypeError):
                flash('Invalid test value. Please enter a valid number.', 'error')
                return redirect(url_for('material_detail', id=material_id))
        
        # Create new test
        new_test = MaterialTest(
            material_id=material_id,
            test_type=test_type,
            test_value=test_value_float,
            test_unit=test_unit if test_unit else None,
            notes=notes if notes else None
        )
        
        db.session.add(new_test)
        db.session.commit()
        flash('Test data added successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error adding test data: {str(e)}")
        flash('Error adding test data. Please try again.', 'error')
    
    return redirect(url_for('material_detail', id=material_id))

@app.route('/delete_material/<int:material_id>', methods=['POST'])
def delete_material(material_id):
    try:
        print(f"Delete request received for material ID: {material_id}")
        material = Material.query.get_or_404(material_id)
        print(f"Found material: {material.name}")
        
        # Delete associated image file if exists
        if material.image_url:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], material.image_url)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print(f"Deleted image file: {image_path}")
                except OSError as e:
                    print(f"Failed to delete image file: {e}")
                    pass  # Continue even if file deletion fails
        
        # Delete associated suppliers and tests (cascade should handle this)
        MaterialSupplier.query.filter_by(material_id=material_id).delete()
        MaterialTest.query.filter_by(material_id=material_id).delete()
        
        # Delete the material
        db.session.delete(material)
        db.session.commit()
        
        print(f"Successfully deleted material: {material.name}")
        
        return jsonify({
            'success': True,
            'message': 'Material deleted successfully!'
        })
        
    except Exception as e:
        print(f"Error deleting material: {str(e)}")
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting material: {str(e)}'
        }), 500

@app.route('/edit_supplier/<int:material_id>', methods=['POST'])
def edit_supplier(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        supplier_id = request.form.get('supplier_id')
        supplier = MaterialSupplier.query.get_or_404(supplier_id)
        
        # Update supplier data
        supplier.supplier_name = request.form.get('supplier_name', '').strip()
        supplier.origin = request.form.get('supplier_origin', '').strip()
        
        # Handle price
        price_str = request.form.get('supplier_price', '').strip()
        if price_str:
            try:
                supplier.price_per_kg = Decimal(price_str)
            except (ValueError, TypeError):
                flash('Invalid price value.', 'error')
                return redirect(url_for('material_detail', id=material_id))
        else:
            supplier.price_per_kg = None
            
        # Handle allocation
        allocation_str = request.form.get('supplier_allocation', '').strip()
        if allocation_str:
            try:
                supplier.monthly_allocation = int(allocation_str)
            except (ValueError, TypeError):
                flash('Invalid allocation value.', 'error')
                return redirect(url_for('material_detail', id=material_id))
        else:
            supplier.monthly_allocation = None
        
        db.session.commit()
        flash('Supplier updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating supplier: {str(e)}")
        flash('Error updating supplier. Please try again.', 'error')
    
    return redirect(url_for('material_detail', id=material_id))

@app.route('/edit_test/<int:material_id>', methods=['POST'])
def edit_test(material_id):
    try:
        material = Material.query.get_or_404(material_id)
        test_id = request.form.get('test_id')
        test = MaterialTest.query.get_or_404(test_id)
        
        test_type = request.form.get('test_type', '').strip()
        test_value = request.form.get('test_value', '').strip()
        test_unit = request.form.get('test_unit', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Validate required fields
        if not test_type:
            flash('Test type is required!', 'error')
            return redirect(url_for('material_detail', id=material_id))
        
        # Handle test_value conversion
        test_value_float = None
        if test_value:
            try:
                test_value_float = float(test_value)
                if test_value_float < 0:
                    flash('Test value cannot be negative.', 'error')
                    return redirect(url_for('material_detail', id=material_id))
            except (ValueError, TypeError):
                flash('Invalid test value. Please enter a valid number.', 'error')
                return redirect(url_for('material_detail', id=material_id))
        
        # Update test data
        test.test_type = test_type
        test.test_value = test_value_float
        test.test_unit = test_unit if test_unit else None
        test.notes = notes if notes else None
        
        db.session.commit()
        flash('Test data updated successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating test data: {str(e)}")
        flash('Error updating test data. Please try again.', 'error')
    
    return redirect(url_for('material_detail', id=material_id))

@app.route('/delete_supplier/<int:supplier_id>', methods=['POST'])
def delete_supplier(supplier_id):
    try:
        supplier = MaterialSupplier.query.get_or_404(supplier_id)
        material_id = supplier.material_id
        
        db.session.delete(supplier)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Supplier deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting supplier: {str(e)}")
        return jsonify({'success': False, 'message': 'Error deleting supplier'})

@app.route('/delete_test/<int:test_id>', methods=['POST'])
def delete_test(test_id):
    try:
        test = MaterialTest.query.get_or_404(test_id)
        material_id = test.material_id
        
        db.session.delete(test)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Test deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting test: {str(e)}")
        return jsonify({'success': False, 'message': 'Error deleting test'})
