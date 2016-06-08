#!/usr/bin/env python

# using only standard library packages for this example.
# if you're building out a deeper integration in python,
# you may want to consider using requests
# http://docs.python-requests.org/en/latest/
import argparse
import datetime
import json
import os
import urllib
import urllib2


API_ROOT = 'https://api.prism.com/v2'
API_KEY = os.environ.get('PRISM_API_KEY', None)

if not API_KEY:
    raise Exception('Environment variable PRISM_API_KEY not defined')


def query_api(url):
    "Do a GET request-response cycle with the api"
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


def test_api_connection(account_id):
    "Ensure we have authentication/permission to the api & that account"
    url = API_ROOT + '/accounts/{}/'.format(account_id)
    try:
        result = query_api(url)
        if result['id'] != account_id:
            raise Exception('API responded with unexpected response')
    except Exception:
        raise Exception("Unable to access that Account resource on API. "
                        "Is your API Key correct and does it have access "
                        "to that account?")


def get_entry_zone_id(account_id):
    "Get the entry zone id for that account"
    url = API_ROOT + '/accounts/{}/zones/?name=entry'.format(account_id)
    result = query_api(url)
    if len(result) != 1:
        raise Exception('Did not find one entry zone on API')
    return result[0]['id']


def get_site_ids(account_id, external_id, label):
    "Get a list of all the site ids for that account"
    url = API_ROOT + '/accounts/{}/sites/'.format(account_id)
    query_params = []
    if external_id is not None:
        query_params += [('external_id', external_id)]
    if label is not None:
        query_params += [('label', label)]
    if query_params:
        url += '?' + urllib.urlencode(query_params)
    result = query_api(url)
    site_ids = [site['id'] for site in result]
    return site_ids


def get_hour_counts(account_id, zone_id, site_ids, hour_start):
    "Get a json object with the hour counts from the api"
    hour_stop = hour_start + datetime.timedelta(hours=1)

    query_params = [('site_id', sid) for sid in site_ids]
    query_params += [
        ('metric', 'count'),
        ('business_hours_only', 'true'),
        ('start', hour_start.isoformat() + 'Z'),
        ('stop', hour_stop.isoformat() + 'Z'),
        ('zone_id', zone_id),
    ]
    url = API_ROOT + '/data/by-site/?' + urllib.urlencode(query_params)

    result = query_api(url)
    return result


def main():

    def str_to_dt(dt_str):
        return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H')

    parser = argparse.ArgumentParser(
        description=("This example integration will write a json object to "
                     "stdout of containing entry counts within business "
                     "hours over a particular hour for all sites within "
                     "a specified account."),
    )
    parser.add_argument(
        '-a', '--account', type=int, required=True,
        help="ID of Prism Account to query api for.",
    )
    parser.add_argument(
        '--hour', type=str_to_dt, required=False,
        help=("UTC datetime with hour resolution in ISO 8601 format. "
              "Example: '--hour 2016-03-01T09'. "
              "If not provided, this will default to the beginning of "
              "the last hour that has most recently fully completed."),
    )
    parser.add_argument(
        '-e', '--external-id', type=str, required=False,
        help="Only query sites with this external ID.",
    )
    parser.add_argument(
        '-l', '--label', type=str, required=False,
        help="Only query sites with this label.",
    )

    args = parser.parse_args()
    if args.hour:
        hour = args.hour
    else:
        now = datetime.datetime.utcnow()
        hour = now - datetime.timedelta(hours=1, minutes=now.minute,
                                        seconds=now.second,
                                        microseconds=now.microsecond)

    test_api_connection(args.account)
    zone_id = get_entry_zone_id(args.account)
    site_ids = get_site_ids(args.account, args.external_id, args.label)
    hour_counts = get_hour_counts(args.account, zone_id, site_ids, hour)

    msg_str = ("\nFor the hour starting at {hour}, here are the entry counts\n"
               "within business hours for {which_sites} in account #{act_id}.\n"
               "Note that a value of 'null' indicates the hour is completely outside\n"
               "of business hours for that site.\n")

    if args.external_id is None and args.label is None:
        which_sites = 'all sites'
    elif args.external_id is not None and args.label is not None:
        which_sites = "sites with external_id '{}' and label '{}'".format(args.external_id, args.label)
    elif args.external_id:
        which_sites = "sites with external_id '{}'".format(args.external_id)
    elif args.label:
        which_sites = "sites with label '{}'".format(args.label)

    msg_kwargs = {
        'hour': hour.isoformat(),
        'which_sites': which_sites,
        'act_id': args.account,
    }
    print msg_str.format(**msg_kwargs)
    print json.dumps(hour_counts, sort_keys=True, indent=4,
                     separators=(',', ': '))


if __name__ == '__main__':
    main()
