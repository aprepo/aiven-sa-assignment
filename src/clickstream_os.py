import os
import dotenv
from opensearchpy import OpenSearch

dotenv.load_dotenv()

_client = None
OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX")

def get_os_client():
    global _client
    if _client is None:
        _client = OpenSearch(
        hosts=[{
            "host": os.getenv("OPENSEARCH_HOST"),
            "port": os.getenv("OPENSEARCH_PORT")
        }],
        http_auth=(
            os.getenv("OPENSEARCH_USER"),
            os.getenv("OPENSEARCH_PASSWORD")
        ),
        use_ssl=True
    )
    return _client


def write_to_os(event):
    client = get_os_client()
    print(event)
    if client is None:
        print("OpenSearch client not initialized")
        return
    response = client.index(index=OPENSEARCH_INDEX, body=event)
    print(f"Indexed to OpenSearch: {response['_id']}")