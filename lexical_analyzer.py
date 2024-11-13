import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

def get_file():
    # open file dialog to select a LOLcode file
    file_path = filedialog.askopenfilename(title="Open LOLcode file", filetypes=[("LOLcode files", "*.lolcode"), ("All files", "*.*")])
    if not file_path:
        return
    
    lexemes = {"keywords": [], "literals": [], "identifiers": []}
    all_tokens = []  # store the tokens in the order they appear
    
    try:
        with open(file_path, 'r') as lol_file:
            line_cnt = 0
            for line in lol_file:
                tokenize_line(line, lexemes, all_tokens, line_cnt)
                line_cnt+=1
        
        # display the lexemes in the GUI
        display_lexemes(lexemes, all_tokens)
    
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
                print(f"ERROR: Illegal character found in line {line_cnt}: {lexemes["errors"][0]}")


def is_within_positions(span, positions):
    for start, end in positions:
        if start <= span[0] < end or start < span[1] <= end:
            return True
    return False

def display_lexemes(lexemes, all_tokens):
    # clear the treeviews before displaying new data
    for item in tree1.get_children():
        tree1.delete(item)
    for item in tree2.get_children():
        tree2.delete(item)
    
    # insert the lexemes into the first treeview (keywords, literals, identifiers)
    max_len = max(len(lexemes["keywords"]), len(lexemes["literals"]), len(lexemes["identifiers"]))
    for i in range(max_len):
        keyword = lexemes["keywords"][i] if i < len(lexemes["keywords"]) else ""
        literal = lexemes["literals"][i] if i < len(lexemes["literals"]) else ""
        identifier = lexemes["identifiers"][i] if i < len(lexemes["identifiers"]) else ""
        
        # insert into the first table with the three columns (keywords, literals, identifiers)
        tree1.insert("", "end", values=(keyword, literal, identifier))
    
    # insert tokens in order into the second treeview (token - classification)
    for token, classification in all_tokens:
        tree2.insert("", "end", values=(token, classification))

# GUI setup
root = tk.Tk()
root.title("LOLcode Lexical Analyzer")
root.geometry("1500x700")

# add a frame to contain the tables and button
frame = tk.Frame(root)
frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# file load button
load_button = tk.Button(frame, text="Load LOLcode File", command=get_file, height=2, width=20, bg="lightblue")
load_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# configure the columns to allow for a scrollbar between the tables
frame.grid_columnconfigure(0, weight=1, minsize=500)  # first table column
frame.grid_columnconfigure(1, weight=0)                # scrollbar column
frame.grid_columnconfigure(2, weight=1, minsize=500)  # second table column

# add the first Treeview (table) for displaying lexemes
columns1 = ("Keywords", "Literals", "Identifiers")
tree1 = ttk.Treeview(frame, columns=columns1, show="headings", height=15)
tree1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# set the column headings for the first table
for col in columns1:
    tree1.heading(col, text=col)
    tree1.column(col, width=200, anchor="center")

# add the second Treeview (table) for displaying token - classification
columns2 = ("Token", "Classification")
tree2 = ttk.Treeview(frame, columns=columns2, show="headings", height=15)
tree2.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# set the column headings for the second table
for col in columns2:
    tree2.heading(col, text=col)
    tree2.column(col, width=300, anchor="center")

# add a scrollbar between the two treeviews
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree1.yview)
scrollbar.grid(row=1, column=1, sticky="ns", padx=10)
tree1.configure(yscrollcommand=scrollbar.set)

# add a scrollbar for the second treeview
scrollbar2 = ttk.Scrollbar(frame, orient="vertical", command=tree2.yview)
scrollbar2.grid(row=1, column=3, sticky="ns", padx=10)
tree2.configure(yscrollcommand=scrollbar2.set)

root.mainloop()
