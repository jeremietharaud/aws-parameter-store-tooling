# aws-parameter-store-tooling

### How this repository works

This repository is used to import/export AWS SSM Parameter store.

## How to install aws-parameter-store

* Clone the repository and install it using the following command (Python3 needed):
```
python setup.py install
```

* Install it using pip:
```
pip install git+git://github.com/jeremietharaud/aws-parameter-store-toooling.git
```

## How to export parameters

Example for retrieving parameters in /path/to/parameters:
```aws-parameter-store -e '//path\to\parameters'```

To retrieve all parameters:
```aws-parameter-store -e //```

Be careful of the interpretation of the slash. You may have to escape them using double slash and bashslash.

Example for importing parameters from a local file (in key/value format):
```aws-parameter-store -i file```

For encrypting parameters using a KMS key (AWS managed key or CMK), use the `-k` option:
```aws-parameter-store -i file -k alias/aws/ssm```

```aws-parameter-store -i file -k kmskeyid```

For deleting parameters from a local file (in key/value format):
```aws-parameter-store -d 'file'```
