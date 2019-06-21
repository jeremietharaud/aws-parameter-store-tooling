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
            response = self.client.describe_parameters(NextToken=nextToken)
            if 'NextToken' in response:
                nextToken = response['NextToken']
            else:
                nextToken = None
            parameters = np.concatenate((parameters, response['Parameters']))
        return parameters

    def delete_parameters(self, file):
        f = open(file, "r")
        kv = json.load(f)
        response = self.client.delete_parameters(Names=list(kv.keys()))
        print("The following parameters have been deleted: ", response['DeletedParameters'])
        return

    def get_parameter_value(self, param):
        response = self.client.get_parameter(Name=param, WithDecryption=True)
        return response['Parameter']['Value']

    def put_parameter(self, key, value, kms_key):
        try:
            current_value = self.get_parameter_value(key)
        except botocore.exceptions.ClientError as e:
            if e.response.get("Error").get("Code") == "ParameterNotFound":
                if kms_key is None:
                    self.client.put_parameter(Name=key, Type='String', Value=value)
                elif kms_key == "default":
                    self.client.put_parameter(Name=key, Type='SecureString', Value=value)
                else:
                    self.client.put_parameter(Name=key, Type='SecureString', KeyId=kms_key, Value=value)
                print("Parameter %s has been added" % key)
                exit(0)
            else:
                raise e
        if value == current_value and kms_key is None:
            print("No update for", key)
        else:
            if kms_key is None:
                self.client.put_parameter(Name=key, Overwrite=True, Type='String', Value=value)
            elif kms_key == "default":
                self.client.put_parameter(Name=key, Overwrite=True, Type='SecureString', Value=value)
            else:
                self.client.put_parameter(Name=key, Overwrite=True, Type='SecureString', KeyId=kms_key, Value=value)
            print("Parameter %s has been updated" % key)

    def put_parameters(self, file, kms_key):
        f = open(file, "r")
        kv = json.load(f)
        for key, value in kv.items():
            self.put_parameter(key, value, kms_key)

    def get_parameters_by_path(self, path='/'):
        response = self.client.get_parameters_by_path(Path=path, Recursive=True, WithDecryption=True)
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


def usage():
    print('Usage: manage.py --export <parameterpath> | --import <file> | --key <kmskeyid> | --delete')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "he:i:k:d:", ["help", "export=", "import=", 'key=', "delete="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    action = None
    action_arg = None
    key = None
    for opt, arg in opts:
        if opt in ("help", "-h"):
            usage()
            sys.exit()
        elif opt in ("--export", "-e"):
            action = "export"
            action_arg = arg
        elif opt in ("--import", "-i"):
            action = "import"
            action_arg = arg
        elif opt in ("--key", "-k"):
            key = arg
        elif opt in ("--delete", "-d"):
            action = "delete"
            action_arg = arg
        else:
            usage()
            sys.exit()

    if action == "export":
        store = ParameterStore()
        print(store.get_parameters_by_path(action_arg))
    elif action == "import":
        store = ParameterStore()
        store.put_parameters(action_arg, key)
    elif action == "delete":
        store = ParameterStore()
        store.delete_parameters(action_arg)
    else:
        usage()


if __name__ == "__main__":
    main(sys.argv[1:])
