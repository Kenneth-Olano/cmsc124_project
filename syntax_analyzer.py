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
        if lexeme[1] == "Identifier":
            # print(lexeme)
            if len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "WILE" or loop_stack[len(loop_stack)-1] == "TIL"):
                loop_stack.append(lexeme)
            elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] != "WILE" or loop_stack[len(loop_stack)-1] != "TIL"):
                messagebox.showerror("SyntaxError", f"No loop label provided.")
                print("No loop label provided.")
                # return
            if len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] == "IM OUTTA YR") and len(loop_stack) == 6 and "IM IN YR" in loop_stack:
                loop_stack.clear()
            elif len(loop_stack) > 0 and (loop_stack[len(loop_stack)-1] != "IM OUTTA YR") and len(loop_stack) == 6 and "IM IN YR" in loop_stack:
                messagebox.showerror("SyntaxError", f"Loop not properly delimited. No 'IM OUTTA YR' detected.")
                print("Loop not properly delimited. No 'IM OUTTA YR' detected.")
                # return
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
                
                

                elif keys == "loopdelimiter":
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
                    

                elif keys == "funcdelimiter":
                    # print("function")
                    if lexeme[0] == "IM IN YR":
                        func_stack.append(lexeme[0])
                    elif lexeme[0] == "IM OUTTA YR":
                        try:
                            func_stack.pop()
                        except:    
                            messagebox.showerror("SyntaxError", f"Invalid function delimiters")
                            print("Invalid function delimiters")
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



    

    
