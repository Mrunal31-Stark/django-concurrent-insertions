#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distributed_system.settings')
django.setup()

# Try to import the models
try:
    from data_simulation.models import User, Product, Order
    print("✅ Successfully imported all models:")
    print(f"  - User: {User}")
    print(f"  - Product: {Product}")
    print(f"  - Order: {Order}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("\nTrying to import models one by one:")
    
    try:
        from data_simulation.models import User
        print("✅ User imported successfully")
    except ImportError as e:
        print(f"❌ User import failed: {e}")
    
    try:
        from data_simulation.models import Product
        print("✅ Product imported successfully")
    except ImportError as e:
        print(f"❌ Product import failed: {e}")
    
    try:
        from data_simulation.models import Order
        print("✅ Order imported successfully")
    except ImportError as e:
        print(f"❌ Order import failed: {e}")
