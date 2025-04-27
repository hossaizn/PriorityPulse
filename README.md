# PriorityPulse


# Backlog Prioritization Tool

A minimal Flask-based web application that helps product teams prioritize their backlog items using the RICE scoring method. This version uses only built-in Python modules and minimal dependencies to run on restricted environments.

## Project Overview

The Product Backlog Prioritization Tool allows you to:

1. Upload a CSV file containing your product backlog items with evaluation metrics
2. Calculate RICE scores for each feature (Reach × Impact × Confidence ÷ Effort)
3. View a color-coded prioritized list of features
4. Download the prioritized list as a CSV file

RICE scoring helps teams make data-driven decisions about which features to prioritize by considering:
- **Reach**: How many users will be affected by this feature
- **Impact**: How much each user will be affected (on a scale of 1-10)
- **Confidence**: How confident you are in your estimates (0-100%)
- **Effort**: How many person-months it will take to implement

## Setup Instructions

### Prerequisites
- Python 3.6+
- Basic web browser

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/backlog-tool.git
   cd backlog-tool
   ```

2. Install minimal dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application Locally

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and visit:
   ```
   http://localhost:5000
   ```

## How to Use

### Uploading Data

1. Prepare a CSV file with the following required columns:
   - `Feature`: Name or description of the feature
   - `Reach`: Estimated number of users affected
   - `Impact`: Score from 1-10 on how much this impacts users
   - `Confidence`: Percentage (0-100) indicating your confidence in the estimates
   - `Effort`: Number of person-months required for implementation

2. On the home page, click "Choose File" and select your CSV file.

3. Click "Calculate RICE Scores" to process your data.

### Viewing Results

The results page displays:
- A table with all your features sorted by RICE score (highest to lowest)
- Color-coding based on priority levels:
  - Green: High priority (RICE > 10)
  - Yellow: Medium priority (5 < RICE ≤ 10)
  - Red: Low priority (RICE ≤ 5)

### Downloading Prioritized Data

1. On the results page, click the "Download CSV" button.
2. The CSV file will include all original columns plus the calculated RICE score.

## Sample Data

A sample CSV file is provided in the `examples` directory. You can also download a sample directly from the application by clicking "Download Sample CSV" on the home page.

## Project Structure

```
priority-pulse/
├── app.py                  # Main Flask application
├── requirements.txt        # Minimal Python dependencies
├── static/
│   └── css/
│       └── style.css       # Custom CSS
├── templates/
│   ├── base.html           # Base HTML
│   ├── upload.html         
│   └── results.html        
├── uploads/                # Temporary storage for processed files
└── examples/
    └── feature_requests.csv  # Sample CSV data
```
