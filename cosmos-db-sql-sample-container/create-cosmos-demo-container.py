# -*- coding: utf-8 -*-

import sys
import json
import requests
import urllib3
urllib3.disable_warnings()
import subprocess
from optparse import OptionParser
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

COSMOS_ACCOUNT_NAME = "<Your Cosmos DB Account Name>"
DATABASE_NAME = "<Database Name>"
PARTITION_NAME = "Country"
API_VERSION = "2018-12-31"
SAMPLE_DATA = "./VolcanoData.json"
CONTAINER_TOKEN = "./create-container-token.js"
DOCUMENT_TOKEN = "./create-document-token.js"
KEY_VAULT_NAME = "<Your Key Vault Name>"
SECRET_NAME = "<Secret Name>"

def get_kv_secret():
    KVUri = f"https://{KEY_VAULT_NAME}.vault.azure.net"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    retrieved_secret = client.get_secret(SECRET_NAME)
    return retrieved_secret.value

def get_resource_token(script):
    secret = get_kv_secret()
    cmd = ['node', script, secret, DATABASE_NAME, options.container_name]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    token = res.stdout.split('|')
    return token

def get_create_container_json():
    payload = {
            "id": options.container_name,
            "indexingPolicy": {
                "automatic": True,
                "indexingMode": "Consistent",
                "includedPaths": [
                    {
                        "path": "/*",
                        "indexes": [
                            {
                                "dataType": "String",
                                "precision": -1,
                                "kind": "Range"
                            }
                        ]
                    }
                ]
            },
            "partitionKey": {
                "paths": [
                    "/" + PARTITION_NAME
                ],
                "kind": "Hash",
                "Version": 2
            }
        }
    return payload

def get_sample_data():
    f = open(SAMPLE_DATA, "r")
    volcano_dict = json.load(f)
    return volcano_dict

def create_container(container_token, create_container_json, colls_api):
    headers = {
            'Authorization': container_token[1],
            'x-ms-date': container_token[0],
            'x-ms-version': API_VERSION,
            'content-type': 'application/json'
    }

    try:
        r = requests.post(colls_api, data=json.dumps(create_container_json), headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    if r.status_code == 409:
        print("There is already the same container name. Try another name.")
        sys.exit()
    if r.status_code == 201:
        print("Container " + options.container_name + " has been successfully created.")

def create_documents(document_token, volcano, document_api):
    headers = {
            'Authorization': document_token[1],
            'x-ms-date': document_token[0],
            'x-ms-version': API_VERSION,
            'content-type': 'application/json'
    }
    print("Preparing sample data. Please wait.")
    for i in volcano:
        headers['x-ms-documentdb-partitionkey'] = "[ \"" + i[PARTITION_NAME] + "\" ]"
        r = requests.post(document_api, data=json.dumps(i), headers=headers, verify=False)

def run():
    # Check required option
    if not options.container_name:
        parser.error('Container name not given')
 
    # Create a container
    container_token = get_resource_token(CONTAINER_TOKEN)
    colls_api = "https://" + COSMOS_ACCOUNT_NAME + ".documents.azure.com/dbs/" + DATABASE_NAME + "/colls"
    create_container_json = get_create_container_json()
    create_container(container_token, create_container_json, colls_api)

    # Create sample documents
    document_token = get_resource_token(DOCUMENT_TOKEN)
    document_api = "https://" + COSMOS_ACCOUNT_NAME + ".documents.azure.com/dbs/" + DATABASE_NAME + "/colls/" + options.container_name + "/docs"
    volcano = get_sample_data()
    create_documents(document_token, volcano, document_api)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-c', '--container', dest='container_name', help='Container Name'), # Container Name
    (options, args) = parser.parse_args()
    run()
