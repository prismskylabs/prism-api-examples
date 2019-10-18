#!/usr/bin/env python

from __future__ import print_function
import sys
import argparse
import datetime
import json
import os
import urllib
import urllib2


def print2err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class ObjFromDict(object):
    def __init__(self, a_dict):
        self.__dict__ = a_dict
        
class RetrieveRefreshedReports:
    def __init__(self, args):
        self.API_ROOT = args.api_root
        self.API_KEY= args.key
        self.offset = args.offset
        self.cfg_id = args.report_configuration
        self.account_id = args.account
        self.by_period_val = args.by_period_type
        self.by_region_val = args.by_region_type
        self.dest_dir = args.destination_dir
        self.list_only = args.list_only
        self.saved_report_types = args.saved_report_types
        
        change_since = datetime.datetime.utcnow() - datetime.timedelta(seconds=int(args.offset*3600))
        self.change_time_str = change_since.strftime('%Y-%m-%dT%H:%M')
        
    def query_api_raw(self, url):
        "Do a GET request-response cycle with the api"
        request = urllib2.Request(url)
        request.add_header('Authorization', 'Token %s' % self.API_KEY)
        request.add_header('period', 'hour')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as err:
            if err.getcode()/100*100 == 400:
                err_data = err.read()
                try:
                    content = json.loads(err_data)
                except Exception as ex:
                    print2err("Error decoding json. Error: %s, Json data: %s" %(str(ex), err_data))
                    raise Exception('API responded with 4XX error: %s' % str(err_data))
                error_msgs = ', '.join(content['error_messages'])
                raise Exception('API responded with 4XX error: %s' % error_msgs)
            raise
        data = response.read()
        return data

    def query_api(self, url):
        "Do a GET request-response cycle with the api"
        data = self.query_api_raw(url)
        try:
            result = json.loads(data)
        except Exception as ex:
            print2err("Error decoding json. Error: %s, Json data: %s" %(str(ex), data))
        return result        
        
    def test_api_connection(self, account_id):
        "Ensure we have authentication/permission to the api & that account"
        url = self.API_ROOT + '/accounts/{}/'.format(account_id)
        try:
            result = self.query_api(url)
            if result['id'] != account_id:
                raise Exception('API responded with unexpected response')
        except Exception as ex:
            raise Exception("Unable to access that Account resource on API. "
                            "Is your API Key correct and does it have access "
                            "to that account? Low level exception:", ex)
    
    def retrieve_refreshed_reports_meta(self):
        """ Get a json object with refreshed reports urls and other meta
            Sample url to get reports:
            http://api.test/v2/accounts/7/report-configurations/2/reports/changed-since/2018-11-30T20:31/
        """
        url =   (self.API_ROOT + 
                    ('/accounts/%d/report-configurations/%d/reports/changed-since/%s/' %
                        (int(self.account_id), int(self.cfg_id), self.change_time_str)
                    )
                 )
        
        result = self.query_api(url)
        return result

    def retrieve_single_refreshed_report(self, url):
        """ Get a json object with refreshed reports urls and other meta
            Sample url to get reports:
            http://api.test/v2/accounts/7/report-configurations/2/reports/changed-since/2018-11-30T20:31/
        """
        url =   (self.API_ROOT + 
                    ('/accounts/%d/report-configurations/%d/reports/changed-since/%s/' %
                        (int(self.account_id), int(self.cfg_id), self.change_time_str)
                    )
                 )
        
        result = self.query_api(url)
        return result
    
    def filename_by(self, start_date, str_kind, kind_val):
        filename = ( 'report__rc=%d__start=%s__by-%s=%s.json' % 
            (int(self.cfg_id), start_date, str_kind, kind_val ))
        filename = os.path.join(self.dest_dir, filename)
        return filename
    
    def save_by_period_json(self, report):
        url = report.by_period_data_url + '?period=' + self.by_period_val
        print('  Downloading by period report with period={0},'.format(self.by_period_val), 
              'start={0}'.format(report.start_date))
        by_period_data = self.query_api_raw(url)
        filename = self.filename_by(report.start_date, 'period', self.by_period_val)
        print('   into file: ', filename, ' ...', end='')
        
        with open(filename, 'w') as fp:
            fp.write(by_period_data)
        print(' Done')
            
        #print ("by_period_data data = " + str(by_period_data))
    def save_by_region_json(self, report):
        url = report.by_region_data_url + '?region=' + self.by_region_val
        print('  Downloading by region report with region={0},'.format(self.by_region_val), 
              'start={0}'.format(report.start_date))
        by_region_data = self.query_api_raw(url)
        filename = self.filename_by(report.start_date, 'region', self.by_region_val)
        print('   into file: ', filename, ' ...', end='')
        
        with open(filename, 'w') as fp:
            fp.write(by_region_data)
        print(' Done')
        
    def download_reports(self, reports):
        print('Downloading reports...')
        for report in reports:
            report = ObjFromDict(report)
            if self.saved_report_types == 'by-period' or self.saved_report_types == 'all':
                self.save_by_period_json(report)
            if self.saved_report_types == 'by-region' or self.saved_report_types == 'all':
                self.save_by_region_json(report)
        print('Download of refreshed reports complete')
    
    def run(self):
        self.test_api_connection(self.account_id)
        reports = self.retrieve_refreshed_reports_meta()
        #print('Json with reports: ' + str(reports))
        print('Reports refreshed since %s:00+00:00 for report configuration = %d: ' % 
              (self.change_time_str, int(self.cfg_id)))
        print('     id,   start_date,  stop_date')
        
        for report in reports:
            report = ObjFromDict(report)
            s = '%7s,   %s,  %s' % (report.id, report.start_date, report.stop_date)
            print( s )

        if not self.list_only:
            self.download_reports(reports)
            

def main():

    #def str_to_dt(dt_str):
    #    return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')

    parser = argparse.ArgumentParser(
        description=("This script will list, retrieve and save reports from Prism Cloud that have been updated "
                     "since given point in time. Reports are typically updated due to new data arriving from "
                     "cameras. Currently daily report will have update every hour within about 15-20 min after "
                     " hour completion. Also any report "
                     "can be updated if information from camera arrived for its time range. "
                     "One of possible reasons of update is end of network outage, when camera "
                     "uploads information it accumulated during time it was not able to reach Prism Cloud." 
                     "This script works with single report configuration and it will retrieve reports "
                     "that were updated for that configuration. For daily kind of reports it, for example, "
                     "may include today's report, yesterday and and 4 days back report. "
                     "This script is needed because due to different sites timezones, particular "
                     "report that need to be refreshed is not just the last one. Also, number of "
                     "reports to refresh may vary with time of day and because of camera network outages."),
    )
    parser.add_argument(
        '-k', '--key', type=str, required=True,
        help="Authorization API key that provides access to Prism REST API usage.",
    )
    parser.add_argument(
        '-a', '--account', type=int, required=True,
        help="Id of Prism Account to query api for.",
    )
    parser.add_argument(
        '-c', '--report-configuration', type=int, required=True,
        help=("Id of report configuration in your Prism Account"),
    )
    parser.add_argument(
        '-o', '--offset', type=float, required=False, default=1.0,
        help=("Time offset from now back in time since which refreshed reports will be scanned and retrieved. "
              "Value is in hours with about two digits of floating point precision. "
              "Reports on cloud side typically will refresh every hour within 15-20 min. "
              "After that reports become visible to this api."
              "Default value is 1.0 hour. It assumes this script runs every hour."),
    )
    parser.add_argument(
        '-R', '--api-root', type=str, required=False, default='https://api.prismsl.net/v2',
        help="API root for flexible testing. Default value: 'https://api.prismsl.net/v2'",
    )
    parser.add_argument(
        '-p', '--by-period-type', type=str, required=False, default='hour',
        help="Possible values: minute-15, hour, day",
    )
    parser.add_argument(
        '-r', '--by-region-type', type=str, required=False, default='site',
        help="Possible values: site, province, country, datalabel",
    )
    parser.add_argument(
        '-t', '--saved-report-types', type=str, required=False, default='all',
        help="Possible values: by-period, by-region, all",
    )
    parser.add_argument(
        '-d', '--destination-dir', type=str, required=False, default='./',
        help="Destination directory where to write files with reports in json format. "
        " Defaults to current directory",
    )
    
    parser.add_argument(
        '-l', '--list-only', 
        help="Only list refreshed reports. Do not attempt to download them. ",
    )

    args = parser.parse_args()
    retrive_reports = RetrieveRefreshedReports(args)
    retrive_reports.run()


if __name__ == '__main__':
    main()
