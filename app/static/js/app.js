// Simple and robust JavaScript for Material Knowledge App

console.log('JavaScript file loaded successfully!');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    
    // Simple delete functionality setup
    setupDeleteButtons();
    
    // Initialize other features
    initSearch();
    
    // Initialize test form validation
    initTestForm();
      // Initialize card edit/delete functionality
    initCardEditDelete();
    
    // Fix modal backdrop issues
    fixModalBackdrop();
    
    console.log('App initialization complete!');
});

function setupDeleteButtons() {
    console.log('Setting up delete buttons...');
    
    // Find all delete buttons
    const deleteButtons = document.querySelectorAll('.delete-btn');
    console.log('Found', deleteButtons.length, 'delete buttons');
    
    deleteButtons.forEach(function(button, index) {
        console.log('Setting up delete button', index + 1);
        
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const materialId = this.getAttribute('data-material-id');
            const materialName = this.getAttribute('data-material-name');
            
            console.log('Delete clicked for:', materialId, materialName);
            
            if (confirm(`Are you sure you want to delete "${materialName}"?`)) {
                deleteMaterial(materialId, materialName);
            }
        });
    });
}

function deleteMaterial(materialId, materialName) {
    console.log('Starting delete process for material:', materialId);
    
    // Show loading message
    const originalContent = document.body.innerHTML;
    
    // Create loading overlay
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'delete-loading';
    loadingDiv.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.8);
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        font-size: 1.2rem;
    `;
    loadingDiv.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-light mb-3" role="status"></div>
            <div>Deleting ${materialName}...</div>
        </div>
    `;
    document.body.appendChild(loadingDiv);
    
    // Perform delete request
    fetch(`/delete_material/${materialId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(function(response) {
        console.log('Delete response status:', response.status);
        if (!response.ok) {
            throw new Error('HTTP error! status: ' + response.status);
        }
        return response.json();
    })
    .then(function(data) {
        console.log('Delete response data:', data);
        
        // Remove loading overlay
        if (document.getElementById('delete-loading')) {
            document.getElementById('delete-loading').remove();
        }
        
        if (data.success) {
            // Show success message
            alert('Material "' + materialName + '" berhasil dihapus!');
            
            // Reload page to refresh the list
            window.location.reload();
        } else {
            alert('Error: ' + (data.message || 'Failed to delete material'));
        }
    })
    .catch(function(error) {
        console.error('Delete error:', error);
        
        // Remove loading overlay
        if (document.getElementById('delete-loading')) {
            document.getElementById('delete-loading').remove();
        }
        
        alert('Error deleting material: ' + error.message);
    });
}

function initSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        console.log('Setting up search functionality');
        
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.row .card');
            let visibleCount = 0;
            
            cards.forEach(function(card) {
                const titleElement = card.querySelector('.card-title');
                const descriptionElement = card.querySelector('.card-text');
                
                if (titleElement && descriptionElement) {
                    const title = titleElement.textContent.toLowerCase();
                    const description = descriptionElement.textContent.toLowerCase();
                    
                    if (title.includes(query) || description.includes(query)) {
                        card.closest('.col-md-6, .col-lg-4').style.display = 'block';
                        visibleCount++;
                    } else {
                        card.closest('.col-md-6, .col-lg-4').style.display = 'none';
                    }
                }
            });
            
            console.log('Search results:', visibleCount, 'materials visible for query:', query);
        });
    }
}

// Test function to verify JavaScript is working
function testFunction() {
    console.log('Test function called - JavaScript is working!');
    alert('JavaScript is working properly!');
}

// Make test function globally available
window.testFunction = testFunction;

console.log('JavaScript setup complete!');

// Search functionality
function initSearch() {
    const searchInput = document.getElementById('search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const cards = document.querySelectorAll('.row .card');
            let visibleCount = 0;
            
            cards.forEach(card => {
                const titleElement = card.querySelector('.card-title');
                const descriptionElement = card.querySelector('.card-text');
                const badgeElement = card.querySelector('.badge');
                
                if (titleElement && descriptionElement) {
                    const title = titleElement.textContent.toLowerCase();
                    const description = descriptionElement.textContent.toLowerCase();
                    const materialType = badgeElement ? badgeElement.textContent.toLowerCase() : '';
                    
                    if (title.includes(query) || description.includes(query) || materialType.includes(query)) {
                        card.closest('.col-md-6, .col-lg-4').style.display = 'block';
                        visibleCount++;
                    } else {
                        card.closest('.col-md-6, .col-lg-4').style.display = 'none';
                    }
                }
            });
            
            // Show/hide no results message
            let noResultsMsg = document.getElementById('no-results');
            if (visibleCount === 0 && query.length > 0) {
                if (!noResultsMsg) {
                    noResultsMsg = document.createElement('div');
                    noResultsMsg.id = 'no-results';
                    noResultsMsg.className = 'empty-state text-center mt-4';
                    noResultsMsg.innerHTML = `
                        <i class="bi bi-search text-muted" style="font-size: 3rem;"></i>
                        <h3 class="text-muted mt-3">No materials found</h3>
                        <p class="text-muted mb-4">Try adjusting your search terms.</p>
                    `;
                    const rowElement = document.querySelector('.row');
                    if (rowElement) {
                        rowElement.after(noResultsMsg);
                    }
                }
            } else if (noResultsMsg) {
                noResultsMsg.remove();
            }
        });
    }
}

// Image preview functionality
function previewImage(input) {
    const file = input.files[0];
    const preview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    
    if (file) {
        // Check file size (5MB limit)
        if (file.size > 5 * 1024 * 1024) {
            alert('File size must be less than 5MB');
            input.value = '';
            if (preview) preview.style.display = 'none';
            return;
        }
        
        // Check file type
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            input.value = '';
            if (preview) preview.style.display = 'none';
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            if (previewImg) {
                previewImg.src = e.target.result;
            }
            if (preview) {
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(file);
    } else {
        if (preview) {
            preview.style.display = 'none';
        }
    }
}

function removePreview() {
    const input = document.getElementById('image_file');
    const preview = document.getElementById('image-preview');
    
    if (input) input.value = '';
    if (preview) preview.style.display = 'none';
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 1050; min-width: 300px;';
    alertDiv.innerHTML = `
        <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }
    }, 5000);
}

// Supplier management functions for add material form
let supplierCount = 1;

function addSupplier() {
    supplierCount++;
    const container = document.getElementById('suppliers-container');
    if (!container) return;
    
    const newSupplier = document.createElement('div');
    newSupplier.className = 'supplier-entry border rounded p-3 mb-3';
    newSupplier.style.opacity = '0';
    newSupplier.style.transform = 'translateY(20px)';
    
    newSupplier.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="mb-0">Supplier ${supplierCount}</h6>
            <button type="button" class="btn btn-outline-danger btn-sm" onclick="removeSupplier(this)">
                <i class="bi bi-trash"></i>
            </button>
        </div>
        <div class="row">
            <div class="col-md-3 mb-2">
                <label class="form-label">Supplier Name</label>
                <input type="text" class="form-control" name="supplier_name[]" placeholder="Supplier ${String.fromCharCode(64 + supplierCount)}">
            </div>
            <div class="col-md-3 mb-2">
                <label class="form-label">Origin</label>
                <input type="text" class="form-control" name="supplier_origin[]" placeholder="Indonesia">
            </div>
            <div class="col-md-3 mb-2">
                <label class="form-label">Price (Rp/kg)</label>
                <input type="number" class="form-control" name="supplier_price[]" step="0.01" placeholder="120000">
            </div>
            <div class="col-md-3 mb-2">
                <label class="form-label">Monthly Allocation (kg)</label>
                <input type="number" class="form-control" name="supplier_allocation[]" placeholder="300">
            </div>
        </div>
    `;
    
    container.appendChild(newSupplier);
    
    // Animate in
    setTimeout(() => {
        newSupplier.style.transition = 'all 0.3s ease';
        newSupplier.style.opacity = '1';
        newSupplier.style.transform = 'translateY(0)';
    }, 10);
}

function removeSupplier(button) {
    const supplierEntry = button.closest('.supplier-entry');
    if (supplierEntry) {
        supplierEntry.style.transition = 'all 0.3s ease';
        supplierEntry.style.opacity = '0';
        supplierEntry.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            supplierEntry.remove();
        }, 300);
    }
}

// Add Test Data form validation and handling
function initTestForm() {
    console.log('Initializing test form...');
    
    const testForm = document.querySelector('#addTestForm');
    if (testForm) {
        console.log('Test form found, setting up validation...');
        
        testForm.addEventListener('submit', function(e) {
            console.log('Test form submit event triggered');
            
            const testType = document.getElementById('test_type').value.trim();
            const testValue = document.getElementById('test_value').value.trim();
            
            // Clear previous validation states
            clearValidationErrors();
            
            let isValid = true;
            
            // Validate test type (required)
            if (!testType) {
                showFieldError('test_type', 'Please select a test type.');
                isValid = false;
            }
              // Validate test value if provided (optional but must be valid number)
            if (testValue) {
                const numValue = parseFloat(testValue);
                if (isNaN(numValue)) {
                    showFieldError('test_value', 'Please enter a valid number for test value.');
                    isValid = false;
                } else if (numValue < 0) {
                    showFieldError('test_value', 'Test value cannot be negative.');
                    isValid = false;
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                console.log('Form validation failed');
                return false;
            }
            
            console.log('Test form submitted with valid data');
            
            // Optional: Show loading state
            const submitBtn = testForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spin me-1"></i>Adding...';
            }
        });
        
        // Reset form when modal is hidden
        const modal = document.getElementById('addTestModal');
        if (modal) {
            modal.addEventListener('hidden.bs.modal', function() {
                testForm.reset();
                clearValidationErrors();
                
                // Reset submit button
                const submitBtn = testForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="bi bi-plus-circle me-1"></i>Add Test Data';
                }
            });
        }
    } else {
        console.log('Test form not found on this page');
    }
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.classList.add('is-invalid');
        
        // Find or create feedback element
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
    }
}

function clearValidationErrors() {
    const invalidFields = document.querySelectorAll('.is-invalid');
    invalidFields.forEach(field => {
        field.classList.remove('is-invalid');
    });
}

// Edit and Delete functionality for cards
function initCardEditDelete() {
    console.log('Initializing card edit/delete functionality...');
    
    // Edit supplier buttons
    document.querySelectorAll('.edit-supplier-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const supplierId = this.getAttribute('data-supplier-id');
            const supplierName = this.getAttribute('data-supplier-name');
            const supplierOrigin = this.getAttribute('data-supplier-origin');
            const supplierPrice = this.getAttribute('data-supplier-price');
            const supplierAllocation = this.getAttribute('data-supplier-allocation');
            
            // Fill edit modal
            document.getElementById('edit_supplier_id').value = supplierId;
            document.getElementById('edit_supplier_name').value = supplierName;
            document.getElementById('edit_supplier_origin').value = supplierOrigin;
            document.getElementById('edit_supplier_price').value = supplierPrice;
            document.getElementById('edit_supplier_allocation').value = supplierAllocation;
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('editSupplierModal'));
            modal.show();
        });
    });
    
    // Delete supplier buttons
    document.querySelectorAll('.delete-supplier-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const supplierId = this.getAttribute('data-supplier-id');
            const supplierName = this.getAttribute('data-supplier-name');
            
            if (confirm(`Are you sure you want to delete supplier "${supplierName}"?`)) {
                deleteSupplierById(supplierId);
            }
        });
    });
    
    // Edit test buttons
    document.querySelectorAll('.edit-test-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const testId = this.getAttribute('data-test-id');
            const testType = this.getAttribute('data-test-type');
            const testValue = this.getAttribute('data-test-value');
            const testUnit = this.getAttribute('data-test-unit');
            const testNotes = this.getAttribute('data-test-notes');
            
            // Fill edit modal
            document.getElementById('edit_test_id').value = testId;
            document.getElementById('edit_test_type').value = testType;
            document.getElementById('edit_test_value').value = testValue;
            document.getElementById('edit_test_unit').value = testUnit;
            document.getElementById('edit_test_notes').value = testNotes;
            
            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('editTestModal'));
            modal.show();
        });
    });
    
    // Delete test buttons
    document.querySelectorAll('.delete-test-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const testId = this.getAttribute('data-test-id');
            const testType = this.getAttribute('data-test-type');
            
            if (confirm(`Are you sure you want to delete test "${testType}"?`)) {
                deleteTestById(testId);
            }
        });
    });
}

function deleteSupplierById(supplierId) {
    fetch(`/delete_supplier/${supplierId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error deleting supplier: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting supplier');
    });
}

function deleteTestById(testId) {
    fetch(`/delete_test/${testId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Error deleting test: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error deleting test');
    });
}

// Fix modal backdrop issues - Aggressive approach
function fixModalBackdrop() {
    console.log('Setting up modal backdrop fix...');
    
    // Override Bootstrap modal backdrop creation
    const originalModal = window.bootstrap?.Modal;
    if (originalModal) {
        console.log('Patching Bootstrap Modal...');
    }
    
    // Force fix any existing backdrops
    function forceFixBackdrop() {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(backdrop => {
            backdrop.style.background = 'rgba(0, 0, 0, 0.5)';
            backdrop.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
            backdrop.style.opacity = '0.5';
            backdrop.style.setProperty('--bs-backdrop-bg', 'rgba(0, 0, 0, 0.5)', 'important');
            backdrop.style.setProperty('--bs-backdrop-opacity', '0.5', 'important');
        });
    }
    
    // Listen for modal events
    document.addEventListener('show.bs.modal', function (event) {
        console.log('Modal showing:', event.target.id);
        setTimeout(forceFixBackdrop, 50);
        setTimeout(forceFixBackdrop, 200);
    });
    
    document.addEventListener('shown.bs.modal', function (event) {
        console.log('Modal shown:', event.target.id);
        forceFixBackdrop();
    });
    
    document.addEventListener('hide.bs.modal', function (event) {
        console.log('Modal hiding:', event.target.id);
    });
    
    document.addEventListener('hidden.bs.modal', function (event) {
        console.log('Modal hidden:', event.target.id);
        
        // Clean up any remaining backdrops
        setTimeout(() => {
            const stuckBackdrops = document.querySelectorAll('.modal-backdrop');
            if (!document.querySelector('.modal.show')) {
                stuckBackdrops.forEach(backdrop => backdrop.remove());
                document.body.classList.remove('modal-open');
                document.body.style.paddingRight = '';
                document.body.style.overflow = '';
            }
        }, 300);
    });
    
    // MutationObserver to catch dynamically created backdrops
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && node.classList?.contains('modal-backdrop')) {
                    console.log('New backdrop detected, fixing...');
                    setTimeout(() => {
                        node.style.background = 'rgba(0, 0, 0, 0.5)';
                        node.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
                        node.style.opacity = '0.5';
                    }, 10);
                }
            });
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Initial fix for any existing backdrops
    forceFixBackdrop();
}

fixModalBackdrop();
