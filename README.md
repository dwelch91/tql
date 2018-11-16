# Text Query Language (tql)
Like the `q` tool (https://harelba.github.io/q/) but Python 3.5+ only, has extensive filtering, 
and uses SQLite to handle its own SQL parsing. 

### Features
* Extensive support for data pre-filtering, conversions, etc. of CSV/TSV data before it is added to database
* Full support for all of SQLite features
* Pretty table output
* CSV output
* Database output
* Table re-mapping
* Column re-mapping
* Automatic or user specified headers/column names
* Full Python 3.5+ support (sorry, no Python 2.x support)
* MIT license

### Planned Features
* Add data to existing database
* Modification queries
* Regex-based filters
* Input from stdin

### Installation


### Documentation

#### Use Cases

##### CSV -> filter/sort/aggregate/etc -> CSV (or table)
Without `-s`/`--save-db` or `-l`/`--load-db`, `qq` will load the CSV into an in-memory database, perform the SQL query, 
and output the result in the chosen output format.

##### CSV -> filter/sort/aggregate/etc -> database -> CSV (or table)
Using `-s`/`--save-db` will force `qq` to retain an on-disk database of the loaded CSV data. 
It will still produce results in the chosen output format. 
The database can then be used for further data mining or re-used in `qq` using the `-l`/`--load-db` switch.

##### CSV + database -> filter/sort/aggregate/etc -> database -> CSV (or table)
Using the `-l`/`--load-db` switch will cause `qq` to load an existing database and load the CSV data into a new table in the database. 
It will still produce results in the chosen output format. 

### How Tos

#### How do I change the order of the columns in the output?
Use SELECT with the column names listed out, the order which they appear will make the output columns in the same order. 
(reword this)

#### How do I filter, sort, etc on a numeric column?
`tql` does not automatically convert CSV data into integers or floats. 
Coerce the data to either an integer or float using a filter on the target column and then SQLite will be able to 
operate on the column as a numeric value for sorting, comparisons, etc.

#### 
