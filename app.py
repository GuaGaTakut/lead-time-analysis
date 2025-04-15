from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Temporary storage for last DataFrame
last_df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    global last_df
    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(filepath)
    else:
        df = pd.read_csv(filepath)

    if 'Lead Time' not in df.columns:
        return jsonify({'error': 'No "Lead Time" column found.'})

    last_df = df.copy()

    results = {
        'average_lead_time': round(df['Lead Time'].mean(), 2),
        'std_dev_lead_time': round(df['Lead Time'].std(), 2),
        'max_lead_time': round(df['Lead Time'].max(), 2),
        'min_lead_time': round(df['Lead Time'].min(), 2)
    }

    fig = px.histogram(df, x='Lead Time', title='Lead Time Distribution')
    histogram_html = pio.to_html(fig, full_html=False)

    return jsonify({
        'stats': results,
        'histogram': histogram_html
    })

@app.route('/download_report', methods=['GET'])
def download_report():
    global last_df

    if last_df.empty:
        return "No data uploaded yet.", 400

    # Create a summary DataFrame
    summary = {
        'Metric': ['Average', 'Standard Deviation', 'Maximum', 'Minimum'],
        'Lead Time': [
            round(last_df['Lead Time'].mean(), 2),
            round(last_df['Lead Time'].std(), 2),
            round(last_df['Lead Time'].max(), 2),
            round(last_df['Lead Time'].min(), 2)
        ]
    }

    summary_df = pd.DataFrame(summary)

    # Save to CSV
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'lead_time_report.csv')
    summary_df.to_csv(report_path, index=False)

    return send_file(report_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
