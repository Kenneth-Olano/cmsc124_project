from tkinter import simpledialog, messagebox
import tkinter as tk

constructs = set([
    "HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R",
    "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF",
    "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT",
    "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE",
    "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL",
    "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY", "AN"
])

class SemanticAnalyzer:
    def __init__(self, all_tokens, function_dict, console_widget):
        self.all_tokens = all_tokens
        self.function_dict = function_dict
        self.symbol_table = {}  # Stores declared variables and their types
        self.function_table = {}  # Stores functions and their return types
        self.scope_stack = []  # Stack to manage scopes (e.g., for functions and loops)
        self.current_index = 0  # Pointer to the current token
        self.current_token = self.all_tokens[self.current_index] if self.all_tokens else None
        self.IT = None
        self.console = console_widget

    def log_to_console(self, message):
        """Utility function to log messages to the console."""
        self.console.config(state=tk.NORMAL)  # Enable the text widget
        self.console.insert(tk.END, message + "\n")
        self.console.config(state=tk.DISABLED)  # Disable editing

    def get_symbol_table(self):
        """Method to get the current symbol table."""
        return self.symbol_table

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
        # self.check_uninitialized_variables()

    def process_token(self, token):
        token_type = token['type']
        token_value = token['token']
        
        if token_type == 'Data Declaration' and token_value == "I HAS A":
            # Check if it's a variable declaration like "I HAS A"
            
            next_token = self.getnext()
            self.declare_variable(next_token)
        elif (token_type == 'Data Declaration' and token_value == "ITZ"):
            # Check if it's a variable declaration like "I HAS A"
            self.assignval_tovar(token)
        elif token_value == "GIMMEH":
            self.execute_input()
        elif (token_type == 'Mathematical Operator'):
            # Check if it's a variable declaration like "I HAS A"
            next_token = self.getnext()
            self.math_checktype(token)
            self.execute_math(self.current_index, [])
        elif (token_type == 'Input/Output') and token_value == 'VISIBLE':
            self.visible(self.current_index)
        elif(token_value == "MAEK" or token_value == "IS NOW A"):
            self.execute_typecasting(token, self.current_index)
        elif token_type == 'Assignment Operator' and token_value == "R":
            # Check if the assignment is to a valid variable
            self.check_variable_assignment(token)
        elif token_value == "WTF?":
            self.execute_switch(self.current_index)
        elif token_type == 'Function Delimiter' and token_value == "HOW IZ I":
            # Function declaration or call (e.g., "HOW IZ I")
            self.process_function(token)
        elif token_type == 'Function Call' and token_value == "I IZ":
            # Check the function call (e.g., "I IZ")
            self.check_function_call(token)
        elif token_type == 'Mathematical Operation':
            self.math_checktype(token)
            next_token = self.getnext()
            self.execute_math(self.current_index+1, [])
        elif token_type == 'Loop Delimiter':
            # Check if we are inside a loop for variable scope management
            self.handle_loop_scope(token)
        elif token_type == "Variable":
            if token_value in self.symbol_table and self.all_tokens[self.current_index]['line'] > self.all_tokens[self.current_index-1]['line'] :
                self.IT = self.symbol_table[token_value]
            elif token_value not in self.symbol_table:
                self.raise_semantic_error(token, f'Variable {token['token']} should be declared.')
        # Further checks could be added here for specific types of tokens



    def execute_switch(self, index):
        self.current_index = self.current_index+1
        self.current_token = self.all_tokens[self.current_index]
        # print(self.IT)
        while self.current_token['token'] != "OMGWTF":
            if self.current_token['token'] == "OMG":
                self.current_index+=1
                self.current_token = self.all_tokens[self.current_index]
                if self.current_token['type'] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Variable"]:
                    value = None
                    if self.current_token['type'] == "NUMBR":
                        value = int(self.current_token['token'])
                    elif self.current_token['type'] == "NUMBAR":
                        value = float(self.current_token['token'])
                    elif self.current_token['type'] == "YARN":
                        value = self.current_token['token'][1:len(self.current_token['token'])-1]
                    elif self.current_token['type'] == "TROOF":
                        value = self.current_token['token']
                    elif self.current_token['type'] == "Variable":
                        if self.current_token['token'] in self.symbol_table:
                            value = self.symbol_table[self.current_token['token']]['value']
                        else:
                            self.raise_semantic_error(self.current_token['token'], f'Variable {self.current_token['token']} should be declared.')
                    # print(value)
                    if value == self.IT['value']:
                        while self.current_token['token'] != "GTFO":
                            print(self.current_token['token'])
                            self.execute_statement(self.current_token, self.current_index)
                            self.current_index+=1
                            self.current_token = self.all_tokens[self.current_index]
                        if self.current_token['token'] == "GTFO":
                            self.advance()
                            while self.current_token['token'] != "OIC":
                                self.current_index+=1
                                self.current_token = self.all_tokens[self.current_index]
                        return
                        
            self.current_index+=1
            self.current_token = self.all_tokens[self.current_index]
        while self.current_token['token'] != "OIC":
            self.execute_statement(self.current_token, self.current_index)
            self.current_index+=1
            self.current_token = self.all_tokens[self.current_index]

    def execute_input(self):
        variable = self.getnext()  # Retrieve the next token (e.g., the variable to store input)
        if variable['token'] in self.symbol_table:
            # Create a pop-up input dialog using tkinter
            root = tk.Tk()
            root.withdraw()  # Hide the main tkinter window
            new_value = simpledialog.askstring("Input Required", f"Enter value for {variable['token']}:")
            root.destroy()  # Close the tkinter window
            
            # If user cancels the input, raise an error
            if new_value is None:
                self.raise_semantic_error(variable, f"No input provided for {variable['token']}.")

            try:
                if new_value == "WIN" or new_value == "FAIL":
                    self.symbol_table[variable['token']]['value'] = new_value
                    self.symbol_table[variable['token']]['type'] = "TROOF"
                elif new_value.count('.') == 1:
                    self.symbol_table[variable['token']]['value'] = float(new_value)
                    self.symbol_table[variable['token']]['type'] = "NUMBAR"
                elif new_value.count('.') == 0:
                    self.symbol_table[variable['token']]['value'] = int(new_value)
                    self.symbol_table[variable['token']]['type'] = "NUMBR"
            except: 
                self.symbol_table[variable['token']]['value'] = f'"{new_value}"'
                self.symbol_table[variable['token']]['type'] = "YARN"
                
            self.symbol_table[variable['token']]['initialized'] = True
        else:
            self.raise_semantic_error(variable, f"Variable {variable['token']} not declared.")

    def math_checktype(self, token):
        value = token
        value_index = self.current_index
        # print(self.symbol_table)

        while True:
            value_index+=1
            value = self.all_tokens[value_index]
            if value['type'] == "NUMBR" or value['type'] == "NUMBAR" or value['token'] in self.symbol_table.keys():
                if value['token'] in self.symbol_table.keys() and self.symbol_table[value['token']]['initialized'] == True:
                    variable = self.symbol_table[value['token']]
                    if variable['type'] == "NUMBR":
                        pass
                    elif variable['type'] == "NUMBAR":
                        pass
                    elif variable['type'] == "YARN":
                        try:
                            yarn = variable['value'][1:len(variable['value'])-1]
                            if "." in yarn:
                                string_to_float = float(yarn)
                            else:   
                                string_to_int = int(yarn)
                        except:
                            self.raise_semantic_error(token, f'Variable {variable['token']} should be type NUMBR or NUMBAR.')
                    elif variable['type'] == "TROOF":
                        troof = variable['value']
                        if troof == "WIN":
                            troof_to_int = 1
                        elif troof == "FAIL":   
                            troof_to_int = 0
                    else:
                        self.raise_semantic_error(token, f'Variable {value['token']} should be type NUMBR or NUMBAR.')
                elif value['token'] in self.symbol_table.keys() and self.symbol_table[value['token']]['initialized'] == False:
                    self.raise_semantic_error(value, f'Variable {value['token']} should be initialized.')
            elif value['type'] == "YARN":
                try:
                    yarn = value['token'][1:len(value['token'])-1]
                    if "." in yarn:
                        string_to_float = float(yarn)
                    else:   
                        string_to_int = int(yarn)
                except:
                    self.raise_semantic_error(token, f'Variable {value['token']} should be type NUMBR or NUMBAR.')
            value_index+=1
            value = self.all_tokens[value_index]
            if value['token'] != "AN":
                break


    def declare_variable(self, token):
        variable_name = token['token']
        
        if variable_name not in self.symbol_table:
            self.symbol_table[variable_name] = {'type': 'undefined', 'initialized': False, 'value':None}
        else:
            # Raise a semantic error if the variable is re-declared
            self.raise_semantic_error(self.current_token, f"Variable '{variable_name}' is already declared.")


    def assignval_tovar(self, token):
        next_token = self.getnext()
        next_index = self.current_index+1
        value = next_token['token']

        if len(self.symbol_table) > 0:
            variable = list(self.symbol_table)[len(self.symbol_table)-1]
            self.symbol_table[variable]['type'] = next_token['type']
            self.symbol_table[variable]['initialized'] = True
            if next_token['type'] == "NUMBR":
                self.symbol_table[variable]['value'] = int(value)
            elif next_token['type'] == "NUMBAR":
                self.symbol_table[variable]['value'] = float(value)
            elif next_token['type'] == "YARN":
                self.symbol_table[variable]['value'] = value
            elif next_token['token'] == "WIN":   
                self.symbol_table[variable]['value'] = True
            elif next_token['token'] == "FAIL":      
                self.symbol_table[variable]['value'] = False
            elif next_token['type'] == "Mathematical Operator":
                self.execute_math(next_index, [])
                if type(self.IT) == int:
                    self.symbol_table[variable]['type'] = "NUMBR"
                elif type(self.IT) == float:
                    self.symbol_table[variable]['type'] = "NUMBAR"
                
                self.symbol_table[variable]['value'] = self.IT
        # print(self.symbol_table)

    def check_variable_assignment(self, token):
        next_token = self.getnext()
        variable_name = next_token['token'] 
        # print(self.symbol_table)
        if variable_name not in self.symbol_table:
            if next_token['type'] in ["NUMBR", "NUMBAR", "YARN", "TROOF"]:
                variable = list(self.symbol_table)[len(self.symbol_table)-1]
                self.symbol_table[variable]['type'] = next_token['type']
                self.symbol_table[variable]['initialized'] = True
                self.symbol_table[variable]['value'] = next_token['token'] 
            elif  next_token['token'] not in constructs:
                self.raise_semantic_error(self.current_token, f"Variable '{variable_name}' is not declared.")
        else:
            self.symbol_table[variable_name]['initialized'] = True

    def process_function(self, token):
        token_index = self.current_index+1
        next_token = self.getnext()
        function_name = next_token['token']
        # Add function to function table if not already defined
        if function_name not in self.function_table:
            self.function_table[function_name] = {'return_type': 'undefined', 'parameters': {}, 'index':token_index}
            if function_name in self.function_dict.keys():
                # print(self.function_dict[function_name].keys())
                for parameter in self.function_dict[function_name].keys():
                    
                    self.function_table[function_name]['parameters'][parameter] = None
                
                while (self.all_tokens[token_index])['token'] != "IF U SAY SO":
                    token_index+=1
                    if (self.all_tokens[token_index])['type'] == "Variable":
                        if (self.all_tokens[token_index])['token'] not  in self.function_table[function_name]['parameters']:
                            self.raise_semantic_error((self.all_tokens[token_index]), f'Variable {(self.all_tokens[token_index])['token']} is out of function {function_name} scope.')
                            break
                        if (self.all_tokens[token_index])['token'] not in self.symbol_table.keys():
                            self.symbol_table[(self.all_tokens[token_index])['token']] = {'type': 'NOOB', 'initialized': False, 'value':"NOOB"}
                        # print(self.symbol_table)
                    elif (self.all_tokens[token_index])['type'] == "Function Parameter":
                        self.symbol_table[(self.all_tokens[token_index])['token']] = {'type': 'NOOB', 'initialized': False, 'value':"NOOB"}
        else:
            # Function already declared, check parameters and types if necessary
            self.raise_semantic_error(self.current_token, f"Function '{function_name}' is already declared.")
            return
        # Push a new scope for function parameters
        self.scope_stack.append({'type': 'function', 'function': function_name})
        

    def check_function_call(self, token):
        token_index = self.current_index+1
        next_token = self.getnext()
        function_name = next_token['token']
        function_index = (self.function_table[function_name])['index']
        # print(self.function_table)
        
        if function_name not in self.function_table:
            self.raise_semantic_error(self.current_token, f"Function '{function_name}' is not declared. Call")
        else:
            
            parameter_count = 0
            actual_parameters = []
            while (self.all_tokens[token_index])['token'] != "MKAY":
                token_index+=1
                if (self.all_tokens[token_index])['type'] == "Variable":
                    if (self.all_tokens[token_index])['token'] not in self.symbol_table:
                        # print((self.all_tokens[token_index])['token'])
                        self.raise_semantic_error((self.all_tokens[token_index]), f'Variable {(self.all_tokens[token_index])['token']} is not declared.')
                        # print(f'Error in {(self.all_tokens[token_index])['token']}')
                        break
                    else:
                        actual_parameters.append((self.all_tokens[token_index])['token'])
                        parameter_count+=1
            if parameter_count != len(self.function_table[function_name]['parameters']):
                self.raise_semantic_error((self.all_tokens[token_index]), f'Function call {function_name} has unmatched parameter count to function declaration.')
            else:
                counter = 0
                for i in self.function_table[function_name]['parameters']:
                    (self.symbol_table[i])['type'] = (self.symbol_table[actual_parameters[counter]])['type']
                    (self.symbol_table[i])['initialized'] = True
                    (self.symbol_table[i])['value'] = (self.symbol_table[actual_parameters[counter]])['value']
                    counter+=1
                self.execute_function(function_name, function_index)
                for i in self.function_table[function_name]['parameters']:
                    (self.symbol_table[i])['type'] = "NOOB"
                    (self.symbol_table[i])['initialized'] = False
                    (self.symbol_table[i])['value'] = "NOOB"
                
    def execute_statement(self, token, index):
        if token['token'] == "VISIBLE":
            self.visible(index)
        elif token['type'] == "Mathematical Operator":
            self.execute_math(index, [])
        elif token['token'] == "GIMMEH":
            self.execute_input()


    def execute_function(self, function_name, function_index):
        function_index+=1
        while((self.all_tokens[function_index])['token'] != "IF U SAY SO"):
            self.execute_statement(self.all_tokens[function_index], function_index)
            function_index+=1
        
    def execute_typecasting(self, token, index):
        next_index = index
        if token['token'] == "MAEK":
            next_index+=1
            next_token = self.all_tokens[next_index]
            if next_token['type'] == "Variable":
                if next_token['token'] in self.symbol_table:
                    variable = next_token['token']
                    next_index+=2
                    to_type = self.all_tokens[next_index]['token']
                    if self.symbol_table[variable]['type'] == "NOOB":
                        if to_type == "TROOF":
                            return {'type': 'TROOF', 'initialized': True, 'value':"FAIL"}
                        else:
                            self.raise_semantic_error(next_token, f'NOOB values can only be typecasted to TROOF.')
                    elif self.symbol_table[variable]['type'] == "NUMBR" or self.symbol_table[variable]['type'] == "NUMBAR":
                        if self.symbol_table[variable]['type'] == "NUMBR" and to_type == "NUMBAR":
                            return {'type': 'NUMBAR', 'initialized': True, 'value':float(self.symbol_table[variable]['value'])}
                        elif self.symbol_table[variable]['type'] == "NUMBAR" and to_type == "NUMBR":
                            return {'type': 'NUMBAR', 'initialized': True, 'value':int(self.symbol_table[variable]['value'])}
                        elif to_type == "YARN":
                            return{'type': 'YARN', 'initialized': True, 'value':f'"{(self.symbol_table[variable]['value'])}"'}
                        elif to_type == "TROOF":
                            print("PANALO")
                            bool_val = bool(self.symbol_table[variable]['value'])
                            print(bool_val)
                            if bool_val == True:
                                print("KUHA")
                                self.IT = 'WIN'
                                return
                            else:
                                return{'type': 'TROOF', 'initialized': True, 'value':'FAIL'}
                        else:
                            self.raise_semantic_error(next_token, f'NUMBR/NUMBAR cannot be casted into NOOB.')
                    elif self.symbol_table[variable]['type'] == "YARN":
                        if to_type == "NUMBR":
                            return{'type': 'NUMBR', 'initialized': True, 'value':int(self.symbol_table[variable]['value'])}
                        elif to_type == "NUMBAR":
                            return {'type': 'NUMBAR', 'initialized': True, 'value':float(self.symbol_table[variable]['value'])}
                        elif to_type == "TROOF":
                            bool_val = bool(self.symbol_table[variable]['value'])
                            if bool_val == True:
                                return {'type': 'TROOF', 'initialized': True, 'value':'WIN'}
                            else:
                                return {'type': 'TROOF', 'initialized': True, 'value':'FAIL'}
                        else:
                            self.raise_semantic_error(next_token, f'YARN cannot be casted into NOOB.')
                    elif self.symbol_table[variable]['type'] == "TROOF":
                        bool_val = True if self.symbol_table[variable]['value'] == "WIN" else False
                        if to_type == "NUMBR":
                            return {'type': 'NUMBR', 'initialized': True, 'value':int(bool_val)}
                        elif to_type == "NUMBAR":
                            return {'type': 'NUMBAR', 'initialized': True, 'value':float(bool_val)}
                        elif to_type == "YARN":
                            return {'type': 'TROOF', 'initialized': True, 'value':f'"{self.symbol_table[variable]['value']}'}
                        else:
                            self.raise_semantic_error(next_token, f'YARN cannot be casted into NOOB.')
                    
                        

    def execute_math(self,index, math_stack):
        current_index = index
        current_token = self.all_tokens[current_index]
        next_token = self.all_tokens[current_index+1]
        start_line = current_token['line']
        current_line = current_token['line']
        next_line = next_token['line']

        while current_line == start_line:
            if current_token['token'] == "SUM OF":
                math_stack.append('+')
            elif current_token['token'] ==  "DIFF OF": 
                math_stack.append('-')
            elif current_token['token'] ==  "PRODUKT OF": 
                math_stack.append('*')
            elif current_token['token'] ==  "QUOSHUNT OF": 
                math_stack.append('/')
            elif current_token['token'] ==  "MOD OF": 
                math_stack.append('%')
            elif current_token['token'] ==  "BIGGR OF": 
                math_stack.append('>')
            elif current_token['token'] ==  "SMALLR OF": 
                math_stack.append('<')
            elif current_token['type'] == "NUMBR" or  current_token['type'] == "NUMBAR" or  current_token['type'] == "TROOF" or  current_token['type'] == "YARN":
                if current_token['type'] == "NUMBR":
                    math_stack.append(int(current_token['token']))
                elif current_token['type'] == "NUMBAR":
                    math_stack.append(float(current_token['token']))
                elif current_token['type'] == "TROOF":
                    if current_token['token'] == "WIN": 
                        math_stack.append(1)
                    elif current_token['token'] == "FAIL": 
                        math_stack.append(0)
                elif current_token['type'] == "YARN":
                    try:
                        if '.' in current_token['token']:
                            math_stack.append(float(current_token['token'])) 
                        else:
                            math_stack.append(int(current_token['token'])) 
                    except:
                        self.raise_semantic_error(current_token, f'Literal {current_token['token']} should be type NUMBR or NUMBAR.')
            elif current_token['type'] == "Variable":
                if current_token['token'] in self.symbol_table and (self.symbol_table[current_token['token']])['initialized'] == True:
                    # print(current_token['token'])
                    if type(self.symbol_table[current_token['token']]['value']) == int:
                        math_stack.append(self.symbol_table[current_token['token']]['value'])
                    elif type(self.symbol_table[current_token['token']]['value']) == float:
                        math_stack.append(self.symbol_table[current_token['token']]['value'])
                    elif type(self.symbol_table[current_token['token']]['value']) == str:
                        if self.symbol_table[current_token['token']]['value'] == "WIN": 
                            math_stack.append(1)
                        elif self.symbol_table[current_token['token']]['value'] == "FAIL": 
                            math_stack.append(0)
                        else:
                            try:
                                if '.' in self.symbol_table[current_token['token']]['value']:
                                    math_stack.append(float(self.symbol_table[current_token['token']]['value'])) 
                                else:
                                    math_stack.append(int(self.symbol_table[current_token['token']]['value'])) 
                            except:
                                self.raise_semantic_error(current_token, f'Variable {current_token['token']} should be type NUMBR or NUMBAR.')
                else:
                    break
            # print(math_stack)
            stack_len = len(math_stack)
            if len(math_stack) >= 3 and ((type(math_stack[stack_len-1]) == int) or (type(math_stack[stack_len-1]) == float)) and ((type(math_stack[stack_len-2]) == int) or (type(math_stack[stack_len-2]) == float)):
                b = math_stack.pop()
                a = math_stack.pop()
                op = math_stack.pop()
                if(op == '+'):
                    math_stack.append(a+b)
                elif (op == '-'):
                    math_stack.append(a-b)
                elif (op == '*'):
                    math_stack.append(a*b)
                elif (op == '/'):
                    math_stack.append(a/b)
                elif (op == '%'):
                    math_stack.append(a%b)
                elif (op == '>'):
                    math_stack.append(max(a,b))
                elif (op == '<'):
                    math_stack.append(min(a,b))
                # print(math_stack)
            current_index +=1
            current_token = self.all_tokens[current_index]
            if current_index == len(self.all_tokens)-1:
                break
            next_token = self.all_tokens[current_index+1]
            current_line = current_token['line']
            next_line = next_token['line']
            # print(math_stack)
        if len(math_stack) >= 3 and ((type(math_stack[len(math_stack)-1]) == int) or (type(math_stack[len(math_stack)-1]) == float)) and ((type(math_stack[len(math_stack)-2]) == int) or (type(math_stack[len(math_stack)-2]) == float)):
            b = math_stack.pop()
            a = math_stack.pop()
            op = math_stack.pop()
            if(op == '+'):
                math_stack.append(a+b)
            elif (op == '-'):
                math_stack.append(a-b)
            elif (op == '*'):
                math_stack.append(a*b)
            elif (op == '/'):
                math_stack.append(a/b)
            elif (op == '%'):
                math_stack.append(a%b)
            elif (op == '>'):
                math_stack.append(max(a,b))
            elif (op == '<'):
                math_stack.append(min(a,b))
        # print(math_stack)
        self.IT = math_stack[0]


    def visible(self, index):
        next_index = index+1
        next_token = self.all_tokens[next_index]
        start_line = next_token['line']
        current_line = next_token['line']
        display_str = ""
        # print(next_token['token'])
        while start_line == current_line:
            if next_token['type'] in ["NUMBR", "NUMBAR", "YARN", "TROOF"]:
                if next_token['type'] == "YARN":
                    self.IT = next_token['token'][1:len(next_token['token'])]
                else:
                    self.IT = next_token['token']
                display_str+=str(self.IT)
                
            elif next_token['type'] == "Variable":
                if type(self.symbol_table[next_token['token']]['value']) == str and '\"' in self.symbol_table[next_token['token']]['value']:
                    self.IT =self.symbol_table[next_token['token']]['value'][1:-1]
                else:
                    self.IT = self.symbol_table[next_token['token']]['value']
                display_str+=str(self.IT)
            elif next_token['type'] == "Mathematical Operator":
                self.execute_math(index, [])
                display_str+=str(self.IT)
            elif next_token['type'] == "Typecast" and next_token['token'] == "MAEK":
                self.execute_typecasting(self.all_tokens[index], index)
                display_str+=str(self.IT)
            elif next_token['type'] == "Concatenate":
                pass
            else:
                # print(next_token['token'])
                pass
            next_index+=1
            next_token = self.all_tokens[next_index]
            current_line = next_token['line']
            
        self.log_to_console(f"> {self.IT}")
        # Further checks can be added to verify function parameters, return types, etc.
    def execute_comparison(self, index):
        comparison_op = self.all_tokens[index]
        start_line = self.current_token['line']
        next_index = index+1
        next_token = self.all_tokens[next_index]
        comparison_stack = []
        
        while start_line == next_token['line']:
            if next_token['type'] in ["TROOF", "NUMBR", "NUMBAR", "YARN"]:
                comparison_stack.append(next_token['token'])
            elif next_token['type'] == "Variable" and next_token['token'] in self.symbol_table:
                comparison_stack.append(self.symbol_table[next_token['token']]['value'])
            elif next_token['type'] == "Math Operator":
                self.math_checktype(next_index)
                self.execute_math(next_index, [])
                comparison_stack.append(self.IT)
        
        if comparison_op['token'] == "BOTH SAEM":
            return comparison_stack[-1] == comparison_stack[-2]
        else:
            return comparison_stack[-1] != comparison_stack[-2]




    def handle_loop_scope(self, token):
        # Add loop-related scope management
        # Loops create a new scope for variables, e.g., "IM IN YR"
        # self.scope_stack.append({'type': 'loop', 'token': token})
        loop_start = self.current_index
        
        while True:
            self.advance()
            if self.current_token['type'] == "Loop":
                var = 0
                self.advance
                loopop = self.current_token['token']
                self.advance()
                self.advance()
                if self.current_token['token'] in self.symbol_table and self.current_token['type'] == "NUMBR":
                    var = self.symbol_table[self.current_token['token']]
                self.advance()
                loop_op = self.current_token['token']
                self.advance()
                loop_type = self.current_token['token']
                if self.execute_comparison(self.current_index) == False:
                    while self.current_token['token'] != "IM OUTTA YR":
                        self.advance()
                    self.advance()
                    return
                while self.current_token['token'] != "GTFO" or self.current_token['token'] != "IM OUTTA YR":                
                    self.execute_statement(self.current_token, self.current_index)
                
                if loop_op == "NERFIN":
                    self.symbol_table[var] -= 1
                elif loop_op == "UPPIN":
                    self.symbol_table[var] += 1
                self.current_index = loop_start
                
                

            
            



    def check_uninitialized_variables(self):
        for variable, data in self.symbol_table.items():
            if (not data['initialized']):
                # print(data['initialized'])
                self.raise_semantic_error(self.current_token, f"Variable '{variable}' is used before initialization.")

    def raise_error(self, expected):
        """Raise a detailed syntax error with token information."""
        if self.current_token:
            raise SyntaxError(
                f"Syntax Error: Expected {expected} but found '{self.current_token['token']}' "
                f"(type: {self.current_token['type']}) at line {self.current_token['line']} "
                f"position {self.current_token['start']}-{self.current_token['end']}."
            )
        else:
            raise SyntaxError(
                f"Syntax Error: Expected {expected} but reached the end of the program."
            )
    def raise_semantic_error(self,token, message):
        """Raise a detailed syntax error with token information."""
        if token:
            messagebox.showerror("Semantic Error", 
                f"Semantic Error: {message}\n" + 
                f"(type: {token['type']}) at line {token['line']} " + 
                f"position {token['start']}-{token['end']}."
            )

    