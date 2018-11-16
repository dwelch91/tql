# Text Query Language (tql)
Like the `q` tool (https://harelba.github.io/q/) but Python 3.5+ only and uses SQLite to handle its own SQL parsing.

### Features
* Extensive support for data pre-filtering, conversions, etc. of CSV/TSV data before it is added to database
* Full support for all of SQLite features
* Pretty table output
* CSV output
* Database output
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


### How Tos

#### How do I change the order of the columns in the output?
Use SELECT with the column names listed out, the order which they appear will make the output columns in the same order. 
(reword this)

#### How do I filter, sort, etc on a numeric column?
`tql` does not automatically convert CSV data into integers or floats. 
Coerce the data to either an integer or float using a filter on the target column and then SQLite will be able to 
operate on the column as a numeric value for sorting, comparisons, etc.

#### 
