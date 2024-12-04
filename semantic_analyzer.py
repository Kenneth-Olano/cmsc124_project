class SemanticAnalyzer:
    def __init__(self, all_tokens):
        self.all_tokens = all_tokens
        self.symbol_table = {}  # Stores declared variables and their types
        self.function_table = {}  # Stores functions and their return types
        self.scope_stack = []  # Stack to manage scopes (e.g., for functions and loops)

    def analyze(self):
        for token in self.all_tokens:
            if token['type'] == 'Keyword' or token['type'] == 'Identifier':
                self.process_token(token)
        
        # Perform post-analysis checks (e.g., uninitialized variables)
        self.check_uninitialized_variables()

    def process_token(self, token):
        token_type = token['type']
        token_value = token['token']
        
        if token_type == 'Data Declaration':
            # Check if it's a variable declaration like "I HAS A"
            self.declare_variable(token)
        
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
        variable_name = token['token']
        
        if variable_name not in self.symbol_table:
            self.symbol_table[variable_name] = {'type': 'undefined', 'initialized': False}
        else:
            # Raise a semantic error if the variable is re-declared
            self.raise_semantic_error(f"Variable '{variable_name}' is already declared.")

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
            pass
        
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
            if not data['initialized']:
                self.raise_semantic_error(f"Variable '{variable}' is used before initialization.")

    def raise_semantic_error(self, message):
        print(f"Semantic Error: {message}")
        # raise Exception(f"Semantic Error: {message}")
class SemanticAnalyzer:
    def __init__(self, all_tokens):
        self.all_tokens = all_tokens
        self.symbol_table = {}  # Stores declared variables and their types
        self.function_table = {}  # Stores functions and their return types
        self.scope_stack = []  # Stack to manage scopes (e.g., for functions and loops)

    def analyze(self):
        for token in self.all_tokens:
            if token['type'] == 'Keyword' or token['type'] == 'Identifier':
                self.process_token(token)
        
        # Perform post-analysis checks (e.g., uninitialized variables)
        self.check_uninitialized_variables()

    def process_token(self, token):
        token_type = token['type']
        token_value = token['token']
        
        if token_type == 'Data Declaration':
            # Check if it's a variable declaration like "I HAS A"
            self.declare_variable(token)
        
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
        variable_name = token['token']
        
        if variable_name not in self.symbol_table:
            self.symbol_table[variable_name] = {'type': 'undefined', 'initialized': False}
        else:
            # Raise a semantic error if the variable is re-declared
            self.raise_semantic_error(f"Variable '{variable_name}' is already declared.")

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
            pass
        
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
            if not data['initialized']:
                self.raise_semantic_error(f"Variable '{variable}' is used before initialization.")

    def raise_semantic_error(self, message):
        print(f"Semantic Error: {message}")
        # raise Exception(f"Semantic Error: {message}")
