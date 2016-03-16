# Entry count per Day per Site

This example integration generates a CSV of entry counts for all
your sites per day, over a given date range.

## Parameters

 * start date, in ISO 8601 format
 * stop date, in ISO 8601 format

## Environment Variables

 * If the environment variable `PRISM_API_KEY` is set, the script will use
   this API key.

## Output

 * a csv of the results is dumped to stdout

## Example

```shell
$ export PRISM_API_KEY='your-api-key-here'
$ ./generator.py 2015-02-12 2015-02-15 > counts.csv
$ cat counts.csv
,2015-02-12,2015-02-13,2015-02-14,2015-02-15
Prism Test Account - London Store - 42,343,454,565,676
Prism Test Account - Buenos Aires - 43,234,345,456,567
```

For more options, please run `./generatory.py --help`.
