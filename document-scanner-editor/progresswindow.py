#!/usr/bin/env python3
"""
Progress Window for Real-time Validation Display
Shows validation progress with table format and error highlighting
"""

import tkinter as tk
from tkinter import ttk
import threading
from typing import Dict, List, Optional

class ProgressWindow:
    def __init__(self, parent, total_rows: int):
        """Initialize the progress window"""
        self.parent = parent
        self.total_rows = total_rows
        self.current_row = 0
        self.cancelled = False
        
        # Create the window
        self.window = tk.Toplevel(parent)
        self.window.title("Validation Progress")
        self.window.geometry("1200x800")
        self.window.configure(bg='#f0f0f0')
        
        # Make window modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.center_window()
        
        # Setup UI
        self.setup_ui()
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self.update_thread.start()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Validation Progress", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(1, weight=1)
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Initializing...")
        self.progress_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=self.total_rows, length=400)
        self.progress_bar.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Progress percentage
        self.percentage_label = ttk.Label(progress_frame, text="0%")
        self.percentage_label.grid(row=2, column=0, sticky=tk.W)
        
        # Cancel button
        self.cancel_button = ttk.Button(progress_frame, text="Cancel", command=self.cancel_validation)
        self.cancel_button.grid(row=2, column=1, sticky=tk.E)
        
        # Current row display
        current_frame = ttk.LabelFrame(main_frame, text="Current Row Data", padding="10")
        current_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        current_frame.columnconfigure(0, weight=1)
        current_frame.rowconfigure(0, weight=1)
        
        # Create treeview for current row data
        self.setup_data_treeview(current_frame)
        
        # Error summary
        error_frame = ttk.LabelFrame(main_frame, text="Error Summary", padding="10")
        error_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        error_frame.columnconfigure(1, weight=1)
        
        # Error counters
        self.total_errors_label = ttk.Label(error_frame, text="Total Errors: 0")
        self.total_errors_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        self.current_row_errors_label = ttk.Label(error_frame, text="Current Row Errors: 0")
        self.current_row_errors_label.grid(row=0, column=1, sticky=tk.W)
        
        # Error breakdown
        self.error_breakdown_label = ttk.Label(error_frame, text="Error Types: None")
        self.error_breakdown_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
    def setup_data_treeview(self, parent):
        """Setup the treeview for displaying current row data"""
        # Create frame for treeview and scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ('Field', 'Value', 'Status', 'Error Message')
        self.data_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        self.data_tree.heading('Field', text='Field')
        self.data_tree.heading('Value', text='Value')
        self.data_tree.heading('Status', text='Status')
        self.data_tree.heading('Error Message', text='Error Message')
        
        self.data_tree.column('Field', width=150, minwidth=100)
        self.data_tree.column('Value', width=200, minwidth=150)
        self.data_tree.column('Status', width=100, minwidth=80)
        self.data_tree.column('Error Message', width=300, minwidth=200)
        
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
        
    def update_progress(self, current_row: int, message: str):
        """Update progress display"""
        self.current_row = current_row
        self.progress_var.set(current_row)
        
        # Calculate percentage
        percentage = (current_row / self.total_rows) * 100
        
        # Update labels
        self.progress_label.config(text=message)
        self.percentage_label.config(text=f"{percentage:.1f}%")
        
    def update_data_display(self, row_data: Dict, row_errors: List[Dict]):
        """Update the data display with current row information"""
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Create error lookup for quick access
        error_lookup = {}
        for error in row_errors:
            error_lookup[error['column']] = error
        
        # Add row data to treeview
        for field, value in row_data.items():
            # Determine status and error message
            if field in error_lookup:
                status = "❌ Error"
                error_message = error_lookup[field]['message']
                tags = ('error',)
            else:
                status = "✅ Valid"
                error_message = ""
                tags = ('valid',)
            
            # Insert into treeview
            item = self.data_tree.insert('', 'end', values=(
                field,
                str(value) if value is not None else "",
                status,
                error_message
            ), tags=tags)
        
        # Update error summary
        self.update_error_summary(row_errors)
        
    def update_error_summary(self, row_errors: List[Dict]):
        """Update error summary display"""
        # Update total errors (this would need to be passed from main application)
        # For now, just show current row errors
        current_errors = len(row_errors)
        self.current_row_errors_label.config(text=f"Current Row Errors: {current_errors}")
        
        # Update error breakdown
        if row_errors:
            error_types = {}
            for error in row_errors:
                error_type = error['error_type']
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            breakdown_text = "Error Types: " + ", ".join([f"{t}: {c}" for t, c in error_types.items()])
            self.error_breakdown_label.config(text=breakdown_text)
        else:
            self.error_breakdown_label.config(text="Error Types: None")
        
    def cancel_validation(self):
        """Cancel the validation process"""
        self.cancelled = True
        self.cancel_button.config(state='disabled', text="Cancelling...")
        self.progress_label.config(text="Cancelling validation...")
        
    def update_loop(self):
        """Update loop for smooth progress updates"""
        while not self.cancelled and self.window.winfo_exists():
            try:
                # Update the window
                self.window.update()
                threading.Event().wait(0.1)  # Small delay
            except:
                break
                
    def close(self):
        """Close the progress window"""
        self.cancelled = True
        if self.window.winfo_exists():
            self.window.destroy()

class ValidationProgressWindow:
    """Alternative simpler progress window"""
    
    def __init__(self, parent, total_rows: int):
        self.parent = parent
        self.total_rows = total_rows
        self.cancelled = False
        
        # Create window
        self.window = tk.Toplevel(parent)
        self.window.title("Validation Progress")
        self.window.geometry("600x400")
        self.window.configure(bg='#f0f0f0')
        
        # Make modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center window
        self.center_window()
        
        # Setup UI
        self.setup_simple_ui()
        
    def center_window(self):
        """Center the window"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_simple_ui(self):
        """Setup simple UI"""
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Validating Course Data", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="15")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Progress label
        self.progress_label = ttk.Label(progress_frame, text="Initializing...")
        self.progress_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=self.total_rows, length=400)
        self.progress_bar.pack(pady=(0, 10))
        
        # Percentage
        self.percentage_label = ttk.Label(progress_frame, text="0%")
        self.percentage_label.pack()
        
        # Current row info
        info_frame = ttk.LabelFrame(main_frame, text="Current Row Information", padding="15")
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Current row text
        self.current_row_text = tk.Text(info_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.current_row_text.yview)
        self.current_row_text.configure(yscrollcommand=scrollbar.set)
        
        self.current_row_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_validation)
        self.cancel_button.pack(side=tk.RIGHT)
        
    def update_progress(self, current_row: int, message: str):
        """Update progress"""
        self.progress_var.set(current_row)
        percentage = (current_row / self.total_rows) * 100
        
        self.progress_label.config(text=message)
        self.percentage_label.config(text=f"{percentage:.1f}%")
        
    def update_data_display(self, row_data: Dict, row_errors: List[Dict]):
        """Update data display"""
        # Clear text
        self.current_row_text.delete(1.0, tk.END)
        
        # Add header
        self.current_row_text.insert(tk.END, "CURRENT ROW DATA:\n")
        self.current_row_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Add field data
        for field, value in row_data.items():
            status = "❌ ERROR" if any(e['column'] == field for e in row_errors) else "✅ VALID"
            self.current_row_text.insert(tk.END, f"{field}: {value}\n")
            self.current_row_text.insert(tk.END, f"Status: {status}\n")
            
            # Add error message if any
            for error in row_errors:
                if error['column'] == field:
                    self.current_row_text.insert(tk.END, f"Error: {error['message']}\n")
            
            self.current_row_text.insert(tk.END, "\n")
        
        # Add error summary
        if row_errors:
            self.current_row_text.insert(tk.END, "ERRORS FOUND:\n")
            self.current_row_text.insert(tk.END, "-" * 30 + "\n")
            for error in row_errors:
                self.current_row_text.insert(tk.END, 
                    f"• {error['column']}: {error['message']}\n")
        
    def cancel_validation(self):
        """Cancel validation"""
        self.cancelled = True
        self.cancel_button.config(state='disabled', text="Cancelling...")
        self.progress_label.config(text="Cancelling validation...")
        
    def close(self):
        """Close window"""
        self.cancelled = True
        if self.window.winfo_exists():
            self.window.destroy()
