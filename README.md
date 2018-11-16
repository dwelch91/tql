# Text Query Language (tql)
Inspired by the`q` tool (https://harelba.github.io/q/) but with some major differences.

### Features
* Extensive support for data pre-filtering, conversions, etc. of CSV/TSV data before it is added to database
* Full support for all of SQLite features
* Pretty table output (Markdown-compatible)
* CSV output
* Database output
* Add data to existing database
* Table remapping
* Column remapping
* Automatic or user specified headers/column names
* Full Python 3.5- support (sorry, no Python 2.x support)
* MIT license

### Planned Features
* Modification queries (TBD)
* Regex-based filters
* Input from stdin
* Column merging and splitting

### Installation


### Documentation

#### Usage

In a nutshell:

`tql "<SQL>" [options]`

Where the `<SQL>` is standard SQLite compatible SQL with the following modifier - when loading CSV data into a table,
use the format `@<filename>` (for `<filename>`s w/o spaces), `@"<filename>"` or `@'<filename>'` 
in the place of table names in `FROM` clauses.

Example:

`tql "SELECT filename, size FROM @./data.csv WHERE size > 1024 SORT BY size DESC;" --auto-filter` 

#### Detailed Options/Parameters

#### Data Filtering

#### Available Data Filters

| Filter      | Num. Params | Syntax                             | In type  | Out type | Description                                               |
|-------------|-------------|------------------------------------|----------|----------|-----------------------------------------------------------|
| abs         | 0           | <column_name>\|abs                  | num      | num      | Take the absolute value of a number.                      |
| add         | 1           | <column_name>\|add|<value>          | num      | num      | Add <value> to number.                                    |
| capitalize  | 0           | <column_name>\|capitalize           | str      | str      | Capitalize string.                                        |
| ceil        | 0           | <column_name>\|ceil                 | num      | num      | Return the ceiling value of a number.                     |
| datetime    | 0           | <column_name>\|datetime             | str      | datetime | Parse a datetime string.                                  |
| datetime_tz | 1           | <column_name>\|datetime_tz|<tz>     | str      | datetime | Prase a datetime string with the specified <tz> timezone. |
| dehumanize  | 0           | <column_name>\|dehumanize           | str      | num      | Convert from human string to number.                      |
| div         | 1           | <column_name>\|div|<value>          | num      | num      | Divide number by <value>.                                 |
| float       | 0           | <column_name>\|float                | str      | float    | Convert to float.                                         |
| floor       | 0           | <column_name>\|floor                | num      | num      | Return the floor value of a number.                       |
| format      | 1           | <column_name>\|format|<format>      | str      | str      | Format data using Python's `format(<format>)` function.   |
| humanize    | 1           | <column_name>\|humanize|<unit>      | num      | str      | Format number to human string.                            |
| int         | 0           | <column_name>\|int                  | str      | int      | Convert to integer.                                       |
| iso8601     | 0           | <column_name>\|iso8601              | datetime | str      | Convert a datetime to an ISO8601 string representation.   |
| length      | 0           | <column_name>\|length               | str      | str      | Return the length of the string.                          |
| ljust       | 1           | <column_name>\|ljust|<width>        | str      | str      | Left justify string in <width> spaces.                    |
| lower       | 0           | <column_name>\|lower                | str      | str      | Convert string to lowercase.                              |
| mult        | 1           | <column_name>\|mult|<value>         | num      | num      | Multiply number by <value>.                               |
| num         | 0           | <column_name>\|num                  | str      | num      | Convert to integer or float.                              |
| number      | 0           | <column_name>\|number               | str      | num      | Convert to integer or float.                              |
| ordinal     | 0           | <column_name>\|ordinal              | num      | str      | Convert number to ordinal string.                         |
| prefix      | 1           | <column_name>\|prefix|<prefix>      | str      | str      | Prefix the string with <prefix>.                          |
| replace     | 2           | <column_name>\|replace|<from>|<to>  | str      | str      | Replace sub-string <from> with <to>.                      |
| reverse     | 0           | <column_name>\|reverse              | str      | str      | Reverse the characters in the string.                     |
| rjust       | 1           | <column_name>\|rjust|<width>        | str      | str      | Right justify string in <width> spaces.                   |
| round       | 1           | <column_name>\|round|<digits>       | num      | num      | Round number to <digits> digits.                          |
| str         | 0           | <column_name>\|str                  | any      | str      | Convert to string.                                        |
| strftime    | 1           | <column_name>\|strftime|<format>    | datetime | str      | Format a datetime using `strftime(<format>)`.             |
| sub         | 1           | <column_name>\|sub|<value>          | num      | num      | Subtract <value> from number.                             |
| substr      | 2           | <column_name>\|substr|<start>|<end> | str      | str      | Return a sub-string.                                      |
| suffix      | 1           | <column_name>\|suffix|<suffix>      | str      | str      | Suffix the string with <suffix>.                          |
| swapcase    | 0           | <column_name>\|swapcase             | str      | str      | Swap string case.                                         |
| title       | 0           | <column_name>\|title                | str      | str      | Convert string to title case.                             |
| trunc       | 0           | <column_name>\|trunc                | num      | num      | Return the number truncated.                              |
| tz          | 1           | <column_name>\|tz|<tz>              | datetime | datetime | Convert a datetime to a new <tz> timezone.                |
| upper       | 0           | <column_name>\|upper                | str      | str      | Convert string to uppercase.                              |
| utc         | 0           | <column_name>\|utc                  | datetime | datetime | Convert a datetime to UTC.                                |
| zfill       | 1           | <column_name>\|zfill|<width>        | str      | str      | Zero fill string to <width> size.                         |

Note: Most filters that take numeric inputs will automatically apply the `num` filter to the column data prior to filtering.
      Filters can be chained together using the pipe (|) character. For example, `c1|num|add|1|human`
      The type of the data after the last filter has run will be the type that is added to the database.


#### Auto Filtering

#### Column Remapping

#### Table Remapping

#### Character Replacements

| Sequence      | Description          |
|---------------|----------------------|
| [:space:]     | Space ( )            |
| [:pipe:]      | Pipe (\|)             |
| [:backslash:] | Blackslash (\)       |
| [:backtick:]  | Backtick (`)         |
| [:squote:]    | Single quote (')     |
| [:dquote:]    | Double quote (")     |
| [:tab:]       | Tab (\t)             |
| [:cr:]        | Carriage return (\r) |
| [:newline:]   | Newline (\n)         |
| [:n:]         | Newline (\n)         |
| [:comma:]     | Comma (,)            |
| [:colon:]     | Colon (:)            |
| [:amp:]       | Ampersand (&)        |
| [:ampersand:] | Ampersand (&)        |
| [:gt:]        | Greater than (>)     |
| [:lt:]        | Less than (<)        |

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

PrettyTable (https://pypi.org/project/PrettyTable/)

Pendulum (https://pendulum.eustace.io/)
