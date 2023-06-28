from flask import (
    Blueprint, flash, jsonify, url_for, current_app
)
from .db import get_db
import json
from flask import Flask , request, abort

bp = Blueprint("api", __name__, url_prefix="/users")

@bp.route('/contract-id/<sub>')
def get_contract_id(sub):
    db = get_db()

    r = db.execute(f"SELECT Contract_Account_ID FROM sub \
                     where Keycloak_Account_ID = '{sub}'").fetchone()
    
    return {"contract_account_id":r[0]}


@bp.route('/history/',methods=['POST'])
def method_name():
    data = request.get_json()
    contract_account_id=int(data['contract_account_id'])
    year=int(data['year'])

    db = get_db()
    r = db.execute(f"SELECT Total_Consumption, Month FROM ppc \
                    where Contract_Account_ID = {contract_account_id} AND Year = {year} ORDER BY Year DESC, Month DESC").fetchall()
    dict={'consumption_month':r}
    return dict

@bp.route('/userinfo/',methods=['POST'])
def get_user_data():
    data = request.get_json()
    contract_account_id=int(data['contract_account_id'])

    db = get_db()
    r = db.execute(f"SELECT AR_PAROXIS_11,Square_Meters,PoD_Postal_Code FROM ppc where Contract_Account_ID = {contract_account_id} LIMIT 1").fetchall()
    dict={'AR_PAROXIS_11,Square_Meters,PoD_Postal_Code':r}
    return dict

@bp.route('/historical_data/',methods=['POST'])
def get_hist_data():
    data = request.get_json()
    contract_account_id=int(data['contract_account_id'])

    db = get_db()
    r = db.execute(f"SELECT Year,Month,Total_Consumption,Metering_Period,PoD_Postal_Code,Square_Meters FROM ppc where Contract_Account_ID = {contract_account_id}").fetchall()
    dict={'Year,Month,Total_Consumption,Metering_Period,PoD_Postal_Code,Square_Meters':r}
    return dict
