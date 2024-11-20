import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import syntax_analyzer


class Token:
    def __init__(self, token, token_type, line, start=None, end=None):
        self.token = token        # The token value (e.g., "HAI", "42", etc.)
        self.type = token_type    # The type of the token (e.g., "Keyword", "Literal", etc.)
        self.line = line          # The line number where the token was found
        self.start = start        # The starting position of the token in the line
        self.end = end            # The ending position of the token in the line

    def __repr__(self):
        return f"Token({self.token}, {self.type}, Line: {self.line}, Pos: {self.start}-{self.end})"


# Set of LOLcode keywords
constructs = set([
    "HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R",
    "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
    "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT",
    "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE",
    "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL",
    "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY", "AN"
])

program_delimiters = {"HAI", "KTHXBYE"}
control_flow = {"O RLY?", "YA RLY", "NO WAI", "WILE", "MEBBE", "IF U SAY SO", "GTFO"}
data_declaration = {"I HAS A", "ITZ", "MAEK"}
input_output = {"VISIBLE", "GIMMEH"}
logical_operators = {"BOTH SAEM", "DIFFRINT", "NOT", "ANY OF", "ALL OF", "BOTH OF", "EITHER OF"}
mathematical_operators = {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"}
functions_and_blocks = {"BTW", "OBTW", "TLDR", "WTF?", "OMG", "OMGWTF"}
other_keywords = {"WON OF", "IS NOW A", "FOUND YR", "IS", "R", "TIL", "UPPIN", "NERFIN", "YR", "IM OUTTA YR"}

# Regex patterns for literals
literal_rules = [
    r"\s-?[0-9]+\s",           # Integer literals
    r"\s-?[0-9]*\.?[0-9]+?\s", # Floating-point literals
    r'\s\".*\"',               # String literals
    r"(WIN|FAIL)\s",           # Boolean literals
    r"\s(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\s"  # Type literals
]

# Regex pattern for identifiers
identifier_rule = r"[a-zA-Z][a-zA-Z0-9_]*"
code_line = []


def on_text_change(event=None):
    update_line_numbers()
    line_numbers_widget.yview_moveto(text_widget.yview()[0])

def append_terminal_output(message):
    terminal_widget.configure(state="normal")
    terminal_widget.insert(tk.END, "> " + message + "\n")
    terminal_widget.configure(state="disabled")
    terminal_widget.see(tk.END)  # Auto-scroll to the end

def on_scroll(*args):
    text_widget.yview(*args)
    line_numbers_widget.yview(*args)

def on_text_scroll(*args):
    line_numbers_widget.yview_moveto(text_widget.yview()[0])

def update_line_numbers():
    line_count = int(text_widget.index("end-1c").split('.')[0])  # Get the total number of lines
    line_numbers_widget.configure(state="normal")
    line_numbers_widget.delete("1.0", tk.END)  # Clear the previous line numbers

    # Insert line numbers
    for i in range(line_count):
        line_numbers_widget.insert(f"{i + 1}.0", f"{i + 1}\n", "center")
    line_numbers_widget.configure(state="disabled")  # Make it non-editable

def get_file():
    # Open file dialog to select a LOLcode file
    file_path = filedialog.askopenfilename(title="Open LOLcode file", filetypes=[("LOLcode files", "*.lol"), ("All files", "*.*")])
    if not file_path:
        return
    
    lexemes = {"keywords": [], "literals": [], "identifiers": []}
    all_tokens = []  # Store the tokens in the order they appear
    
    try:
        with open(file_path, 'r') as lol_file:
            line_cnt = 1
            for line in lol_file:
                code_line.append(line)
                tokenize_line(line, lexemes, all_tokens, line_cnt)
                line_cnt += 1
        
        # Display the lexemes in the GUI
        all_tokens = sorted(sorted(all_tokens, key=lambda x: x['end']),  key=lambda y: y['line'])
        # print(all_tokens)
        display_lexemes(lexemes, all_tokens)
        update_line_numbers()
        append_terminal_output(f"\"{os.path.basename(file_path)}\" successfully read!")
        
        syntax_analyzer.syntax_analyzer(all_tokens)  # Pass tokens to the syntax analyzer
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file:\n{e}")

def tokenize_line(line, lexemes, all_tokens, line_cnt):
    # Track positions of found keywords and literals to exclude them from identifier checks
    positions = {"keywords": [], "literals": [], "identifiers": []}

    # Define patterns for detecting variable, function, and loop identifiers
    variable_keywords = ["I HAS A", "I HAS", "GIMMEH", "MAEK", "YR","VISIBLE"]
    function_keywords = ["HOW IZ I"]
    loop_keywords = ["IM IN YR", "IM OUTTA YR"]

    # Identify keywords
    keywords = re.finditer(r"\b(?:{})\b".format("|".join(map(re.escape, constructs)).replace("?", r"\?")), line)
    for keyword in keywords:
        lexeme = keyword.group().strip()

        # Classify the keyword into a specific category
        if lexeme in program_delimiters:
            token_type = "Program Delimiter"
        elif lexeme in control_flow:
            token_type = "Control Flow"
        elif lexeme in data_declaration:
            token_type = "Data Declaration"
        elif lexeme in input_output:
            token_type = "Input/Output"
        elif lexeme in logical_operators:
            token_type = "Logical Operator"
        elif lexeme in mathematical_operators:
            token_type = "Mathematical Operator"
        elif lexeme in functions_and_blocks:
            token_type = "Functions and Blocks"
        else:
            token_type = "Other Keyword"

        lexemes["keywords"].append(lexeme)
        all_tokens.append({
            "token": lexeme,
            "type": token_type,
            "line": line_cnt,
            "start": keyword.start(),
            "end": keyword.end()
        })
        positions["keywords"].append(keyword.span())

    # Identify literals
    for rule in literal_rules:
        literals = re.finditer(rule, line)
        for literal in literals:
            if not is_within_positions(literal.span(), positions["keywords"]):
                lexeme = literal.group().strip()
                lexemes["literals"].append(lexeme)
                all_tokens.append({
                    "token": lexeme,
                    "type": "Literal",
                    "line": line_cnt,
                    "start": literal.start(),
                    "end": literal.end()
                })
                positions["literals"].append(literal.span())

    # Identify identifiers
    identifiers = re.finditer(identifier_rule, line)
    for identifier in identifiers:
        identifier_text = identifier.group().strip()
        if (identifier_text not in constructs and
                not is_within_positions(identifier.span(), positions["keywords"]) and
                not is_within_positions(identifier.span(), positions["literals"])):

            # Heuristic-based classification of the identifier
            identifier_type = "Identifier"  # Default classification

            # Check if the identifier is part of a variable declaration (e.g., "I HAS A")
            for keyword in variable_keywords:
                if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
                    identifier_type = "Variable"
                    break

            # Check if the identifier is part of a function (e.g., "HOW IZ I")
            for keyword in function_keywords:
                if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
                    identifier_type = "Function"
                    break

            # Check if the identifier is part of a loop (e.g., "IM IN YR")
            for keyword in loop_keywords:
                if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
                    identifier_type = "Loop"
                    break

            lexemes["identifiers"].append(identifier_text)
            all_tokens.append({
                "token": identifier_text,
                "type": identifier_type,
                "line": line_cnt,
                "start": identifier.start(),
                "end": identifier.end()
            })
            positions["identifiers"].append(identifier.span())

    # Identify errors (unclassified tokens)
    remaining_text = re.finditer(r"\S+", line)
    for text in remaining_text:
        if not (is_within_positions(text.span(), positions["keywords"]) or
                is_within_positions(text.span(), positions["literals"]) or
                is_within_positions(text.span(), positions["identifiers"])):  # Unclassified token
            lexeme = text.group().strip()
            lexemes.setdefault("errors", []).append(lexeme)
            all_tokens.append({
                "token": lexeme,
                "type": "Error",
                "line": line_cnt,
                "start": text.start(),
                "end": text.end()
            })


def is_within_positions(span, positions):
    for start, end in positions:
        if start <= span[0] < end or start < span[1] <= end:
            return True
    return False

def display_lexemes(lexemes, all_tokens):
    text_widget.delete("1.0", tk.END)
    for item in tree2.get_children():
        tree2.delete(item)

    # Display code lines in the text widget
    for i in range(len(code_line)):
        line_text = f"{code_line[i].strip()}\n"
        text_widget.insert(tk.END, line_text)

    # Insert tokens into the Treeview (Token - Classification - Line)
    for token in all_tokens:
        tree2.insert("", "end", values=(token["token"], token["type"], token["line"]))

root = tk.Tk()
root.title("LOLcode Lexical Analyzer")
root.geometry("1500x700")

# add a frame to contain the tables and button
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(frame)
button_frame.grid(row=0, column=1, sticky="w")
# file load button
load_button = tk.Button(button_frame, text="Load LOLcode File", command=get_file, height=2, width=20, bg="lightblue")
load_button.grid(row=0, column=0, padx=10, pady=10)
# load_button.pack(side="left", padx=5)
execute_button = tk.Button(button_frame, text="Execute LOLcode File", command=None, height=2, width=30, bg="green", fg="white")
execute_button.grid(row=0, column=1, padx=10, pady=10)
# load_button.pack(side="left", padx=5)

# configure the columns to allow for a scrollbar between the tables
frame.grid_columnconfigure(1, weight=1, minsize=500)  # first table column
frame.grid_columnconfigure(0, weight=0, minsize=5)                # scrollbar column
frame.grid_columnconfigure(2, weight=1, minsize=500)  # second table column

# add a text widget for displaying lexemes
text_widget = tk.Text(frame, wrap="word", height=15, width=60)
text_widget.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# add a vertical scrollbar for the text widget
text_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
text_scrollbar.grid(row=1, column=2, sticky="ns", padx=10)
text_widget.configure(yscrollcommand=text_scrollbar.set)

# add the second Treeview (table) for displaying token - classification
columns2 = ("Token", "Classification")
tree2 = ttk.Treeview(frame, columns=columns2, show="headings", height=15)
tree2.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# set the column headings for the second table
for col in columns2:
    tree2.heading(col, text=col)
    tree2.column(col, width=100, anchor="center")

# add a scrollbar for the second treeview
scrollbar2 = ttk.Scrollbar(frame, orient="vertical", command=tree2.yview)
scrollbar2.grid(row=1, column=3, sticky="ns", padx=10)
tree2.configure(yscrollcommand=scrollbar2.set)

# Add two Text widgets: one for code and another for line numbers
line_numbers_widget = tk.Text(frame, width=5, height=15, state="disabled", bg="lightgray")
line_numbers_widget.grid(row=1, column=0, pady=10, sticky ="wns")
# add a vertical scrollbar for the text line widget
line_numbers_widget.configure(yscrollcommand=text_scrollbar.set)
line_numbers_widget.tag_configure("center", justify="center")
# textline_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=line_numbers_widget.yview)
text_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_scroll)
text_scrollbar.grid(row=1, column=1, sticky="nse", padx=10)

text_widget.configure(yscrollcommand=text_scrollbar.set)
line_numbers_widget.configure(yscrollcommand=text_scrollbar.set)
text_widget['yscrollcommand'] = on_text_scroll
# Bind the function to update line numbers on any text change
text_widget.bind("<KeyRelease>", on_text_change)  # On key release
text_widget.bind("<ButtonRelease-1>", on_text_change)  # On mouse click

terminal_widget = tk.Text(frame, wrap="word", height=10, bg="black", fg="white", insertbackground="white")
terminal_widget.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configure the terminal widget to be non-editable (optional)
terminal_widget.configure(state="disabled")

# Add a vertical scrollbar for the terminal
terminal_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=terminal_widget.yview)
terminal_scrollbar.grid(row=2, column=4, sticky="ns")
terminal_widget.configure(yscrollcommand=terminal_scrollbar.set)


root.mainloop()
