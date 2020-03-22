from storage_clients import MySqlClient


def create_views():
    with MySqlClient() as mysql_client:
        mysql_client.execute(f"""
            CREATE VIEW all_summaries AS 
            SELECT r.*, d.Date, d.Url 
            FROM ranks r, documents d
            WHERE r.MLARank <= 200
            AND r.DocumentId = d.Id
            ORDER BY MLARank
            """)


if __name__ == '__main__':
    create_views()
