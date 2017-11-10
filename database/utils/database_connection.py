import psycopg2

class databaseConnection(object):
    DATABASES = {
        'STG': {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'dbname': 're',
        },
        'TEST': {
            'host': 'localhost',
            'port': 5432,
            'user': 'postgres',
            'dbname': 'zone_test',
        },
    }

    @classmethod
    def stage(cls):
        conn = psycopg2.connect(**cls.DATABASES['STG'])
        print '\n Connected to stage database.'
        return conn

    @classmethod
    def test(cls):
        conn = psycopg2.connect(**cls.DATABASES['TEST'])
        print '\n Connected to stage database.'
        return conn
