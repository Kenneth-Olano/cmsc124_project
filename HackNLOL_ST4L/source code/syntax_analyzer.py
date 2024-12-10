import tkinter as tk  # Import tkinter to access widget methods in the syntax analyzer

class SyntaxAnalyzer:
    def __init__(self, tokens, console_widget):
        self.tokens = tokens  # List of tokens generated by the lexical analyzer
        self.current_index = 0  # Pointer to the current token
        self.current_token = self.tokens[self.current_index] if self.tokens else None
        self.function_dict = {}
        self.console = console_widget
        self.inFunction = False

    def log_to_console(self, message):
        """Utility function to log messages to the console."""
        self.console.config(state=tk.NORMAL)  # Enable the text widget
        self.console.insert(tk.END, message + "\n")
        self.console.config(state=tk.DISABLED)  # Disable editing

    def advance(self):
        """Advance the token pointer to the next token."""
        self.current_index += 1
        self.current_token = (
            self.tokens[self.current_index] if self.current_index < len(self.tokens) else None
        )

    def skip_comment(self):
        """Skip any comments encountered during parsing."""
        while self.current_token and self.current_token["type"] == "Comment":
            self.advance()

    def match(self, token_type, expected_token=None):
        self.skip_comment()
        """Check if the current token matches the expected type and optional specific token."""
        if self.current_token and self.current_token["type"] == token_type:
            if expected_token and self.current_token["token"] != expected_token:
                self.raise_error(f"'{expected_token}'")
            else:
                self.advance()
        else:
            self.raise_error(token_type)

    def raise_error(self, expected):
        """Raise a detailed syntax error with token information."""
        if self.current_token:
            error_message = (
                f"Syntax Error: Expected {expected} but found '{self.current_token['token']}' "
                f"(type: {self.current_token['type']}) at line {self.current_token['line']} "
                f"position {self.current_token['start']}-{self.current_token['end']}."
            )
        else:
            error_message = f"Syntax Error: Expected {expected} but reached the end of the program."

        # Log the error message to the console
        self.log_to_console(error_message)

        # Stop parsing by raising an exception
        raise Exception(error_message)


    def parse_program(self):
        """Parse the <program> rule."""
        self.match("Program Delimiter", "HAI")  # Start of the program
        while self.current_token and self.current_token["token"] != "KTHXBYE":
            self.parse_toplevel()  # Parse statements within the program
        self.match("Program Delimiter", "KTHXBYE")  # End of the program
        return self.function_dict, self.tokens

    def parse_toplevel(self):
        self.skip_comment()
        """Parse the <toplevel> rule."""
        if not self.current_token:
            return

        token_type = self.current_token["type"]
        token_value = self.current_token["token"]

        if token_type == "Function Delimiter":
            self.inFunction = True
            self.parse_function()
            self.inFunction = False
        elif token_type == "Control Flow":
            self.parse_control_flow()
        elif token_type == "Switch":
            self.parse_switch()
        elif token_type == "Loop Delimiter":
            self.parse_loop()
        elif token_type == "Data Initialization":
            self.parse_initialization()
        else:
            self.parse_statement()
        
    def parse_statement(self):
        self.skip_comment()
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
        elif token_type == "Data Initialization":
            self.parse_initialization()
        elif token_type == "Mathematical Operator":
            self.parse_mathop()
        elif token_type == "Logical Operator":
            self.parse_logicop()
        elif token_type == "Variable":
            self.parse_identifier()
        elif token_type == "Function Call":
            self.parse_function_call()
        elif token_type == "Typecast" and token_type == "MAEK":
            self.parse_exp_typecast()
        else:
            self.raise_error("a valid statement")

    def parse_declaration(self):
        self.skip_comment()
        """Parse the <declaration> rule."""
        self.match("Data Declaration", "I HAS A")  # Match the "I HAS A" keyword
        self.parse_identifier()  # Expect a Variable identifier
        if self.current_token and self.current_token["token"] == "ITZ":
            # self.advance()
            self.match("Data Declaration", "ITZ")
            self.parse_value()
    def parse_control_flow(self):
        self.match("Control Flow", "O RLY?")  # Expect the "O RLY?" token (start of conditional check)
        self.match("Control Flow", "YA RLY")  # Expect the "YA RLY" token (start of true-block)
        
        # Parse the block of statements under "YA RLY"
        while self.current_token and self.current_token["token"] != "NO WAI" and self.current_token["token"] != "OIC":
            self.parse_statement()  # Parse statements in the true block
        
        # Check for "NO WAI" (if it exists), otherwise move on
        if self.current_token and self.current_token["token"] == "NO WAI":
            self.match("Control Flow", "NO WAI")  # Match the "NO WAI" token (start of the false block)
            
            # Parse the block of statements under "NO WAI"
            while self.current_token and self.current_token["token"] != "OIC":
                self.parse_statement()  # Parse statements in the false block
        
        self.match("Control Flow", "OIC")  # Match the "OIC" token (end of the control flow)


    def parse_switch(self):
        """
        Parse the 'WTF?' construct in LOLCODE for correct syntax.
        Ensures valid structure for OMG, GTFO, OMGWTF, and OIC.
        """
        self.match("Switch", "WTF?")
        has_default_case = False

        while self.current_token and self.current_token["token"] != "OIC":
            if self.current_token["token"] == "OMG":
                # Parse an individual case
                self.match("Switch", "OMG")
                self.parse_value()  # Ensure valid value follows OMG
                # Parse statements inside the case
                while self.current_token["token"] not in ["GTFO", "OMG", "OMGWTF", "OIC"]:
                    self.parse_statement()
                # Match GTFO if present
                if self.current_token["token"] == "GTFO":
                    self.match("Return Statement", "GTFO")

            elif self.current_token["token"] == "OMGWTF":
                if has_default_case:
                    self.raise_error("Multiple default cases (OMGWTF) are not allowed.")
                has_default_case = True
                self.match("Switch", "OMGWTF")
                # Parse statements inside the default case
                while self.current_token["token"] not in ["OIC"]:
                    self.parse_statement()
            
            else:
                # Raise an error for unexpected tokens
                self.raise_error(f"Unexpected token in switch: {self.current_token['token']}")

        # Ensure we end with OIC
        self.match("Control Flow", "OIC")


    def parse_identifier(self):
        self.skip_comment()
        """Parse the <identifier> rule."""
        if self.current_token and self.current_token["type"] == "Variable":
            self.advance()
            if self.current_token["type"] == "Typecast":
                self.parse_imp_typecast()
            elif self.current_token["type"] == "Assignment Operator":
                self.parse_variable_assignment()
        elif self.current_token and self.current_token["type"] == "Loop":
            self.advance()
        elif self.current_token and self.current_token["type"] == "Function":
            self.advance()
        else:
            self.raise_error("Identifier")

    def parse_imp_typecast(self):
        self.skip_comment()
        self.match("Typecast", "IS NOW A")
        self.match("LITERAL")

    def parse_exp_typecast(self):
        self.skip_comment()
        self.match("Typecast", "MAEK")
        self.match("Variable")
        self.match("LITERAL")

    def parse_value(self):
        self.skip_comment()
        """Parse the <value> rule."""
        if self.current_token and self.current_token["type"] in ["Typecast", "Concatenate", "Logical Operator", "NUMBR", "NUMBAR", "YARN", "TROOF", "Literal", "Variable" ,"Identifier", "Mathematical Operator"]:
            
            if self.current_token["type"] == "Mathematical Operator":
                self.parse_mathop()
            elif self.current_token["type"] == "Logical Operator":
                self.parse_logicop()
            elif self.current_token["type"] == "Concatenate":
                self.parse_concatenate()
            elif self.current_token["type"] == "Typecast" and self.current_token["token"] == "MAEK":
                self.parse_exp_typecast()
            elif self.current_token and self.current_token["type"] == "Variable":
                self.parse_identifier()
            else:
                self.advance()
        else:
            self.raise_error("Literal or Identifier")
    
    def parse_connector(self, connector):
        self.skip_comment()
        self.match("Connector", connector)
        return True
        

    def parse_mathop(self):
        self.skip_comment()
        try:
            self.match("Mathematical Operator")
            self.parse_value()
            self.parse_connector("AN")
            self.parse_value()
        except SyntaxError as e:
            print("mathop syntax error")
            self.raise_error("a valid Math operation")
        

    def parse_variable_assignment(self):
        self.skip_comment()
        """Parse variable assignment statements."""  # The variable being assigned
        self.match("Assignment Operator", "R")  # The assignment operator
        self.parse_value()  # The value or expression being assigned

    def parse_input(self):
        self.skip_comment()
        """Parse the <input> rule for GIMMEH."""
        self.match("Input/Output", "GIMMEH")  # Match the GIMMEH keyword
        self.parse_identifier()  # Expect an identifier to store the input

    def parse_function_call(self):
        self.skip_comment()
        """Parse function call statements."""
        self.match("Function Call")
        if self.current_token['type'] == "Variable":
            self.tokens[self.current_index]['type']= "Function"
        self.match("Function")
        while self.current_token and self.current_token["token"] in ["YR", "AN"]:
            if self.current_token["token"] == "YR":
                self.advance()
                self.parse_value()
            elif self.parse_connector("AN"):
                pass
        if self.current_token and self.current_token["token"] == "MKAY":
            self.match("Function Call", "MKAY")
        else:
            self.raise_error("'MKAY' after function call")

    def parse_function(self):
        self.skip_comment()
        """Parse function constructs."""
        self.match("Function Delimiter", "HOW IZ I")

        # Checks if there is function identifier
        if self.current_token["type"] != "Variable":
            self.raise_error("Invalid function identifier after 'HOW IZ I'")
        else:
            self.tokens[self.current_index]['type']= "Function"
            # print(self.tokens)
        self.function_dict[self.current_token['token']] = {}
        current_function =self.current_token['token']
        self.advance()

        # Parse parameters if there are any
        while self.current_token and self.current_token["token"] in ["YR", "AN"]:
            if self.current_token["token"] == "YR":
                self.advance()
                self.function_dict[current_function][self.current_token['token']] = None
                self.tokens[self.current_index]['type']= "Function Parameter"
                self.match("Function Parameter")
            elif self.parse_connector("AN"):
                pass
        
        # Ensure there are no function declarations inside and handle the statements
        return_found = False
        while self.current_token and self.current_token["token"] != "IF U SAY SO":
            if self.current_token["token"] == "HOW IZ I":
                self.raise_error("Nested function declaration found in the function body")
            if self.current_token["token"] == "FOUND YR":
                self.match("Return Statement", self.current_token["token"])
                if self.current_token["type"] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Function", "Variable"]:
                    self.advance()
                    return_found = True
                    break
                elif self.current_token["type"] == "Mathematical Operator":
                    self.parse_mathop()
                    return_found = True
                    break
                elif self.current_token["type"] == "Logical Operator":
                    self.parse_logicop()
                    return_found = True
                    break
                else:
                    self.raise_error("Valid return value")
            elif  self.current_token["token"] == "GTFO":
                self.match("Return Statement", self.current_token["token"])
                return_found = True
                break
            else:
                if self.current_token["type"] == "Variable":
                    self.current_token["type"] == "Function Parameter"
                self.parse_statement()
        
        if return_found == False:
            self.raise_error("Missing return statement ('FOUND YR' or 'GTFO') inside the function")
        self.match("Function Delimiter", "IF U SAY SO")
        
    def parse_loopop(self):
        self.skip_comment()
        try:
            self.match("Loop Operator")
        except SyntaxError as e:
            self.raise_error("Loop Operator")

    def parse_looptype(self):
        self.skip_comment()
        try:
            self.match("Loop Type")
        except SyntaxError as e:
            self.raise_error("Loop Type")

    def parse_logicop(self):
        self.skip_comment()
        try:
            self.match("Logical Operator")
            self.parse_value()
            self.parse_connector("AN")
            self.parse_value()
        except SyntaxError as e:
            self.raise_error("a valid logic operation")

    def parse_loop(self):
        self.skip_comment()
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
        self.skip_comment()
        """Parse the <print> rule."""
        current_line = self.current_token["line"]
        self.match("Input/Output", "VISIBLE")
        
        while self.current_token and self.current_token['line'] == current_line and self.current_token["type"] in ["Logical Operator", "Concatenate", "NUMBR", "NUMBAR", "YARN", "TROOF", "Literal", "Identifier", "Function", "Variable", "Mathematical Operator"]:
            if self.current_token["type"] == "Mathematical Operator":
                self.parse_mathop()
            elif self.current_token["type"] == "Logical Operator":
                self.parse_logicop()
            elif self.current_token["type"] == "Concatenate":
                self.parse_concatenate()
            elif self.current_token["type"] in ["NUMBR", "NUMBAR", "YARN", "TROOF", "Function", "Variable"]:
                self.advance()
            else:
                self.raise_error("Valid print operands")

            # Check for valid print connectors (either "AN" or "+" operator)
            if self.current_token['line'] == current_line and (self.current_token["token"] == "+" or self.current_token["token"] == "AN"):
                self.advance()  # Move to the next token if valid connector
            elif self.current_token['line'] != current_line:
                break  # Exit the loop if the line has changed
            else:
                self.raise_error("Valid print connector")

    def parse_concatenate(self):
        self.skip_comment()
        self.match("Concatenate", "SMOOSH")
        current_line = self.current_token["line"]
        while current_line == self.current_token["line"] and self.current_token["type"] in ["YARN", "Variable"]:
            self.match(self.current_token["type"])
            if current_line == self.current_token["line"]:
                self.parse_connector("AN")
            else:
                break

    def parse_initialization(self):
        self.skip_comment()
        """Parse the <control_flow> rule."""
        if self.current_token["token"] == "WAZZUP":
            self.match("Data Initialization", "WAZZUP")
            while self.current_token and self.current_token["token"] != "BUHBYE":
                self.parse_declaration()
            self.match("Data Initialization", "BUHBYE")
        else:
            self.raise_error("a valid control flow construct")

    def parse(self):
        """Start the parsing process."""
        try:
            self.parse_program()
            self.log_to_console("Parsing successful!")
        except Exception as e:
            # Log any unexpected errors
            self.log_to_console(f"Unexpected error: {e}")


    