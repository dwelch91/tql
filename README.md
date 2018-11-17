## tql - Read, Modify, and Generate Tabular Data 
Inspired by the`q` tool (https://harelba.github.io/q/)...

### Features
* Support for reading of CSV, TSV, HTML, JSON, LTSV, Markdown, MediaWiki, Excel, etc. formats
* Extensive support for data pre-filtering, conversions, etc. of input data before it is added to database
* Full support for all of SQLite features
* Support for writing in CSV, TSV, Excel, LaTex, Markdown, JSON, rst, TOML, etc. formats
* Create database, add data to existing database, or use in-memory database
* Table name remapping
* Column name remapping
* Automatic or user specified headers/column names
* Full Python 3.5+ support (sorry, no Python 2.x support)
* MIT license

### Planned Features
* Input from stdin
* Regex-based filters
* Locale based filters
* Encodings support
* CSV column merging and splitting
* Modification queries (TBD)
* Callable API

### Installation


### Documentation

#### Usage

In a nutshell:

`tql "<SQL>" [options]`

Where the `<SQL>` is standard SQLite compatible SQL with the following modifier - when loading CSV data into a table,
use the format `@<filename>` (for `<filename>`s w/o spaces), `@"<filename>"` or `@'<filename>'` 
in the place of table names in `FROM` clause(s).

Example:

`tql "SELECT filename, size FROM @./data.csv WHERE size > 1024 SORT BY size DESC;" --auto-filter` 

#### Detailed Usage

```
tql [-h] 
    [--dialect {excel,excel-tab,unix}]
    [--delimiter DELIMITER] [--quotechar QUOTECHAR]
    [--output OUTPUT] [--output-format {table,csv}]
    [--save-db SAVE_DB | --load-db LOAD_DB]
    [--skip-lines SKIP_LINES] [--headers HEADERS]
    [--debug] [--filter FILTER] [--auto-filter]
    [--filter-list] [--remap-column REMAP_COLUMN]
    [--remap-table REMAP_TABLE]
    [sql [sql ...]]

positional arguments:
  sql                   The SQL to execute. Use filenames surrounded by single
                        or double quotes to specify CSV sources instead of
                        existing tables in the FROM clause(s). You can use
                        [:...:] replacements for special characters (see
                        --help-filters for more information.

optional arguments:
  -h, --help            show this help message and exit
  --dialect {excel,excel-tab,unix}, -t {excel,excel-tab,unix}
                        Specify the CSV dialect. Valid values are excel,
                        excel-tab, unix. Default is `unix`.
  --delimiter DELIMITER, -d DELIMITER
                        Specify the CSV delimiter to use. Default is a comma
                        (,).
  --quotechar QUOTECHAR, --quote-char QUOTECHAR, -q QUOTECHAR
                        Specify the CSV quote charactor. Default is double
                        quote (").
  --output OUTPUT, -o OUTPUT
                        Output file. Default is stdout (-).
  --output-format {table,csv}, --out-format {table,csv}, --out-fmt {table,csv}, -f {table,csv}
                        Output format. Valid value are 'table' and 'csv'.
                        Default is table.
  --save-db SAVE_DB, -s SAVE_DB
                        Specify a SQLite database to use (instead of using an
                        in-memory database. The database will remain after tql
                        exits.
  --load-db LOAD_DB, -l LOAD_DB
                        Load an existing database instead of creating a new
                        one.
  --skip-lines SKIP_LINES, --skip SKIP_LINES, -k SKIP_LINES
                        Skip `SKIP_LINES` lines at the beginning of the file.
                        Default is 0.
  --headers HEADERS, -r HEADERS
                        Don't use the first non-skipped line for header/column
                        names, use these header/column names instead. Format
                        is a comma separated list of column names. Column
                        names must not be SQLite reserved words.
  --debug, -g           Turn on debug output.
  --filter FILTER, -e FILTER
                        Specify a column filter. Use one filter per
                        switch/param. Format is <column_name>|filter|<0 or
                        more params or additional filters in filter chain>.
                        Filters have a variable number of parameters (0+).
                        Filters may be chained.
  --auto-filter, -a     Automatically apply the `num` filter to all column
                        data.
  --filter-list, --help-filters
  --remap-column REMAP_COLUMN, --remap-header REMAP_COLUMN, -m REMAP_COLUMN
                        A single column re-map in the form
                        <col_name>=<new_col_name>. Use one switch for each
                        column re-mapping. This overrides any column/header
                        names that are auto-discovered or passed in via
                        --headers/-r. You can use [:...:] replacements for
                        special characters (see --help-filters for more
                        information.
  --remap-table REMAP_TABLE, --remap-file REMAP_TABLE, -T REMAP_TABLE
                        A single table re-map in the form
                        <table_name>=<new_table_name>. Use one switch for each
                        table re-mapping. This overrides any table names that
                        are auto-generated from filenames passed in via the
                        SQL statement. You can use [:...:] replacements for
                        special characters (see --help-filters for more
                        information.
```

#### Data Filtering

#### Available Data Filters

| Filter      | Num. Params | Syntax                             | In type  | Out type | Description                                               |
|-------------|-------------|------------------------------------|----------|----------|-----------------------------------------------------------|
| abs         | 0           | <column_name>\|abs                  | num      | num      | Take the absolute value of a number.                      |
| add         | 1           | <column_name>\|add\|\<value\>          | num      | num      | Add \<value\> to number.                                    |
| capitalize  | 0           | <column_name>\|capitalize           | str      | str      | Capitalize string.                                        |
| ceil        | 0           | <column_name>\|ceil                 | num      | num      | Return the ceiling value of a number.                     |
| center      | 1           | <column_name>\|center|\<width\>     | str      | str      | Center string in width of \<width\> spaces.               |
| datetime    | 0           | <column_name>\|datetime             | str      | datetime | Parse a datetime string.                                  |
| datetime_tz | 1           | <column_name>\|datetime_tz\|\<tz\>     | str      | datetime | Prase a datetime string with the specified \<tz\> timezone. |
| dehumanize  | 0           | <column_name>\|dehumanize           | str      | num      | Convert from human string to number.                      |
| div         | 1           | <column_name>\|div\|\<value\>          | num      | num      | Divide number by \<value\>.                                 |
| float       | 0           | <column_name>\|float                | str      | float    | Convert to float.                                         |
| floor       | 0           | <column_name>\|floor                | num      | num      | Return the floor value of a number.                       |
| format      | 1           | <column_name>\|format\|\<format\>      | str      | str      | Format data using Python's `format(\<format\>)` function.   |
| humanize    | 1           | <column_name>\|humanize\|\<unit\>      | num      | str      | Format number to human string.                            |
| int         | 0           | <column_name>\|int                  | str      | int      | Convert to integer.                                       |
| iso8601     | 0           | <column_name>\|iso8601              | datetime | str      | Convert a datetime to an ISO8601 string representation.   |
| length      | 0           | <column_name>\|length               | str      | str      | Return the length of the string.                          |
| ljust       | 1           | <column_name>\|ljust\|\<width\>        | str      | str      | Left justify string in \<width\> spaces.                    |
| lstrip      | 1           | <column_name>\|lstrip\|\<chars\>        | str      | str      | Remove characters from left.                     |
| lower       | 0           | <column_name>\|lower                | str      | str      | Convert string to lowercase.                              |
| mult        | 1           | <column_name>\|mult\|\<value\>         | num      | num      | Multiply number by \<value\>.                               |
| num         | 0           | <column_name>\|num                  | str      | num      | Convert to integer or float.                              |
| number      | 0           | <column_name>\|number               | str      | num      | Convert to integer or float.                              |
| ordinal     | 0           | <column_name>\|ordinal              | num      | str      | Convert number to ordinal string.                         |
| prefix      | 1           | <column_name>\|prefix\|\<prefix\>      | str      | str      | Prefix the string with \<prefix\>.                          |
| replace     | 2           | <column_name>\|replace\|\<from\>\|\<to\>  | str      | str      | Replace sub-string \<from\> with \<to\>.                      |
| reverse     | 0           | <column_name>\|reverse              | str      | str      | Reverse the characters in the string.                     |
| rjust       | 1           | <column_name>\|rjust\|\<width\>        | str      | str      | Right justify string in \<width\> spaces.                   |
| rstrip      | 1           | <column_name>\|rstrip\|\<chars\>        | str      | str      | Remove characters from right.                   |
| round       | 1           | <column_name>\|round\|\<digits\>       | num      | num      | Round number to \<digits\> digits.                          |
| str         | 0           | <column_name>\|str                  | any      | str      | Convert to string.                                        |
| strftime    | 1           | <column_name>\|strftime\|\<format\>    | datetime | str      | Format a datetime using `strftime(\<format\>)`.             |
| sub         | 1           | <column_name>\|sub\|\<value\>          | num      | num      | Subtract \<value\> from number.                             |
| substr      | 2           | <column_name>\|substr\|\<start\>\|\<end\> | str      | str      | Return a sub-string.                                      |
| suffix      | 1           | <column_name>\|suffix\|\<suffix\>      | str      | str      | Suffix the string with \<suffix\>.                          |
| swapcase    | 0           | <column_name>\|swapcase             | str      | str      | Swap string case.                                         |
| thousands   | 0           | <column_name>\|thousands            | num      | str      | Format number with thousands separators.                  |
| title       | 0           | <column_name>\|title                | str      | str      | Convert string to title case.                             |
| trunc       | 0           | <column_name>\|trunc                | num      | num      | Return the number truncated.                              |
| tz          | 1           | <column_name>\|tz\|\<tz\>              | datetime | datetime | Convert a datetime to a new \<tz\> timezone.                |
| upper       | 0           | <column_name>\|upper                | str      | str      | Convert string to uppercase.                              |
| utc         | 0           | <column_name>\|utc                  | datetime | datetime | Convert a datetime to UTC.                                |
| zfill       | 1           | <column_name>\|zfill\|\<width\>        | str      | str      | Zero fill string to \<width\> size.                         |

Notes: 

Most filters that take numeric inputs will automatically apply the `num` filter to the column data prior to filtering.

Filters can be chained together using the pipe (|) character. For example, `c1|num|add|1|human`

The type of the data after the last filter has run will be the type that is added to the database.


#### Auto Filtering

#### Column Remapping

#### Table Remapping

#### Character Replacements

| Sequence        | Character Replacement  |
|-----------------|------------------------|
| `[:space:]`     | Space (` `)            |
| `[:pipe:]`      | Pipe (`\|`)            |
| `[:backslash:]` | Blackslash (`\`)       |
| `[:backtick:]`  | Backtick (`)           |
| `[:squote:]`    | Single quote (`'`)     |
| `[:dquote:]`    | Double quote (`"`)     |
| `[:tab:]`       | Tab (`\t`)             |
| `[:cr:]`        | Carriage return (`\r`) |
| `[:newline:]`   | Newline (`\n`)         |
| `[:n:]`         | Newline (`\n`)         |
| `[:comma:]`     | Comma (`,`)            |
| `[:colon:]`     | Colon (`:`)            |
| `[:amp:]`       | Ampersand (`&`)        |
| `[:ampersand:]` | Ampersand (`&`)        |
| `[:gt:]`        | Greater than (`>`)     |
| `[:lt:]`        | Less than (`<`)        |

#### Save Database

#### Load Database

#### Output Formats

#### Use Cases

##### CSV -> filter/sort/aggregate/etc (SQL) -> CSV (or table)
Without `-s`/`--save-db` or `-l`/`--load-db`, `tql` will load the CSV into an in-memory database, perform the SQL query, 
and output the result in the chosen output format.  If the data set is too large for memory, use `-s`/`--save-db` to force
`tql` to use a on-disk database and will only then be limited by available disk space and/or SQLite database size limitations.

##### CSV -> filter/sort/aggregate/etc (SQL) -> database -> CSV (or table)
Using `-s`/`--save-db` will force `tql` to retain an on-disk database of the loaded CSV data. 
It will still produce results in the chosen output format. 
The database can then be used in subsequent `-l`/`--load-db` workflows or manipulated using any desired SQLite database tool.

##### CSV - database -> filter/sort/aggregate/etc (SQL) -> database -> CSV (or table)
Using the `-l`/`--load-db` switch will cause `tql` to load an existing database and load the CSV data into a new table in the database. 
It will still produce results in the chosen output format. The database can then be used in subsequent `-l`/`--load-db` 
workflows or manipulated using any desired SQLite database tool.

##### Database -> filter/sort/aggregate/etc (SQL) -> CSV (or table)
Using the `-l`/`--load-db` switch will cause `tql` to load an existing database. If using regular tables for the 
`FROM` clauses (ie, non-CSV files), the specified SQL will be run against the database and a CSV (or table) will
produce results in the chosen output format. 

### FAQs

#### How do I change the order of the columns in the output?
Use `SELECT` with the column names listed out; the order which they appear will produce output columns in the same order. 

#### How do I filter, sort, etc on a numeric column?
`tql` does not automatically convert CSV data into integers or floats. 
There are two options:
1. Coerce the data to either an integer or float using a filter (e.g., `int`) on the target column and then SQLite will be able to 
operate on the column as a numeric value for sorting, comparisons, etc.
2. Use the `-a`/`--auto-filter` switch that will try to convert all column data to numeric values. Data that cannot be converted
to a numeric value will remain a string.

### Acknowledgements

Python (https://www.python.org/)

SQLite (https://www.sqlite.org/index.html)

Pendulum (https://pendulum.eustace.io/)

pytablereader (https://github.com/thombashi/pytablereader)

pytablewriter (https://github.com/thombashi/pytablewriter)
