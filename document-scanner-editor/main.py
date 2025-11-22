#!/usr/bin/env python3
"""
Course Data Validator - Main Application
Comprehensive UI application for validating course data
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import re
from urllib.parse import urlparse
import os
from typing import Dict, List, Optional
from datetime import datetime

# Import our custom modules
from validators import validators
from io_file import excel_handler
from progresswindow import ProgressWindow

class CourseDataValidatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Course Data Validator - Professional Edition")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Data storage
        self.df = None
        self.validation_errors = []
        self.progress_window = None
        self.is_validating = False
        
        # Setup UI
        self.setup_ui()
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header
        self.setup_header(main_container)
        
        # Main content area with notebook
        self.setup_notebook(main_container)
        
        # Status bar
        self.setup_status_bar(main_container)
        
    def setup_header(self, parent):
        """Setup the header section"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, text="Course Data Validator", 
                               font=('Arial', 18, 'bold'), foreground='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Input section
        input_frame = ttk.LabelFrame(header_frame, text="Data Input", padding="15")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # File input
        ttk.Label(input_frame, text="Excel/CSV File:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(input_frame, textvariable=self.file_path_var, width=60, font=('Arial', 9))
        file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(input_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=5)
        
        # Google Sheets input
        ttk.Label(input_frame, text="Google Sheets URL:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sheets_url_var = tk.StringVar()
        sheets_entry = ttk.Entry(input_frame, textvariable=self.sheets_url_var, width=60, font=('Arial', 9))
        sheets_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        ttk.Button(input_frame, text="Load Sheets", command=self.load_google_sheets).grid(row=1, column=2, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Validation", command=self.start_validation)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(button_frame, text="Export Results", command=self.export_results, state='disabled')
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.sample_button = ttk.Button(button_frame, text="Create Sample Data", command=self.create_sample_data)
        self.sample_button.pack(side=tk.LEFT)
        
    def setup_notebook(self, parent):
        """Setup the notebook with tabs"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Summary tab
        self.setup_summary_tab()
        
        # Validation Results tab
        self.setup_validation_tab()
        
        # Data View tab
        self.setup_data_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
    def setup_summary_tab(self):
        """Setup the summary tab"""
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Summary")
        
        # Summary content
        summary_content = ttk.Frame(summary_frame, padding="20")
        summary_content.pack(fill=tk.BOTH, expand=True)
        
        # Welcome message
        welcome_text = """
Welcome to Course Data Validator!

This application helps you validate course data from Excel files, CSV files, or Google Sheets.

Features:
• Validate Institution IDs (must be numeric)
• Check Course IDs for uniqueness
• Validate course name capitalization
• Check required fields (L3 Tagging, Degree Type, etc.)
• Validate date formats (YYYY-MM-DD)
• Test URLs for accessibility (no 404 errors)
• Validate study modes and status values
• Export results with color-coded highlighting

To get started:
1. Select an Excel/CSV file or enter a Google Sheets URL
2. Click "Start Validation" to begin the process
3. View results in the Validation Results tab
4. Export the validated data with error highlighting

Click "Create Sample Data" to generate test files with intentional errors.
        """
        
        self.summary_text = scrolledtext.ScrolledText(summary_content, height=20, width=80, 
                                                     font=('Arial', 10), wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.insert(tk.END, welcome_text)
        self.summary_text.config(state=tk.DISABLED)
        
    def setup_validation_tab(self):
        """Setup the validation results tab"""
        validation_frame = ttk.Frame(self.notebook)
        self.notebook.add(validation_frame, text="Validation Results")
        
        # Validation content
        validation_content = ttk.Frame(validation_frame, padding="20")
        validation_content.pack(fill=tk.BOTH, expand=True)
        validation_content.columnconfigure(0, weight=1)
        validation_content.rowconfigure(1, weight=1)
        
        # Results header
        results_header = ttk.Frame(validation_content)
        results_header.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.results_label = ttk.Label(results_header, text="No validation results yet", 
                                      font=('Arial', 12, 'bold'))
        self.results_label.pack(side=tk.LEFT)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(validation_content, height=25, width=100, 
                                                     font=('Consolas', 9), wrap=tk.WORD)
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_data_tab(self):
        """Setup the data view tab"""
        data_frame = ttk.Frame(self.notebook)
        self.notebook.add(data_frame, text="Data View")
        
        # Data content
        data_content = ttk.Frame(data_frame, padding="20")
        data_content.pack(fill=tk.BOTH, expand=True)
        data_content.columnconfigure(0, weight=1)
        data_content.rowconfigure(0, weight=1)
        
        # Data treeview
        self.setup_data_treeview(data_content)
        
    def setup_data_treeview(self, parent):
        """Setup the data treeview"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        self.data_tree = ttk.Treeview(tree_frame, show='headings', height=20)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.data_tree.xview)
        
        self.data_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.data_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure parent grid weights
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
    def setup_settings_tab(self):
        """Setup the settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings content
        settings_content = ttk.Frame(settings_frame, padding="20")
        settings_content.pack(fill=tk.BOTH, expand=True)
        
        # Validation options
        options_frame = ttk.LabelFrame(settings_content, text="Validation Options", padding="15")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Checkboxes for validation types
        self.validate_urls_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Validate URLs (check for broken links)", 
                       variable=self.validate_urls_var).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.validate_dates_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Validate Date Formats", 
                       variable=self.validate_dates_var).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        self.validate_uniqueness_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Check for Duplicates", 
                       variable=self.validate_uniqueness_var).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.validate_capitalization_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Validate Capitalization", 
                       variable=self.validate_capitalization_var).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # URL validation info
        url_info_frame = ttk.LabelFrame(settings_content, text="URL Validation Info", padding="15")
        url_info_frame.pack(fill=tk.X, pady=(0, 20))
        
        url_info_text = """
URL Validation Settings:
• 404 (Not Found) - Flagged as error
• 410 (Gone) - Flagged as error  
• 500, 502, 503, 504 (Server Errors) - Flagged as error
• 403 (Forbidden) - NOT flagged (often blocks bots but URL exists)
• 401 (Unauthorized) - NOT flagged (might require login)
• 429 (Too Many Requests) - NOT flagged (temporary)
• Timeouts and connection errors - Flagged as error

This helps avoid false positives from servers that block automated requests.
        """
        
        url_info_label = ttk.Label(url_info_frame, text=url_info_text, justify=tk.LEFT, font=('Arial', 9))
        url_info_label.pack(anchor=tk.W)
        
    def setup_status_bar(self, parent):
        """Setup the status bar"""
        self.status_var = tk.StringVar(value="Ready to validate data")
        status_bar = ttk.Label(parent, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_file(self):
        """Browse for Excel or CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel or CSV file",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.sheets_url_var.set("")  # Clear sheets URL
            self.status_var.set(f"Selected file: {os.path.basename(file_path)}")
            
    def extract_sheet_id(self, url: str) -> Optional[str]:
        """Extract Google Sheets ID from URL"""
        pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
        
    def load_google_sheets(self):
        """Load data from Google Sheets"""
        sheets_url = self.sheets_url_var.get().strip()
        if not sheets_url:
            messagebox.showerror("Error", "Please enter a Google Sheets URL")
            return
            
        try:
            # Extract sheet ID
            sheet_id = self.extract_sheet_id(sheets_url)
            if not sheet_id:
                messagebox.showerror("Error", "Invalid Google Sheets URL")
                return
                
            self.status_var.set("Loading Google Sheets data...")
            self.root.update()
            
            # Load Google Sheets data
            self.df = self.load_sheets_data(sheet_id)
            
            if self.df is not None:
                self.status_var.set(f"Loaded {len(self.df)} rows from Google Sheets")
                self.file_path_var.set("")  # Clear file path
                self.update_data_display()
                messagebox.showinfo("Success", f"Successfully loaded {len(self.df)} rows from Google Sheets")
            else:
                self.status_var.set("Failed to load Google Sheets data")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Google Sheets: {str(e)}")
            self.status_var.set("Error loading Google Sheets")
            
    def load_sheets_data(self, sheet_id: str) -> Optional[pd.DataFrame]:
        """Load data from Google Sheets using service account"""
        try:
            # Check for credentials file
            creds_file = 'credentials.json'
            if os.path.exists(creds_file):
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                
                creds = Credentials.from_service_account_file(creds_file, scopes=scope)
                client = gspread.authorize(creds)
                
                # Open the spreadsheet
                spreadsheet = client.open_by_key(sheet_id)
                worksheet = spreadsheet.get_worksheet(0)  # First sheet
                
                # Get all values
                data = worksheet.get_all_records()
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                return df
            else:
                messagebox.showwarning("Warning", 
                    "Google Sheets credentials not found. Please add 'credentials.json' file for Google Sheets support.")
                return None
                
        except Exception as e:
            print(f"Error loading Google Sheets: {e}")
            return None
            
    def start_validation(self):
        """Start the validation process"""
        if self.is_validating:
            messagebox.showwarning("Warning", "Validation is already in progress!")
            return
            
        # Check if we have data
        if self.df is None:
            # Try to load from file
            file_path = self.file_path_var.get().strip()
            if not file_path:
                messagebox.showerror("Error", "Please select a file or enter Google Sheets URL")
                return
                
            try:
                self.status_var.set("Loading file...")
                self.root.update()
                
                if file_path.endswith('.csv'):
                    self.df, columns = excel_handler.read_csv_file(file_path)
                else:
                    self.df, columns = excel_handler.read_excel_file(file_path)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.status_var.set("Error loading file")
                return
        
        # Clean the data
        self.df = excel_handler.clean_data(self.df)
        
        # Start validation in separate thread
        self.is_validating = True
        self.start_button.config(state='disabled', text="Validating...")
        self.status_var.set("Starting validation...")
        
        validation_thread = threading.Thread(target=self.run_validation)
        validation_thread.daemon = True
        validation_thread.start()
        
    def run_validation(self):
        """Run the validation process"""
        try:
            # Create progress window
            self.progress_window = ProgressWindow(self.root, len(self.df))
            
            # Get all course IDs for uniqueness check
            all_course_ids = []
            if 'Course Id' in self.df.columns:
                all_course_ids = self.df['Course Id'].dropna().tolist()
            
            # Initialize validation errors
            self.validation_errors = []
            
            # Validate each row
            for index, row in self.df.iterrows():
                # Check if user cancelled
                if self.progress_window.cancelled:
                    break
                    
                # Update progress
                self.progress_window.update_progress(index + 1, f"Validating row {index + 1}/{len(self.df)}")
                
                # Validate the row
                row_errors = validators.validate_all_fields(row.to_dict(), index, all_course_ids)
                self.validation_errors.extend(row_errors)
                
                # Update progress window with current row data
                self.progress_window.update_data_display(row.to_dict(), row_errors)
                
                # Small delay to show progress
                import time
                time.sleep(0.1)
            
            # Close progress window
            if self.progress_window:
                self.progress_window.close()
            
            # Update main window
            self.root.after(0, self.validation_complete)
            
        except Exception as e:
            if self.progress_window:
                self.progress_window.close()
            self.root.after(0, lambda: self.validation_error(str(e)))
            
    def validation_complete(self):
        """Called when validation is complete"""
        self.is_validating = False
        self.start_button.config(state='normal', text="Start Validation")
        
        # Display results
        self.display_results()
        
        # Enable export button
        self.export_button.config(state='normal')
        
        # Update status
        total_errors = len(self.validation_errors)
        self.status_var.set(f"Validation complete. Found {total_errors} errors.")
        
        # Show completion message
        if total_errors == 0:
            messagebox.showinfo("Success", "Validation complete! No errors found.")
        else:
            messagebox.showinfo("Validation Complete", 
                              f"Validation complete!\n\nFound {total_errors} errors.\n\nCheck the Validation Results tab for details.")
        
    def validation_error(self, error_message: str):
        """Called when validation encounters an error"""
        self.is_validating = False
        self.start_button.config(state='normal', text="Start Validation")
        messagebox.showerror("Validation Error", f"Error during validation: {error_message}")
        self.status_var.set("Validation failed")
        
    def display_results(self):
        """Display validation results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if not self.validation_errors:
            self.results_text.insert(tk.END, "VALIDATION SUCCESSFUL!\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.results_text.insert(tk.END, f"Successfully validated {len(self.df)} rows.\n")
            self.results_text.insert(tk.END, "No validation errors found.\n\n")
            self.results_label.config(text="Validation Successful - No Errors")
            return
        
        # Summary
        total_errors = len(self.validation_errors)
        rows_with_errors = len(set(error['row'] for error in self.validation_errors))
        
        self.results_text.insert(tk.END, f"VALIDATION COMPLETE WITH ERRORS\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Total Rows Processed: {len(self.df)}\n")
        self.results_text.insert(tk.END, f"Total Errors Found: {total_errors}\n")
        self.results_text.insert(tk.END, f"Rows with Errors: {rows_with_errors}\n\n")
        
        # Error breakdown by type
        error_types = {}
        for error in self.validation_errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        self.results_text.insert(tk.END, "ERROR BREAKDOWN BY TYPE:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        for error_type, count in error_types.items():
            self.results_text.insert(tk.END, f"• {error_type}: {count} errors\n")
        
        self.results_text.insert(tk.END, "\nDETAILED ERRORS BY ROW:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        
        # Group errors by row
        errors_by_row = {}
        for error in self.validation_errors:
            row = error['row']
            if row not in errors_by_row:
                errors_by_row[row] = []
            errors_by_row[row].append(error)
        
        # Display errors by row
        for row in sorted(errors_by_row.keys()):
            self.results_text.insert(tk.END, f"\nRow {row}:\n")
            for error in errors_by_row[row]:
                self.results_text.insert(tk.END, 
                    f"  • {error['column']}: {error['message']}\n")
                self.results_text.insert(tk.END, 
                    f"    Value: '{error['value']}'\n")
        
        self.results_label.config(text=f"Validation Complete - {total_errors} Errors Found")
        self.results_text.config(state=tk.DISABLED)
        
        # Update data display
        self.update_data_display()
        
    def update_data_display(self):
        """Update the data view tab"""
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        if self.df is None:
            return
            
        # Set up columns
        columns = list(self.df.columns)
        self.data_tree['columns'] = columns
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=150, minwidth=100)
            
        # Add data rows
        for index, row in self.df.iterrows():
            values = [str(row[col]) if not pd.isna(row[col]) else '' for col in columns]
            
            # Check if row has errors
            row_errors = [e for e in self.validation_errors if e['row'] == index + 1]
            tags = ('error_row',) if row_errors else ('valid_row',)
            
            self.data_tree.insert('', 'end', values=values, tags=tags)
            
    def export_results(self):
        """Export validation results to Excel"""
        if self.df is None:
            messagebox.showinfo("Info", "No data to export")
            return
            
        try:
            output_path = filedialog.asksaveasfilename(
                title="Save validation results",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if output_path:
                self.status_var.set("Exporting results...")
                self.root.update()
                
                # Export to Excel
                excel_handler.write_excel_with_validation_results(
                    self.df, self.validation_errors, output_path
                )
                
                self.status_var.set(f"Results exported to {os.path.basename(output_path)}")
                messagebox.showinfo("Success", f"Results exported successfully to:\n{output_path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")
            self.status_var.set("Export failed")
            
    def clear_all(self):
        """Clear all results and data"""
        self.df = None
        self.validation_errors = []
        self.file_path_var.set("")
        self.sheets_url_var.set("")
        
        # Clear displays
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        # Reset buttons
        self.export_button.config(state='disabled')
        self.results_label.config(text="No validation results yet")
        self.status_var.set("Ready to validate data")
        
    def create_sample_data(self):
        """Create sample data files"""
        try:
            # Import and run sample data creation
            from create_sample_data import main as create_sample_main
            create_sample_main()
            
            messagebox.showinfo("Success", 
                              "Sample data files created successfully!\n\n"
                              "Files created:\n"
                              "• sample_course_data.xlsx\n"
                              "• sample_course_data_extended.xlsx\n"
                              "• sample_course_data.csv\n\n"
                              "These files contain intentional errors for testing.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample data: {str(e)}")
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    app = CourseDataValidatorApp()
    app.run()

if __name__ == "__main__":
    main()
            
    def load_sheets_data(self, sheet_id: str) -> Optional[pd.DataFrame]:
        """Load data from Google Sheets using service account"""
        try:
            # Check for credentials file
            creds_file = 'credentials.json'
            if os.path.exists(creds_file):
                scope = ['https://spreadsheets.google.com/feeds',
                        'https://www.googleapis.com/auth/drive']
                
                creds = Credentials.from_service_account_file(creds_file, scopes=scope)
                client = gspread.authorize(creds)
                
                # Open the spreadsheet
                spreadsheet = client.open_by_key(sheet_id)
                worksheet = spreadsheet.get_worksheet(0)  # First sheet
                
                # Get all values
                data = worksheet.get_all_records()
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                return df
            else:
                messagebox.showwarning("Warning", 
                    "Google Sheets credentials not found. Please add 'credentials.json' file for Google Sheets support.")
                return None
                
        except Exception as e:
            print(f"Error loading Google Sheets: {e}")
            return None
            
    def start_validation(self):
        """Start the validation process"""
        if self.is_validating:
            messagebox.showwarning("Warning", "Validation is already in progress!")
            return
            
        # Check if we have data
        if self.df is None:
            # Try to load from file
            file_path = self.file_path_var.get().strip()
            if not file_path:
                messagebox.showerror("Error", "Please select a file or enter Google Sheets URL")
                return
                
            try:
                self.status_var.set("Loading file...")
                self.root.update()
                
                if file_path.endswith('.csv'):
                    self.df, columns = excel_handler.read_csv_file(file_path)
                else:
                    self.df, columns = excel_handler.read_excel_file(file_path)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                self.status_var.set("Error loading file")
                return
        
        # Clean the data
        self.df = excel_handler.clean_data(self.df)
        
        # Start validation in separate thread
        self.is_validating = True
        self.start_button.config(state='disabled', text="🔄 Validating...")
        self.status_var.set("Starting validation...")
        
        validation_thread = threading.Thread(target=self.run_validation)
        validation_thread.daemon = True
        validation_thread.start()
        
    def run_validation(self):
        """Run the validation process"""
        try:
            # Create progress window
            self.progress_window = ProgressWindow(self.root, len(self.df))
            
            # Get all course IDs for uniqueness check
            all_course_ids = []
            if 'Course Id' in self.df.columns:
                all_course_ids = self.df['Course Id'].dropna().tolist()
            
            # Initialize validation errors
            self.validation_errors = []
            
            # Validate each row
            for index, row in self.df.iterrows():
                # Check if user cancelled
                if self.progress_window.cancelled:
                    break
                    
                # Update progress
                self.progress_window.update_progress(index + 1, f"Validating row {index + 1}/{len(self.df)}")
                
                # Validate the row
                row_errors = validators.validate_all_fields(row.to_dict(), index, all_course_ids)
                self.validation_errors.extend(row_errors)
                
                # Update progress window with current row data
                self.progress_window.update_data_display(row.to_dict(), row_errors)
                
                # Small delay to show progress
                import time
                time.sleep(0.1)
            
            # Close progress window
            if self.progress_window:
                self.progress_window.close()
            
            # Update main window
            self.root.after(0, self.validation_complete)
            
        except Exception as e:
            if self.progress_window:
                self.progress_window.close()
            self.root.after(0, lambda: self.validation_error(str(e)))
            
    def validation_complete(self):
        """Called when validation is complete"""
        self.is_validating = False
        self.start_button.config(state='normal', text="🚀 Start Validation")
        
        # Display results
        self.display_results()
        
        # Enable export button
        self.export_button.config(state='normal')
        
        # Update status
        total_errors = len(self.validation_errors)
        self.status_var.set(f"Validation complete. Found {total_errors} errors.")
        
        # Show completion message
        if total_errors == 0:
            messagebox.showinfo("Success", "✅ Validation complete! No errors found.")
        else:
            messagebox.showinfo("Validation Complete", 
                              f"Validation complete!\n\nFound {total_errors} errors.\n\nCheck the Validation Results tab for details.")
        
    def validation_error(self, error_message: str):
        """Called when validation encounters an error"""
        self.is_validating = False
        self.start_button.config(state='normal', text="🚀 Start Validation")
        messagebox.showerror("Validation Error", f"Error during validation: {error_message}")
        self.status_var.set("Validation failed")
        
    def display_results(self):
        """Display validation results"""
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        if not self.validation_errors:
            self.results_text.insert(tk.END, "✅ VALIDATION SUCCESSFUL!\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.results_text.insert(tk.END, f"Successfully validated {len(self.df)} rows.\n")
            self.results_text.insert(tk.END, "No validation errors found.\n\n")
            self.results_label.config(text="✅ Validation Successful - No Errors")
            return
        
        # Summary
        total_errors = len(self.validation_errors)
        rows_with_errors = len(set(error['row'] for error in self.validation_errors))
        
        self.results_text.insert(tk.END, f"❌ VALIDATION COMPLETE WITH ERRORS\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Total Rows Processed: {len(self.df)}\n")
        self.results_text.insert(tk.END, f"Total Errors Found: {total_errors}\n")
        self.results_text.insert(tk.END, f"Rows with Errors: {rows_with_errors}\n\n")
        
        # Error breakdown by type
        error_types = {}
        for error in self.validation_errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        self.results_text.insert(tk.END, "ERROR BREAKDOWN BY TYPE:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        for error_type, count in error_types.items():
            self.results_text.insert(tk.END, f"• {error_type}: {count} errors\n")
        
        self.results_text.insert(tk.END, "\nDETAILED ERRORS BY ROW:\n")
        self.results_text.insert(tk.END, "-" * 30 + "\n")
        
        # Group errors by row
        errors_by_row = {}
        for error in self.validation_errors:
            row = error['row']
            if row not in errors_by_row:
                errors_by_row[row] = []
            errors_by_row[row].append(error)
        
        # Display errors by row
        for row in sorted(errors_by_row.keys()):
            self.results_text.insert(tk.END, f"\nRow {row}:\n")
            for error in errors_by_row[row]:
                self.results_text.insert(tk.END, 
                    f"  • {error['column']}: {error['message']}\n")
                self.results_text.insert(tk.END, 
                    f"    Value: '{error['value']}'\n")
        
        self.results_label.config(text=f"❌ Validation Complete - {total_errors} Errors Found")
        self.results_text.config(state=tk.DISABLED)
        
        # Update data display
        self.update_data_display()
        
    def update_data_display(self):
        """Update the data view tab"""
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        if self.df is None:
            return
            
        # Set up columns
        columns = list(self.df.columns)
        self.data_tree['columns'] = columns
        
        for col in columns:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=150, minwidth=100)
            
        # Add data rows
        for index, row in self.df.iterrows():
            values = [str(row[col]) if not pd.isna(row[col]) else '' for col in columns]
            
            # Check if row has errors
            row_errors = [e for e in self.validation_errors if e['row'] == index + 1]
            tags = ('error_row',) if row_errors else ('valid_row',)
            
            self.data_tree.insert('', 'end', values=values, tags=tags)
            
    def export_results(self):
        """Export validation results to Excel"""
        if self.df is None:
            messagebox.showinfo("Info", "No data to export")
            return
            
        try:
            output_path = filedialog.asksaveasfilename(
                title="Save validation results",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            
            if output_path:
                self.status_var.set("Exporting results...")
                self.root.update()
                
                # Export to Excel
                excel_handler.write_excel_with_validation_results(
                    self.df, self.validation_errors, output_path
                )
                
                self.status_var.set(f"Results exported to {os.path.basename(output_path)}")
                messagebox.showinfo("Success", f"Results exported successfully to:\n{output_path}")
                
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")
            self.status_var.set("Export failed")
            
    def clear_all(self):
        """Clear all results and data"""
        self.df = None
        self.validation_errors = []
        self.file_path_var.set("")
        self.sheets_url_var.set("")
        
        # Clear displays
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
            
        # Reset buttons
        self.export_button.config(state='disabled')
        self.results_label.config(text="No validation results yet")
        self.status_var.set("Ready to validate data")
        
    def create_sample_data(self):
        """Create sample data files"""
        try:
            # Import and run sample data creation
            from create_sample_data import main as create_sample_main
            create_sample_main()
            
            messagebox.showinfo("Success", 
                              "Sample data files created successfully!\n\n"
                              "Files created:\n"
                              "• sample_course_data.xlsx\n"
                              "• sample_course_data_extended.xlsx\n"
                              "• sample_course_data.csv\n\n"
                              "These files contain intentional errors for testing.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sample data: {str(e)}")
        
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    app = CourseDataValidatorApp()
    app.run()

if __name__ == "__main__":
    main()
