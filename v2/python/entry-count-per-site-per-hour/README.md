# Entry count per Day per Site

This example integration will dump a json object to stdout of containing
entry counts within business hours over a particular hour for all sites
within a specified account.

## Required Parameters

 * -a ACCOUNT, --account ACCOUNT
   ID of Prism Account to query api for.

## Optional Parameters

 * --hour HOUR
   UTC datetime with hour resolution in ISO 86001 format.
   Example: '--hour 2016-03-01T09'. If not provided, this
   will default to the beginning of the last hour that
   has most recently fully completed.

## Environment Variables

 * If the environment variable `PRISM_API_KEY` is set, the script will use
   this API key.

## Output

 * Some descriptive text and a json object containing the counts
   will be written to stdout.

## Example

```
$ export PRISM_API_KEY='your-api-key-here'
$ ./retrieve-hour-counts.py --hour 2016-03-15T18 -a 471

For the hour starting at 2016-03-15T18:00:00, here are the entry counts
within business hours for all sites in account #471. Note that a
value of 'null' indicates the hour is completely outside of business
hours for that site.

[
    {
        "count": 7,
        "site_id": 504
    },
    {
        "count": null,
        "site_id": 1059
    }
]
```

For more options, please run `./retrieve-hour-counts.py --help`.
