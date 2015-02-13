# Entry count per Day per Site

This example integration generates a CSV of entry counts for all
your sites per day, over a given date range.

## Parameters

 * start date, in ISO 8601 format
 * stop date, in ISO 8601 format

## Environment Variables

 * If the environemnt variable `PRISM_API_KEY` is set, the script will use
   this api key.

## Output

 * a csv of the results if dumped to stdout

## Example

```shell
$ export PRISM_API_KEY=':your-api-key-here'
$ ./generator.py 2014-02-12 2015-02-15
,2014-02-12,2014-02-13,2014-02-14,2014-02-15
London Store (#42),343,454,565,676
Buenos Aires (#43),234,345,456,567
```

For more options, please run `./generatory.py --help`.
