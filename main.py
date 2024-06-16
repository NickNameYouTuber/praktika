import argparse
from parser import parse_logs
from viewer import view_logs
from db import setup_database

def main():
    parser = argparse.ArgumentParser(description="Apache Log Aggregator")
    parser.add_argument('action', choices=['parse', 'view', 'setup'], help='Action to perform')
    parser.add_argument('--start_date', help='Start date for viewing logs')
    parser.add_argument('--end_date', help='End date for viewing logs')
    parser.add_argument('--filter', choices=['ip', 'status'], help='Filter for viewing logs')

    args = parser.parse_args()

    if args.action == 'setup':
        setup_database()
    elif args.action == 'parse':
        parse_logs()
    elif args.action == 'view':
        view_logs(args.start_date, args.end_date, args.filter)

if __name__ == "__main__":
    import gui
    gui.start_gui()
