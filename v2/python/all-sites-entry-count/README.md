# Entry count for all sites for a particular hour

This example integration will write a json object to stdout of containing
entry counts within business hours over a particular hour for all sites
within a specified account.

## Example 1

```
$ export PRISM_API_KEY='your-api-key-here'
$ ./retrieve-counts.py --hour 2016-03-15T18 -a 471 -e UK

For the hour starting at 2016-03-15T18:00:00, here are the entry counts
within business hours for sites with external_id 'UK' in account #471.
Note that a value of 'null' indicates the hour is completely outside
of business hours for that site.

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

## Example 2

```
$ export PRISM_API_KEY='your-api-key-here'
$ ./retrieve-counts.py --hour 2016-03-15T18 -a 471 -l UK

For the hour starting at 2016-03-15T18:00:00, here are the entry counts
within business hours for sites with label 'UK' in account #471.
Note that a value of 'null' indicates the hour is completely outside
of business hours for that site.

[
    {
        "count": 7,
        "site_id": 504
    },
    {
        "count": null,
        "site_id": 1059
    },
    {
        "count": 23,
        "site_id": 1060
    },
]
```

For more information and options, please run `./retrieve-counts.py --help`
or consult the Prism API v2 documentation.
