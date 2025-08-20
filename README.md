# Distributed Database System with Django

A Django-based distributed database system that demonstrates concurrent insertions across multiple databases with comprehensive validation and reporting capabilities.

## 🎯 Project Overview

This project implements a **distributed database architecture** using Django, where different models (Users, Products, Orders) are stored in separate databases. The system demonstrates:

- **Multi-database routing** with custom database routers
- **Concurrent insertions** using threading
- **Data validation** at both model and application levels
- **Performance monitoring** and success rate analysis

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   users.db      │    │  products.db    │    │   orders.db     │
│                 │    │                 │    │                 │
│ • User Model    │    │ • Product Model │    │ • Order Model   │
│ • Validation    │    │ • Validation    │    │ • Validation    │
│ • Constraints   │    │ • Constraints   │    │ • Constraints   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │   Django Router         │
                    │ • Route by model type   │
                    │ • Handle migrations     │
                    │ • Manage connections    │
                    └─────────────────────────┘
                                 │
                    ┌─────────────────────────┐
                    │   Management Commands   │
                    │ • simulate_insertions   │
                    └─────────────────────────┘
```

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- **Basic knowledge** of Django and Python

## 🚀 Installation & Setup

### 1. Set Up Project Directory

**Option A: Extract from ZIP/Archive**
```bash
# Extract the project files to your desired location
# Navigate to the project directory
cd path/to/django_internship_assignment/distributed_system
```

**Option B: Copy Project Files**
```bash
# Copy the entire project folder to your desired location
# Navigate to the project directory
cd path/to/django_internship_assignment/distributed_system
```

**Option C: Create Project Structure Manually**
```bash
# Create the project directory structure
mkdir django_internship_assignment
cd django_internship_assignment
mkdir distributed_system
cd distributed_system
# Copy all project files into this directory
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** If `requirements.txt` doesn't exist, install manually:
```bash
pip install django reportlab
```

### 4. Database Setup

The project uses SQLite databases for simplicity. The system will automatically create:
- `default.db` - Django system tables
- `users.db` - User data
- `products.db` - Product data  
- `orders.db` - Order data

### 5. Run Migrations

```bash
# Create migrations
python manage.py makemigrations data_simulation

# Apply migrations to all databases
python manage.py migrate
```

## 🎮 Usage

### Basic Commands

#### 1. Simulate Concurrent Insertions

```bash
# Run with default 10 threads
python manage.py simulate_insertions
python manage.py migrate --database=users_db
python manage.py migrate --database=products_db  
python manage.py migrate --database=orders_db
# Run with custom number of threads
python manage.py simulate_insertions --threads 15
```

**What it does:**
- Creates 10+ simultaneous threads
- Each thread attempts to insert data into appropriate database
- Validates data at multiple levels
- Reports success/failure for each insertion

### Command Options

| Command | Option | Description | Default |
|---------|--------|-------------|---------|
| `simulate_insertions` | `--threads` | Number of concurrent threads | 10 |

## 📊 Understanding the Results

### Success Metrics

- **Success Rate**: Percentage of successful insertions
- **Execution Time**: Total time taken for all operations
- **Thread Performance**: Individual thread success/failure

### Validation Rules

#### Users (users.db)
- ✅ **Valid**: Name (2+ characters), Valid email format
- ❌ **Invalid**: Empty name, Duplicate email, Invalid email format

#### Products (products.db)
- ✅ **Valid**: Name (2+ characters), Positive price (0.01 - 999,999.99)
- ❌ **Invalid**: Empty name, Negative price, Price too high

#### Orders (orders.db)
- ✅ **Valid**: Positive user_id, Positive product_id, Positive quantity (1-1000)
- ❌ **Invalid**: Zero/negative quantities, Non-existent user/product IDs

## 🔧 Project Structure

```
distributed_system/
├── data_simulation/           # Main application
│   ├── models.py             # Database models (User, Product, Order)
│   ├── routers.py            # Database routing logic
│   └── management/
│       └── commands/
│           ├── simulate_insertions.py    # Basic insertion command
│           └── generate_pdf_report.py    # PDF report command (optional)
├── distributed_system/        # Django project settings
│   ├── settings.py           # Database configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI application
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── setup.bat                 # Windows setup script
├── setup.sh                  # Unix/Linux setup script
└── README.md                  # This file
```

## ⚙️ Configuration

### Database Settings

The project uses multiple SQLite databases configured in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'default.db',
    },
    'users_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'users.db',
    },
    'products_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'products.db',
    },
    'orders_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'orders.db',
    },
}

# Database routing
DATABASE_ROUTERS = ['data_simulation.routers.DatabaseRouter']
```

### Router Configuration

The `DatabaseRouter` class in `routers.py` handles:
- **Read operations**: Routes to appropriate database based on model
- **Write operations**: Ensures data goes to correct database
- **Migrations**: Controls which database gets which model tables

## 🧪 Testing

### Run Basic Test

```bash
# Test if models can be imported
python test_import.py
```

### Verify Database Tables

```bash
# Check migration status
python manage.py showmigrations data_simulation

# Check specific database
python manage.py showmigrations --database=users_db
```

### Verify Database Tables

```bash
# Check migration status
python manage.py showmigrations data_simulation

# Check specific database
python manage.py showmigrations --database=users_db
```

## 📈 Performance Analysis

### Expected Results

With 10 threads, typical results:
- **Execution Time**: 2-4 seconds
- **Success Rate**: 80-90%
- **Failed Insertions**: Usually 2-5 (due to validation rules)

### Factors Affecting Performance

- **Thread Count**: More threads = faster execution but potential conflicts
- **Data Validation**: Complex validation rules may slow down insertions
- **System Resources**: CPU and memory availability
- **Database Size**: Larger databases may have slower insertions

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```
ImportError: cannot import name 'Product' from 'data_simulation.models'
```
**Solution**: Ensure all models are properly defined and migrations are applied.

#### 2. Database Connection Errors
```
OperationalError: no such table: data_simulation_user
```
**Solution**: Run migrations and ensure router is properly configured.

#### 3. PDF Generation Errors
```
ModuleNotFoundError: No module named 'reportlab'
```
**Solution**: Install reportlab: `pip install reportlab`

#### 4. Migration Issues
```
django.db.utils.OperationalError: table already exists
```
**Solution**: Reset databases and recreate migrations.

### Reset Everything

If you encounter persistent issues:

```bash
# Remove all database files
Remove-Item "*.db" -Force

# Remove migration files
Remove-Item "data_simulation\migrations\0001_initial.py" -Force

# Recreate everything
python manage.py makemigrations data_simulation
python manage.py migrate
```

## 🔒 Security Considerations

- **Development Only**: This project uses SQLite for demonstration
- **No Authentication**: No user authentication implemented
- **Data Validation**: Input validation prevents malicious data
- **File Permissions**: Ensure proper file permissions for database files

## 🚀 Production Deployment

For production use, consider:

1. **Database**: Use PostgreSQL, MySQL, or other production databases
2. **Authentication**: Implement proper user authentication
3. **Environment Variables**: Use environment variables for sensitive settings
4. **Logging**: Add comprehensive logging for monitoring
5. **Testing**: Implement unit tests and integration tests
6. **Documentation**: Add API documentation if building web services

## 📦 Alternative Setup Methods

### **Using Setup Scripts (Recommended)**

**Windows Users:**
```bash
# Simply double-click setup.bat or run in Command Prompt
setup.bat
```

**Unix/Linux/macOS Users:**
```bash
# Make script executable and run
chmod +x setup.sh
./setup.sh
```

### **Manual Setup**
If you prefer manual setup or encounter issues with automated scripts:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Linux/macOS:
source venv/bin/activate

# 3. Install Django
pip install django

# 4. Create migrations
python manage.py makemigrations data_simulation

# 5. Apply migrations
python manage.py migrate

# 6. Test the system
python manage.py simulate_insertions
```

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Database Routing](https://docs.djangoproject.com/en/stable/topics/db/multi-db/)
- [Python Threading](https://docs.python.org/3/library/threading.html)

## 🤝 Project Sharing

To share this project with others:

1. **ZIP the entire project folder** including all files and subdirectories
2. **Share the ZIP file** via email, cloud storage, or file sharing service
3. **Recipients can extract** and follow the setup instructions above
4. **No GitHub account required** - works completely offline

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👨‍💻 Author

Created as part of a Django internship assignment demonstrating distributed database concepts.

---

## 🎉 Quick Start Summary

```bash
# 1. Setup
# Extract/copy project files to your desired location
cd path/to/django_internship_assignment/distributed_system
python -m venv venv
venv\Scripts\activate  # Windows
pip install django reportlab

# 2. Run
python manage.py makemigrations data_simulation
python manage.py migrate
python manage.py simulate_insertions

# 3. Generate PDF Report (Optional)
python manage.py generate_pdf_report

# 4. Enjoy your concurrent insertion simulation! 🎯
```

**Happy Coding! 🚀**
