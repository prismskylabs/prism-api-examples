# Entry count for all sites for a particular hour

This example will show how to retrieve for reports that 
changed since certain point in time.
Also, this example integration will show how to retrieve counts by date 
for particular report configuration in Prism App.

## Retrieving refreshed reports

Recently Prism App started to refresh daily reports every hour.
Every hour daily report is re-calculated to account for counts
data that arrived for that hour.
This example shows how to download reports that were refreshed
since certain point in time. Typical invocation would ask
to list reports refreshed since hour ago. However, it is
possible to ask for reports refreshed since any point in time.

Example contains two files:

retrieve-refreshed-reports.py  
retrieve-refreshed-reports.sh

retrieve-refreshed-reports.py  file is python script implementing all logic
of iteraction with Prism REST API to obtain refreshed reports.

retrieve-refreshed-reports.sh file is example invocation script which
demonstrates parametrization of invoking retrieve-refreshed-reports.py 
for succesful downloading of refreshed reports.

For running mentioned scripts user needs to have installed python 2.7.x,
have it available in PATH.
Also, user needs to have access to some unix shell. 
Bash is a good option, but script shall work with any posix shell.
Also, it shall be possible to run python script from Windows, but 
retrieve-refreshed-reports.sh script then needs to be re-written
to conform to windows shell.


retrieve-refreshed-reports.py has more options than shown in example invocation.
It is recommended to run it as
./retrieve-refreshed-reports.py --help

in order to see all the parameters.

In order to run script for retrieving refreshed reports you need to 
fullfill the following steps:

1. In your Prism Account create report. Note URL by which you access report in 
Prism App. From URL, you shall be able to derive two important numbers needed 
for retrieving reports:
 - account_id
 - report_configuration_id
When you access your report in Prism App, your URL will look like
https://app.prism.com/<account_id>/reports/<report_configuration_id>/<date>
where account_id and report_configuration_id are integer numbers.
Record these numbers as you need them further.

2. Reach Prism Support to obtain API key for accessing reports via 
Prism REST API. You may already have such key if you already used 
Prism REST API. In such case, just use it. You do not need to 
obtain another key.

3.  Once you have account_id, report_configuration_id and API key,
    go and edit retrieve-refreshed-reports.sh file and substitute
    there your values. Once you added these values, you are ready
    to invoke the script. When you edit the file, make sure you do not 
    have extra spaces around assignment symbol = . Unix shell variable 
    assignment requires no space around assign symbol.
    If you insert extra space around =, script will fail.

4. Once you are able to retrieve some reports, next step is 
to adjust reports parametrization for your particular  need.
By default, script saves both by-period and by-region reports.
by-period has period set as 'hour' and 
by-region has region set as 'site'.
You can customize these settings. In order to see all possible 
settings run
./retrieve-refreshed-reports.py --help

5. By default refreshed reports are returned for last hour.
It is because we expect this script will be mostly used for retrieving
hourly updates of daily reports and hence it will be run once every hour.
You can change this for say weekly reports to run once every 4 hours or 
once a day.

6. By default script lists reports, then downloads them 
and saves into current folder under names correspondent to dates
and report configuration. Script outputs exact file names
under which reports were saved. Real integration can 
parse  file name format and read data from those files.

7.There are more customizations that are possible if you need that.
Script allows to do the following:
 - Only list refreshed reports without downloading them
 - Download only by-region or only by-period reports.
 - User can change region type in by-region
 - User can change period type in by-period


# Example of retrieving report by date

Retrieving report by date is demonstrated in script named
retrieve-report-by-date.sh

It uses curl command to do that and it requires it to be 
available in PATH.

In order to execute this script successfully you also need to get
account_id, report_configuration_id and API key as mentioned 
in previous example.
Once you have this data, edit retrieve-report-by-date.sh and
inject there your parameters. Once ready, execute the script
and you shall be able to retrieve report for the date
indicated in that script.

For more information, consult the Prism API v2 documentation.
If you have any questions, please, contact Prism Support.

