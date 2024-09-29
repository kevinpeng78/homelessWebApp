from flask import Flask, render_template, request, jsonify
import geopandas as gpd
import os

app = Flask(__name__)

# Load data on startup
dataPath = "completedHomelessData.zip"
gdf = gpd.read_file(dataPath)
gdf = gdf.explode()
gdf = gdf.groupby('NAME').first().reset_index()

towns = gdf['NAME'].tolist()

@app.route('/')
def index():
    return render_template('index.html', towns=towns)

@app.route('/get_town_data')
def get_town_data():
    selectedTown = request.args.get('town')
    townData = gdf.loc[gdf['NAME'] == selectedTown]
    if townData.empty:
        return jsonify({'error': 'Town not found'}), 404
    displayColumns = ['iP', 'iUE', 'iNS', 'iSP', 'iRI']
    columnNames = {
        'iP': 'Poverty Index',
        'iUE': 'Unemployment Index',
        'iNS': 'Lack of Education Index',
        'iSP': 'Single Parent Index',
        'iRI': 'Rent Income Index'
    }
    data = {}
    for col in displayColumns:
        data[columnNames[col]] = round(townData.iloc[0][col], 3)
    data['Homelessness Index'] = round(townData.iloc[0]['iH'], 3)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
