## Cosmos DB SQL API sample container

This script is to automate creating Cosmos DB SQL API container and sample document. Sample data used here is based on [this VolcanoData.json](https://github.com/Azure-Samples/azure-cosmos-db-sample-data/blob/main/SampleData/VolcanoData.json)

#### How to use

1. Deploy Cosmos DB SQL API account and create database
    1. Refer to [This Quickstart](https://docs.microsoft.com/en-us/azure/cosmos-db/sql/create-cosmosdb-resources-portal) for Cosmos DB deployment.
1. Deploy Azure KeyVault and create a Secret for Cosmos DB Master Key
    1. Refer to [this documentation](https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal) for Azure KeyVault deployment.
    2. Create a Secret in Azure KeyVault following [this instruction](https://docs.microsoft.com/azure/cosmos-db/access-secrets-from-keyvault) 
1. Open `./cosmos-db-sql-sample-container/create-cosmos-demo-container.py` and update variables according to your configuration
1. Install Python libraries
    1. Azure Active Directory ID library. `pip install azure-identity`
    1. Azure KeyVault Secret library. `pip install azure-keyvault-secrets`
1. Run `create-cosmos-demo-container.py`

#### How to run

```Python
python3 ./cosmos-db-sql-sample-container/create-cosmos-demo-container.py -c <Container Name>
```

#### Script settings

|Parameter|Notes|Default value|
|---|---|---|
|COSMOS_ACCOUNT_NAME|Your Cosmos DB Account Name||
|DATABASE_NAME| Your Database Name||
|PARTITION_NAME|Partition Name|Country|
|API_VERSION|Cosmos DB API Version|2018-12-31|
|SAMPLE_DATA|Sample data file path|./VolcanoData.json|
|CONTAINER_TOKEN|Container resource token script path|./create-container-token.js|
|DOCUMENT_TOKEN|Document resource token script path|./create-document-token.js|
|KEY_VAULT_NAME|Your Key Vault Name|
|SECRET_NAME|Secret Name|
