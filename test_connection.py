#!/usr/bin/env python3
"""Test Snowflake connection with provided credentials"""

import os
import sys
from snowflake.snowpark import Session

def test_connection():
    try:
        # Load environment variables
        connection_parameters = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA"),
            "role": os.getenv("SNOWFLAKE_ROLE")
        }
        
        print("Testing Snowflake connection with:")
        print(f"  Account: {connection_parameters['account']}")
        print(f"  User: {connection_parameters['user']}")
        print(f"  Warehouse: {connection_parameters['warehouse']}")
        print(f"  Database: {connection_parameters['database']}")
        print(f"  Schema: {connection_parameters['schema']}")
        print(f"  Role: {connection_parameters['role']}")
        print()
        
        # Create session
        session = Session.builder.configs(connection_parameters).create()
        
        # Test query
        result = session.sql("SELECT CURRENT_VERSION()").collect()
        print(f"✅ Connection successful!")
        print(f"✅ Snowflake version: {result[0][0]}")
        
        # Test permissions
        result = session.sql("SELECT CURRENT_ROLE()").collect()
        print(f"✅ Current role: {result[0][0]}")
        
        # Check if Container Services is available
        result = session.sql("SHOW COMPUTE POOLS").collect()
        print(f"✅ Compute pools query successful (found {len(result)} pools)")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Load .env file manually
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    
    success = test_connection()
    sys.exit(0 if success else 1)