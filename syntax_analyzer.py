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
        "ifelse": ("O RLY?", "YA RLY", "NO WAI", "OIC"),
        "return": ('FOUND YR', 'GTFO'),
        "concat": ("SMOOSH"),
        "input": ("GIMMEH"),
        "print": ("VISIBLE"),
        "valconnect": ("AN"),
        "assignment": ("varident R value"),
        "value": ("literal", "varident", "funcident"),
        "toplvl": ("funcdelimiter", "expr", "toplvl"),
        "expr": ("expr newline expr", 
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
    # count = 0
    for lexeme in lexemes:
        # print(lexeme)
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
                            messagebox.showerror("Error", f"Invalid program delimiters")
                            print("Invalid program delimiters")
                            return



                # Function delimiter
                elif keys == "funcdelimiter":
                    # print("function")
                    # Function declaration
                    if lexeme[0] == "HOW IZ I":
                        # Check if a function declaration is already open
                        if func_stack and func_stack[-1] == lexeme[0]:
                            messagebox.showerror("SyntaxError", f"Nested function declarations are not allowed")
                            print("Error: Nested function declarations")
                            return
                        # Push "HOW IZ I" to the stack and validate the next lexeme
                        func_stack.append(lexeme[0])

                    elif lexeme[0] == "IF U SAY SO":
                        # Checks if the latest function declaration matches with the "IF U SAY SO"
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
                    if lexeme[0] == "OIC":
                        try:
                            ifelse_stack.pop()
                        except:
                            messagebox.showerror("Error", f"Invalid if-else delimiters")
                            print("Invalid if-else delimiters")
                            return

    if(len(program_stack) == 0):
        print("> VALID PROGRAM DELIMITERS")
    else:
        print("Invalid program delimiters")

    if(len(ifelse_stack) == 0):
        print("> VALID IF ELSE")
    else:
        print("Invalid if else delimiters")
    
    if(len(func_stack) == 0):
        print("> VALID IF ELSE")
    else:
        print("Invalid function delimiters")



    

    
