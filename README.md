# Material Knowledge Database

A modern web application for managing engineering materials used in battery production. Built with Flask and Bootstrap 5.

## Features

- **Material Management**: Add, view, and organize engineering materials
- **Supplier Tracking**: Track multiple suppliers with pricing and allocation data
- **Test Data Recording**: Store and view material testing results
- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **Search Functionality**: Quick search across materials
- **Mobile Responsive**: Works perfectly on all devices

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Icons**: Bootstrap Icons

## Usage

### Adding Materials
1. Click the "Add New Material" button or use the floating action button
2. Fill in the material details including:
   - Basic information (name, type, description)
   - Usage information (where it's used, monthly usage, battery types)
   - Supplier information (multiple suppliers supported)
   - Optional image

### Viewing Materials
- Browse all materials on the main page
- Use the search bar to filter materials
- Click "View Details" to see complete material information

### Managing Suppliers
- Add multiple suppliers per material
- Track pricing, origin, and monthly allocations
- Mark primary suppliers

### Recording Test Data
- Add various types of tests (Porosity, XRD, Density, etc.)
- Record test values with units
- Add notes for additional context

## Screenshots

The application features a modern, gradient-based design with:
- Beautiful card layouts for material display
- Intuitive navigation with breadcrumbs
- Responsive design that works on all devices
- Interactive elements with smooth animations
- Professional color scheme suitable for engineering applications

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
