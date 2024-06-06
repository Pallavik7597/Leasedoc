from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndex,
    SearchIndexer,
    SimpleField,
    SearchFieldDataType,
)
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# connect to search and indexer client
 
def connect(service_endpoint,key, index_name):
    indexers_client = SearchIndexerClient(service_endpoint, AzureKeyCredential(key))
    search_client = SearchClient(service_endpoint,index_name,AzureKeyCredential(key))
    return indexers_client, search_client

# delete document from index

def delete(search_client, metadata_storage_path):
    search_client.delete_documents(documents=[{"metadata_storage_path":metadata_storage_path}]) 
  
# running the Indexer 

def run(indexers_client, indexer_name):
    indexers_client.run_indexer(indexer_name) 


# not tested 
    
def create_indexer(service_endpoint,key,index_name,container_name,connection_string,datasource_name,indexers_client, indexer_name):
    # create an index
    index_name = index_name
    fields = [
    ]
    index = SearchIndex(name=index_name,fields=fields)
    ind_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    ind_client.create_index(index)

    # create a datasource
    container = SearchIndexerDataContainer(name=container_name)
    data_source_connection = SearchIndexerDataSourceConnection(
        name=datasource_name, type="azureblob", connection_string=connection_string, container=container
    )
    data_source = indexers_client.create_data_source_connection(data_source_connection)

    # create an indexer
    indexer = SearchIndexer(
        name=indexer_name, data_source_name=datasource_name, target_index_name=index_name
    )
    result = indexers_client.create_indexer(indexer)
    # [END create_indexer]
