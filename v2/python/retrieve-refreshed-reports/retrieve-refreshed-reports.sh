
# Example for invocation of retrieve-refreshed-reports.py script
# This script can be invoked from anywhere  and it will
# execute retrieve-refreshed-reports.py and will save 
# reports into designated destimation directory

SCRIPT=$(readlink -f "$0")    # Absolute path to this script
SCRIPTS_DIR=$(dirname "$SCRIPT")

API_ROOT="http://api.prism.com/v2"  #  "http://api.test/v2"
AUTH_KEY=<key>  # API key
ACCOUNT=7       # account_id
REPORT_CFG=2    # report_configuration_id
HOURS_BACK="1.0"
BY_PERIOD=hour
BY_REGION=site
DEST_DIR=./
SAVED_RPRT_TYPES=all

$SCRIPTS_DIR/retrieve-refreshed-reports.py \
    --api-root $API_ROOT \
    --key $AUTH_KEY \
    --account $ACCOUNT \
    --report-configuration $REPORT_CFG \
    --offset $HOURS_BACK \
    --saved-report-types $SAVED_RPRT_TYPES \
    --by-period-type $BY_PERIOD \
    --by-region-type $BY_REGION \
    --destination-dir $DEST_DIR

