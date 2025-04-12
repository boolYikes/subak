import clickhouse_connect
import os
import json
from datetime import datetime

conn = json.loads(os.environ['CLICKHOUSE_CONN'])
DATA_DIR = "/data"
client = clickhouse_connect.get_client(
        host=conn['host'],
        port=conn['port'],
        username=conn['username'],
        password=conn['password'],
        database=conn['database'],
    )

TABLES = {
    "region": ["r_regionkey", "r_name", "r_comment"],
    "nation": ["n_nationkey", "n_name", "n_regionkey", "n_comment"],
    "supplier": ["s_suppkey", "s_name", "s_address", "s_nationkey", "s_phone", "s_acctbal", "s_comment"],
    "customer": ["c_custkey", "c_name", "c_address", "c_nationkey", "c_phone", "c_acctbal", "c_mktsegment", "c_comment"],
    "part": ["p_partkey", "p_name", "p_mfgr", "p_brand", "p_type", "p_size", "p_container", "p_retailprice", "p_comment"],
    "partsupp": ["ps_partkey", "ps_suppkey", "ps_availqty", "ps_supplycost", "ps_comment"],
    "orders": ["o_orderkey", "o_custkey", "o_orderstatus", "o_totalprice", "o_orderdate", "o_orderpriority", "o_clerk", "o_shippriority", "o_comment"],
    "lineitem": ["l_orderkey", "l_partkey", "l_suppkey", "l_linenumber", "l_quantity", "l_extendedprice", "l_discount", "l_tax", "l_returnflag", "l_linestatus", "l_shipdate", "l_commitdate", "l_receiptdate", "l_shipinstruct", "l_shipmode", "l_comment"]
}

TYPE_MAPPING = {
    "INTEGER": "Int32",
    "NUMERIC": "Float64",
    "TEXT": "String",
    "DATE": "Date"
}

def guess_type(col):
    if "date" in col:
        return TYPE_MAPPING["DATE"]
    elif col.endswith("key") or col.endswith("number") or col.endswith("priority"):
        return TYPE_MAPPING["INTEGER"]
    elif any(word in col for word in ["price", "cost", "discount", "tax", "bal", "quantity"]):
        return TYPE_MAPPING["NUMERIC"]
    else:
        return TYPE_MAPPING["TEXT"]

def create_table(name, cols):
    col_defs = [f"{col} {guess_type(col)}" for col in cols]
    ddl = f"""
    CREATE TABLE IF NOT EXISTS {name} (
        {', '.join(col_defs)}
    ) ENGINE = MergeTree()
    ORDER BY tuple();
    """
    client.command(ddl)

def to_date(dat, fmt="%Y-%m-%d"):
    try:
        return datetime.strptime(dat, fmt).date()
    except:
        return dat

def load_table(name, cols):
    path = os.path.join(DATA_DIR, f"{name}.tbl")
    data = []
    with open(path, "r") as f:
        for line in f:
            row = line.strip().split("|")
            row = list(map(to_date, row))
            if len(row) < len(cols):
                continue
            data.append(tuple(row[:len(cols)]))
    client.insert(name, data, column_names=cols)

for table, columns in TABLES.items():
    print(f"Creating/loading: {table}")
    create_table(table, columns)
    load_table(table, columns)

print("✅ ClickHouse TPC-H Load Complete.")
