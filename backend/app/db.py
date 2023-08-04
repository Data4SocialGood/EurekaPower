import sqlite3
import csv
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        #g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    cursor = db.cursor()
    insert_records = "INSERT INTO ppc (\
            Year,\
            Month,\
            Power_Supplier,\
            HM_EKD,\
            Contract_Account_ID,\
            Login_Date,\
            AR_PAROXIS_11,\
            Meter_Number,\
            Start_Period,\
            End_Period,\
            Total_ConsumptionDayPeak,\
            Total_ConsumptionNightOffpeak,\
            Total_Consumption,\
            Metering_Period,\
            PoD_Postal_Code,\
            Square_Meters)\
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    
    file = open(f"{current_app.root_path}/Inovationhub_mini A.csv")
    contents = csv.reader(file)
    print(f"{current_app.root_path}/client_db/Inovationhub_mini A.csv")
    cursor.executemany(insert_records, contents)

    # Test users.  (Contract_Account_ID, Keycloak_ID(Sub)) 
    insert_users = "INSERT INTO sub (Contract_Account_ID, Keycloak_Account_ID) VALUES (:Contract_Account_ID,:Keycloak_Account_ID)"
    users = ({"Contract_Account_ID": "363000024", "Keycloak_Account_ID":"a24275cd-3fa9-4567-8579-480a9b9dd51c"})
    cursor.execute(insert_users,users)

    db.commit()
    close_db()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
