# aws-parameter-store-tooling

### How this repository works

This repository is used to import/export AWS SSM Parameter store.

## How to export parameters

Example for retrieving parameters in /path/to/parameters:
```python manage.py -e '//path\to\parameters'```

To retrieve all parameters:
```python manage.py -e '//'```

Be careful of the interpretation of the slash. You may have to escape them using double slash and bashslash.

Example for importing parameters from a local file (in key/value format):
```python manage.py -i 'file'```

For encrypting parameters using a KMS key (AWS managed key or CMK), use the `-k` option:
```python manage.py -i 'file' -k alias/aws/ssm```

```python manage.py -i 'file' -k <kmskeyid>```

For deleting parameters from a local file (in key/value format):
```python manage.py -d 'file'```
