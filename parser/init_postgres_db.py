from __future__ import annotations

import os

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DDL = """
CREATE TABLE IF NOT EXISTS encar_listings (
    car_id BIGINT PRIMARY KEY,
    "марка" TEXT NOT NULL DEFAULT '',
    "модель" TEXT NOT NULL DEFAULT '',
    "год" TEXT,
    "пробег" INTEGER,
    "цена" BIGINT,
    "фото" TEXT,
    detail_url TEXT NOT NULL DEFAULT '',
    title_raw TEXT,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS encar_listings_updated_at_idx
    ON encar_listings (updated_at DESC);
"""


def main() -> None:
    host = os.environ.get("PGHOST", "localhost")
    port = int(os.environ.get("PGPORT", "5432"))
    user = os.environ.get("PGUSER", "postgres")
    password = os.environ.get("PGPASSWORD", "1234")
    new_db = os.environ.get("PGDATABASE_NEW", "encar")

    admin = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname="postgres",
    )
    admin.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        with admin.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (new_db,),
            )
            if not cur.fetchone():
                cur.execute(
                    sql.SQL("CREATE DATABASE {} ENCODING %s TEMPLATE template0").format(
                        sql.Identifier(new_db)
                    ),
                    ["UTF8"],
                )
                print(f"Created database: {new_db}")
            else:
                print(f"Database already exists: {new_db}")
    finally:
        admin.close()

    conn = psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=new_db,
    )
    try:
        conn.set_client_encoding("UTF8")
        with conn.cursor() as cur:
            cur.execute(DDL)
        conn.commit()
        print("Table encar_listings is ready (columns: марка, модель, год, пробег, цена, фото, …).")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
