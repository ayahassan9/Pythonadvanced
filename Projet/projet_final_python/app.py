from flask import Flask, request, render_template, url_for, redirect
import pandas as pd
import os
import plotly.express as px

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handles the upload of CSV files."""
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return redirect(url_for('preview_file', filename=file.filename))
    return render_template('upload.html')

@app.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    """Displays a preview of the CSV file and its descriptive statistics."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path)
    preview = df.head().to_html(classes='table table-striped table-bordered', index=False)
    # Calculate descriptive statistics for numeric columns
    stats = df.describe().to_html(classes='table table-striped table-bordered', index=True)
    return render_template('preview.html', preview=preview, stats=stats, filename=filename)

@app.route('/visualize/<filename>', methods=['GET', 'POST'])
def visualize_file(filename):
    """Generates visualizations for the CSV data."""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(file_path)
    if request.method == 'POST':
        x_axis = request.form['x_axis']
        y_axis = request.form['y_axis']
        graph_type = request.form['graph_type']
        if graph_type == 'scatter':
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{graph_type.capitalize()} Plot")
        elif graph_type == 'line':
            fig = px.line(df, x=x_axis, y=y_axis, title=f"{graph_type.capitalize()} Chart")
        elif graph_type == 'bar':
            fig = px.bar(df, x=x_axis, y=y_axis, title=f"{graph_type.capitalize()} Graph")
        graph = fig.to_html(full_html=False)
        return render_template('visualize.html', graph=graph, columns=df.columns)
    return render_template('visualize.html', columns=df.columns)
if __name__ == '__main__':
    app.run(debug=True)