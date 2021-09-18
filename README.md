# YMLAlchemy

YMLAlchemy is a Python-based library to convert YAML string to SQLAlchemy read-only queries.

## Installation

Installation via PyPI:

```shell
 pip install ymlalchemy
```

## YAML Query Language Syntax

Description

### FROM

Name of the table from which to select data. For now, YMLAlchemy supports only one table.

| Identifier | Data Type |
|--|--|
| `$column` | String |

*Usage:*

```yaml
$from: Product
```

### COLUMNS

Field names of the table you want to select data from.

| Identifier | Data Type |
|--|--|
| `$column` | List |

*Column Definition:*

| Identifier | Description | Required |
|--|--|--|
| `$name` | Name of column | `True` |
| `$alias` | Alias of column | `False` |
| `$func` | Aggregate function of column. avg, sum, etc... | `False` |

*Usage:*

```yaml
$column:
  -
    $name: Color
    $alias: Color of Product
  -
    $name: ListPrice
    $alias: List Price of Product
    $func: avg
```

### GROUP

Field names of the table you want to group the same values into summary rows.

| Identifier | Data Type |
|--|--|
| `$group` | List |

*Column Definition:*

| Identifier | Description | Required |
|--|--|--|
| `$name` | Name of column | `True` |

*Usage:*  

```yaml
$group:
  -
    $name: Color
```

### ORDER

Field names of the table you want to sort result-set in ascending or descending order.

| Identifier | Data Type |
|--|--|
| `$order` | List |

*Column Definition:*

| Identifier | Description | Required | Defaults |
|--|--|--|--|
| `$name` | Name of column | `True` | -- |
| `$direction` | Ascending or descending order | `Fase` | `asc` or `desc` |

*Usage:*  

```yaml
$order:
  -
    $name: Name
    $direction: asc
```

### WHERE

Filtering records  to return.

| Identifier | Data Type |
|--|--|
| `$where` | List |

*Column Definition:*

| Identifier | Description | Required |
|--|--|--|
| `$name` | Name of column | `True` |
| `$filter` | List of filter definitions | `True` |

*Filter Definition:*

Filtering consists of the following two parts.

*Operator Definition:*

This part is optional.

| Identifier | Description |
|--|--|
| `$and` | Combines where statements with `AND` |
| `$or` | Combines where statements with `OR` |
| `$not` | Combines where statements with `NOT` |

*Comparator Definition:*

This part is required.

| Identifier | Description | SQL Part (MySQL) |
|--|--|--|
| `$eq` | Equal | `COLUMN = 'value'`  |
| `$gt` | Greator than |  `COLUMN > 'value'` |
| `$gte` | Greater than or equal  | `COLUMN >= 'value'`  |
|`$lt`| Less than |  `COLUMN > 'value'` |
| `$lte`| Less than or equal | `COLUMN <= 'value'`  |
| `$neq`| Not equal |  `COLUMN != 'value'` |
| `$like`| Like | `COLUMN LIKE '%value%'`  |
| `$ilike`| Case-insensitive like |  `COLUMN ILIKE '%value%'` |
| `$nlike`| Not like | `COLUMN NOT LIKE '%value%'` |
| `$nilike`| Case-insensitive not like | `COLUMN NOT ILIKE '%value%'`  |
| `$in`| In | `COLUMN IN ['value1', 'value2]`  |
| `$nin`| Not in | `COLUMN NOT IN ['value1', 'value2]`  |
| `$is (:null)`| is null |  `COLUMN IS NULL`  |
| `$nis (:null)`| Is not null | `COLUMN IS NOT NULL`  |
| `$contains`| Contains (Operand should contain 1 column) | `COLUMN LIKE '%value%'` |
| `$startswith`| Starts with | `COLUMN LIKE 'value%'`  |
| `$endswith` | Ends with | `COLUMN LIKE '%value'`  |

*Usage:*  

```yaml
$where:
  -
    $name: Class
    $filter:
      $is: null

  -
    $name: Color
    $filter:
      $nis: null
  -
    $name: SellStartDate
    $filter:
      $gt: 2013-01-01
  -
    $name: Style
    $filter:
      $or:
        $startswith:
          - U
          - M
```

### HAVING

Filtering with aggregate functions.

| Identifier | Data Type |
|--|--|
| `$having` | List |

*Column Definition:*

| Identifier | Description | Required |
|--|--|--|
| `$name` | Name of column | `True` |
| `$func` | Aggregate function name | `True` |
| `$filter` | Filtering part. Same sytntax with the filter part of WHERE statement. | `True` |

*Usage:*  

```yaml
$having:
  -
    $name: Review
    $func: avg
    $filter:
      $and:
        $lt: 1500
        $gt: 1000
  -
    $name: Stars
    $func: count
    $filter:
      $lt: 20
```

### LIMIT

Specifying the number of records to return.

| Identifier | Data Type |
|--|--|
| `$limit` | Integer |

*Usage:*  

```yaml
$limit: 10
```

### OFFSET

Specifying an offset from where to start returning data.

| Identifier | Data Type |
|--|--|
| `$offset` | Integer |

*Usage:*  

```yaml
$offset: 10
```

## License

MIT License

Copyright (c) 2021 Ahmet Önol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
