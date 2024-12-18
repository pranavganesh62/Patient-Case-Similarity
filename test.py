import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def preprocess_data():
    test = pd.read_csv('./test.csv')
    train = pd.read_csv('./train.csv')
    data = pd.concat([test, train])
    data = data.drop(columns=['TenYearCHD', 'is_smoking', 'education'])
    for column in ['cigsPerDay', 'BPMeds', 'totChol', 'BMI', 'heartRate', 'glucose']:
        data[column] = data[column].fillna(data[column].median())
    return data, train


def encode_data(X, original_columns):
    for column in X:
        if column in ['age', 'cigsPerDay', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP',
                      'diaBP', 'BMI', 'heartRate', 'glucose']:
            X[column] = pd.to_numeric(X[column], errors='coerce')
    cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    X_encoded = pd.get_dummies(X, columns=cat_features, drop_first=True)
    imputer = SimpleImputer(strategy='median')
    X_encoded_imputed = imputer.fit_transform(X_encoded)  # This will return a numpy.ndarray
    X_encoded_imputed = pd.DataFrame(X_encoded_imputed, columns=X_encoded.columns)
    return X_encoded_imputed


def encode_input_data(input_data, X_encoded):
    input_df = pd.DataFrame([input_data])
    for column in input_df.columns:
        if column in ['age', 'cigsPerDay', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP',
                      'diaBP', 'BMI', 'heartRate', 'glucose']:
            input_df[column] = pd.to_numeric(input_df[column], errors='coerce')

    cat_features = input_df.select_dtypes(include=['object', 'category']).columns.tolist()
    input_df_encoded = pd.get_dummies(input_df, columns=cat_features, drop_first=True)
    input_df_encoded = input_df_encoded.reindex(columns=X_encoded.columns, fill_value=0)
    input_df_encoded = pd.DataFrame(input_df_encoded, columns=X_encoded.columns)
    return input_df_encoded


def find_similar_patients(input_data, X_encoded):
    input_df_encoded = encode_input_data(input_data, X_encoded)
    combined_data = pd.concat([X_encoded, input_df_encoded],ignore_index=True)
    print(combined_data)
    sim_matrix = cosine_similarity(combined_data)
    sim_df = pd.DataFrame(sim_matrix, index=combined_data.index, columns=combined_data.index)

    patient_id = len(X_encoded)
    similarities = sim_df.iloc[patient_id].sort_values(ascending=False).iloc[1:6]
    return similarities


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = {
        'BMI': data['BMI'],
        'BPMeds': data['BPMeds'],
        'age': data['age'],
        'cigsPerDay': data['cigsPerDay'],
        'diaBP': data['diaBP'],
        'diabetes': data['diabetes'],
        'glucose': data['glucose'],
        'heartRate': data['heartRate'],
        'id': data['id'],
        'prevalentHyp': data['prevalentHyp'],
        'prevalentStroke': data['prevalentStroke'],
        'sex': data['sex'],
        'sysBP': data['sysBP'],
        'totChol': data['totChol'],
    }
    pushing_data = {
        'id': data['id'],
        'age': data['age'],
        'education': 1,
        'sex': data['sex'],
        'is_smoking': 'NO',
        'cigsPerDay': data['cigsPerDay'],
        'BPMeds': data['BPMeds'],
        'prevalentStroke': data['prevalentStroke'],
        'prevalentHyp': data['prevalentHyp'],
        'diabetes': data['diabetes'],
        'totChol': data['totChol'],
        'sysBP': data['sysBP'],
        'diaBP': data['diaBP'],
        'BMI': data['BMI'],
        'heartRate': data['heartRate'],
        'glucose': data['glucose'],
        'TenYearCHD': 0,
    }
    data, train = preprocess_data()
    y = train['TenYearCHD']
    X = train[data.columns.difference(['TenYearCHD'])]
    original_columns = X.columns
    X_encoded = encode_data(X, original_columns)
    similar_patients = find_similar_patients(input_data, X_encoded)
    print(similar_patients)
    try:
        existing_data = pd.read_csv('./train.csv')
        csv_columns = existing_data.columns.tolist()
        new_patient = pd.DataFrame([pushing_data], columns=csv_columns)
        df_complete=pd.concat([existing_data,new_patient],axis=0)
        df_complete.to_csv('./train.csv', index=False)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(similar_patients.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
