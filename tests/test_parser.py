import unittest
from yamlalchemy import parse
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, Query
from sqlalchemy.ext.automap import automap_base

base = automap_base()


def get_engine() -> str:
    uri = URL.create(**{
        'drivername': "mysql+pymysql",
        "username": "guest",
        "host": "relational.fit.cvut.cz",
        "port": "3306",
        "password": "relational",
        "database": "AdventureWorks2014"
    })

    engine = create_engine(uri)
    if engine.connect():
        return engine


class TestParser(unittest.TestCase):
    def test_query(self):
        yaml_content = """
            $from: Product
            $column:
                -
                    $name: Color
                    $alias: Color of Product
                -
                    $name: SafetyStockLevel
                    $alias: Minimum Inventory Amount
                    $func: sum
                -
                    $name: ListPrice
                    $alias: List Price of Product
                    $func: avg
            $group:
                -
                    $name: Color    
            $where:
                -
                    $name: Class
                    $filter:
                        $contains:
                            - A
                -
                    $name: Class
                    $filter:
                        $is: null

                -
                    $name: Color
                    $filter:
                        $nis: null
                -
                    $name: SellStartDate
                    $filter:
                        $gt: 2013-01-01
            
            $having:
                -
                    $name: SafetyStockLevel
                    $func: sum
                    $filter:
                        $and:
                            $gt: 1
                            $lt: 1000
            $order:
                -
                    $name: Name
                    $direction: asc
            $limit: 10
            $offset: 0

                    
        """
        engine = get_engine()
        base.prepare(engine, reflect=True)
        session = Session(engine)
        qs = parse(yaml_content, session, base).to_query()
        self.assertIsInstance(qs, Query)


if __name__ == '__main__':
    unittest.main()
