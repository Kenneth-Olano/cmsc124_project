import re

class Token:
    def __init__(self, token, token_type, line, start=None, end=None):
        self.token = token        # The token value (e.g., "HAI", "42", etc.)
        self.type = token_type    # The type of the token (e.g., "Keyword", "Literal", etc.)
        self.line = line          # The line number where the token was found
        self.start = start        # The starting position of the token in the line
        self.end = end            # The ending position of the token in the line

    def __hash__(self):
        return hash((self.token))

    def __eq__(self, value):
        if isinstance(value, Token):
            return self.token
        return None
    
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
control_flow = {"O RLY?", "YA RLY", "NO WAI", "MEBBE", "OIC"}
data_initialization = {"WAZZUP", "BUHBYE"}
data_declaration = {"I HAS A", "ITZ"}
input_output = {"VISIBLE", "GIMMEH"}
connector = {"AN", "YR"}
loop_type = {"TIL", "WILE"}
logical_operators = {"BOTH SAEM", "DIFFRINT", "NOT", "ANY OF", "ALL OF", "BOTH OF", "EITHER OF"}
mathematical_operators = {"SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF"}
switch = {"WTF?", "OMG", "OMGWTF"}
return_statements = {"FOUND YR", "GTFO"}
function_call = {"I IZ", "MKAY"}
assignment = {"R"}
loop_op = {"UPPIN", "NERFIN"}
typecast = {"IS NOW A", "MAEK"}
other_keywords = {"WON OF","IS"}
function_keywords = {"HOW IZ I", "IF U SAY SO"}
loop_keywords = {"IM IN YR", "IM OUTTA YR"}
concatenate = {"SMOOSH", "+"}
comments = {"BTW", "OBTW", "TLDR"}

# Regex patterns for literals
literal_rules = [
    r'"([^"]*)"',               # String literals
    r"\s-?[0-9]*\.[0-9]+", # Floating-point literals
    r"\s-?[0-9]+",           # Integer literals
    r"(WIN|FAIL)\s",           # Boolean literals
    r"(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\s"  # Type literals
]

# Regex pattern for identifiers
identifier_rule = r"[a-zA-Z][a-zA-Z0-9_]*"
code_line = []


import re

def tokenize_line(line, lexemes, all_tokens, line_cnt):
    # Track positions of all found tokens to avoid overlap
    positions = []

    literaltype_arr = ["YARN", "NUMBAR", "NUMBR", "TROOF"]

    # Handle inline comments
    btw_match = re.search(r"\bBTW\b", line)
    if btw_match:
        comment_text = line[btw_match.start():].strip()
        lexemes["comments"].append(comment_text)
        all_tokens.append({
            "token": comment_text,
            "type": "Comment",
            "line": line_cnt,
            "start": btw_match.start(),
            "end": len(line)
        })
        # Exclude the comment from further tokenization
        positions.append((btw_match.start(), len(line)))

    # Identify keywords
    keywords = re.finditer(r"\b(?:{})\b".format("|".join(map(re.escape, constructs)).replace("?", r"\?")), line)
    for keyword in keywords:
        start, end = keyword.span()
        if not is_within_positions((start, end), positions):
            lexeme = keyword.group().strip()
            if lexeme == "O RLY":
                lexeme = "O RLY?"
            elif lexeme == "WTF":
                lexeme = "WTF?"

            # Classify the keyword
            token_type = classify_keyword(lexeme)
            lexemes["keywords"].append(lexeme)
            all_tokens.append({
                "token": lexeme,
                "type": token_type,
                "line": line_cnt,
                "start": start,
                "end": end
            })
            positions.append((start, end))

    # Identify literals
    for idx, rule in enumerate(literal_rules):
        literals = re.finditer(rule, line)
        for literal in literals:
            start, end = literal.span()
            if not is_within_positions((start, end), positions):
                lexeme = literal.group().strip()
                lexemes["literals"].append(lexeme)
                all_tokens.append({
                    "token": lexeme,
                    "type": literaltype_arr[idx],
                    "line": line_cnt,
                    "start": start,
                    "end": end
                })
                positions.append((start, end))

    # Identify identifiers
    identifiers = re.finditer(identifier_rule, line)
    for identifier in identifiers:
        start, end = identifier.span()
        if not is_within_positions((start, end), positions):
            identifier_text = identifier.group().strip()
            if identifier_text not in constructs:
                identifier_type = classify_identifier(identifier_text, line[:start])
                lexemes["identifiers"].append(identifier_text)
                all_tokens.append({
                    "token": identifier_text,
                    "type": identifier_type,
                    "line": line_cnt,
                    "start": start,
                    "end": end
                })
                positions.append((start, end))

    # Identify unclassified tokens (errors)
    remaining_text = re.finditer(r"\S+", line)
    for text in remaining_text:
        start, end = text.span()
        lexeme = text.group().strip()

        # Skip tokens inside comments
        if is_within_positions((start, end), positions):
            continue  # Skip the token if it's within a comment

        if lexeme == "+":
            # Label `+` as Concatenate if it's not part of a comment
            lexemes.setdefault("concatenation", []).append(lexeme)
            all_tokens.append({
                "token": lexeme,
                "type": "Concatenate",  # Updated type
                "line": line_cnt,
                "start": start,
                "end": end
            })
        elif not is_within_positions((start, end), positions):  # Unclassified token
            # If it's not `+`, treat it as an error
            lexemes.setdefault("errors", []).append(lexeme)
            all_tokens.append({
                "token": lexeme,
                "type": "Error",
                "line": line_cnt,
                "start": start,
                "end": end
            })
            
        positions.append((start, end))


def is_within_positions(span, positions):
    """Check if a span overlaps with any recorded positions."""
    for start, end in positions:
        if start <= span[0] < end or start < span[1] <= end:
            return True
    return False



def classify_keyword(lexeme):
    """Classify a keyword into a specific type."""
    if lexeme in program_delimiters:
        return "Program Delimiter"
    elif lexeme in control_flow:
        return "Control Flow"
    elif lexeme in data_declaration:
        return "Data Declaration"
    elif lexeme in input_output:
        return "Input/Output"
    elif lexeme in logical_operators:
        return "Logical Operator"
    elif lexeme in mathematical_operators:
        return "Mathematical Operator"
    elif lexeme in switch:
        return "Switch"
    elif lexeme in function_keywords:
        return "Function Delimiter"
    elif lexeme in return_statements:
        return "Return Statement"
    elif lexeme in data_initialization:
        return "Data Initialization"
    elif lexeme in connector:
        return "Connector"
    elif lexeme in loop_keywords:
        return "Loop Delimiter"
    elif lexeme in assignment:
        return "Assignment Operator"
    elif lexeme in loop_op:
        return "Loop Operator"
    elif lexeme in loop_type:
        return "Loop Type"
    elif lexeme in concatenate:
        return "Concatenate"
    elif lexeme in function_call:
        return "Function Call"
    elif lexeme in comments:
        return "Comment"
    elif lexeme in typecast:
        return "Typecast"
    else:
        return "Other Keyword"


def classify_identifier(identifier_text, context):
    """Classify an identifier based on the previous token (lexeme)."""
    
    # Ensure there's some context before the identifier
    if context.strip():  # Check if the context is not empty or just whitespace
        prev_tokens = context.strip().split()  # Split the context into words
        if prev_tokens:  # Ensure there's at least one word before the identifier
            prev_token = prev_tokens[-1]  # Get the last word before the identifier
            
            # If the previous token is part of a loop-related keyword
            if prev_token in loop_keywords:
                return "Loop"  # The identifier is part of a loop
            
            # If the previous token is part of a function-related keyword
            if prev_token in function_keywords:
                return "Function"  # The identifier is part of a function
    
    # Default classification if no loop or function context is found
    return "Variable"


def analyze_code(code):
    lexemes = {"keywords": [], "literals": [], "identifiers": [], "comments": []}
    all_tokens = []
    line_cnt = 1

    # Tokenize each line of code
    for line in code.splitlines():
        tokenize_line(line, lexemes, all_tokens, line_cnt)
        line_cnt += 1

    # Sort tokens by line and position
    all_tokens.sort(key=lambda x: (x['line'], x['start']))
    return all_tokens

