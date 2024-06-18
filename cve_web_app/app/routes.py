import pandas as pd
from flask import render_template, request
from app import app
from tinydb import TinyDB, Query
import plotly.express as px
import os
import json

# Path to the cves_db.json file in the fetch directory
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'cves_db.json')
db = TinyDB(db_path)

@app.route('/')
def index():
    cves = db.all()
    return render_template('index.html', cves=cves)

@app.route('/visualizations')
def visualizations():
    cves = db.all()
    data = [cve['data'] for cve in cves]

    df = pd.json_normalize(data)

    # Ensure columns exist before using them
    if 'cve.metrics.cvssMetricV31.0.cvssData.baseSeverity' in df.columns:
        severity_data = df['cve.metrics.cvssMetricV31.0.cvssData.baseSeverity'].value_counts().reset_index()
        severity_data.columns = ['severity', 'count']
    else:
        severity_data = pd.DataFrame(columns=['severity', 'count'])

    if 'cve.affects.vendor.vendorData.0.vendorName' in df.columns:
        vendor_data = df['cve.affects.vendor.vendorData.0.vendorName'].value_counts().reset_index()
        vendor_data.columns = ['vendor', 'count']
    else:
        vendor_data = pd.DataFrame(columns=['vendor', 'count'])

    if 'cve.description.description_data.0.value' in df.columns:
        description_data = df['cve.description.description_data.0.value'].value_counts().reset_index()
        description_data.columns = ['description', 'count']
    else:
        description_data = pd.DataFrame(columns=['description', 'count'])

    # Convert to JSON serializable format
    severity_data_json = severity_data.to_dict(orient='records')
    vendor_data_json = vendor_data.to_dict(orient='records')
    description_data_json = description_data.to_dict(orient='records')

    return render_template(
        'visualizations.html',
        severity_data=severity_data_json,
        vendor_data=vendor_data_json,
        description_data=description_data_json
    )
