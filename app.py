from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
import csv
import os
import io
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if the uploaded file has a CSV extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


def calculate_rice(data, headers):
    """Calculate RICE score for each row in the data"""
    try:
        # Find the column indices
        reach_idx = headers.index('Reach')
        impact_idx = headers.index('Impact')
        confidence_idx = headers.index('Confidence')
        effort_idx = headers.index('Effort')

        # Process each row and add RICE score
        processed_data = []
        for row in data:
            try:
                # Convert values to float for calculation
                reach = float(row[reach_idx])
                impact = float(row[impact_idx])
                confidence = float(row[confidence_idx])
                effort = float(row[effort_idx])

                # Calculate RICE score
                rice = (reach * impact *
                        (confidence / 100)) / effort if effort > 0 else 0

                # Add RICE score to the row
                new_row = row.copy()
                new_row.append(rice)
                processed_data.append(new_row)
            except (ValueError, ZeroDivisionError):
                # Handle rows with invalid data
                new_row = row.copy()
                new_row.append(0)  # Default RICE score for invalid rows
                processed_data.append(new_row)

        # Sort data by RICE score (descending)
        processed_data.sort(key=lambda x: x[-1], reverse=True)

        return processed_data
    except Exception as e:
        raise ValueError(f"Error calculating RICE scores: {str(e)}")


@app.route('/')
def index():
    """Display the file upload form"""
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    # If user doesn't select file, browser submits an empty file
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        try:
            # Read CSV file
            csv_data = []
            file_content = io.StringIO(file.read().decode('utf-8'))
            csv_reader = csv.reader(file_content)
            headers = next(csv_reader)  # Get the header row

            for row in csv_reader:
                csv_data.append(row)

            # Check for required columns
            required_columns = [
                'Feature', 'Reach', 'Impact', 'Confidence', 'Effort'
            ]
            missing_columns = [
                col for col in required_columns if col not in headers
            ]

            if missing_columns:
                flash(
                    f"Missing required columns: {', '.join(missing_columns)}")
                return redirect(url_for('index'))

            # Calculate RICE scores
            processed_data = calculate_rice(csv_data, headers)

            # Add RICE to headers
            new_headers = headers.copy()
            new_headers.append('RICE')

            # Store processed data in session as CSV
            output = io.StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow(new_headers)
            csv_writer.writerows(processed_data)

            session['last_processed_data'] = output.getvalue()

            # Generate a unique filename for this upload
            filename = f"{uuid.uuid4().hex}.csv"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            with open(filepath, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(new_headers)
                csv_writer.writerows(processed_data)

            session['last_file_path'] = filepath

            # Convert data to dict format for template
            dict_data = []
            for row in processed_data:
                row_dict = {}
                for i, col in enumerate(new_headers):
                    if i < len(row):
                        # Format RICE score to 2 decimal places if it's the RICE column
                        if col == 'RICE':
                            row_dict[col] = round(row[i], 2)
                        else:
                            row_dict[col] = row[i]
                    else:
                        row_dict[col] = ""
                dict_data.append(row_dict)

            return render_template('results.html',
                                   data=dict_data,
                                   columns=new_headers)

        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(url_for('index'))

    flash('Invalid file format. Please upload a CSV file.')
    return redirect(url_for('index'))


@app.route('/download')
def download_file():
    # Check if there's processed data in the session
    if 'last_processed_data' not in session:
        flash('No processed data available for download')
        return redirect(url_for('index'))

    # Return the CSV as a downloadable attachment
    return send_file(io.BytesIO(session['last_processed_data'].encode()),
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='prioritized_backlog.csv')


@app.route('/sample')
def download_sample():
    """Provide a sample CSV file for users to download"""
    sample_file = os.path.join('examples', 'feature_requests.csv')
    return send_file(sample_file,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='sample_features.csv')


def create_sample_csv():
    """Create a sample CSV file with dummy data"""
    sample_file = os.path.join('examples', 'feature_requests.csv')
    os.makedirs('examples', exist_ok=True)

    if not os.path.exists(sample_file):
        features = [
            'User authentication system', 'Dashboard analytics',
            'Mobile responsive design', 'Export to PDF feature',
            'Email notification system'
        ]
        reach = [5000, 3000, 8000, 1000, 6000]
        impact = [8, 7, 9, 5, 6]
        confidence = [80, 90, 70, 95, 85]
        effort = [13, 5, 8, 3, 10]

        with open(sample_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Feature', 'Reach', 'Impact', 'Confidence', 'Effort'])
            for i in range(5):
                writer.writerow([
                    features[i], reach[i], impact[i], confidence[i], effort[i]
                ])


# Always create sample file on startup
create_sample_csv()

if __name__ == '__main__':
    app.run(debug=True)
