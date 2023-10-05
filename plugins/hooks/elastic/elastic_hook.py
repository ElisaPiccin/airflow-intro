from airflow.plugins_manager import AirflowPlugin
from airflow.hooks.base import BaseHook # inherit from BaseHook

from elasticsearch import Elasticsearch

class ElasticHook (BaseHook):

    def __init__(self, conn_id='elastic_default', *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = self.get_connection(conn_id)

        conn_config = {}
        hosts = []

        if conn.host:
            hosts = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['http_auth'] = (conn.login, conn.password)

        self.es = Elasticsearch(hosts, **conn_config)
        self.index = conn.schema # in Elasticsearch data are stored in indexes (~folders)

    def info(self):
        return self.es.info() # return the info of the Elasticsearch cluster instance
    
    def set_index(self, index):
        self.index = index
    
    def add_doc(self, index, doc_type, doc):
        # add data to a specific index
        self.set_index(index)
        result = self.es.index(index=index, doc_type=doc_type, body=doc)
        return result

# This class is NEEDED for registering the plugin in Airflow (needs RESTART)    
class AirflowElasticPlugin(AirflowPlugin):
    name = 'elastic' # name of the plugin
    hooks = [ElasticHook]