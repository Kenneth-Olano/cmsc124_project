from tkinter import messagebox

def syntax_analyzer(lexemes):
    constructs = {
        "programdelimiter":("HAI", "KTHXBYE"),
        "initialize": ("WAZZUP", "BUHBYE"),
        "typecast": ("MAEK", "A", "IS NOW A"),
        "declaration": ("I HAS A", "ITZ"),
        "comparison":("BOTH SAEM", "DIFFRINT"),
        "arithmetic":('SUM OF','DIFF OF','PRODUKT OF', 'QUOSHUNT OF', 'MOD OF', 'BIGGR OF', 'SMALLR OF'),
        "literal": ('NUMBR', 'NUMBAR', 'YARN', 'TROOF', 'NOOB'),
        "boolean": ('BOTH OF', 'EITHER OF', 'WON OF', 'NOT'),
        "infboolean": ('ALL OF', 'ANY OF'),
        "loopdelimiter" : ('IM IN YR', 'IM OUTTA YR', 'YR', 'TIL', 'WILE'),
        "loopop": ('UPPIN', 'NERFIN'),
        "funcdelimiter": ('HOW IZ I', 'IF U SAY SO'),
        "funccall": ('I IZ', 'MKAY'),
        "funcparam": ('YR', 'AN'),
        "switch": ("WTF?", "OMGWTF", "OIC"),
        "case": ("OMG", "GTFO"),
        "ifelse": ("O RLY", "YA RLY", "NO WAI", "OIC"),
        "return": ('FOUND YR', 'GTFO'),
        "concat": ("SMOOSH"),
        "input": ("GIMMEH"),
        "print": ("VISIBLE"),
        "valconnect": ("AN"),
        "assignment": ("R"),
        "value": ("literal", "varident", "funcident"),
        "toplvl": ("funcdelimiter", "expr", "toplvl"),
        "expr": ("expr", 
                "print",
                "arithmetic",
                "boolean",
                "infboolean",
                "assignment",
                "comparison",
                "switch",
                "ifelse",
                "loopdelimiter",
                "input",
                "concat",
                "typecast",
                "funccall",
                "return",
                ""),
        "newline": "\n"
    }
    program_stack = []
    func_stack = []
    ifelse_stack = []
    initialize_stack = []
    loop_stack = []
    count = 0
    for lexeme in lexemes: 
        # print(lexeme)
        if lexeme[1] == "Identifier": #WILL BE CHANGED TO "LoopIdentifier" once specified
            # print(lexeme)
            if len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1][1] == "Identifier"):
                pass
            else:
                if len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "WILE" or loop_stack[len(loop_stack)-1] == "TIL"):
                    loop_stack.append(lexeme)
                elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "IM OUTTA YR") and len(loop_stack) == 6 and "IM IN YR" in loop_stack:
                    loop_stack.clear()
                elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] != "WILE" or loop_stack[len(loop_stack)-1] != "TIL"):
                    messagebox.showerror("SyntaxError", f"No loop label provided.")
                    print(lexeme)
                    print("No loop label provided.")
                    return
                elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] != "IM OUTTA YR") and len(loop_stack) == 6 and "IM IN YR" in loop_stack:
                    messagebox.showerror("SyntaxError", f"Loop not properly delimited. No 'IM OUTTA YR' detected.")
                    print("Loop not properly delimited. No 'IM OUTTA YR' detected.")
                    return
        for keys in constructs.keys():
            if lexeme[0] in constructs[keys]:
                if keys == "programdelimiter":
                    # print("delimiter")
                    if lexeme[0] == "HAI":
                        program_stack.append(lexeme[0])
                    elif lexeme[0] == "KTHXBYE":
                        try:
                            program_stack.pop()
                        except:    
                            messagebox.showerror("SyntaxError", f"Invalid program delimiters")
                            print("Invalid program delimiters")
                            return

            
                elif keys == "initialize":
                    if lexeme[0] == "WAZZUP":
                        initialize_stack.append(lexeme[0])
                    elif lexeme[0] == "BUHBYE":
                        try:
                            initialize_stack.pop()
                        except:    
                            messagebox.showerror("SyntaxError", f"Invalid syntax for variable initialization. BUHBYE before WAZZUP.")
                            print("Invalid variable initialization delimiters")
                            return
                
                

                elif keys == "loopdelimiter": #HAS TO BE REVISED ONCE TOKENS ARE FIXED AND APPENDED IN SEQUENCE
                    if lexeme[0] == "IM IN YR":
                        loop_stack.append(lexeme[0])
                    elif lexeme[0] == "YR":
                        if loop_stack[len(loop_stack)-1] in constructs["loopop"]:
                            loop_stack.append(lexeme[0])
                        else:
                            messagebox.showerror("SyntaxError", f"No loop operation provided.")
                            print("No loop operation provided.")
                            return
                    elif lexeme[0] == "TIL" or lexeme[0] == "WILE":
                        if loop_stack[len(loop_stack)-1] == "YR":
                            loop_stack.append(lexeme[0]) 
                    elif lexeme[0] == "IM OUTTA YR":
                        loop_stack.append(lexeme[0])
                        
                    
                        # if len(loop_stack) > 0 and loop_stack[len(loop_stack)-1] == "YR":
                        #     loop_stack.append(lexeme)
                        # if len(loop_stack) > 0 and loop_stack[len(loop_stack)-1] == "IM OUTTA YR":
                        #     if len(loop_stack) == 7:
                        #         loop_stack.clear()

                elif keys == "loopop":
                    if (lexeme[0] == "UPPIN" or lexeme[0] == "NERFIN") and loop_stack[len(loop_stack)-1] == "IM IN YR": 
                        loop_stack.append(lexeme[0])
                    

                # Function delimiter
                elif keys == "funcdelimiter":
                    # print("function")
                    # Function declaration
                    if lexeme[0] == "HOW IZ I":
                        if func_stack and func_stack[-1] == lexeme[0]:
                            messagebox.showerror("SyntaxError", f"Nested function declarations are not allowed")
                            print("Error: Nested function declaration")
                            return
                        
                        # Push 'HOW IZ I' to the stack
                        func_stack.append(lexeme[0])
                    elif lexeme[0] == "IF U SAY SO":
                        # Checks if the latest function declaration has a matching 'IF U SAY SO'
                        if func_stack and func_stack[-1] == lexeme[0]:
                            func_stack.pop()
                        else:    
                            messagebox.showerror("SyntaxError", f"'IF U SAY SO' has no matching 'HOW IZ I'")
                            print("Error: Unmatched 'IF U SAY SO'")
                            return

                elif keys == "ifelse":
                    # print("ifelse")
                    if lexeme[0] == "O RLY":
                        ifelse_stack.append(lexeme[0])
                    elif lexeme[0] == "YA RLY": #if YA RLY is encountered
                        if "O RLY" not in ifelse_stack: #check if it is enclosed in an O RLY clause
                            messagebox.showerror("SyntaxError", f"YA RLY imposed with imposing O RLY first.")
                            return
                        else: #push to stack
                            ifelse_stack.append(lexeme[0])
                    elif lexeme[0] == "NO WAI": #when NO WAI is encoutered
                        error_string = ""
                        if "O RLY" not in ifelse_stack: #check if it is enclosed by an O RLY clause
                            error_string+= "NO WAI imposed with imposing O RLY first.\n"
                        if "YA RLY" not in ifelse_stack: #also check if NO WAI is preceeded by a YA RLY clase
                            error_string += "NO WAI imposed with imposing YA RLY first."
                        if len(error_string) != 0:
                            messagebox.showerror("SyntaxError", error_string)
                            return
                    elif lexeme[0] == "OIC": #if OIC is encountered
                        try:
                            if ifelse_stack[len(ifelse_stack)-1] == "YA RLY": #the top of stack should always be YA RLY when OIC is encountered, pop 2x if so
                                ifelse_stack.pop()
                                ifelse_stack.pop()
                        except:
                            messagebox.showerror("SyntaxError", f"OIC Keyword: Invalid if-else delimiters")
                            print("OIC Invalid if-else delimiters")
                            return
                count+=1
                # print(lexeme)
                print(loop_stack)
                
    if(len(program_stack) == 0):
        print("> VALID PROGRAM DELIMITERS")
    else:
        print("Invalid program delimiters")

    if(len(initialize_stack) == 0):
        print("> VALID INITIALIZATION DELIMITERS")
    else:
        print("Invalid initialization section delimiters")

    if (len(loop_stack) == 0):
        print("> VALID LOOP")
    else:
        print("Invalid loop syntax")

    if(len(ifelse_stack) == 0):
        print("> VALID IF ELSE")
    else:
        print("Invalid if else delimiters")
    
    if(len(func_stack) == 0):
        print("> VALID IF ELSE")
    else:
        print("Invalid function delimiters")



"""" class SyntaxAnalyzer:
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
        elif token_type == "Identifier":
            if self.current_token["token"] == "IM IN YR":
                self.parse_loop()
            else:
                self.parse_variable_assignment()
        else:
            self.raise_error("a valid statement")

    def parse_declaration(self):
        """Parse the <declaration> rule."""
        self.match("Data Declaration")  # Match the "I HAS A" keyword
        self.parse_identifier()  # Expect a Variable identifier
        if self.current_token and self.current_token["token"] == "ITZ":
            self.match("Data Declaration", "ITZ")
            self.parse_value()

    def parse_identifier(self):
        """Parse the <identifier> rule."""
        if self.current_token and self.current_token["type"] == "Identifier":
            self.advance()
        else:
            self.raise_error("Identifier")

    def parse_value(self):
        """Parse the <value> rule."""
        if self.current_token and self.current_token["type"] in ["Literal", "Identifier"]:
            self.advance()
        else:
            self.raise_error("Literal or Identifier")

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

    def parse_loop(self):
        """Parse loop constructs."""
        self.match("Control Flow", "IM IN YR")
        self.parse_identifier()
        while self.current_token and self.current_token["token"] != "IM OUTTA YR":
            self.parse_statement()
        self.match("Control Flow", "IM OUTTA YR")

    def parse_print(self):
        """Parse the <print> rule."""
        self.match("Input/Output", "VISIBLE")
        if self.current_token and self.current_token["type"] in ["Literal", "Identifier"]:
            self.advance()
        else:
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
"""

    