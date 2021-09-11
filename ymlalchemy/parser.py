from os import name
from typing import Dict, List
from sqlalchemy.ext.automap import AutomapBase
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.schema import Table, Column
import yaml
from ymlalchemy.contants import *
from sqlalchemy import MetaData
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import and_, or_, not_


metadata = MetaData()


class QueryBuilder:
    session = None
    table = None
    columns = []
    groups = []
    order_by = []
    where = []

    def __init__(self, session: Session):
        self.session = session

    def set_table(self, table: Table):
        self.table = table

    def set_columns(self, columns: List[Column]):
        self.columns = columns

    def set_groups(self, groups: List[Column]):
        self.groups = groups

    def set_order_by(self, order_by: List[Column]):
        self.order_by = order_by

    def set_where(self, where_clause: List[Column]):
        self.where = where_clause

    def to_query(self):
        query = self.session.query(self.table)
        query = query.with_entities(*self.columns)
        query = query.filter(*self.where)
        query = query.group_by(*self.groups)
        query = query.order_by(*self.order_by)
        return query


def where(col: Column, where_clause: List[dict]) -> Column:
    for op, clause in where_clause.items():
        filter_criteria = []
        if op in OPERATORS:
            for comp, values in clause.items():
                if isinstance(values, list) is False:
                    values = [values]
                if comp in COMPARATORS:
                    if comp == COMP_NEQ:
                        _values = [col != value for value in values]
                    if comp == COMP_GT:
                        _values = [col > value for value in values]
                    if comp == COMP_GTE:
                        _values = [col >= value for value in values]
                    if comp == COMP_LT:
                        _values = [col < value for value in values]
                    if comp == COMP_LTE:
                        _values = [col <= value for value in values]
                    if comp == COMP_EQ:
                        _values = [col == value for value in values]
                    if comp == COMP_LIKE:
                        _values = [col.like(value) for value in values]
                    if comp == COMP_NLIKE:
                        _values = [col.not_like(value)
                                   for value in values]
                    if comp == COMP_ILIKE:
                        _values = [col.ilike(value)
                                   for value in values]
                    if comp == COMP_NILIKE:
                        _values = [col.not_ilike(value)
                                   for value in values]
                    if comp == COMP_IN:
                        _values = [col.in_(values)]
                    if comp == COMP_NIN:
                        _values = [col.notin_(values)]
                    if comp == COMP_IS:
                        _values = [col.is_(value) for value in values]
                    if comp == COMP_NIS:
                        _values = [col.is_not(value)
                                   for value in values]
                    if comp == COMP_CONTAINS:
                        _values = [col.contains(value)
                                   for value in values]
                    if comp == COMP_STARTS_WITH:
                        _values = [col.startswith(value)
                                   for value in values]
                    if comp == COMP_ENDS_WITH:
                        _values = [col.endswith(value)
                                   for value in values]

                    filter_criteria.extend(_values)

        if op in COMPARATORS:
            pass
        col = and_(*filter_criteria)
        if op == OP_OR:
            col = or_(*filter_criteria)
        if op == OP_NOT:
            col = not_(*filter_criteria)
    return col


def query_fragment(table: Table, columns: List[dict]) -> List[Column]:
    if isinstance(columns, list) is False:
        raise Exception(
            f"Columns must be as list of dict. {type(columns)} given.")

    cols = []
    for column in columns:
        name = column.get(NAME, None)
        alias = column.get(ALIAS, None)
        expr = column.get(FUNC, None)
        direction = column.get(DIRECTION, None)
        where_clause = column.get(FILTER, None)
        col = getattr(table, name)

        if expr is not None:
            column_aggr_func = getattr(func, expr)
            col = column_aggr_func(col)

        if direction is not None and direction in QUERY_ORDERS:
            if direction.lower() == ORDER_ASC:
                col = col.asc()
            if direction.lower() == ORDER_DESC:
                col = col.desc()

        if where_clause is not None:
            col = where(col, where_clause)

        if alias:
            col = col.label(alias)

        cols.append(col)

    return cols


def parse(yaml_content: str or dict, session: Session, reflection: AutomapBase) -> "QueryBuilder":
    """
    Initial entry point for ymlalchemy.
    Parses the given YAML string to create a SqlAlchemy query

    args:
        yaml_content: YAML content or Python dictionary.
        session: SqlAlchemy Session
        reflection: SqlAlchemy AutomapBase
    """

    if not yaml_content:
        raise Exception('No yaml content given.')
    qd = yaml_content
    if isinstance(yaml_content, dict) is False:
        qd = yaml.safe_load(yaml_content)

    if not isinstance(qd, dict):
        raise TypeError(
            "Argument for query parsing must be a Python dictionary.")

    if FROM not in qd:
        raise Exception(f"Missing \"{FROM}\" argument in query.")

    if COLUMN not in qd:
        qd[COLUMN] = []

    if GROUP not in qd:
        qd[GROUP] = []

    if ORDER not in qd:
        qd[ORDER] = []

    if WHERE not in qd:
        qd[WHERE] = {}

    table = reflection.classes[qd[FROM]]
    columns = query_fragment(table, qd[COLUMN])
    group_by = query_fragment(table, qd[GROUP])
    order_by = query_fragment(table, qd[ORDER])
    where = query_fragment(table, qd[WHERE])

    qb = QueryBuilder(session=session)
    qb.set_table(table)
    qb.set_columns(columns)
    qb.set_where(where)
    qb.set_groups(group_by)
    qb.set_order_by(order_by)

    return qb
