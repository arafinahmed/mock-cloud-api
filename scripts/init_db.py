#!/usr/bin/env python3
"""
Database initialization script for Mock Cloud API
Creates initial environments, security groups, and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import Base, Environment, SecurityGroup
from app.schemas import EnvironmentCreate, SecurityGroupCreate

def init_database():
    """Initialize database with sample data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Environment).count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        print("Initializing database with sample data...")
        
        # Create default environment
        default_env = EnvironmentCreate(
            name="default",
            network_cidr="10.0.0.0/16",
            description="Default environment for development and testing"
        )
        db_env = Environment(**default_env.dict())
        db.add(db_env)
        
        # Create development environment
        dev_env = EnvironmentCreate(
            name="development",
            network_cidr="10.1.0.0/16",
            description="Development environment"
        )
        db_dev_env = Environment(**dev_env.dict())
        db.add(db_dev_env)
        
        # Create production environment
        prod_env = EnvironmentCreate(
            name="production",
            network_cidr="10.2.0.0/16",
            description="Production environment"
        )
        db_prod_env = Environment(**prod_env.dict())
        db.add(prod_env)
        
        # Create default security group
        default_sg = SecurityGroupCreate(
            name="default",
            description="Default security group with basic rules",
            rules='{"inbound": [{"protocol": "tcp", "port": 22, "source": "0.0.0.0/0"}], "outbound": [{"protocol": "all", "port": "all", "destination": "0.0.0.0/0"}]}'
        )
        db_sg = SecurityGroup(**default_sg.dict())
        db.add(db_sg)
        
        # Create web security group
        web_sg = SecurityGroupCreate(
            name="web",
            description="Security group for web servers",
            rules='{"inbound": [{"protocol": "tcp", "port": 80, "source": "0.0.0.0/0"}, {"protocol": "tcp", "port": 443, "source": "0.0.0.0/0"}], "outbound": [{"protocol": "all", "port": "all", "destination": "0.0.0.0/0"}]}'
        )
        db_web_sg = SecurityGroup(**web_sg.dict())
        db.add(db_web_sg)
        
        # Commit all changes
        db.commit()
        
        print("Database initialized successfully!")
        print(f"Created {db.query(Environment).count()} environments")
        print(f"Created {db.query(SecurityGroup).count()} security groups")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
