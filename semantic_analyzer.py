constructs = set([
    "HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R",
    "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
    "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT",
    "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE",
    "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL",
    "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY", "AN"
])

class SemanticAnalyzer:
    def __init__(self, all_tokens):
        self.all_tokens = all_tokens
        self.symbol_table = {}  # Stores declared variables and their types
        self.function_table = {}  # Stores functions and their return types
        self.scope_stack = []  # Stack to manage scopes (e.g., for functions and loops)
        self.current_index = 0  # Pointer to the current token
        self.current_token = self.all_tokens[self.current_index] if self.all_tokens else None

    def getnext(self):
        """Advance the token pointer to the next token."""
        return self.all_tokens[self.current_index+1] if self.current_index < len(self.all_tokens) else None

    def advance(self):
        self.current_index += 1
        self.current_token = (
            self.all_tokens[self.current_index] if self.current_index < len(self.all_tokens) else None
        )  
        
    def match(self, token_type, expected_token=None):
        """Check if the current token matches the expected type and optional specific token."""
        if self.current_token and self.current_token["type"] == token_type:
            if expected_token and self.current_token["token"] != expected_token:
                self.raise_error(f"'{expected_token}'")
            self.advance()
        else:
            self.raise_error(token_type)

    def analyze(self):
        while self.current_token and self.current_token["token"] != "KTHXBYE":
            if self.current_token['token'] in constructs or self.current_token['type'] in ["Loop", "Variable", "Function"]:
                self.process_token(self.current_token)  # Parse statements within the program
            self.advance()
        
        # Perform post-analysis checks (e.g., uninitialized variables)
        self.check_uninitialized_variables()

    def process_token(self, token):
        token_type = token['type']
        token_value = token['token']
        
        if token_type == 'Data Declaration' and token_value == "I HAS A":
            # Check if it's a variable declaration like "I HAS A"
            self.declare_variable(token)
        elif (token_type == 'Data Declaration' and token_value == "ITZ") or (token_type=='Assignment Operator' and token_value=="R"):
            # Check if it's a variable declaration like "I HAS A"
            self.assignval_tovar(token)

        elif token_type == 'Assignment Operator':
            # Check if the assignment is to a valid variable
            self.check_variable_assignment(token)
        
        elif token_type == 'Function Delimiter':
            # Function declaration or call (e.g., "HOW IZ I")
            self.process_function(token)
        
        elif token_type == 'Function Call':
            # Check the function call (e.g., "I IZ")
            self.check_function_call(token)
        
        elif token_type == 'Loop Delimiter':
            # Check if we are inside a loop for variable scope management
            self.handle_loop_scope(token)
        
        # Further checks could be added here for specific types of tokens

    def declare_variable(self, token):
        next_token = self.getnext()
        variable_name = next_token['token']
        
        if variable_name not in self.symbol_table:
            self.symbol_table[variable_name] = {'type': 'undefined', 'initialized': False, 'value':None}
            print(self.symbol_table)
        else:
            # Raise a semantic error if the variable is re-declared
            self.raise_semantic_error(f"Variable '{variable_name}' is already declared.")

    def assignval_tovar(self, token):
        next_token = self.getnext()
        value = next_token['token']

        if len(self.symbol_table) > 0:
            variable = list(self.symbol_table)[len(self.symbol_table)-1]
            self.symbol_table[variable]['type'] = next_token['type']
            self.symbol_table[variable]['initialized'] = True
            self.symbol_table[variable]['value'] = value


    def check_variable_assignment(self, token):
        variable_name = token['token']
        
        if variable_name not in self.symbol_table:
            self.raise_semantic_error(f"Variable '{variable_name}' is not declared.")
        else:
            self.symbol_table[variable_name]['initialized'] = True

    def process_function(self, token):
        function_name = token['token']
        # Add function to function table if not already defined
        if function_name not in self.function_table:
            self.function_table[function_name] = {'return_type': 'undefined', 'parameters': []}
        else:
            # Function already declared, check parameters and types if necessary
            self.raise_semantic_error(f"Function '{function_name}' is already declared.")
            return
        # Push a new scope for function parameters
        self.scope_stack.append({'type': 'function', 'function': function_name})
        

    def check_function_call(self, token):
        function_name = token['token']
        
        if function_name not in self.function_table:
            self.raise_semantic_error(f"Function '{function_name}' is not declared.")
        
        # Further checks can be added to verify function parameters, return types, etc.

    def handle_loop_scope(self, token):
        # Add loop-related scope management
        # Loops create a new scope for variables, e.g., "IM IN YR"
        self.scope_stack.append({'type': 'loop', 'token': token})

    def check_uninitialized_variables(self):
        for variable, data in self.symbol_table.items():
            print(data['initialized'])
            if not data['initialized']:
                # print(data['initialized'])
                self.raise_semantic_error(f"Variable '{variable}' is used before initialization.")

    def raise_semantic_error(self, message):
        print(f"Semantic Error: {message} at line {self.current_token['line']} {self.current_token['start']}-{self.current_token['end']}")
        # raise Exception(f"Semantic Error: {message}")
