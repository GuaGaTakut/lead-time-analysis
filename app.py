@app.route('/download_report', methods=['GET'])
def download_report():
    global last_df

    if last_df.empty:
        return "No data uploaded yet.", 400

    df = last_df.copy()

    # Summary stats
    average = df['Lead Time'].mean()
    std_dev = df['Lead Time'].std()
    max_val = df['Lead Time'].max()
    min_val = df['Lead Time'].min()

    # Add lead time variance column (row deviation from mean)
    df['Lead Time Variance'] = df['Lead Time'] - average

    report_path = os.path.join(app.config['UPLOAD_FOLDER'], 'full_lead_time_report.csv')

    # Optional monthly average (if date column exists)
    monthly_path = None
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        monthly_avg = df.groupby(df['Date'].dt.to_period('M'))['Lead Time'].mean().reset_index()
        monthly_avg.columns = ['Month', 'Average Lead Time']
        monthly_path = os.path.join(app.config['UPLOAD_FOLDER'], 'monthly_avg_lead_time.csv')
        monthly_avg.to_csv(monthly_path, index=False)

    # Save detailed dataset
    df.to_csv(report_path, index=False)

    # Optionally zip both reports
    if monthly_path:
        import zipfile
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'lead_time_reports.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(report_path, arcname='full_lead_time_report.csv')
            zf.write(monthly_path, arcname='monthly_avg_lead_time.csv')
        return send_file(zip_path, as_attachment=True)

    return send_file(report_path, as_attachment=True)
