from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Read Excel or CSV
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        df = pd.read_csv(filepath)

    # Assuming a column called 'Lead Time'
    if 'Lead Time' not in df.columns:
        return jsonify({'error': 'No "Lead Time" column found.'})

    results = {
        'average_lead_time': round(df['Lead Time'].mean(), 2),
        'std_dev_lead_time': round(df['Lead Time'].std(), 2),
        'max_lead_time': round(df['Lead Time'].max(), 2),
        'min_lead_time': round(df['Lead Time'].min(), 2)
    }

    # Generate histogram
    fig = px.histogram(df, x='Lead Time', title='Lead Time Distribution')
    histogram_html = pio.to_html(fig, full_html=False)

    return jsonify({
        'stats': results,
        'histogram': histogram_html
    })

if __name__ == '__main__':
    app.run(debug=True)
