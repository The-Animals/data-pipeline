from storage_clients import MySqlClient


def create_views():
    with MySqlClient() as mysql_client:
        for mla_id in range(1, 88):
            try:
                mysql_client.execute(f'DROP VIEW summaries_{mla_id}')
            except:
                pass
            mysql_client.execute(f"""
                CREATE VIEW summaries_{mla_id} AS 
                SELECT r.*, d.Date, d.Url, m.FirstName, m.LastName
                FROM ranks r, documents d, mlas m
                WHERE r.MLAId = {mla_id}
                AND r.DocumentId = d.Id
                AND r.MLAId = m.Id
                ORDER BY MLARank
                LIMIT 1000
            """)

if __name__ == '__main__':
    create_views()
