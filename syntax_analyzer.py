from tkinter import messagebox

# def syntax_analyzer(lexemes):
#     constructs = {
#         "programdelimiter":("HAI", "KTHXBYE"),
#         "initialize": ("WAZZUP", "BUHBYE"),
#         "typecast": ("MAEK", "A", "IS NOW A"),
#         "declaration": ("I HAS A", "ITZ"),
#         "comparison":("BOTH SAEM", "DIFFRINT"),
#         "arithmetic":('SUM OF','DIFF OF','PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF'),
#         "literal": ('NUMBR', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'),
#         "boolean": ('BOTH OF', 'EITHER OF', 'WON OF', 'NOT'),
#         "infboolean": ('ALL OF', 'ANY OF'),
#         "loopdelimiter" : ('IM IN YR', 'IM OUTTA YR', 'YR', 'TIL', 'WILE'),
#         "loopop": ('UPPIN', 'NERFIN'),
#         "funcdelimiter": ('HOW IZ I', 'IF U SAY SO'),
#         "funccall": ('I IZ', 'MKAY'),
#         "funcparam": ('YR', 'AN'),
#         "switch": ("WTF?", "OMGWTF", "OIC"),
#         "case": ("OMG", "GTFO"),
#         "ifelse": ("O RLY", "YA RLY", "NO WAI", "OIC"),
#         "return": ('FOUND YR', 'GTFO'),
#         "concat": ("SMOOSH"),
#         "input": ("GIMMEH"),
#         "print": ("VISIBLE"),
#         "valconnect": ("AN"),
#         "assignment": ("R"),
#         "value": ("literal", "varident", "funcident"),
#         "toplvl": ("funcdelimiter", "expr", "toplvl"),
#         "expr": ("expr", 
#                 "print",
#                 "arithmetic",
#                 "boolean",
#                 "infboolean",
#                 "assignment",
#                 "comparison",
#                 "switch",
#                 "ifelse",
#                 "loopdelimiter",
#                 "input",
#                 "concat",
#                 "typecast",
#                 "funccall",
#                 "return",
#                 ""),
#         "newline": "\n"
#     }
#     program_stack = []
#     func_stack = []
#     ifelse_stack = []
#     initialize_stack = []
#     loop_stack = []
#     vardeclaration_stack = []
#     count = 0
#     for lexeme in lexemes: 
#         print(lexeme)
#         if lexeme['type'] == "Loop": #WILL BE CHANGED TO "LoopIdentifier" once specified
#             # print(lexeme)
#             if len(loop_stack) > 0 and type(loop_stack[len(loop_stack)-1]) == dict and (loop_stack[len(loop_stack)-1]['type'] == "Loop"):
#                 pass
#             else:
#                 if len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "IM IN YR" or loop_stack[len(loop_stack)-1] == "IM IN YR"):
#                     loop_stack.append(lexeme)
#                 elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "IM OUTTA YR") and len(loop_stack) == 7 and "IM IN YR" in loop_stack:
#                     loop_stack.clear()
#                 elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "YR"):
#                     loop_stack.append(lexeme)
#                 elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "WILE" or loop_stack[len(loop_stack)-1] == "TIL"):
#                     # messagebox.showerror("SyntaxError", f"No loop label provided.")
#                     # # print(lexeme)
#                     # print("No loop label provided.")
#                     # return
#                     continue
#                 elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] != "IM OUTTA YR") and len(loop_stack) == 6 and "IM IN YR" in loop_stack:
#                     messagebox.showerror("SyntaxError", f"Loop not properly delimited. No 'IM OUTTA YR' detected.")
#                     print("Loop not properly delimited. No 'IM OUTTA YR' detected.")
#                     return
        
#         if lexeme['type'] == "Literal":
#             if len(vardeclaration_stack)> 0 and vardeclaration_stack[len(vardeclaration_stack)-1] == "ITZ":
#                 vardeclaration_stack.clear()

#         if lexeme['type'] == "Variable":
#             if len(vardeclaration_stack)> 0 and (vardeclaration_stack[len(vardeclaration_stack)-1] == "I HAS A" or vardeclaration_stack[len(vardeclaration_stack)-1] == "ITZ"):
#                 vardeclaration_stack.append(lexeme)
#             elif len(vardeclaration_stack) > 0 and vardeclaration_stack[len(vardeclaration_stack)-1] != "I HAS A":
#                 messagebox.showerror("SyntaxError", f"Variable name invoked without variable declaration keyword I HAS A")
#                 print("Variable name invoked without variable declaration keyword I HAS A.")
#                 # return
            

#         for keys in constructs.keys():
#             if lexeme['token'] in constructs[keys]:
#                 if keys == "programdelimiter":
#                     # print("delimiter")
#                     if lexeme['token'] == "HAI":
#                         program_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "KTHXBYE":
#                         try:
#                             program_stack.pop()
#                         except:    
#                             messagebox.showerror("SyntaxError", f"Invalid program delimiters")
#                             print("Invalid program delimiters")
#                             return

            
#                 elif keys == "initialize":
#                     if lexeme['token'] == "WAZZUP":
#                         initialize_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "BUHBYE":
#                         try:
#                             initialize_stack.pop()
#                         except:    
#                             messagebox.showerror("SyntaxError", f"Invalid syntax for variable initialization. BUHBYE before WAZZUP.")
#                             print("Invalid variable initialization delimiters")
#                             return
                
                
#                 elif keys == "declaration":
#                     if lexeme['token'] == "I HAS A":
#                         if "I HAS A" not in vardeclaration_stack:
#                             vardeclaration_stack.append(lexeme['token'])
#                         elif type(vardeclaration_stack[len(vardeclaration_stack)-1]) == dict and vardeclaration_stack[len(vardeclaration_stack)-1]['type'] == "Variable":
#                             vardeclaration_stack.clear()
#                             vardeclaration_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "ITZ":
#                         if "I HAS A" in vardeclaration_stack and type(vardeclaration_stack[len(vardeclaration_stack)-1])==dict and vardeclaration_stack[len(vardeclaration_stack)-1]['type'] == "Variable":
#                             vardeclaration_stack.append(lexeme['token'])
#                         else:
#                             messagebox.showerror("SyntaxError", f"ITZ invoked before variable name declaration I HAS A.")
#                             print("ITZ invoked before variable name declaration I HAS A.")
#                             return

                    

#                 elif keys == "loopdelimiter": #HAS TO BE REVISED ONCE TOKENS ARE FIXED AND APPENDED IN SEQUENCE
#                     if lexeme['token'] == "IM IN YR":
#                         loop_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "YR":
#                         if loop_stack[len(loop_stack)-1] in constructs["loopop"]:
#                             loop_stack.append(lexeme['token'])
#                         else:
#                             messagebox.showerror("SyntaxError", f"No loop operation provided.")
#                             print("No loop operation provided.")
#                             return
#                     elif lexeme['token'] == "TIL" or lexeme['token'] == "WILE":
#                         if type(loop_stack[len(loop_stack)-1]) == dict and loop_stack[len(loop_stack)-1]['type'] == "Loop":
#                             loop_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "IM OUTTA YR":
#                         loop_stack.append(lexeme['token'])
                        
                    
#                         # if len(loop_stack) > 0 and loop_stack[len(loop_stack)-1] == "YR":
#                         #     loop_stack.append(lexeme)
#                         # if len(loop_stack) > 0 and loop_stack[len(loop_stack)-1] == "IM OUTTA YR":
#                         #     if len(loop_stack) == 7:
#                         #         loop_stack.clear()

#                 elif keys == "loopop":
#                     if (lexeme['token'] == "UPPIN" or lexeme['token'] == "NERFIN") and type(loop_stack[len(loop_stack)-1]) == dict and loop_stack[len(loop_stack)-1]['type'] == "Loop": 
#                         loop_stack.append(lexeme['token'])
                    

#                 # Function delimiter
#                 elif keys == "funcdelimiter":
#                     # print("function")
#                     # Function declaration
#                     if lexeme['token'] == "HOW IZ I":
#                         if "HOW IZ I" in func_stack:
#                         # if func_stack and func_stack[-1] == lexeme['token']:
#                             messagebox.showerror("SyntaxError", f"Nested function declarations are not allowed")
#                             print("Error: Nested function declaration")
#                             return
                        
#                         # Push 'HOW IZ I' to the stack
#                         func_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "IF U SAY SO":
#                         # Checks if the latest function declaration has a matching 'IF U SAY SO'
#                         if func_stack[len(func_stack-1)]  == lexeme['token']:
#                             func_stack.pop()
#                         else:    
#                             messagebox.showerror("SyntaxError", f"'IF U SAY SO' has no matching 'HOW IZ I'")
#                             print("Error: Unmatched 'IF U SAY SO'")
#                             return

#                 elif keys == "ifelse":
#                     # print("ifelse")
#                     if lexeme['token'] == "O RLY":
#                         ifelse_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "YA RLY": #if YA RLY is encountered
#                         if "O RLY" not in ifelse_stack: #check if it is enclosed in an O RLY clause
#                             messagebox.showerror("SyntaxError", f"YA RLY imposed with imposing O RLY first.")
#                             return
#                         else: #push to stack
#                             ifelse_stack.append(lexeme['token'])
#                     elif lexeme['token'] == "NO WAI": #when NO WAI is encoutered
#                         error_string = ""
#                         if "O RLY" not in ifelse_stack: #check if it is enclosed by an O RLY clause
#                             error_string+= "NO WAI imposed with imposing O RLY first.\n"
#                         if "YA RLY" not in ifelse_stack: #also check if NO WAI is preceeded by a YA RLY clase
#                             error_string += "NO WAI imposed with imposing YA RLY first."
#                         if len(error_string) != 0:
#                             messagebox.showerror("SyntaxError", error_string)
#                             return
#                     elif lexeme['token'] == "OIC": #if OIC is encountered
#                         try:
#                             if ifelse_stack[len(ifelse_stack)-1] == "YA RLY": #the top of stack should always be YA RLY when OIC is encountered, pop 2x if so
#                                 ifelse_stack.pop()
#                                 ifelse_stack.pop()
#                         except:
#                             messagebox.showerror("SyntaxError", f"OIC Keyword: Invalid if-else delimiters")
#                             print("OIC Invalid if-else delimiters")
#                             return
#                 count+=1
#                 # print(lexeme)
#         print(func_stack)
#         # print(loop_stack)
                
#     if(len(program_stack) == 0):
#         print("> VALID PROGRAM DELIMITERS")
#     else:
#         print("Invalid program delimiters")

#     if(len(initialize_stack) == 0):
#         print("> VALID INITIALIZATION DELIMITERS")
#     else:
#         print("Invalid initialization section delimiters")

#     if len(vardeclaration_stack) == 0:
#         print("> VALID VARIABLE DECLARATIONS")
#     else:
#         print("Invalid variable declaration")
#     if (len(loop_stack) == 0):
#         print("> VALID LOOP")
#     else:
#         print("Invalid loop syntax")

#     if(len(ifelse_stack) == 0):
#         print("> VALID IF ELSE")
#     else:
#         print("Invalid if else delimiters")



class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens generated by the lexical analyzer
        self.current_index = 0  # Pointer to the current token
        self.current_token = self.tokens[self.current_index] if self.tokens else None

    def advance(self):
        """Advance the token pointer to the next token."""
        self.current_index += 1
        self.current_token = (
            self.tokens[self.current_index] if self.current_index < len(self.tokens) else None
        )

    def match(self, token_type, expected_token=None):
        """Check if the current token matches the expected type and optional specific token."""
        if self.current_token and self.current_token["type"] == token_type:
            if expected_token and self.current_token["token"] != expected_token:
                self.raise_error(f"'{expected_token}'")
            self.advance()
        else:
            self.raise_error(token_type)

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

    def parse_program(self):
        """Parse the <program> rule."""
        self.match("Program Delimiter", "HAI")  # Start of the program
        while self.current_token and self.current_token["token"] != "KTHXBYE":
            self.parse_statement()  # Parse statements within the program
        self.match("Program Delimiter", "KTHXBYE")  # End of the program

    def parse_statement(self):
        """Parse the <statement> rule."""
        if not self.current_token:
            return

        token_type = self.current_token["type"]
        token_value = self.current_token["token"]

        if token_type == "Data Declaration":
            self.parse_declaration()
        elif token_type == "Input/Output" and token_value == "VISIBLE":
            self.parse_print()
        elif self.current_token["type"] == "Input/Output" and self.current_token["token"] == "GIMMEH":
            self.parse_input()
        elif token_type == "Control Flow":
            self.parse_control_flow()
        elif token_type == "Data Initialization":
            self.parse_initialization()
        elif token_type == "Mathematical Operator":
            self.parse_mathop()
        elif token_type == "Variable":
            self.parse_variable_assignment()
        elif token_type == "Loop Delimiter":
            self.parse_loop()
        else:
            self.raise_error("a valid statement")

    def parse_declaration(self):
        """Parse the <declaration> rule."""
        self.match("Data Declaration", "I HAS A")  # Match the "I HAS A" keyword
        self.parse_identifier()  # Expect a Variable identifier
        if self.current_token and self.current_token["token"] == "ITZ":
            # self.advance()
            self.match("Data Declaration", "ITZ")
            self.parse_value()

    def parse_initialization(self):
        """Parse the <initialization> rule"""
        self.match("Data Initialization", "WAZZUP")
        while self.current_token and self.current_token["token"] != "BUHBYE":
            self.parse_declaration()
        self.match("Data Initialization", "BUHBYE")

    def parse_identifier(self):
        """Parse the <identifier> rule."""
        if self.current_token and self.current_token["type"] == "Variable":
            self.advance()
        elif self.current_token and self.current_token["type"] == "Loop":
            self.advance()
        else:
            self.raise_error("Identifier")

    def parse_value(self):
        """Parse the <value> rule."""
        if self.current_token and self.current_token["type"] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Literal", "Variable" ,"Identifier", "Mathematical Operator"]:
            print(self.current_token['token'])
            if self.current_token["type"] == "Mathematical Operator":
                # print(self.current_token['token'])
                self.parse_mathop()
                
            else:
                # print(self.current_token['token'])
                self.advance()
        else:
            self.raise_error("Literal or Identifier")
    
    def parse_connector(self, connector):
        self.match("Connector", connector)
        

    def parse_mathop(self):
        try:
            self.match("Mathematical Operator")
            self.parse_value()
            self.parse_connector("AN")
            self.parse_value()
        except SyntaxError as e:
            print("mathop syntax error")
            self.raise_error("a valid Math operation")
        

    def parse_variable_assignment(self):
        """Parse variable assignment statements."""
        self.parse_identifier()  # The variable being assigned
        self.match("Assignment Operator", "R")  # The assignment operator
        self.parse_value()  # The value or expression being assigned

    def parse_input(self):
        """Parse the <input> rule for GIMMEH."""
        self.match("Input/Output", "GIMMEH")  # Match the GIMMEH keyword
        self.parse_identifier()  # Expect an identifier to store the input

    def parse_function_call(self):
        """Parse function call statements."""
        self.parse_identifier()
        if self.current_token and self.current_token["token"] == "MKAY":
            self.match("Input/Output", "MKAY")
        else:
            self.raise_error("'MKAY' after function call")

    def parse_loopop(self):
        try:
            self.match("Loop Operator")
        except SyntaxError as e:
            self.raise_error("Loop Operator")

    def parse_looptype(self):
        try:
            self.match("Loop Type")
        except SyntaxError as e:
            self.raise_error("Loop Type")

    def parse_logicop(self):
        try:
            self.match("Logical Operator")
            self.parse_value()
            self.parse_connector("AN")
            self.parse_value()
        except SyntaxError as e:
            self.raise_error("a valid logic operation")

    def parse_loop(self):
        """Parse loop constructs."""
        self.match("Loop Delimiter", "IM IN YR")
        self.parse_identifier()
        self.parse_loopop()
        self.parse_connector("YR")
        self.parse_identifier()
        self.parse_looptype()
        self.parse_logicop()
        while self.current_token and self.current_token["token"] != "IM OUTTA YR":
            self.parse_statement()
        self.match("Loop Delimiter", "IM OUTTA YR")
        self.parse_identifier()

    def parse_print(self):
        """Parse the <print> rule."""
        self.match("Input/Output", "VISIBLE")
        if self.current_token and self.current_token["type"] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Literal","Identifier", "Function", "Variable", "Mathematical Operator"]:
            if self.current_token["type"] == "Mathematical Operator":
                self.parse_mathop()
            else:
                self.advance()
        else:
            print("print error")
            self.raise_error("Literal or Identifier")

    def parse_control_flow(self):
        """Parse the <control_flow> rule."""
        if self.current_token["token"] == "WAZZUP":
            self.match("Control Flow", "WAZZUP")
            self.parse_statement()
            self.match("Control Flow", "BUHBYE")
        else:
            self.raise_error("a valid control flow construct")

    def parse(self):
        """Start the parsing process."""
        try:
            self.parse_program()
            print("Parsing successful!")
        except SyntaxError as e:
            print(e)


    