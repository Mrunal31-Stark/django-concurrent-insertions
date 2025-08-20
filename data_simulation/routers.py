# data_simulation/routers.py
class DatabaseRouter:
    """
    A router to control all database operations on models for different databases
    """
    
    route_app_labels = {'data_simulation'}
    
    def db_for_read(self, model, **hints):
        """Suggest the database to read from."""
        if model._meta.app_label == 'data_simulation':
            if model.__name__ == 'User':
                return 'users_db'
            elif model.__name__ == 'Product':
                return 'products_db'
            elif model.__name__ == 'Order':
                return 'orders_db'
        return None
    
    def db_for_write(self, model, **hints):
        """Suggest the database to write to."""
        if model._meta.app_label == 'data_simulation':
            if model.__name__ == 'User':
                return 'users_db'
            elif model.__name__ == 'Product':
                return 'products_db'
            elif model.__name__ == 'Order':
                return 'orders_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if models are in the same app."""
        db_set = {'default', 'users_db', 'products_db', 'orders_db'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that certain models' migrations only go to specific databases."""
        if app_label == 'data_simulation':
            if db == 'users_db' and model_name == 'user':
                return True
            elif db == 'products_db' and model_name == 'product':
                return True
            elif db == 'orders_db' and model_name == 'order':
                return True
            elif db == 'default':
                return False
            return False
        return db == 'default'