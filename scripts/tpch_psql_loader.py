import psycopg2
import os
import csv
import json


DATA_DIR = "/data"
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

psql_conn = json.loads(os.environ['PSQL_CONN'])
conn = psycopg2.connect(
    dbname=psql_conn["dbname"],
    user=psql_conn["user"],
    password=psql_conn["password"],
    host=psql_conn["host"],
    port=psql_conn["port"]
)
cur = conn.cursor()

def create_table(name, cols):
    col_defs = []
    for col in cols:
        if col.endswith("key") or col.endswith("number"):
            col_defs.append(f"{col} INTEGER")
        elif "date" in col:
            col_defs.append(f"{col} DATE")
        elif col.startswith("l_") and "price" in col:
            col_defs.append(f"{col} NUMERIC(12,2)")
        elif col.endswith("bal") or col.endswith("price") or col.endswith("cost") or col.endswith("quantity") or col.endswith("discount") or col.endswith("tax"):
            col_defs.append(f"{col} NUMERIC")
        else:
            col_defs.append(f"{col} TEXT")

    schema = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(col_defs)});"
    cur.execute(schema)
    conn.commit()

def load_table(name, cols):
    path = os.path.join(DATA_DIR, f"{name}.tbl")
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            if not row or row == ['']:
                continue
            values = row[:len(cols)]
            placeholders = ','.join(['%s'] * len(cols))
            cur.execute(f"INSERT INTO {name} VALUES ({placeholders})", values)
    conn.commit()

for table, columns in TABLES.items():
    print(f"Loading table: {table}")
    create_table(table, columns)
    load_table(table, columns)

cur.close()
conn.close()
print("✅ PostgreSQL TPC-H Load Complete.")
