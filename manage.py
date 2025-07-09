from app import app, db
from flask.cli import with_appcontext
import click

@click.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command()
@with_appcontext
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    click.echo('Dropped all tables.')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")
