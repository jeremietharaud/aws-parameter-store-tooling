# aws-parameter-store-tooling

### How this repository works

This repository is used to import/export AWS SSM Parameter store.

## How to export parameters

Example for retrieving parameters in /path/to/parameters:
```python manage.py -e '//path\to\parameters'```

To retrieve all parameters:
```python manage.py -e '//'```

Be careful of the interpretation of the slash. You may have to escape them using double slash and bashslash.
