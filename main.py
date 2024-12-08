import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lexical_analyzer import analyze_code  # Import the lexical analysis function
from syntax_analyzer import SyntaxAnalyzer
from semantic_analyzer import SemanticAnalyzer

class LOLcodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLcode Compiler")
        
        # Initialize code variable to store the current LOLcode
        self.code = ""

        # Top Half: File Explorer, Text Editor, Tokens List, Symbol Table
        self.create_top_half()

        # Middle: Execute/Run Button
        self.create_run_button()

        # Bottom Half: Console
        self.create_console()

    def create_top_half(self):
        # Frame for the top section
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Make columns equal in width and rows to fill the space
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)
        top_frame.grid_columnconfigure(3, weight=1)

        top_frame.grid_rowconfigure(0, weight=0)  # Row for file selector
        top_frame.grid_rowconfigure(1, weight=1)  # Row for text editor, tokens, symbol table

        # File Explorer
        self.file_label = tk.Label(top_frame, text="Select LOLcode File:", font=("Helvetica", 12))
        self.file_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.file_button = tk.Button(top_frame, text="Browse", command=self.get_file, font=("Helvetica", 12))
        self.file_button.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Text Editor (with border)
        self.text_editor_frame = tk.Frame(top_frame, borderwidth=2, relief="solid", bg="gray")
        self.text_editor_frame.grid(row=1, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
        self.text_editor = tk.Text(self.text_editor_frame, height=15, width=50, font=("Arial", 12))
        self.text_editor.pack(fill="both", expand=True)

        # List of Tokens (with border and two columns: Lexeme and Classification)
        self.tokens_frame = tk.Frame(top_frame, borderwidth=2, relief="solid", bg="gray")
        self.tokens_frame.grid(row=1, column=2, padx=0, pady=0, sticky="nsew")
        self.tokens_label = tk.Label(self.tokens_frame, text="List of Tokens:", font=("Helvetica", 12))
        self.tokens_label.pack(pady=5)

        self.tokens_treeview = ttk.Treeview(self.tokens_frame, columns=("Lexeme", "Classification"), show="headings")
        self.tokens_treeview.heading("Lexeme", text="Lexeme")
        self.tokens_treeview.heading("Classification", text="Classification")
        self.tokens_treeview.column("Lexeme", width=150)
        self.tokens_treeview.column("Classification", width=150)
        self.tokens_treeview.pack(fill="both", expand=True)

        # Symbol Table (with border, using Treeview)
        self.symbol_table_frame = tk.Frame(top_frame, borderwidth=2, relief="solid", bg="gray")
        self.symbol_table_frame.grid(row=1, column=3, padx=0, pady=0, sticky="nsew")
        self.symbol_table_label = tk.Label(self.symbol_table_frame, text="Symbol Table:", font=("Helvetica", 12))
        self.symbol_table_label.pack(pady=5)

        self.symbol_table_treeview = ttk.Treeview(self.symbol_table_frame, columns=("Variable Name", "Value"), show="headings")
        self.symbol_table_treeview.heading("Variable Name", text="Variable Name")
        self.symbol_table_treeview.heading("Value", text="Value")
        self.symbol_table_treeview.column("Variable Name", width=150)
        self.symbol_table_treeview.column("Value", width=150)
        self.symbol_table_treeview.pack(fill="both", expand=True)


    def create_run_button(self):
        # Frame for the run button
        run_frame = tk.Frame(self.root)
        run_frame.pack(fill="both", expand=True)

        self.run_button = tk.Button(run_frame, text="Execute/Run", command=self.run_code, font=("Helvetica", 12))
        self.run_button.pack(pady=20, fill="both")

    def create_console(self):
        # Frame for the console section
        console_frame = tk.Frame(self.root)
        console_frame.pack(fill="both", expand=True)

        self.console_text = tk.Text(console_frame, height=10, width=100, bg="black", fg="white", insertbackground="white", font=("Courier", 12))
        self.console_text.pack(padx=10, pady=10)
        self.console_text.config(state=tk.DISABLED)  # Make console text not editable

    def get_file(self):
        # Open file dialog to select a LOLcode file
        file_path = filedialog.askopenfilename(title="Open LOLcode file", filetypes=[("LOLcode files", "*.lol"), ("All files", "*.*")])
        if not file_path:
            return
        
        # Load file content into the text editor
        with open(file_path, 'r') as file:
            self.code = file.read()  # Store code in instance variable
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(tk.END, self.code)

    def run_code(self):
        # Get the code from the text editor
        code = self.text_editor.get(1.0, tk.END).strip()

        # Clear the tokens and symbol table
        self.tokens_treeview.delete(*self.tokens_treeview.get_children())
        self.symbol_table_treeview.delete(*self.symbol_table_treeview.get_children())
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)  # Clear previous output
        self.console_text.config(state=tk.DISABLED)

        try:
            # Lexical Analysis
            lexemes, all_tokens = analyze_code(code)

            # Display tokens in the treeview
            for token in all_tokens:
                print(f"Inserting token: {token['token']} with type: {token['type']}")  # Debugging line
                self.tokens_treeview.insert("", "end", values=(token['token'], token['type']))

            # Syntax and Semantic Analysis
            syntax_analyzer = SyntaxAnalyzer(all_tokens)
            func_dict = syntax_analyzer.parse_program()
            semantic_analyzer = SemanticAnalyzer(all_tokens, func_dict)
            semantic_analyzer.analyze()

            # Get symbol table from the semantic analyzer and display it
            symbol_table = semantic_analyzer.get_symbol_table()

            for var, info in symbol_table.items():
                self.symbol_table_treeview.insert("", "end", values=(var, info['value']))


            # Output to console
            self.console_text.config(state=tk.NORMAL)
            self.console_text.insert(tk.END, "Code executed successfully!\n")
            self.console_text.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running the code: {e}")


root = tk.Tk()
app = LOLcodeApp(root)
root.mainloop()