from flask import (
    Blueprint, jsonify, current_app
)
from .db import get_db
import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from flask import Flask , request, abort

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    if dropnan:
        agg.dropna(inplace=True)

    return agg

bp = Blueprint("prediction", __name__, url_prefix="/predict")

@bp.route('/consumption',methods=['POST'])
def predict_consumption():
    data = request.get_json()
    contract_account_id=data['contract_account_id']

    db = get_db()
    r = db.execute(f"SELECT Total_Consumption, Square_Meters, PoD_Postal_Code FROM ppc \
                    where Contract_Account_ID = {contract_account_id} ORDER BY Year DESC, Month DESC LIMIT 12").fetchall()
    db_result = [list(ele) for ele in r]

    sc=MinMaxScaler(feature_range=(-1, 1))

    #X_tmp=np.array([[100,10,111],[150,10,111],[200,10,111],[100,10,111],[100,10,111],[150,10,111],[200,10,111],[100,10,111],[100,10,111],[150,10,111],[200,10,111],[100,10,111],[100,10,111],[150,10,111],[200,10,111],[100,10,111]])
    X_tmp = np.array(db_result)
    scaled = sc.fit_transform(X_tmp)
    sqm_tmp=scaled[0,1]
    postal_code=scaled[0,2]
    X_tmp=series_to_supervised(scaled, 11, 1)
    model_lstm=keras.models.load_model(f"{current_app.root_path}/saved_soppco_model")
    X_tmp=X_tmp.values
    print("X_tmp.shape=",str(X_tmp.shape))
    X_tmp=X_tmp.reshape(X_tmp.shape[0],12,3)
    y_pred_lstm = model_lstm.predict(X_tmp)[-1]

    y_tmp=y_pred_lstm.reshape(y_pred_lstm.shape[0],-1)
    y_complete_new=np.concatenate((y_tmp,sqm_tmp*np.ones(y_tmp.shape),postal_code*np.ones(y_tmp.shape)),axis=1)
    y_pred_unsc=sc.inverse_transform(y_complete_new)

    print(str(y_pred_unsc))
    ret={'prediction':y_pred_unsc[:,0].tolist()}
    #return str(y_pred_unsc[:,0].tolist()) #y_pred_lstm.shape
    return ret

#Example: Access to database and perform a simple query
#Check schema.sql 
@bp.route('/example')
def method_name():
    db = get_db()
    r = db.execute(f"SELECT id, PoD_Postal_Code FROM ppc LIMIT 5").fetchall()
    return jsonify(r)  