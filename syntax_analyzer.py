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




                elif keys == "funcdelimiter":
                    # print("function")
                    if lexeme[0] == "IM IN YR":
                        func_stack.append(lexeme[0])
                    elif lexeme[0] == "IM OUTTA YR":
                        try:
                            func_stack.pop()
                        except:    
                            messagebox.showerror("Error", f"Invalid function delimiters")
                            print("Invalid function delimiters")
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



    

    
