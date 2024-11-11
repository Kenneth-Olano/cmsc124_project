import re

constructs = set(["HAI", "KTHXBYE", "WAZZUP", "BUHBYE", "BTW", "OBTW", "TLDR", "I HAS A", "ITZ", "R", "SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH OF", "EITHER OF", "WON OF", "NOT", "ANY OF", "ALL OF", "BOTH SAEM", "DIFFRINT", "SMOOSH", "MAEK", "A", "IS NOW A", "VISIBLE", "GIMMEH", "O RLY?", "YA RLY", "MEBBE", "NO WAI", "OIC", "WTF?", "OMG", "OMGWTF", "IM IN YR", "UPPIN", "NERFIN", "YR", "TIL", "WILE", "IM OUTTA YR", "HOW IZ I", "IF U SAY SO", "GTFO", "FOUND YR", "I IZ", "MKAY"])
literal_rules = [r"\s-?[0-9]+\s", r"\s-?[0-9]*\.?[0-9]+?\s", r'\s\".*\"', r"(WIN|FAIL)\s", r"\s(TROOF|NOOB|NUMBR|NUMBAR|YARN|TYPE)\s"]
keyword_rules = r"[A-Z][A-Z '?]*\s?"

def get_file():
    lol_file = open('file.lolcode', 'r')
    lexemes = {"literals":[], "identifiers":[], "keywords":[]}
    for i in lol_file:
        tokenize_line(i, lexemes)
    print(lexemes)

def tokenize_line(line, lexemes):
    keywords = re.findall(keyword_rules, line)
    # print(keywords)
    for i in constructs:
        for j in keywords:
            # print(j)
            if i in j:
                # print(i)
                lexemes["keywords"].append(i)
    
    for i in literal_rules:
        literal = re.findall(i, line)
        for lit in literal:
            lexemes["literals"].append(lit)
    
    identifiers = re.findall(r"[a-zA-Z][a-zA-Z0-9_]*\n", line)
    for i in identifiers:
        isLiteral = False
        for j in literal_rules:
            if re.match(j, i):
                isLiteral = True
                break
        if isLiteral == False and i[:len(i)-1] not in constructs:
            lexemes["identifiers"].append(i[:len(i)-1])


    
    # tokens = line
    # line_len = len(tokens)-1
    # i = 0
    
    # while i < line_len:
    #     start_quote = -1
    #     end_quote = -1
    #     if tokens[i] == "\"" and start_quote == -1:
    #         start_quote = i
    #         for j in range(i+1, len(tokens)):
    #             if tokens[j] == "\"":
    #                 end_quote = j+1
    #                 break
    #         if start_quote != -1 and end_quote != -1:
    #             lexemes["literals"].append(tokens[start_quote:]+tokens[:end_quote])
    #             tokens = tokens[:start_quote] + tokens[end_quote:]
    #             i = end_quote
    #             continue
    #     i+=1
    # tokens.split()
    # categorize_line(line, lexemes)

# def categorize_token(token):
#     if token in constructs:
#         return 2
#     else:
#         for i in literal_rules:
#             isLiteral = re.match(i, token)
#             if isLiteral != None:
#                 break
#         if isLiteral != None:
#             return 3
#         elif re.match(r"^([a-zA-Z])[a-zA-Z0-9_]*$", token): #is identifier
#             return 1
#         else:
#             return 0


# def categorize_line(line, lexemes):
#     category = categorize_token(i) #return 1 if identifier, return 2 if literal, if return 3 if keyword
#     match category:
#         case 1:
#             lexemes["identifiers"].append(i)
#         case 2:
#             lexemes["literals"].append(i)
#         case 3:
#             lexemes["keywords"].append(i)
#         case _:
#             print(i)
#             print("ERROR! Illegal character detected.")
        
            
get_file()

    


