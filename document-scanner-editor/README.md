# Course Data Validator

A comprehensive Python application for validating course data from Excel files, CSV files, or Google Sheets with real-time progress tracking and error highlighting.

## 🚀 Features

### **Data Input Support**
- **Excel Files** (.xlsx, .xls)
- **CSV Files** (.csv)
- **Google Sheets** (with API credentials)

### **Validation Rules**
- **Institution ID**: Must be numeric
- **Course ID**: Must be numeric and unique
- **Course Name**: Must start with capital letter, conjunctions lowercase
- **L3 Tagging**: Must not be blank
- **Degree Type**: Must not be blank
- **Course Type**: Must not be blank
- **Course Start Date**: Must be in YYYY-MM-DD format
- **Course Level URL**: Must be working URLs (no 404 errors)
- **Course Intake IDs**: Count must match start dates, must be unique
- **Show**: Must be "Yes" or "No"
- **Course Status**: Must be "Open" or "Closed"
- **Study Mode**: Must be "Full time" or "Part time"

### **Real-time Features**
- **Progress Window**: Shows validation progress with current row data
- **Error Highlighting**: Color-coded errors in real-time
- **Data Table View**: Interactive table with error indicators
- **Export Results**: Excel export with color-coded error highlighting

## 📁 File Structure

```
document-scanner-editor/
├── main.py                 # Main application with GUI
├── validators.py           # All validation functions
├── I_o_file.py            # Excel/CSV I/O operations
├── progresswindow.py      # Real-time progress display
├── create_sample_data.py  # Sample data generator
├── run.py                 # Application launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Setup
1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### For Google Sheets Support
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create a service account and download `credentials.json`
4. Place `credentials.json` in the project directory

## 🎯 Usage

### Quick Start
1. **Run the application**:
   ```bash
   python run.py
   # or
   python main.py
   ```

2. **Load data**:
   - Click "Browse" to select an Excel/CSV file, OR
   - Enter a Google Sheets URL and click "Load Sheets"

3. **Start validation**:
   - Click "Start Validation"
   - Watch real-time progress in the popup window

4. **View results**:
   - Check the "Validation Results" tab for detailed errors
   - View data in the "Data View" tab

5. **Export results**:
   - Click "Export Results" to save as Excel file with error highlighting

### Create Sample Data
- Click "Create Sample Data" to generate test files with intentional errors
- Use these files to test the validation features

## 📊 Output Format

### Excel Export Features
- **Validated Data Sheet**: Original data with color-coded error highlighting
- **Validation Summary Sheet**: Statistics and error breakdown
- **Error Details Sheet**: Detailed list of all errors

### Error Color Coding
- **Red**: URL errors (404s, not accessible)
- **Orange**: Duplicate/Unique errors
- **Yellow**: Capitalization errors
- **Pink**: Blank field errors
- **Blue**: Date format errors
- **Purple**: Count mismatch errors
- **Light Blue**: Status errors

## 🔧 Configuration

### Validation Options
The application validates all fields by default. You can modify validation rules in `validators.py`.

### Data Format
The application handles various column name formats and automatically maps them to standard names:
- `Instituti` → `Institution Id`
- `Course I` → `Course Id`
- `Course TDegree` → `Degree Type`
- `Course` → `Course Name`
- `L3 Taggi` → `L3 Tagging`
- `Course sCourse` → `Course start date`
- And more...

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Google Sheets Not Working**:
   - Ensure `credentials.json` is in the project directory
   - Check that Google Sheets API is enabled

3. **Tkinter Not Found**:
   ```bash
   # Ubuntu/Debian
   sudo apt install python3-tk
   
   # macOS
   brew install python-tk
   ```

4. **Permission Errors**:
   - Ensure you have write permissions in the project directory

### Error Types
- **Numeric**: Non-numeric values in numeric fields
- **Unique**: Duplicate values where uniqueness is required
- **Capitalization**: Wrong capitalization in course names
- **Blank**: Required fields that are empty
- **Date**: Invalid date formats
- **URL**: Non-working or inaccessible URLs
- **Count**: Mismatched counts between related fields
- **Status**: Invalid status values

## 📝 Sample Data Format

The application expects data in this format:

| Institution Id | Course Id | Course Name | L3 Tagging | Course start date | ... |
|----------------|-----------|-------------|------------|-------------------|-----|
| 108 | 986855 | Business | Business | 2024-09-01 | ... |
| 108 | 986856 | Computer Science | Computer Science | 2024-09-01 | ... |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the error messages in the application
3. Create an issue with detailed information

---

**Happy Validating! 🎉**
