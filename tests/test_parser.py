import unittest
from ymlalchemy import parse
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, Query
from sqlalchemy.ext.automap import automap_base
import pandas as pd

base = automap_base()


def get_engine() -> str:
    uri = URL.create(**{
        'drivername': "mysql+pymysql",
        "username": "root",
        "host": "127.0.0.1",
        "port": "3306",
        "password": "q1w2e3r4t5",
        "database": "datasets"
    })

    engine = create_engine(uri)
    if engine.connect():
        return engine


class TestParser(unittest.TestCase):
    def test_query(self):
        yaml_content = """
            $from: ramen_ratings
            $column:
                -
                    $name: Style
                    $alias: Stil
                -
                    $name: Country
                    $alias: Ülke
                -
                    $name: Stars
                    $alias: Yıldız Sayısı
                    $func: count
            $group:
                -
                    $name: Style
                -
                    $name: Country
            $order:
                -
                    $name: Stars
                    $func: count
                    $direction: desc
                -
                    $name: Style
                    $direction: asc
            $where:
                -
                    $name: Style
                    $filter: 
                        $or:
                            $startswith:
                                - c
                                - K

                    
        """
        engine = get_engine()
        base.prepare(engine, reflect=True)
        session = Session(engine)
        """
        qs = Parser.parse(yaml_content).to_query(session, base)
        """
        qs = parse(yaml_content, session, base).to_query()
        self.assertIsInstance(qs, Query)

        df = pd.read_sql_query(qs.statement, session.connection())
        self.assertIsInstance(df, pd.DataFrame)
        # self.assertListEqual(df.columns.tolist(), ['Stil', 'Ülke', 'Counf of Stars'])
        print(qs.statement)
        print(df)


if __name__ == '__main__':
    unittest.main()
