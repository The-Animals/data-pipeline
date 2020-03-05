from storage_clients import MySqlClient


def create_views(): 
    with MySqlClient() as mysql_client: 
        for mla_id in range(1, 88):
            mysql_client.execute(f'CREATE VIEW summaries_{mla_id} AS SELECT * FROM ranks WHERE MLAId = {mla_id} ORDER BY Rank LIMIT 2000')

if __name__ == '__main__':
    create_views()