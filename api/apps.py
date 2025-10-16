from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        Preloading all data in cache/memory.
        """
        try:
            # Importing the module here, because it avoids crashing the app if the db is not ready.
            from .search_sort_filter_v3 import ManualSQLQueryEngine
            # Preloading all data into cache/memory
            ManualSQLQueryEngine._get_all_data()

        except Exception as e:
            print(f"An unexpected error occured: {e} \
                  probably you need to migrate or makemigrations!")
