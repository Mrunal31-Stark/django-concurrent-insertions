# data_simulation/management/commands/simulate_insertions.py
import threading
import time
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from data_simulation.models import User, Product, Order

class Command(BaseCommand):
    help = 'Simulate concurrent insertions into multiple databases'
    
    def __init__(self):
        super().__init__()
        self.results = {
            'users': {'successful': [], 'failed': []},
            'products': {'successful': [], 'failed': []},
            'orders': {'successful': [], 'failed': []}
        }
        self.lock = threading.Lock()
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--threads',
            type=int,
            default=10,
            help='Number of threads to use for concurrent insertions'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Starting concurrent insertions simulation...\n')
        )
        
        # Test data as provided in the assignment
        users_data = [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
            {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
            {'id': 4, 'name': 'David', 'email': 'david@example.com'},
            {'id': 5, 'name': 'Eve', 'email': 'eve@example.com'},
            {'id': 6, 'name': 'Frank', 'email': 'frank@example.com'},
            {'id': 7, 'name': 'Grace', 'email': 'grace@example.com'},
            {'id': 8, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 9, 'name': 'Henry', 'email': 'henry@example.com'},
            {'id': 10, 'name': '', 'email': 'jane@example.com'},  # Invalid: empty name
        ]
        
        products_data = [
            {'id': 1, 'name': 'Laptop', 'price': Decimal('1000.00')},
            {'id': 2, 'name': 'Smartphone', 'price': Decimal('700.00')},
            {'id': 3, 'name': 'Headphones', 'price': Decimal('150.00')},
            {'id': 4, 'name': 'Monitor', 'price': Decimal('300.00')},
            {'id': 5, 'name': 'Keyboard', 'price': Decimal('50.00')},
            {'id': 6, 'name': 'Mouse', 'price': Decimal('30.00')},
            {'id': 7, 'name': 'Laptop', 'price': Decimal('1000.00')},
            {'id': 8, 'name': 'Smartwatch', 'price': Decimal('250.00')},
            {'id': 9, 'name': 'Gaming Chair', 'price': Decimal('500.00')},
            {'id': 10, 'name': 'Earbuds', 'price': Decimal('-50.00')},  # Invalid: negative price
        ]
        
        orders_data = [
            {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2},
            {'id': 2, 'user_id': 2, 'product_id': 2, 'quantity': 1},
            {'id': 3, 'user_id': 3, 'product_id': 3, 'quantity': 5},
            {'id': 4, 'user_id': 4, 'product_id': 4, 'quantity': 1},
            {'id': 5, 'user_id': 5, 'product_id': 5, 'quantity': 3},
            {'id': 6, 'user_id': 6, 'product_id': 6, 'quantity': 4},
            {'id': 7, 'user_id': 7, 'product_id': 7, 'quantity': 2},
            {'id': 8, 'user_id': 8, 'product_id': 8, 'quantity': 0},  # Invalid: zero quantity
            {'id': 9, 'user_id': 9, 'product_id': 1, 'quantity': -1},  # Invalid: negative quantity
            {'id': 10, 'user_id': 10, 'product_id': 11, 'quantity': 2},  # Invalid: non-existent product_id
        ]
        
        # Create threads for concurrent insertions
        threads = []
        
        # Create threads for users
        for i, user_data in enumerate(users_data):
            thread = threading.Thread(
                target=self.insert_user,
                args=(user_data, i + 1),
                name=f"UserThread-{i+1}"
            )
            threads.append(thread)
        
        # Create threads for products
        for i, product_data in enumerate(products_data):
            thread = threading.Thread(
                target=self.insert_product,
                args=(product_data, i + 1),
                name=f"ProductThread-{i+1}"
            )
            threads.append(thread)
        
        # Create threads for orders
        for i, order_data in enumerate(orders_data):
            thread = threading.Thread(
                target=self.insert_order,
                args=(order_data, i + 1),
                name=f"OrderThread-{i+1}"
            )
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        self.stdout.write("Starting all insertion threads...\n")
        
        for thread in threads:
            thread.start()
            time.sleep(0.1)  # Small delay to simulate real-world conditions
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Print results
        self.print_results(end_time - start_time)
    
    def insert_user(self, user_data, thread_id):
        """Insert user with validation"""
        thread_name = threading.current_thread().name
        try:
            with transaction.atomic(using='users_db'):
                user = User(**user_data)
                user.clean()  # Application-level validation
                user.save(using='users_db')
                
                with self.lock:
                    self.results['users']['successful'].append({
                        'thread': thread_name,
                        'data': user_data,
                        'result': str(user)
                    })
                    
        except Exception as e:
            with self.lock:
                self.results['users']['failed'].append({
                    'thread': thread_name,
                    'data': user_data,
                    'error': str(e)
                })
    
    def insert_product(self, product_data, thread_id):
        """Insert product with validation"""
        thread_name = threading.current_thread().name
        try:
            with transaction.atomic(using='products_db'):
                product = Product(**product_data)
                product.clean()  # Application-level validation
                product.save(using='products_db')
                
                with self.lock:
                    self.results['products']['successful'].append({
                        'thread': thread_name,
                        'data': product_data,
                        'result': str(product)
                    })
                    
        except Exception as e:
            with self.lock:
                self.results['products']['failed'].append({
                    'thread': thread_name,
                    'data': product_data,
                    'error': str(e)
                })
    
    def insert_order(self, order_data, thread_id):
        """Insert order with validation"""
        thread_name = threading.current_thread().name
        try:
            with transaction.atomic(using='orders_db'):
                order = Order(**order_data)
                order.clean()  # Application-level validation
                order.save(using='orders_db')
                
                with self.lock:
                    self.results['orders']['successful'].append({
                        'thread': thread_name,
                        'data': order_data,
                        'result': str(order)
                    })
                    
        except Exception as e:
            with self.lock:
                self.results['orders']['failed'].append({
                    'thread': thread_name,
                    'data': order_data,
                    'error': str(e)
                })
    
    def print_results(self, execution_time):
        """Print detailed results of all insertions"""
        self.stdout.write(self.style.SUCCESS(f"\n{'='*80}"))
        self.stdout.write(self.style.SUCCESS("CONCURRENT INSERTION SIMULATION RESULTS"))
        self.stdout.write(self.style.SUCCESS(f"{'='*80}"))
        self.stdout.write(f"Total execution time: {execution_time:.2f} seconds\n")
        
        # Print Users results
        self.stdout.write(self.style.HTTP_INFO("USERS TABLE (users.db):"))
        self.stdout.write(f"Successful insertions: {len(self.results['users']['successful'])}")
        self.stdout.write(f"Failed insertions: {len(self.results['users']['failed'])}\n")
        
        if self.results['users']['successful']:
            self.stdout.write(self.style.SUCCESS("✓ Successful User Insertions:"))
            for result in self.results['users']['successful']:
                self.stdout.write(f"  [{result['thread']}] {result['result']}")
        
        if self.results['users']['failed']:
            self.stdout.write(self.style.ERROR("✗ Failed User Insertions:"))
            for result in self.results['users']['failed']:
                self.stdout.write(f"  [{result['thread']}] {result['data']} - Error: {result['error']}")
        
        self.stdout.write("")
        
        # Print Products results
        self.stdout.write(self.style.HTTP_INFO("PRODUCTS TABLE (products.db):"))
        self.stdout.write(f"Successful insertions: {len(self.results['products']['successful'])}")
        self.stdout.write(f"Failed insertions: {len(self.results['products']['failed'])}\n")
        
        if self.results['products']['successful']:
            self.stdout.write(self.style.SUCCESS("✓ Successful Product Insertions:"))
            for result in self.results['products']['successful']:
                self.stdout.write(f"  [{result['thread']}] {result['result']}")
        
        if self.results['products']['failed']:
            self.stdout.write(self.style.ERROR("✗ Failed Product Insertions:"))
            for result in self.results['products']['failed']:
                self.stdout.write(f"  [{result['thread']}] {result['data']} - Error: {result['error']}")
        
        self.stdout.write("")
        
        # Print Orders results
        self.stdout.write(self.style.HTTP_INFO("ORDERS TABLE (orders.db):"))
        self.stdout.write(f"Successful insertions: {len(self.results['orders']['successful'])}")
        self.stdout.write(f"Failed insertions: {len(self.results['orders']['failed'])}\n")
        
        if self.results['orders']['successful']:
            self.stdout.write(self.style.SUCCESS("✓ Successful Order Insertions:"))
            for result in self.results['orders']['successful']:
                self.stdout.write(f"  [{result['thread']}] {result['result']}")
        
        if self.results['orders']['failed']:
            self.stdout.write(self.style.ERROR("✗ Failed Order Insertions:"))
            for result in self.results['orders']['failed']:
                self.stdout.write(f"  [{result['thread']}] {result['data']} - Error: {result['error']}")
        
        self.stdout.write("")
        
        # Summary
        total_successful = (len(self.results['users']['successful']) + 
                          len(self.results['products']['successful']) + 
                          len(self.results['orders']['successful']))
        total_failed = (len(self.results['users']['failed']) + 
                       len(self.results['products']['failed']) + 
                       len(self.results['orders']['failed']))
        
        self.stdout.write(self.style.SUCCESS(f"{'='*80}"))
        self.stdout.write(self.style.SUCCESS("SUMMARY:"))
        self.stdout.write(f"Total successful insertions: {total_successful}")
        self.stdout.write(f"Total failed insertions: {total_failed}")
        self.stdout.write(f"Success rate: {(total_successful/(total_successful+total_failed)*100):.1f}%")
        self.stdout.write(self.style.SUCCESS(f"{'='*80}"))
