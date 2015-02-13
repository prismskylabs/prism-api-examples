#!/usr/bin/env python
import argparse




def main():
    parser = argparse.ArgumentParser(
        description="Generate a CSV of entry counts per day per site.",
    )
    parser.add_argument(
        'start_date', type=str,
        help='Date to start generating counts (ex: 2015-01-15)'
    )
    parser.add_argument(
        'stop_date', type=str,
        help='Date to stop generating counts (ex: 2015-02-20)'
    )
    args = parser.parse_args()
    print args

if __name__ == '__main__':
    main()
