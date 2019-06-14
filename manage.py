import boto3
import botocore
import numpy as np
import json
import sys
import getopt


class ParameterStore:
    """Class used to import and export AWS SSM Parameter Store
    """
    def __init__(self):
        self.client = boto3.client('ssm')

    def describe_parameters(self):
        response = self.client.describe_parameters()
        parameters = response['Parameters']
        if 'NextToken' in response:
            nextToken = response['NextToken']
        else:
            nextToken = None
        while nextToken is not None:
            response = self.client.describe_parameters(
                NextToken=nextToken
            )
            if 'NextToken' in response:
                nextToken = response['NextToken']
            else:
                nextToken = None
            parameters = np.concatenate((parameters, response['Parameters']))
        return parameters

    def get_parameter_value(self, param):
        response = self.client.get_parameter(
            Name=param,
            WithDecryption=True
        )
        return response['Parameter']['Value']

    def put_parameter(self, key, value):
        try:
            current_value = self.get_parameter_value(key)
        except botocore.exceptions.ClientError as e:
            if e.response.get("Error").get("Code") == "ParameterNotFound":
                self.client.put_parameter(
                    Name=key,
                    Type='String',
                    Value=value
                )
                print("Parameter %s has been added" % key)
                exit(0)
            else:
                raise e
        if value == current_value:
            print("No update for", key)
        else:
            self.client.put_parameter(
                Name=key,
                Overwrite=True,
                Type='String',
                Value=value
            )
            print("Parameter %s has been updated" % key)


    def put_parameters(self, file):
        f = open(file, "r")
        kv = json.load(f)
        for key, value in kv.items():
            self.put_parameter(key, value)


    def get_parameters_by_path(self, path='/'):
        response = self.client.get_parameters_by_path(
            Path=path,
            Recursive=True,
            WithDecryption=True
        )
        parameters = response['Parameters']
        if 'NextToken' in response:
            nextToken = response['NextToken']
        else:
            nextToken = None
        while nextToken is not None:
            response = self.client.get_parameters_by_path(
                Path=path,
                Recursive=True,
                WithDecryption=True,
                NextToken=nextToken
            )
            if 'NextToken' in response:
                nextToken = response['NextToken']
            else:
                nextToken = None
            parameters = np.concatenate((parameters, response['Parameters']))
        kv = {param['Name']: param['Value'] for param in parameters}
        return json.dumps(kv, indent=4, sort_keys=True)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "he:i:", ["help","export=", "import="])
    except getopt.GetoptError:
        print('Usage: manage.py export <parameterpath> | import <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("help", "-h"):
            print('Usage: manage.py export <parameterpath> | import <file>')
            sys.exit()
        elif opt in ("export", "-e"):
            store = ParameterStore()
            print(store.get_parameters_by_path(arg))
            sys.exit()
        elif opt in ("import", "-i"):
            store = ParameterStore()
            store.put_parameters(arg)
            sys.exit()
    print('Usage: manage.py export <parameterpath> | import <file>')


if __name__ == "__main__":
    main(sys.argv[1:])
