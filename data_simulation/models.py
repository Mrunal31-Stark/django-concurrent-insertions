# data_simulation/models.py
from django.db import models
import re
from decimal import Decimal

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    
    class Meta:
        app_label = 'data_simulation'
    
    def clean(self):
        """Application-level validation for User model"""
        errors = []
        
        # Validate name
        if not self.name or not self.name.strip():
            errors.append("Name cannot be empty")
        elif len(self.name.strip()) < 2:
            errors.append("Name must be at least 2 characters long")
        
        # Validate email
        if not self.email or not self.email.strip():
            errors.append("Email cannot be empty")
        else:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email.strip()):
                errors.append(f"Invalid email format: {self.email}")
        
        if errors:
            raise ValueError(f"User validation errors: {', '.join(errors)}")
    
    def __str__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        app_label = 'data_simulation'
    
    def clean(self):
        """Application-level validation for Product model"""
        errors = []
        
        # Validate name
        if not self.name or not self.name.strip():
            errors.append("Product name cannot be empty")
        elif len(self.name.strip()) < 2:
            errors.append("Product name must be at least 2 characters long")
        
        # Validate price
        if self.price is None:
            errors.append("Price cannot be None")
        elif self.price < 0:
            errors.append(f"Price cannot be negative: {self.price}")
        elif self.price > Decimal('999999.99'):
            errors.append(f"Price too high: {self.price}")
        
        if errors:
            raise ValueError(f"Product validation errors: {', '.join(errors)}")
    
    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField()
    
    class Meta:
        app_label = 'data_simulation'
    
    def clean(self):
        """Application-level validation for Order model"""
        errors = []
        
        # Validate user_id
        if self.user_id is None:
            errors.append("User ID cannot be None")
        elif self.user_id <= 0:
            errors.append(f"User ID must be positive: {self.user_id}")
        
        # Validate product_id
        if self.product_id is None:
            errors.append("Product ID cannot be None")
        elif self.product_id <= 0:
            errors.append(f"Product ID must be positive: {self.product_id}")
        
        # Validate quantity
        if self.quantity is None:
            errors.append("Quantity cannot be None")
        elif self.quantity <= 0:
            errors.append(f"Quantity must be positive: {self.quantity}")
        elif self.quantity > 1000:
            errors.append(f"Quantity too high: {self.quantity}")
        
        if errors:
            raise ValueError(f"Order validation errors: {', '.join(errors)}")
    
    def __str__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity})"