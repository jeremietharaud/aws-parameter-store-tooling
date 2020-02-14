import argparse
import boto3
import botocore
import numpy as np
import json


class ParameterStore:
    """Class used to import and export AWS SSM Parameter Store
    """
    def __init__(self):
        self.client = boto3.client('ssm')

    def delete_parameters(self, file):
        f = open(file, "r")
        try:
            kv = json.load(f)
            list_params = list(kv.keys())
            for i in range(0, len(list_params), 10):
                response = self.client.delete_parameters(Names=list_params[i:i+10])
                print("The following parameters have been deleted: ", response['DeletedParameters'])
        except Exception as e:
            print(e)
            exit(1)

    def get_parameter_value(self, param):
        response = self.client.get_parameter(Name=param, WithDecryption=True)
        return response['Parameter']['Value']

    def put_parameter(self, key, value, kms_key):
        try:
            current_value = self.get_parameter_value(key)
        except botocore.exceptions.ClientError as e:
            if e.response.get("Error").get("Code") == "ParameterNotFound":
                if kms_key is None:
                    if type(value) is list:
                        self.client.put_parameter(Name=key, Type='StringList', Value=value[0])
                    else:
                        self.client.put_parameter(Name=key, Type='String', Value=value)
                elif kms_key == "default":
                    self.client.put_parameter(Name=key, Type='SecureString', Value=value)
                else:
                    self.client.put_parameter(Name=key, Type='SecureString', KeyId=kms_key, Value=value)
                print("Parameter %s has been added" % key)
                return
            else:
                print(e)
                exit(1)
        if value == current_value and kms_key is None:
            print("No update for %s" % key)
        else:
            if kms_key is None:
                if type(value) is list:
                    self.client.put_parameter(Name=key, Overwrite=True, Type='StringList', Value=value[0])
                else:
                    self.client.put_parameter(Name=key, Overwrite=True, Type='String', Value=value)
            elif kms_key == "default":
                self.client.put_parameter(Name=key, Overwrite=True, Type='SecureString', Value=value)
            else:
                self.client.put_parameter(Name=key, Overwrite=True, Type='SecureString', KeyId=kms_key, Value=value)
            print("Parameter %s has been updated" % key)

    def put_parameters(self, file, kms_key):
        f = open(file, "r")
        try:
            kv = json.load(f)
            for key, value in kv.items():
                self.put_parameter(key, value, kms_key)
        except Exception as e:
            print(e)
            exit(1)

    def get_parameters_by_path(self, path='/'):
        paginator = self.client.get_paginator('get_parameters_by_path')
        pages = paginator.paginate(Path=path, Recursive=True, WithDecryption=True)
        parameters = []
        try:
            for page in pages:
                parameters = np.concatenate((parameters, page['Parameters']))
            kv = {param['Name']: param['Value'] for param in parameters}
            return json.dumps(kv, indent=4, sort_keys=True)
        except Exception as e:
            print(e)
            exit(1)


def main():
    parser = argparse.ArgumentParser(description='Manage parameters of AWS Parameter Store')
    parser.add_argument(
        '--export', '-e', metavar='<PARAMETER PATH>', type=str,
        required=False, help='Export parameters of AWS Parameter Store')
    parser.add_argument(
        '--upload', '-i', metavar='<FILE>', type=str,
        required=False, help='Import a JSON file into AWS Parameter Store')
    parser.add_argument(
        '--key', '-k', metavar='<KMS KEY>', type=str,
        required=False, help='KMS key alias or id used to read/create parameters in AWS Parameter Store')
    parser.add_argument(
        '--delete', '-d', metavar='<FILE>', type=str,
        required=False, help='Delete the parameters of the JSON file in AWS Parameter Store')

    args = parser.parse_args()

    if args.export:
        store = ParameterStore()
        print(store.get_parameters_by_path(args.export))
        exit(0)

    if args.upload:
        store = ParameterStore()
        store.put_parameters(args.upload, args.key)
        exit(0)

    if args.delete:
        store = ParameterStore()
        store.delete_parameters(args.delete)
        exit(0)

    parser.print_help()


if __name__ == "__main__":
    main()
