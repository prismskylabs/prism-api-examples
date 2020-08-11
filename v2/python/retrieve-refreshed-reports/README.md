# Entry count for all sites for a particular hour

This example will show how to retrieve reports that 
have changed since a certain point in time.
Also, this example integration will show how to retrieve counts by date
for particular report configuration in the Prism App.

## Retrieving refreshed reports

Recently Prism App started to update daily reports every hour.
Every hour the daily report is re-calculated to account for new counts
that arrived for that hour.
This example shows how to download reports that were refreshed
since a certain point in time. A typical invocation would ask
to list reports refreshed since an hour ago. However, it is
possible to ask for reports refreshed since any point in time.

Example contains two files:

retrieve-refreshed-reports.py  
retrieve-refreshed-reports.sh

retrieve-refreshed-reports.py  file is a python script implementing all logic
of interaction with Prism REST API to obtain refreshed reports.

retrieve-refreshed-reports.sh file is an example of invocation script which
demonstrates parametrization of invoking retrieve-refreshed-reports.py 
for successful downloading of updated reports.

For running mentioned scripts users need to have installed python 2.7.x,
have it available in PATH.
Also, a user needs to have access to Unix shell. 
Bash is a good option, but the script shall work with any posix shell.
Also, it shall be possible to run a python script from Windows, but 
retrieve-refreshed-reports.sh script then needs to be re-written
to conform to windows shell.


retrieve-refreshed-reports.py has more options than shown in the example invocation.
It is recommended to run it as
$ ./retrieve-refreshed-reports.py --help
in order to see all the parameters.

In order to run a script for retrieving refreshed reports you need to 
fulfill the following steps:

1. In your Prism Account create a report. Note URL by which you access the report in 
Prism App. From URL, you shall be able to derive two important numbers needed 
for retrieving reports:
 - account_id
 - report_configuration_id

When you access your report in Prism App, your URL will look like
https://app.prism.com/<account_id>/reports/<report_configuration_id>/<date>
where account_id and report_configuration_id are integer numbers.
Record these numbers as you need them further to pass to script as parameter
or to form your URL to download report.

2. Reach Prism Support to obtain API key for accessing reports via 
Prism REST API. You may already have such key if you already used 
Prism REST API. In such a case, just use it. You do not need to obtain
another key.

3.  Once you have account_id, report_configuration_id and API key,
go and edit retrieve-refreshed-reports.sh file and substitute there
your values. Once you added these values, you are ready 
to invoke the script. When you edit the file, make sure you do not 
have extra spaces around assignment symbol = . Unix shell variable 
assignment requires no space around assign symbol.
If you insert extra space around =, the script will fail.

$ ./retrieve-refreshed-reports.sh

4. Once you are able to retrieve a report, the next step is 
to adjust reports parametrization for your particular need.
By default, script saves both by-period and by-region reports.
by-period has a period set as 'hour' and by-region
has region set as 'site'.
You can customize these settings. In order to see all possible 
settings run

$ ./retrieve-refreshed-reports.py --help

5. By default refreshed reports are returned for last hour.
It is because we expect this script will be mostly used for retrieving
hourly updates of daily reports and hence it will be run once every hour.
You can change this to say weekly reports to run once every 4 hours or 
once a day.

6. By default script lists reports, then downloads them and
saves into a current folder under names correspondent to dates
and report configuration. The script outputs exact file names
under which reports were saved. Real integration can parse
file name format and read data from those files.

7. Files saved by the script are in json format by default.
It is possible to save as csv format too. Pass

    --format csv

option in order to save all files in csv file format.

8. There are more customizations that are possible if you need that.
Script allows to do the following:
 - Only list refreshed reports without downloading them. An example for past 24 hours:
 
 $ ./retrieve-refreshed-reports.py -k <API_key> -a <account_id> -c <report_configuration_id> -o 24.0 -R "http://api.prismsl.net/v2" -p site -l LIST_ONLY
 
 - Download only by-region or only by-period reports:
 
 $ ./retrieve-refreshed-reports.py -k <API_key> -a <account_id> -c <report_configuration_id> -o 1.0 -R "http://api.prismsl.net/v2" -r site -t by-region
 $ ./retrieve-refreshed-reports.py -k <API_key> -a <account_id> -c <report_configuration_id> -o 1.0 -R "http://api.prismsl.net/v2" -p hour -t by-period
 
 - User can change region type in by-region
 - User can change period type in by-period

# Example of retrieving report by date

Retrieving report by date is demonstrated in the script named
retrieve-report-by-date.sh

It uses curl command to do that and it requires it to be 
available in PATH.

In order to execute this script successfully you also need to get
account_id, report_configuration_id and API key as mentioned 
in the previous example.
Once you have this data, edit retrieve-report-by-date.sh and
inject there your parameters. Once ready, execute the script
and you shall be able to retrieve a report for the date
indicated in that script.

For more information, consult the Prism API v2 documentation.
If you have any questions, please, contact Prism Support at support@prism.com.
