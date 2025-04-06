import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import os

class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Generator")
        self.root.geometry("900x700")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Code Generation Options
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Code Generation Options", padding=10)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Right panel - Code Preview and Output
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Generated Code", padding=10)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize UI components
        self.create_options_panel()
        self.create_output_panel()
        
        # Load templates
        self.templates = self.load_templates()
        
    def create_options_panel(self):
        # Code type selection
        ttk.Label(self.options_frame, text="Code Type:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.code_type = tk.StringVar()
        code_types = ['Function', 'Class', 'Script', 'GUI Application', 'Data Processing', 'Web Scraper']
        self.code_type_combobox = ttk.Combobox(self.options_frame, textvariable=self.code_type, values=code_types, state='readonly')
        self.code_type_combobox.grid(row=1, column=0, sticky=tk.EW, pady=(0, 10))
        self.code_type_combobox.current(0)
        self.code_type_combobox.bind('<<ComboboxSelected>>', self.update_options)
        
        # Options frame (will be populated dynamically)
        self.dynamic_options_frame = ttk.Frame(self.options_frame)
        self.dynamic_options_frame.grid(row=2, column=0, sticky=tk.EW)
        
        # Generate button
        self.generate_button = ttk.Button(self.options_frame, text="Generate Code", command=self.generate_code)
        self.generate_button.grid(row=3, column=0, pady=20)
        
        # Save button
        self.save_button = ttk.Button(self.options_frame, text="Save Code", command=self.save_code)
        self.save_button.grid(row=4, column=0, pady=5)
        
        # Template management
        ttk.Label(self.options_frame, text="Templates:", style='Header.TLabel').grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        self.template_name = tk.StringVar()
        ttk.Entry(self.options_frame, textvariable=self.template_name).grid(row=6, column=0, sticky=tk.EW, pady=(0, 5))
        
        self.save_template_button = ttk.Button(self.options_frame, text="Save as Template", command=self.save_template)
        self.save_template_button.grid(row=7, column=0, pady=5)
        
        self.load_template_button = ttk.Button(self.options_frame, text="Load Template", command=self.load_template)
        self.load_template_button.grid(row=8, column=0, pady=5)
        
    def create_output_panel(self):
        # Code display
        self.code_display = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, width=80, height=30, font=('Courier New', 10))
        self.code_display.pack(fill=tk.BOTH, expand=True)
        
        # Copy button
        self.copy_button = ttk.Button(self.output_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, pady=5)
        
        # Clear button
        self.clear_button = ttk.Button(self.output_frame, text="Clear", command=self.clear_code)
        self.clear_button.pack(side=tk.RIGHT, pady=5)
    
    def update_options(self, event=None):
        # Clear previous options
        for widget in self.dynamic_options_frame.winfo_children():
            widget.destroy()
        
        code_type = self.code_type.get()
        row = 0
        
        # Common options
        ttk.Label(self.dynamic_options_frame, text="Function/Class Name:").grid(row=row, column=0, sticky=tk.W)
        self.name_var = tk.StringVar(value="my_" + code_type.lower().replace(" ", "_"))
        ttk.Entry(self.dynamic_options_frame, textvariable=self.name_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Description:").grid(row=row, column=0, sticky=tk.W)
        self.desc_var = tk.StringVar(value=f"A {code_type.lower()}")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.desc_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        # Type-specific options
        if code_type == "Function":
            self.setup_function_options(row)
        elif code_type == "Class":
            self.setup_class_options(row)
        elif code_type == "Script":
            self.setup_script_options(row)
        elif code_type == "GUI Application":
            self.setup_gui_options(row)
        elif code_type == "Data Processing":
            self.setup_data_processing_options(row)
        elif code_type == "Web Scraper":
            self.setup_web_scraper_options(row)
    
    def setup_function_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="Parameters:").grid(row=row, column=0, sticky=tk.W)
        self.params_var = tk.StringVar(value="param1, param2='default'")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.params_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Return Value:").grid(row=row, column=0, sticky=tk.W)
        self.return_var = tk.StringVar(value="None")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.return_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Docstring:").grid(row=row, column=0, sticky=tk.W)
        self.docstring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.docstring_var).grid(row=row, column=1, sticky=tk.W)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Example:").grid(row=row, column=0, sticky=tk.W)
        self.example_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.example_var).grid(row=row, column=1, sticky=tk.W)
    
    def setup_class_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="Parent Class:").grid(row=row, column=0, sticky=tk.W)
        self.parent_var = tk.StringVar(value="object")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.parent_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Methods:").grid(row=row, column=0, sticky=tk.W)
        self.methods_var = tk.StringVar(value="__init__, do_something")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.methods_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Docstring:").grid(row=row, column=0, sticky=tk.W)
        self.docstring_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.docstring_var).grid(row=row, column=1, sticky=tk.W)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Example Usage:").grid(row=row, column=0, sticky=tk.W)
        self.example_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.example_var).grid(row=row, column=1, sticky=tk.W)
    
    def setup_script_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="Script Purpose:").grid(row=row, column=0, sticky=tk.W)
        self.purpose_var = tk.StringVar(value="Process data")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.purpose_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Input Type:").grid(row=row, column=0, sticky=tk.W)
        self.input_type_var = tk.StringVar(value="file")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.input_type_var, 
                     values=["file", "user input", "API", "database"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Output Type:").grid(row=row, column=0, sticky=tk.W)
        self.output_type_var = tk.StringVar(value="console")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.output_type_var, 
                     values=["console", "file", "database", "API"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Error Handling:").grid(row=row, column=0, sticky=tk.W)
        self.error_handling_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.error_handling_var).grid(row=row, column=1, sticky=tk.W)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Logging:").grid(row=row, column=0, sticky=tk.W)
        self.logging_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.logging_var).grid(row=row, column=1, sticky=tk.W)
    
    def setup_gui_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="GUI Framework:").grid(row=row, column=0, sticky=tk.W)
        self.gui_framework_var = tk.StringVar(value="Tkinter")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.gui_framework_var, 
                    values=["Tkinter", "PyQt", "Kivy", "PyGTK"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Main Widgets:").grid(row=row, column=0, sticky=tk.W)
        self.widgets_var = tk.StringVar(value="Label, Entry, Button")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.widgets_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Window Title:").grid(row=row, column=0, sticky=tk.W)
        self.window_title_var = tk.StringVar(value="My Application")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.window_title_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Main Loop:").grid(row=row, column=0, sticky=tk.W)
        self.main_loop_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.main_loop_var).grid(row=row, column=1, sticky=tk.W)
    
    def setup_data_processing_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="Data Source:").grid(row=row, column=0, sticky=tk.W)
        self.data_source_var = tk.StringVar(value="CSV file")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.data_source_var, 
                    values=["CSV file", "Excel file", "JSON file", "Database", "API"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Processing Steps:").grid(row=row, column=0, sticky=tk.W)
        self.processing_steps_var = tk.StringVar(value="clean, transform, analyze")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.processing_steps_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Output Format:").grid(row=row, column=0, sticky=tk.W)
        self.output_format_var = tk.StringVar(value="CSV")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.output_format_var, 
                    values=["CSV", "Excel", "JSON", "Database", "Plot"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Include Visualization:").grid(row=row, column=0, sticky=tk.W)
        self.visualization_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.dynamic_options_frame, variable=self.visualization_var).grid(row=row, column=1, sticky=tk.W)
    
    def setup_web_scraper_options(self, row):
        ttk.Label(self.dynamic_options_frame, text="Target Website:").grid(row=row, column=0, sticky=tk.W)
        self.website_var = tk.StringVar(value="example.com")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.website_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Data to Scrape:").grid(row=row, column=0, sticky=tk.W)
        self.scrape_data_var = tk.StringVar(value="titles, links")
        ttk.Entry(self.dynamic_options_frame, textvariable=self.scrape_data_var).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Library:").grid(row=row, column=0, sticky=tk.W)
        self.scraper_lib_var = tk.StringVar(value="BeautifulSoup")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.scraper_lib_var, 
                    values=["BeautifulSoup", "Scrapy", "Selenium", "Requests"]).grid(row=row, column=1, sticky=tk.EW)
        row += 1
        
        ttk.Label(self.dynamic_options_frame, text="Output Format:").grid(row=row, column=0, sticky=tk.W)
        self.scraper_output_var = tk.StringVar(value="CSV")
        ttk.Combobox(self.dynamic_options_frame, textvariable=self.scraper_output_var, 
                    values=["CSV", "JSON", "Database", "Console"]).grid(row=row, column=1, sticky=tk.EW)
    
    def generate_code(self):
        code_type = self.code_type.get()
        
        if code_type == "Function":
            code = self.generate_function()
        elif code_type == "Class":
            code = self.generate_class()
        elif code_type == "Script":
            code = self.generate_script()
        elif code_type == "GUI Application":
            code = self.generate_gui_app()
        elif code_type == "Data Processing":
            code = self.generate_data_processing()
        elif code_type == "Web Scraper":
            code = self.generate_web_scraper()
        else:
            code = "# Select a code type to generate"
        
        self.code_display.delete(1.0, tk.END)
        self.code_display.insert(tk.END, code)
    
    def generate_function(self):
        name = self.name_var.get()
        params = self.params_var.get()
        return_val = self.return_var.get()
        desc = self.desc_var.get()
        include_docstring = self.docstring_var.get()
        include_example = self.example_var.get()
        
        code = f"def {name}({params}):\n"
        
        if include_docstring:
            code += f'    """{desc}\n\n'
            code += f'    Args:\n'
            
            # Add parameter descriptions
            for param in params.split(','):
                param = param.strip().split('=')[0]
                if param:
                    code += f'        {param}: Description of {param}\n'
            
            code += f'\n    Returns:\n'
            code += f'        {return_val}: Description of return value\n'
            code += '    """\n\n'
        
        # Function body
        code += f'    # TODO: Implement function logic\n'
        code += f'    return {return_val}\n\n'
        
        if include_example:
            code += f'# Example usage:\n'
            example_params = ', '.join([p.strip().split('=')[0] for p in params.split(',') if p.strip()])
            code += f'result = {name}({example_params})\n'
            code += f'print(result)\n'
        
        return code
    
    def generate_class(self):
        name = self.name_var.get()
        parent = self.parent_var.get()
        methods = [m.strip() for m in self.methods_var.get().split(',')]
        desc = self.desc_var.get()
        include_docstring = self.docstring_var.get()
        include_example = self.example_var.get()
        
        code = f"class {name}({parent}):\n"
        
        if include_docstring:
            code += f'    """{desc}\n    """\n\n'
        
        # __init__ method
        if "__init__" in methods:
            code += f'    def __init__(self):\n'
            code += f'        """Initialize the {name} instance."""\n'
            code += f'        super().__init__()\n'
            code += f'        # TODO: Initialize attributes\n\n'
        
        # Other methods
        for method in methods:
            if method != "__init__":
                code += f'    def {method}(self):\n'
                code += f'        """TODO: Document this method."""\n'
                code += f'        # TODO: Implement method logic\n'
                code += f'        pass\n\n'
        
        if include_example:
            code += f'# Example usage:\n'
            code += f'obj = {name}()\n'
            if len(methods) > 1 and methods[1] != "__init__":
                code += f'obj.{methods[1]}()\n'
        
        return code
    
    def generate_script(self):
        name = self.name_var.get()
        purpose = self.purpose_var.get()
        input_type = self.input_type_var.get()
        output_type = self.output_type_var.get()
        include_error_handling = self.error_handling_var.get()
        include_logging = self.logging_var.get()
        
        code = f'#!/usr/bin/env python3\n'
        code += f'# {name}.py - {purpose}\n\n'
        code += f'import sys\n'
        
        if include_logging:
            code += f'import logging\n\n'
            code += f'# Configure logging\n'
            code += f'logging.basicConfig(\n'
            code += f'    level=logging.INFO,\n'
            code += f'    format="%(asctime)s - %(levelname)s - %(message)s"\n'
            code += f')\n'
            code += f'logger = logging.getLogger(__name__)\n\n'
        
        # Input handling
        code += f'def get_input():\n'
        code += f'    """Get input data based on configuration."""\n'
        
        if input_type == "file":
            code += f'    input_file = input("Enter input file path: ")\n'
            code += f'    try:\n'
            code += f'        with open(input_file, "r") as f:\n'
            code += f'            data = f.read()\n'
            code += f'        return data\n'
            code += f'    except FileNotFoundError:\n'
            code += f'        print(f"Error: File {{input_file}} not found")\n'
            code += f'        sys.exit(1)\n\n'
        elif input_type == "user input":
            code += f'    print("Enter your data (press Ctrl+D when finished):")\n'
            code += f'    data = sys.stdin.read()\n'
            code += f'    return data\n\n'
        elif input_type == "API":
            code += f'    import requests\n'
            code += f'    url = input("Enter API URL: ")\n'
            code += f'    try:\n'
            code += f'        response = requests.get(url)\n'
            code += f'        response.raise_for_status()\n'
            code += f'        return response.json()\n'
            code += f'    except requests.exceptions.RequestException as e:\n'
            code += f'        print(f"API Error: {{e}}")\n'
            code += f'        sys.exit(1)\n\n'
        elif input_type == "database":
            code += f'    import sqlite3\n'
            code += f'    db_file = input("Enter database file path: ")\n'
            code += f'    query = input("Enter SQL query: ")\n'
            code += f'    try:\n'
            code += f'        conn = sqlite3.connect(db_file)\n'
            code += f'        cursor = conn.cursor()\n'
            code += f'        cursor.execute(query)\n'
            code += f'        return cursor.fetchall()\n'
            code += f'    except sqlite3.Error as e:\n'
            code += f'        print(f"Database Error: {{e}}")\n'
            code += f'        sys.exit(1)\n'
            code += f'    finally:\n'
            code += f'        conn.close()\n\n'
        
        # Processing function
        code += f'def process_data(data):\n'
        code += f'    """Process the input data."""\n'
        code += f'    # TODO: Implement data processing logic\n'
        code += f'    processed_data = data  # Placeholder\n'
        code += f'    return processed_data\n\n'
        
        # Output handling
        code += f'def save_output(data):\n'
        code += f'    """Save output data based on configuration."""\n'
        
        if output_type == "console":
            code += f'    print("Processing complete. Result:")\n'
            code += f'    print(data)\n\n'
        elif output_type == "file":
            code += f'    output_file = input("Enter output file path: ")\n'
            code += f'    try:\n'
            code += f'        with open(output_file, "w") as f:\n'
            code += f'            f.write(str(data))\n'
            code += f'        print(f"Data saved to {{output_file}}")\n'
            code += f'    except IOError as e:\n'
            code += f'        print(f"Error saving file: {{e}}")\n'
            code += f'        sys.exit(1)\n\n'
        elif output_type == "database":
            code += f'    import sqlite3\n'
            code += f'    db_file = input("Enter database file path: ")\n'
            code += f'    table = input("Enter table name: ")\n'
            code += f'    try:\n'
            code += f'        conn = sqlite3.connect(db_file)\n'
            code += f'        cursor = conn.cursor()\n'
            code += f'        # TODO: Implement database insert logic\n'
            code += f'        conn.commit()\n'
            code += f'        print(f"Data saved to {{table}} table")\n'
            code += f'    except sqlite3.Error as e:\n'
            code += f'        print(f"Database Error: {{e}}")\n'
            code += f'        sys.exit(1)\n'
            code += f'    finally:\n'
            code += f'        conn.close()\n\n'
        elif output_type == "API":
            code += f'    import requests\n'
            code += f'    url = input("Enter API endpoint URL: ")\n'
            code += f'    try:\n'
            code += f'        response = requests.post(url, json=data)\n'
            code += f'        response.raise_for_status()\n'
            code += f'        print("Data successfully sent to API")\n'
            code += f'    except requests.exceptions.RequestException as e:\n'
            code += f'        print(f"API Error: {{e}}")\n'
            code += f'        sys.exit(1)\n\n'
        
        # Main function
        code += f'def main():\n'
        if include_logging:
            code += f'    logger.info("Starting script")\n'
        
        if include_error_handling:
            code += f'    try:\n'
            code += f'        data = get_input()\n'
            if include_logging:
                code += f'        logger.info("Data retrieved successfully")\n'
            
            code += f'        processed_data = process_data(data)\n'
            if include_logging:
                code += f'        logger.info("Data processed successfully")\n'
            
            code += f'        save_output(processed_data)\n'
            if include_logging:
                code += f'        logger.info("Output saved successfully")\n'
            
            code += f'    except Exception as e:\n'
            if include_logging:
                code += f'        logger.error(f"Error: {{e}}", exc_info=True)\n'
            code += f'        print(f"Error: {{e}}", file=sys.stderr)\n'
            code += f'        sys.exit(1)\n'
        else:
            code += f'    data = get_input()\n'
            code += f'    processed_data = process_data(data)\n'
            code += f'    save_output(processed_data)\n'
        
        code += f'\n\nif __name__ == "__main__":\n'
        code += f'    main()\n'
        
        return code
    
    def generate_gui_app(self):
        name = self.name_var.get()
        framework = self.gui_framework_var.get()
        widgets = [w.strip() for w in self.widgets_var.get().split(',')]
        window_title = self.window_title_var.get()
        include_main_loop = self.main_loop_var.get()
        
        code = f'# {name}.py - {window_title}\n\n'
        
        if framework == "Tkinter":
            code += f'import tkinter as tk\n'
            code += f'from tkinter import ttk\n\n'
            
            code += f'class {name}:\n'
            code += f'    def __init__(self, root):\n'
            code += f'        self.root = root\n'
            code += f'        self.root.title("{window_title}")\n'
            code += f'        self.setup_ui()\n\n'
            
            code += f'    def setup_ui(self):\n'
            code += f'        """Setup the user interface."""\n'
            
            for widget in widgets:
                widget_name = widget.lower().replace(" ", "_")
                if widget == "Label":
                    code += f'        self.{widget_name} = ttk.Label(self.root, text="{widget}:")\n'
                    code += f'        self.{widget_name}.grid(row={widgets.index(widget)}, column=0, padx=5, pady=5)\n'
                elif widget == "Entry":
                    code += f'        self.{widget_name} = ttk.Entry(self.root)\n'
                    code += f'        self.{widget_name}.grid(row={widgets.index(widget)}, column=1, padx=5, pady=5)\n'
                elif widget == "Button":
                    code += f'        self.{widget_name} = ttk.Button(self.root, text="{widget}", command=self.on_button_click)\n'
                    code += f'        self.{widget_name}.grid(row={widgets.index(widget)}, column=0, columnspan=2, pady=10)\n'
                elif widget == "Text":
                    code += f'        self.{widget_name} = tk.Text(self.root, height=10, width=40)\n'
                    code += f'        self.{widget_name}.grid(row={widgets.index(widget)}, column=0, columnspan=2, padx=5, pady=5)\n'
                elif widget == "Checkbutton":
                    code += f'        self.{widget_name}_var = tk.BooleanVar()\n'
                    code += f'        self.{widget_name} = ttk.Checkbutton(\n'
                    code += f'            self.root, text="Enable feature", variable=self.{widget_name}_var\n'
                    code += f'        )\n'
                    code += f'        self.{widget_name}.grid(row={widgets.index(widget)}, column=0, columnspan=2, sticky=tk.W, padx=5)\n'
            
            code += f'\n    def on_button_click(self):\n'
            code += f'        """Handle button click events."""\n'
            code += f'        print("Button clicked!")\n'
            code += f'        # TODO: Add button click logic\n\n'
            
            if include_main_loop:
                code += f'if __name__ == "__main__":\n'
                code += f'    root = tk.Tk()\n'
                code += f'    app = {name}(root)\n'
                code += f'    root.mainloop()\n'
        
        elif framework == "PyQt":
            code += f'from PyQt5.QtWidgets import (\n'
            code += f'    QApplication, QMainWindow, QWidget, QVBoxLayout,\n'
            
            qt_widgets = []
            for widget in widgets:
                if widget == "Label":
                    qt_widgets.append("QLabel")
                elif widget == "Entry":
                    qt_widgets.append("QLineEdit")
                elif widget == "Button":
                    qt_widgets.append("QPushButton")
                elif widget == "Text":
                    qt_widgets.append("QTextEdit")
                elif widget == "Checkbutton":
                    qt_widgets.append("QCheckBox")
            
            code += f'    {", ".join(qt_widgets)}\n'
            code += f')\n'
            code += f'from PyQt5.QtCore import Qt\n\n'
            
            code += f'class {name}(QMainWindow):\n'
            code += f'    def __init__(self):\n'
            code += f'        super().__init__()\n'
            code += f'        self.setWindowTitle("{window_title}")\n'
            code += f'        self.setup_ui()\n\n'
            
            code += f'    def setup_ui(self):\n'
            code += f'        """Setup the user interface."""\n'
            code += f'        central_widget = QWidget()\n'
            code += f'        self.setCentralWidget(central_widget)\n'
            code += f'        layout = QVBoxLayout()\n'
            code += f'        central_widget.setLayout(layout)\n\n'
            
            for widget in widgets:
                widget_name = widget.lower().replace(" ", "_")
                if widget == "Label":
                    code += f'        self.{widget_name} = QLabel("{widget}")\n'
                    code += f'        layout.addWidget(self.{widget_name})\n'
                elif widget == "Entry":
                    code += f'        self.{widget_name} = QLineEdit()\n'
                    code += f'        layout.addWidget(self.{widget_name})\n'
                elif widget == "Button":
                    code += f'        self.{widget_name} = QPushButton("{widget}")\n'
                    code += f'        self.{widget_name}.clicked.connect(self.on_button_click)\n'
                    code += f'        layout.addWidget(self.{widget_name})\n'
                elif widget == "Text":
                    code += f'        self.{widget_name} = QTextEdit()\n'
                    code += f'        layout.addWidget(self.{widget_name})\n'
                elif widget == "Checkbutton":
                    code += f'        self.{widget_name} = QCheckBox("Enable feature")\n'
                    code += f'        layout.addWidget(self.{widget_name})\n'
            
            code += f'\n    def on_button_click(self):\n'
            code += f'        """Handle button click events."""\n'
            code += f'        print("Button clicked!")\n'
            code += f'        # TODO: Add button click logic\n\n'
            
            if include_main_loop:
                code += f'if __name__ == "__main__":\n'
                code += f'    app = QApplication([])\n'
                code += f'    window = {name}()\n'
                code += f'    window.show()\n'
                code += f'    app.exec_()\n'
        
        return code
    
    def generate_data_processing(self):
        name = self.name_var.get()
        data_source = self.data_source_var.get()
        processing_steps = [s.strip() for s in self.processing_steps_var.get().split(',')]
        output_format = self.output_format_var.get()
        include_visualization = self.visualization_var.get()
        
        code = f'# {name}.py - Data Processing Script\n\n'
        code += f'import pandas as pd\n'
        
        if data_source == "CSV file":
            code += f'def load_csv_data(file_path):\n'
            code += f'    """Load data from a CSV file."""\n'
            code += f'    return pd.read_csv(file_path)\n\n'
        elif data_source == "Excel file":
            code += f'def load_excel_data(file_path, sheet_name=0):\n'
            code += f'    """Load data from an Excel file."""\n'
            code += f'    return pd.read_excel(file_path, sheet_name=sheet_name)\n\n'
        elif data_source == "JSON file":
            code += f'def load_json_data(file_path):\n'
            code += f'    """Load data from a JSON file."""\n'
            code += f'    return pd.read_json(file_path)\n\n'
        elif data_source == "Database":
            code += f'import sqlite3\n'
            code += f'def load_db_data(db_file, query):\n'
            code += f'    """Load data from a database."""\n'
            code += f'    conn = sqlite3.connect(db_file)\n'
            code += f'    data = pd.read_sql(query, conn)\n'
            code += f'    conn.close()\n'
            code += f'    return data\n\n'
        elif data_source == "API":
            code += f'import requests\n'
            code += f'def load_api_data(url):\n'
            code += f'    """Load data from an API."""\n'
            code += f'    response = requests.get(url)\n'
            code += f'    response.raise_for_status()\n'
            code += f'    return pd.DataFrame(response.json())\n\n'
        
        # Processing functions
        for step in processing_steps:
            step_name = step.lower().replace(" ", "_")
            code += f'def {step_name}_data(data):\n'
            code += f'    """{step.capitalize()} the data."""\n'
            
            if step == "clean":
                code += f'    # Handle missing values\n'
                code += f'    data = data.dropna()\n'
                code += f'    # Remove duplicates\n'
                code += f'    data = data.drop_duplicates()\n'
                code += f'    return data\n\n'
            elif step == "transform":
                code += f'    # Example transformation: normalize numeric columns\n'
                code += f'    numeric_cols = data.select_dtypes(include=["number"]).columns\n'
                code += f'    data[numeric_cols] = (data[numeric_cols] - data[numeric_cols].mean()) / data[numeric_cols].std()\n'
                code += f'    return data\n\n'
            elif step == "analyze":
                code += f'    # Perform analysis\n'
                code += f'    analysis = data.describe()\n'
                code += f'    # Add custom analysis as needed\n'
                code += f'    return analysis\n\n'
            else:
                code += f'    # TODO: Implement {step} logic\n'
                code += f'    return data\n\n'
        
        # Output functions
        code += f'def save_output(data, output_file):\n'
        code += f'    """Save processed data in the specified format."""\n'
        
        if output_format == "CSV":
            code += f'    data.to_csv(output_file, index=False)\n'
            code += f'    print(f"Data saved to {{output_file}} as CSV")\n\n'
        elif output_format == "Excel":
            code += f'    data.to_excel(output_file, index=False)\n'
            code += f'    print(f"Data saved to {{output_file}} as Excel")\n\n'
        elif output_format == "JSON":
            code += f'    data.to_json(output_file, orient="records")\n'
            code += f'    print(f"Data saved to {{output_file}} as JSON")\n\n'
        elif output_format == "Database":
            code += f'    import sqlite3\n'
            code += f'    table_name = input("Enter table name: ")\n'
            code += f'    conn = sqlite3.connect(output_file)\n'
            code += f'    data.to_sql(table_name, conn, if_exists="replace", index=False)\n'
            code += f'    conn.close()\n'
            code += f'    print(f"Data saved to {{table_name}} table in {{output_file}}")\n\n'
        elif output_format == "Plot":
            code += f'    import matplotlib.pyplot as plt\n'
            code += f'    # Example plot\n'
            code += f'    if len(data.select_dtypes(include=["number"]).columns) > 0:\n'
            code += f'        data.plot(kind="hist", alpha=0.5)\n'
            code += f'        plt.savefig(output_file)\n'
            code += f'        print(f"Plot saved to {{output_file}}")\n'
            code += f'    else:\n'
            code += f'        print("No numeric columns to plot")\n\n'
        
        # Visualization if requested
        if include_visualization:
            code += f'def visualize_data(data):\n'
            code += f'    """Generate visualizations of the data."""\n'
            code += f'    import matplotlib.pyplot as plt\n'
            code += f'    \n'
            code += f'    # Example visualizations\n'
            code += f'    numeric_cols = data.select_dtypes(include=["number"]).columns\n'
            code += f'    \n'
            code += f'    if len(numeric_cols) > 0:\n'
            code += f'        # Histograms for numeric columns\n'
            code += f'        data[numeric_cols].hist(bins=20, figsize=(10, 8))\n'
            code += f'        plt.tight_layout()\n'
            code += f'        plt.show()\n'
            code += f'        \n'
            code += f'        # Correlation heatmap if multiple numeric columns\n'
            code += f'        if len(numeric_cols) > 1:\n'
            code += f'            import seaborn as sns\n'
            code += f'            plt.figure(figsize=(8, 6))\n'
            code += f'            sns.heatmap(data[numeric_cols].corr(), annot=True, cmap="coolwarm")\n'
            code += f'            plt.title("Correlation Heatmap")\n'
            code += f'            plt.show()\n'
            code += f'    else:\n'
            code += f'        print("No numeric columns for visualization")\n\n'
        
        # Main function
        code += f'def main():\n'
        code += f'    # Load data\n'
        
        if data_source == "CSV file":
            code += f'    input_file = input("Enter CSV file path: ")\n'
            code += f'    data = load_csv_data(input_file)\n'
        elif data_source == "Excel file":
            code += f'    input_file = input("Enter Excel file path: ")\n'
            code += f'    data = load_excel_data(input_file)\n'
        elif data_source == "JSON file":
            code += f'    input_file = input("Enter JSON file path: ")\n'
            code += f'    data = load_json_data(input_file)\n'
        elif data_source == "Database":
            code += f'    db_file = input("Enter database file path: ")\n'
            code += f'    query = input("Enter SQL query: ")\n'
            code += f'    data = load_db_data(db_file, query)\n'
        elif data_source == "API":
            code += f'    url = input("Enter API URL: ")\n'
            code += f'    data = load_api_data(url)\n'
        
        code += f'    print("\\nOriginal Data:")\n'
        code += f'    print(data.head())\n\n'
        
        # Processing steps
        for step in processing_steps:
            step_name = step.lower().replace(" ", "_")
            code += f'    # {step.capitalize()} data\n'
            code += f'    data = {step_name}_data(data)\n'
            code += f'    print("\\nAfter {step}:")\n'
            code += f'    print(data.head())\n\n'
        
        # Visualization if requested
        if include_visualization:
            code += f'    # Visualize data\n'
            code += f'    visualize_data(data)\n\n'
        
        # Save output
        code += f'    # Save processed data\n'
        code += f'    output_file = input("Enter output file path (without extension): ")\n'
        
        if output_format == "CSV":
            code += f'    save_output(data, output_file + ".csv")\n'
        elif output_format == "Excel":
            code += f'    save_output(data, output_file + ".xlsx")\n'
        elif output_format == "JSON":
            code += f'    save_output(data, output_file + ".json")\n'
        elif output_format == "Database":
            code += f'    save_output(data, output_file + ".db")\n'
        elif output_format == "Plot":
            code += f'    save_output(data, output_file + ".png")\n'
        
        code += f'\n\nif __name__ == "__main__":\n'
        code += f'    main()\n'
        
        return code
    
    def generate_web_scraper(self):
        name = self.name_var.get()
        website = self.website_var.get()
        scrape_data = [s.strip() for s in self.scrape_data_var.get().split(',')]
        library = self.scraper_lib_var.get()
        output_format = self.scraper_output_var.get()
        
        code = f'# {name}.py - Web Scraper for {website}\n\n'
        
        if library == "BeautifulSoup":
            code += f'import requests\n'
            code += f'from bs4 import BeautifulSoup\n'
        elif library == "Scrapy":
            code += f'import scrapy\n'
        elif library == "Selenium":
            code += f'from selenium import webdriver\n'
            code += f'from selenium.webdriver.common.by import By\n'
            code += f'from selenium.webdriver.support.ui import WebDriverWait\n'
            code += f'from selenium.webdriver.support import expected_conditions as EC\n'
        elif library == "Requests":
            code += f'import requests\n'
        
        code += f'import pandas as pd\n\n'
        
        # Scraper function
        if library == "BeautifulSoup":
            code += f'def scrape_{name.lower()}():\n'
            code += f'    """Scrape data from {website} using BeautifulSoup."""\n'
            code += f'    url = "https://{website}"\n'
            code += f'    try:\n'
            code += f'        response = requests.get(url)\n'
            code += f'        response.raise_for_status()\n'
            code += f'        soup = BeautifulSoup(response.text, "html.parser")\n'
            code += f'        \n'
            code += f'        # Initialize data storage\n'
            code += f'        data = {{}}\n'
            
            for item in scrape_data:
                item_name = item.lower().replace(" ", "_")
                code += f'        data["{item}"] = []\n'
            
            code += f'        \n'
            code += f'        # TODO: Implement scraping logic\n'
            code += f'        # Example for scraping titles:\n'
            code += f'        # for element in soup.select("h2.title"):\n'
            code += f'        #     data["titles"].append(element.text.strip())\n'
            code += f'        \n'
            code += f'        return pd.DataFrame(data)\n'
            code += f'    except requests.exceptions.RequestException as e:\n'
            code += f'        print(f"Error scraping website: {{e}}")\n'
            code += f'        return pd.DataFrame()\n\n'
        
        elif library == "Selenium":
            code += f'def scrape_{name.lower()}():\n'
            code += f'    """Scrape data from {website} using Selenium."""\n'
            code += f'    url = "https://{website}"\n'
            code += f'    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed\n'
            code += f'    try:\n'
            code += f'        driver.get(url)\n'
            code += f'        \n'
            code += f'        # Wait for page to load\n'
            code += f'        WebDriverWait(driver, 10).until(\n'
            code += f'            EC.presence_of_element_located((By.TAG_NAME, "body"))\n'
            code += f'        )\n'
            code += f'        \n'
            code += f'        # Initialize data storage\n'
            code += f'        data = {{}}\n'
            
            for item in scrape_data:
                item_name = item.lower().replace(" ", "_")
                code += f'        data["{item}"] = []\n'
            
            code += f'        \n'
            code += f'        # TODO: Implement scraping logic\n'
            code += f'        # Example for scraping titles:\n'
            code += f'        # for element in driver.find_elements(By.CSS_SELECTOR, "h2.title"):\n'
            code += f'        #     data["titles"].append(element.text)\n'
            code += f'        \n'
            code += f'        return pd.DataFrame(data)\n'
            code += f'    except Exception as e:\n'
            code += f'        print(f"Error scraping website: {{e}}")\n'
            code += f'        return pd.DataFrame()\n'
            code += f'    finally:\n'
            code += f'        driver.quit()\n\n'
        
        # Save function
        code += f'def save_data(data, output_file):\n'
        code += f'    """Save scraped data in the specified format."""\n'
        
        if output_format == "CSV":
            code += f'    data.to_csv(output_file, index=False)\n'
            code += f'    print(f"Data saved to {{output_file}} as CSV")\n\n'
        elif output_format == "JSON":
            code += f'    data.to_json(output_file, orient="records")\n'
            code += f'    print(f"Data saved to {{output_file}} as JSON")\n\n'
        elif output_format == "Database":
            code += f'    import sqlite3\n'
            code += f'    table_name = input("Enter table name: ")\n'
            code += f'    conn = sqlite3.connect(output_file)\n'
            code += f'    data.to_sql(table_name, conn, if_exists="replace", index=False)\n'
            code += f'    conn.close()\n'
            code += f'    print(f"Data saved to {{table_name}} table in {{output_file}}")\n\n'
        elif output_format == "Console":
            code += f'    print("Scraped Data:")\n'
            code += f'    print(data)\n\n'
        
        # Main function
        code += f'def main():\n'
        code += f'    print(f"Scraping data from {website}...")\n'
        code += f'    data = scrape_{name.lower()}()\n'
        code += f'    \n'
        code += f'    if not data.empty:\n'
        code += f'        print("\\nSample of scraped data:")\n'
        code += f'        print(data.head())\n'
        code += f'        \n'
        code += f'        # Save data\n'
        
        if output_format == "CSV":
            code += f'        output_file = input("Enter output CSV file path: ")\n'
            code += f'        save_data(data, output_file)\n'
        elif output_format == "JSON":
            code += f'        output_file = input("Enter output JSON file path: ")\n'
            code += f'        save_data(data, output_file)\n'
        elif output_format == "Database":
            code += f'        output_file = input("Enter output database file path: ")\n'
            code += f'        save_data(data, output_file)\n'
        elif output_format == "Console":
            code += f'        save_data(data, None)\n'
        
        code += f'    else:\n'
        code += f'        print("No data was scraped")\n'
        code += f'\n\nif __name__ == "__main__":\n'
        code += f'    main()\n'
        
        return code
    
    def copy_to_clipboard(self):
        code = self.code_display.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("Copied", "Code copied to clipboard!")
    
    def clear_code(self):
        self.code_display.delete(1.0, tk.END)
    
    def save_code(self):
        code = self.code_display.get(1.0, tk.END)
        if not code.strip():
            messagebox.showwarning("Empty", "No code to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
            title="Save Python File"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(code)
                messagebox.showinfo("Saved", f"File saved successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")
    
    def load_templates(self):
        """Load templates from file or return empty dict if file doesn't exist."""
        template_file = "code_templates.json"
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}
    
    def save_templates(self):
        """Save templates to file."""
        template_file = "code_templates.json"
        try:
            with open(template_file, 'w') as f:
                json.dump(self.templates, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save templates:\n{e}")
            return False
    
    def save_template(self):
        template_name = self.template_name.get().strip()
        if not template_name:
            messagebox.showwarning("Missing Name", "Please enter a template name!")
            return
        
        # Get current settings
        template_data = {
            "code_type": self.code_type.get(),
            "name": self.name_var.get(),
            "description": self.desc_var.get()
        }
        
        # Add type-specific settings
        code_type = self.code_type.get()
        if code_type == "Function":
            template_data.update({
                "params": self.params_var.get(),
                "return_value": self.return_var.get(),
                "docstring": self.docstring_var.get(),
                "example": self.example_var.get()
            })
        elif code_type == "Class":
            template_data.update({
                "parent": self.parent_var.get(),
                "methods": self.methods_var.get(),
                "docstring": self.docstring_var.get(),
                "example": self.example_var.get()
            })
        elif code_type == "Script":
            template_data.update({
                "purpose": self.purpose_var.get(),
                "input_type": self.input_type_var.get(),
                "output_type": self.output_type_var.get(),
                "error_handling": self.error_handling_var.get(),
                "logging": self.logging_var.get()
            })
        elif code_type == "GUI Application":
            template_data.update({
                "framework": self.gui_framework_var.get(),
                "widgets": self.widgets_var.get(),
                "window_title": self.window_title_var.get(),
                "main_loop": self.main_loop_var.get()
            })
        elif code_type == "Data Processing":
            template_data.update({
                "data_source": self.data_source_var.get(),
                "processing_steps": self.processing_steps_var.get(),
                "output_format": self.output_format_var.get(),
                "visualization": self.visualization_var.get()
            })
        elif code_type == "Web Scraper":
            template_data.update({
                "website": self.website_var.get(),
                "scrape_data": self.scrape_data_var.get(),
                "library": self.scraper_lib_var.get(),
                "output_format": self.scraper_output_var.get()
            })
        
        self.templates[template_name] = template_data
        
        if self.save_templates():
            messagebox.showinfo("Saved", f"Template '{template_name}' saved successfully!")
    
    def load_template(self):
        if not self.templates:
            messagebox.showinfo("No Templates", "No templates available to load.")
            return
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Load Template")
        popup.geometry("400x300")
        
        # Template list
        ttk.Label(popup, text="Select Template:").pack(pady=5)
        
        template_list = tk.Listbox(popup)
        for template in sorted(self.templates.keys()):
            template_list.insert(tk.END, template)
        template_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Load button
        def on_load():
            selection = template_list.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a template to load!")
                return
            
            template_name = template_list.get(selection[0])
            template_data = self.templates[template_name]
            
            # Set basic fields
            self.code_type.set(template_data["code_type"])
            self.name_var.set(template_data["name"])
            self.desc_var.set(template_data["description"])
            
            # Update UI to show current code type options
            self.update_options()
            
            # Set type-specific fields
            code_type = template_data["code_type"]
            if code_type == "Function":
                self.params_var.set(template_data["params"])
                self.return_var.set(template_data["return_value"])
                self.docstring_var.set(template_data["docstring"])
                self.example_var.set(template_data["example"])
            elif code_type == "Class":
                self.parent_var.set(template_data["parent"])
                self.methods_var.set(template_data["methods"])
                self.docstring_var.set(template_data["docstring"])
                self.example_var.set(template_data["example"])
            elif code_type == "Script":
                self.purpose_var.set(template_data["purpose"])
                self.input_type_var.set(template_data["input_type"])
                self.output_type_var.set(template_data["output_type"])
                self.error_handling_var.set(template_data["error_handling"])
                self.logging_var.set(template_data["logging"])
            elif code_type == "GUI Application":
                self.gui_framework_var.set(template_data["framework"])
                self.widgets_var.set(template_data["widgets"])
                self.window_title_var.set(template_data["window_title"])
                self.main_loop_var.set(template_data["main_loop"])
            elif code_type == "Data Processing":
                self.data_source_var.set(template_data["data_source"])
                self.processing_steps_var.set(template_data["processing_steps"])
                self.output_format_var.set(template_data["output_format"])
                self.visualization_var.set(template_data["visualization"])
            elif code_type == "Web Scraper":
                self.website_var.set(template_data["website"])
                self.scrape_data_var.set(template_data["scrape_data"])
                self.scraper_lib_var.set(template_data["library"])
                self.scraper_output_var.set(template_data["output_format"])
            
            popup.destroy()
            messagebox.showinfo("Loaded", f"Template '{template_name}' loaded successfully!")
        
        ttk.Button(popup, text="Load Selected Template", command=on_load).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()