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
* Full Python 3.5+ support (sorry, no Python 2.x support)
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

#### Auto Filtering

#### Column Remapping

#### Table Remapping

#### Character Replacements

#### Save Database

#### Load Database

#### Use Cases

##### CSV -> filter/sort/aggregate/etc (SQL) -> CSV (or table)
Without `-s`/`--save-db` or `-l`/`--load-db`, `tql` will load the CSV into an in-memory database, perform the SQL query, 
and output the result in the chosen output format.  If the data set is too large for memory, use `-s`/`--save-db` to force
`tql` to use a on-disk database and will only then be limited by available disk space and/or SQLite database size limitations.

##### CSV -> filter/sort/aggregate/etc (SQL) -> database -> CSV (or table)
Using `-s`/`--save-db` will force `tql` to retain an on-disk database of the loaded CSV data. 
It will still produce results in the chosen output format. 
The database can then be used in subsequent `-l`/`--load-db` workflows or manipulated using any desired SQLite database tool.

##### CSV + database -> filter/sort/aggregate/etc (SQL) -> database -> CSV (or table)
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
