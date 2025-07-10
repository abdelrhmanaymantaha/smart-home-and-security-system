#!/usr/bin/env python3
"""
Test script to verify PostgreSQL connection and User registration
"""

from init import app, db, User
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

def test_postgresql_connection():
    """Test PostgreSQL connection and create tables"""
    with app.app_context():
        try:
            # Test database connection
            print("Testing PostgreSQL connection...")
            print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Check if tables exist
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Existing tables: {tables}")
             
            # Create tables if they don't exist
            db.create_all()
            print("Tables created/verified successfully!")
            
            # Test User model
            test_username = "test_user_postgresql"
            test_password = "test_password"
            
            # Check if test user exists
            existing_user = db.session.query(User).filter_by(username=test_username).first()
            if existing_user:
                print(f"Test user '{test_username}' already exists")
            else:
                # Create test user
                hashed_password = generate_password_hash(test_password)
                new_user = User(username=test_username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                print(f"Test user '{test_username}' created successfully in PostgreSQL!")
                
                # Verify user was created
                created_user = db.session.query(User).filter_by(username=test_username).first()
                if created_user:
                    print(f"User verification successful: ID={created_user.id}, Username={created_user.username}")
                else:
                    print("ERROR: User was not found after creation!")
            
            return True
            
        except Exception as e:
            print(f"ERROR: PostgreSQL connection failed: {str(e)}")
            return False

if __name__ == "__main__":
    success = test_postgresql_connection()
    if success:
        print("\n✅ PostgreSQL connection and User registration test PASSED!")
    else:
        print("\n❌ PostgreSQL connection and User registration test FAILED!") 