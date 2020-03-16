from storage_clients import MySqlClient


def create_views():
    with MySqlClient() as mysql_client:
        for mla_id in range(1, 88):
            try:
                mysql_client.execute(f'DROP VIEW summaries_{mla_id}')
            except:
                pass
            mysql_client.execute(f'CREATE VIEW summaries_{mla_id} AS SELECT * FROM ranks WHERE MLAId = {mla_id} ORDER BY MLARank LIMIT 2000')

if __name__ == '__main__':
    create_views()
