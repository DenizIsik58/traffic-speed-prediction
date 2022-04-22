#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_speed_prediction.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
    from traffic_speed_prediction.auto_ml import auto_ml
    from util.db.database_commands import DatabaseCommands
    print("LOADING DB:")
    DatabaseCommands.load_database()






   #from util.db.database_commands import DatabaseCommands
    #from traffic_speed_prediction.auto_ml import auto_ml
    #DatabaseCommands.load_database()
    #DatabaseCommands.extract_data_and_write_to_csv()
    #auto_ml.train()
    #DatabaseCommands.getNearestCoordsAndPredictions(25.759138, 62.24248)
    #DatabaseCommands.getNearestCoordsAndPredictions(30.622457, 62.171684)


