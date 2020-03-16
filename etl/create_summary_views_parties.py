from storage_clients import MySqlClient


def create_views():
    with MySqlClient() as mysql_client:
        for party in ["UCP", "NDP"]:
            try:
                mysql_client.execute(f'DROP VIEW {party}')
            except:
                pass
            mysql_client.execute(f'CREATE VIEW {party} AS SELECT * FROM ranks WHERE Caucus = \'{party}\' AND PartyRank > 0 ORDER BY PartyRank LIMIT 2000')

if __name__ == '__main__':
    create_views()
