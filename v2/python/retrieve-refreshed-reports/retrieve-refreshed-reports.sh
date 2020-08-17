
# Example for invocation of retrieve-refreshed-reports.py script
# This script can be invoked from anywhere  and it will
# execute retrieve-refreshed-reports.py and will save 
# reports into designated destimation directory

SCRIPTS_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

API_ROOT="https://api.prismsl.net/v2"   
AUTH_KEY=<key>       # API key
ACCOUNT=7            # account_id
REPORT_CFG=123       # report_configuration_id
HOURS_BACK="1.0"     # 1.0 - for one hour ago, 24.0 - twenty four hours ago...
BY_PERIOD=hour       # possible values: day, hour, minute-15
BY_REGION=site       # possible values: site, province, country, datalabel
DEST_DIR=./
SAVED_RPRT_TYPES=all # possible values: by-period, by-region, all
FORMAT=json          # possible values: csv, json


$SCRIPTS_DIR/retrieve-refreshed-reports.py \
    --api-root $API_ROOT \
    --key $AUTH_KEY \
    --account $ACCOUNT \
    --report-configuration $REPORT_CFG \
    --offset $HOURS_BACK \
    --saved-report-types $SAVED_RPRT_TYPES \
    --by-period-type $BY_PERIOD \
    --by-region-type $BY_REGION \
    --destination-dir $DEST_DIR \
    --format $FORMAT


