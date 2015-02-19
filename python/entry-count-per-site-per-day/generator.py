#!/usr/bin/env python

# using only standard library pacakges for this example.
# if you're building out a deeper integration in python,
# you may want to consider using requests
# http://docs.python-requests.org/en/latest/
import argparse
import codecs
import csv
import datetime
import json
import os
import sys
import urllib2


API_ROOT = 'https://api.prism.com/v1/'
API_KEY = os.environ.get('PRISM_API_KEY', None)
TRIPWIRE_TYPE = 'entry'

if not API_KEY:
    raise Exception('Environment variable PRISM_API_KEY not defined')


def get_sites():
    api_root = get_resource(API_ROOT)
    accounts_url = api_root['accounts_url']
    accounts = get_resource(accounts_url)

    # list of all sites in any of the accounts this api key can access
    # that have an 'entry' tripwire type defined
    all_sites = []
    for account in accounts:

        # check to see if the account has an 'entry' tripwire type
        tripwire_types_url = account['tripwire_types_url']
        tripwire_types = get_resource(tripwire_types_url)
        if not any([tt['name'] == 'entry' for tt in tripwire_types]):
            continue

        sites_url = account['sites_url']
        sites = get_resource(sites_url)
        # attatch the account name to the site object
        for site in sites:
            site['account_name'] = account['name']
        all_sites.extend(sites)

    return all_sites


def get_counts(site, start_date, stop_date):
    people_count_url = site['people_count_url']
    people_count_url += '&period=day'
    people_count_url += '&tripwire_type_name=entry'

    # if api is given a datetime without timezone information,
    # it uses the site's timezone. As of v1.0, this is undocumented
    # behavior but will be formalized in an upcoming release.
    people_count_url += '&start=%s' % start_date
    # the stop is exclusive
    people_count_url += '&stop=%s' % (stop_date + datetime.timedelta(days=1))

    count_resource = get_resource(people_count_url)

    # datetimes are returned from api in UTC.
    # rather than introduce a dependency on pytz, let's
    # do some date math to determine which count corresponds to which day
    # this won't be necessary once the api supports returning counts in
    # the site's timezone - which is slated for a future release.
    counts = {}
    cur_date = start_date
    cur_index = 0
    while cur_date <= stop_date:
        counts[str(cur_date)] = count_resource['counts'][cur_index]['count']
        cur_date += datetime.timedelta(days=1)
        cur_index += 1
    return counts


def get_resource(url):
    request = urllib2.Request(url)
    request.add_header('Authorization', 'Token %s' % API_KEY)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as err:
        if err.getcode()/10*10 == 400:
            content = json.loads(err.read())
            error_msgs = ', '.join(content['error_messages'])
            raise Exception('API responded with 4XX error: %s' % error_msgs)
        raise
    data = response.read()
    result = json.loads(data)
    return result


def parse_date(date_as_str):
    try:
        dt = datetime.datetime.strptime(date_as_str, '%Y-%m-%d')
    except Exception:
        msg = "Invalid date format: '%s'. Expected format: YYYY-MM-DD"
        raise Exception(msg % date_as_str)
    return dt.date()


def validate_dates(start_date, stop_date):
    if stop_date < start_date:
        raise Exception('Stop date must be after start date')

    if stop_date - start_date > datetime.timedelta(days=120):
        raise Exception('Stop date must not be over 120 past start date')


def compute_dates(start_date, stop_date):
    dates = []
    cur_date = start_date
    while cur_date <= stop_date:
        dates.append(cur_date)
        cur_date += datetime.timedelta(days=1)
    return dates


def print_header(writer, dates):
    cells = [''] + dates
    writer.writerow(cells)


def print_row(writer, site_display_name, site_counts, dates):
    # handle unicode characters in site names
    cells = [codecs.encode(site_display_name, 'utf-8')]
    for cur_date in dates:
        cells.append(site_counts[str(cur_date)])
    writer.writerow(cells)


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

    # parse and validate our input
    start_date = parse_date(args.start_date)
    stop_date = parse_date(args.stop_date)
    validate_dates(start_date, stop_date)
    dates = compute_dates(start_date, stop_date)

    # collect the date from the api
    sites = get_sites()
    counts_by_site = {}
    for site in sites:
        key = '%s - %s' % (site['account_name'], site['name'])
        if site['external_id']:
            key += ' - %s' % site['external_id']
        counts = get_counts(site, start_date, stop_date)
        counts_by_site[key] = counts


    # dump out the response
    writer = csv.writer(sys.stdout)
    print_header(writer, dates)
    for site_display_name, site_counts in counts_by_site.iteritems():
        print_row(writer, site_display_name, site_counts, dates)


if __name__ == '__main__':
    main()
