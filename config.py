import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Gunakan SQLite untuk development (lebih mudah)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///material_knowledge.db'
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'images')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Jika ingin menggunakan MySQL, uncomment baris di bawah dan comment baris SQLite di atas
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/material_knowledge_db?ssl_disabled=true'


