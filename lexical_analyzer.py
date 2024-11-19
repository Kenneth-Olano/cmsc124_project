import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import syntax_analyzer

# set of LOLcode keywords
constructs = set([
    "HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R",
    "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
    "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT",
    "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE",
    "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL",
    "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY", "AN"
])

keyword_types = {
    "HAI":"Code Delimiter", "KTHXBYE": "Code Delimiter", "WAZZUP": "Variable Declaration"
}

# regex patterns for literals
literal_rules = [
    r"\s-?[0-9]+\s",           # integer literals
    r"\s-?[0-9]*\.?[0-9]+?\s", # floating-point literals
    r'\s\".*\"',               # string literals
    r"(WIN|FAIL)\s",           # boolean literals
    r"\s(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\s"  # type literals
]

# regex pattern for identifiers
identifier_rule = r"[a-zA-Z][a-zA-Z0-9_]*"
code_line = []
def get_file():
    # open file dialog to select a LOLcode file
    file_path = filedialog.askopenfilename(title="Open LOLcode file", filetypes=[("LOLcode files", "*.lol"), ("All files", "*.*")])
    if not file_path:
        return
    
    lexemes = {"keywords": [], "literals": [], "identifiers": []}
    all_tokens = []  # store the tokens in the order they appear
    
    try:
        with open(file_path, 'r') as lol_file:
            line_cnt = 1
            for line in lol_file:
                code_line.append(line)
                tokenize_line(line, lexemes, all_tokens, line_cnt)
                line_cnt+=1
        
        # display the lexemes in the GUI
        display_lexemes(lexemes, all_tokens)
        update_line_numbers()
        # print(lol_file)
        append_terminal_output(f"\"{os.path.basename(file_path)}\" successfully read!")
        syntax_analyzer.syntax_analyzer(all_tokens)
        return all_tokens
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file:\n{e}")

def tokenize_line(line, lexemes, all_tokens, line_cnt):
    # track positions of found keywords and literals to exclude them from identifier checks
    positions = {"keywords": [], "literals": [], "identifiers": []}
    error_flag = 0 #0 means error has occurred and 1 means error has not occurred yet
    # identify keywords (constructs) first
    # We create a regular expression pattern to match any keyword in the constructs set
    keywords = re.finditer(r"\b(?:{})\b".format("|".join(map(re.escape, constructs))), line)
    # print(keywords)
    # iterate over all the keyword matches found in the line
    for keyword in keywords:
        # add the matched keyword to the lexemes dictionary under 'keywords'
        lexemes["keywords"].append(keyword.group().strip())
        # add the keyword and its classification to the all_tokens list
        all_tokens.append((keyword.group().strip(), "Keyword"))
        # store the position of the keyword (start and end indices)
        positions["keywords"].append(keyword.span())
        # error_flag = 0

    #does the same for literals
    for rule in literal_rules: 
        literals = re.finditer(rule, line)
        for literal in literals:
            if not is_within_positions(literal.span(), positions["keywords"]):
                lexemes["literals"].append(literal.group().strip())
                all_tokens.append((literal.group().strip(), "Literal"))
                positions["literals"].append(literal.span())
                # if error_flag == :
                #     error_flag = 1

    #does the same for identifiers
    identifiers = re.finditer(identifier_rule, line)
    for identifier in identifiers:
        identifier_text = identifier.group().strip()
        if (identifier_text not in constructs and
            not is_within_positions(identifier.span(), positions["keywords"]) and
            not is_within_positions(identifier.span(), positions["literals"])):

            lexemes["identifiers"].append(identifier_text)
            all_tokens.append((identifier_text, "Identifier"))
            positions["identifiers"].append(identifier.span())
            # print(identifier_text)

    remaining_text = re.finditer(r"\S+", line)  # Find non-whitespace sequences in the line
    for text in remaining_text:
        if not (is_within_positions(text.span(), positions["keywords"]) or
                is_within_positions(text.span(), positions["literals"]) or
                is_within_positions(text.span(), positions["identifiers"])):
            # Add to lexemes as an error (for display purposes, if needed)
            lexemes.setdefault("errors", []).append(text.group().strip())
            # Add the error and classification to all_tokens
            all_tokens.append((text.group().strip(), "Error"))
            if len(lexemes["errors"]) > 0:
                print(lexemes["errors"])
                print(f"ERROR: Illegal character found in line {line_cnt}: {lexemes["errors"][0]}")
    
    


def is_within_positions(span, positions):
    for start, end in positions:
        if start <= span[0] < end or start < span[1] <= end:
            return True
    return False

def display_lexemes(lexemes, all_tokens):
    text_widget.delete("1.0", tk.END)
    for item in tree2.get_children():
        tree2.delete(item)

    # display lexemes in the text widget
    max_len = max(len(lexemes["keywords"]), len(lexemes["literals"]), len(lexemes["identifiers"]))
    for i in range(len(code_line)):

        line_text = f"{code_line[i].strip()}\n"
        text_widget.insert(tk.END, line_text)
    
    # insert tokens in order into the second Treeview (token - classification)
    for token, classification in all_tokens:
        tree2.insert("", "end", values=(token, classification))

# Function to update line numbers in the non-editable column
def update_line_numbers():
    line_count = int(text_widget.index("end-1c").split('.')[0])  # Get the total number of lines
    line_numbers_widget.configure(state="normal")
    line_numbers_widget.delete("1.0", tk.END)  # Clear the previous line numbers

    # Insert line numbers
    for i in range(line_count):
        line_numbers_widget.insert(f"{i + 1}.0", f"{i + 1}\n", "center")
    line_numbers_widget.configure(state="disabled")  # Make it non-editable
    

# Function to handle text modifications and update line numbers
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

# GUI setup
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
