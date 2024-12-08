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
    r"\s-?[0-9]+\s",           # Integer literals
    r"\s-?[0-9]*\.[0-9]+?\s", # Floating-point literals
    r'\s\".*\"',               # String literals
    r"(WIN|FAIL)\s",           # Boolean literals
    r"\s(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\s"  # Type literals
]

# Regex pattern for identifiers
identifier_rule = r"[a-zA-Z][a-zA-Z0-9_]*"
code_line = []


def tokenize_line(line, lexemes, all_tokens, line_cnt):
    # Track positions of found keywords and literals to exclude them from identifier checks
    positions = {"keywords": [], "literals": [], "identifiers": []}
    literaltype_arr = ["NUMBR", "NUMBAR", "YARN", "TROOF"]
    # Define patterns for detecting variable, function, and loop identifiers
    variable_keywords = ["I HAS A", "I HAS", "GIMMEH", "MAEK", "YR","VISIBLE"]
    

    # Identify keywords
    keywords = re.finditer(r"\b(?:{})\b".format("|".join(map(re.escape, constructs)).replace("?", r"\?")), line)
    
    for keyword in keywords:
        lexeme = keyword.group().strip()
        if lexeme == "O RLY":
            lexeme = "O RLY?"
        elif lexeme == "WTF":
            lexeme = "WTF?"
        
            
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
        elif lexeme in switch:
            token_type = "Switch"
        elif lexeme in function_keywords:
            token_type = "Function Delimiter"
        elif lexeme in return_statements:
            token_type = "Return Statement"
        elif lexeme in data_initialization:
            token_type = "Data Initialization"
        elif lexeme in connector:
            token_type = "Connector"
        elif lexeme in loop_keywords:
            token_type = "Loop Delimiter"
        elif lexeme in assignment:
            token_type = "Assignment Operator"
        elif lexeme in loop_op:
            token_type = "Loop Operator"
        elif lexeme in loop_type:
            token_type = "Loop Type"
        elif lexeme in concatenate:
            token_type = "Concatenate"
        elif lexeme in function_call:
            token_type = "Function Call"
        elif lexeme in comments:
            token_type = "Comment"
        elif lexeme in typecast:
            token_type = "Typecast"
        else:
            # print(lexeme)
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
    literalrule_index = 0
    for rule in literal_rules:
        literals = re.finditer(rule, line)
        for literal in literals:
            if not is_within_positions(literal.span(), positions["keywords"]) :
                lexeme = literal.group().strip()
                lexemes["literals"].append(lexeme)
                if literalrule_index in range(0, 4):
                    all_tokens.append({
                        "token": lexeme,
                        "type": literaltype_arr[literalrule_index],
                        "line": line_cnt,
                        "start": literal.start(),
                        "end": literal.end()
                    })
                else:
                    all_tokens.append({
                        "token": lexeme,
                        "type": "Literal",
                        "line": line_cnt,
                        "start": literal.start(),
                        "end": literal.end()
                    })
                positions["literals"].append(literal.span())
        literalrule_index+=1
    # print(lexemes['literals'])
    # Identify identifiers
    identifiers = re.finditer(identifier_rule, line)
    for identifier in identifiers:
        identifier_text = identifier.group().strip()
        if (identifier_text not in constructs and
                not is_within_positions(identifier.span(), positions["keywords"]) and
                not is_within_positions(identifier.span(), positions["literals"])):
            
            # Heuristic-based classification of the identifier
            identifier_type = "Variable"  # Default classification

            # Check if the identifier is part of a variable declaration (e.g., "I HAS A")
            # for keyword in variable_keywords:
            #     if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
            #         identifier_type = "Variable"
            #         break
            #     elif len(line) == 0:
            #         identifier_type = "Variable"
            #         break

            # Check if the identifier is part of a function (e.g., "HOW IZ I")
            for keyword in function_keywords:
                if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
                    function_line = line[:identifier.start()].split()
                    if function_line[len(function_line)-1] == "YR":
                        identifier_type = "Function Parameter"
                    else:
                        identifier_type = "Function"
                    break
                
            for keyword in function_call:
                if keyword in line[:identifier.start()]:  # Check if keyword precedes the identifier
                    function_line = line[:identifier.start()].split()
                    if function_line[len(function_line)-1] == "YR":
                        # identifier_type = "Function Parameter"
                        pass
                    elif function_line[len(function_line)-1] == "IZ":
                        identifier_type = "Function"
                    break

            # Check if the identifier is part of a loop (e.g., "IM IN YR")
            for keyword in loop_keywords:
                if keyword in line[:identifier.start()] and len(positions["identifiers"])==0:  # Check if keyword precedes the identifier
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
            if lexeme == "+":
                all_tokens.append({
                "token": lexeme,
                "type": "Concatenate",
                "line": line_cnt,
                "start": text.start(),
                "end": text.end()
                })
            else:
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

def analyze_code(code):
    lexemes = {"keywords": [], "literals": [], "identifiers": []}
    all_tokens = []
    line_cnt = 1

    # Tokenize each line of code
    for line in code.splitlines():
        tokenize_line(line, lexemes, all_tokens, line_cnt)
        line_cnt += 1

    # After tokenization, sort all tokens by their start position to ensure correct order
    all_tokens.sort(key=lambda x: (x['line'], x['start']))

    return lexemes, all_tokens


