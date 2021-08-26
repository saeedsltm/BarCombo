import pandas as pn
pn.set_option('mode.chained_assignment', None)

# Modified Version of itertools.product
def product(args):
    pools = [tuple(pool) for pool in args]
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

# Calculate Bar Combinations and Inserting in DF
def makeCombo(df, bars, values, eq_name):   
    c = len(df)
    cc = 1
    for (b, v) in zip(bars, values):
        df.loc[c] = [None]*len(df.keys())
        for (bb, vv) in zip(b, v):
            df[bb][c] = vv
        df = df.rename(index={c:"%s-%d"%(eq_name,cc)})
        c+=1; cc+=1
    return df

# Define All Bar Names for ASD           
barsDic = {
    "DL":[1],
    "SDL":[1],
    "WALL":[1],
    "LL1":[1],
    "LL2":[1],
    "LLPAR":[1],
    "LLR":[1],
    "PS0":[1],
    "PSE":[1.4],
    "EX":[1.4],
    "EXP":[1.4],
    "EXN":[1.4],
    "EY":[1.4],
    "EYP":[1.4],
    "EYN":[1.4],
    "EV":[0.3],
    "WXP":[1.4],
    "WYP":[1.4],
    "Wi+":[1.4],
    "Wi-":[1.4],
    "+T30":[0.2],
    "-T30":[0.2]   
    }

def getASD(orderedBars, apply_30_flag, NL_flag, AI=None):
    # Create a New DataFrame
    df = pn.DataFrame(columns=list(barsDic.keys()))
    # Combo: 1
    validBars = ["DL", "SDL", "WALL", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]
    df = makeCombo(df, product(bars), product(vals), "1")
    # Combo: 2
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]       
    df = makeCombo(df, product(bars), product(vals), "2")
    # Combo: 3
    validBars = ["DL", "SDL", "WALL", "LLR", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    df = makeCombo(df, product(bars), product(vals), "3")
    # Combo: 4
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [0.75]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [0.75]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [0.75]    
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.75]    
    df = makeCombo(df, product(bars), product(vals), "4")
    # Combo: 5
    validBars = ["DL", "SDL", "WALL", "PS0", "WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [1.0, 1.0]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [1.0, 1.0]; bars.remove(['Wi-'])
    df = makeCombo(df, product(bars), product(vals), "5")
    # Combo: 6
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", "WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [0.75]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [0.75]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [0.75]
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.75]        
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [0.75, 0.75]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [0.75, 0.75]; bars.remove(['Wi-'])
    df = makeCombo(df, product(bars), product(vals), "6")
    # Combo: 7
    for j in [0.7, -0.7]:
        for i in ["EX", "EXP", "EXN"]:
            validBars = ["DL", "SDL", "WALL", "PS0", i, "EY", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if apply_30_flag and ("EY" and "EY" in orderedBars): indx = bars.index(['EY']); bars[indx] = ["EY", "EY"]; vals[indx] = [0.7, -0.7]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL"]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV"]; vals[indx] = [0.7, -0.7]
            df = makeCombo(df, product(bars), product(vals), "7")
        for i in ["EY", "EYP", "EYN"]:
            validBars = ["DL", "SDL", "WALL", "PS0", i, "EX", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if apply_30_flag and ("EX" and "EX" in orderedBars): indx = bars.index(['EX']); bars[indx] = ["EX", "EX"]; vals[indx] = [0.7, -0.7]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL"]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV"]; vals[indx] = [0.7, -0.7]
            df = makeCombo(df, product(bars), product(vals), "7")
    # Combo: 8
    for j in [0.525, -0.525]:
        for i in ["EX", "EXP", "EXN"]:
            validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", i, "EY", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]
            if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [0.75]
            if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [0.75]
            if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [0.75]
            if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.75]        
            if apply_30_flag and ("EY" and "EY" in orderedBars): indx = bars.index(['EY']); bars[indx] = ["EY", "EY"]; vals[indx] = [0.525, -0.525]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL"]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV"]; vals[indx] = [0.525, -0.525]
            df = makeCombo(df, product(bars), product(vals), "8")
        for i in ["EY", "EYP", "EYN"]:
            validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", i, "EX", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]
            if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [0.75]
            if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [0.75]
            if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [0.75]
            if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.75]                    
            if apply_30_flag and ("EX" and "EX" in orderedBars): indx = bars.index(['EX']); bars[indx] = ["EX", "EX"]; vals[indx] = [0.525, -0.525]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL",]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV",]; vals[indx] = [0.525, -0.525]
            df = makeCombo(df, product(bars), product(vals), "8")
    # Combo: 9
    validBars = ["DL", "SDL", "WALL", "PS0", "WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.6]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.6]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.6]     
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [1.0, 1.0]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [1.0, 1.0]; bars.remove(['Wi-'])
    df = makeCombo(df, product(bars), product(vals), "9")
    # Combo: 10
    for j in [0.7, -0.7]:
        for i in ["EX", "EXP", "EXN"]:
            validBars = ["DL", "SDL", "WALL", "PS0", i, "EY", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.6]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.6]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.6]             
            if apply_30_flag and ("EY" and "EY" in orderedBars): indx = bars.index(['EY']); bars[indx] = ["EY", "EY"]; vals[indx] = [0.7, -0.7]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL"]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV"]; vals[indx] = [0.7, -0.7]
            df = makeCombo(df, product(bars), product(vals), "10")
        for i in ["EY", "EYP", "EYN"]:
            validBars = ["DL", "SDL", "WALL", "PS0", i, "EX", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.6]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.6]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.6]                         
            if apply_30_flag and ("EX" and "EX" in orderedBars): indx = bars.index(['EX']); bars[indx] = ["EX", "EX"]; vals[indx] = [0.7, -0.7]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL"]; vals[indx] = [1+AI, 1-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV"]; vals[indx] = [0.7, -0.7]
            df = makeCombo(df, product(bars), product(vals), "10")
    # Add Notional Bar
    if NL_flag:
        df["NL"] = [None for _ in range(len(df))]
        c = len(df)
        for i in range(len(df)):
            df.loc[len(df)] = df.iloc[i]
            df.at[df.index[i+c], "NL"] = 0.05
            df = df.rename(index={i+c:"N"+df.index[i]})      
    return df
    
#_________ASD
##orderedBars = ["DL", "SDL", "WALL","LL1", "LL2", "LLPAR", "LLR", "PS0", "WXP", "WYP", "Wi+", "Wi-", "EX", "EY", "EXP", "EYP", "EXN", "EYN", "EV", "+T30", "-T30"]
##df= getASD(orderedBars, True, True, None)
##df.to_excel("test.xls")

#===========================================================
        
#Define All Bar Names for LRFD           
barsDic = {
    "DL":[1.4],
    "SDL":[1.4],
    "WALL":[1.4],
    "LL1":[1.6],
    "LL2":[1.6],
    "LLPAR":[1.6],
    "LLR":[0.5],
    "PS0":[1.6],
    "PSE":[1.4],
    "EX":[1.4],
    "EXP":[1.4],
    "EXN":[1.4],
    "EY":[1.4],
    "EYP":[1.4],
    "EYN":[1.4],
    "EV":[0.3],
    "WXP":[1.4],
    "WYP":[1.4],
    "Wi+":[1.6],
    "Wi-":[1.6],
    "+T30":[0.2],
    "-T30":[0.2]    
    }

def getLRFD(orderedBars, apply_30_flag, NL_flag, AI=None):
    # Create a New DataFrame
    df = pn.DataFrame(columns=list(barsDic.keys()))
    # Combo: 1
    validBars = ["DL", "SDL", "WALL"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]
    df = makeCombo(df, product(bars), product(vals), "1")
    # Combo: 1-1
    validBars = ["DL", "SDL", "WALL", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "PS0" in orderedBars: indx = bars.index(['PS0']); bars[indx] = ["PS0", "PS0"]; vals[indx] = [0.9, 1.6]
    df = makeCombo(df, product(bars), product(vals), "1-1")
    # Combo: 2
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1.6]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1.6]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1.6]
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.5]
    if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]    
    df = makeCombo(df, product(bars), product(vals), "2")
    # Combo: 3
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1]    
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [1.6]    
    if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]
    df = makeCombo(df, product(bars), product(vals), "3")   
    # Combo: 3-1
    validBars = ["DL", "SDL", "WALL", "LLR", "PS0", "WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [0.8, 0.8]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [0.8, 0.8]; bars.remove(['Wi-'])
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [1.6]    
    if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]
    df = makeCombo(df, product(bars), product(vals), "3-1")
    # Combo: 4
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR","WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1]
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.5]        
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [1.6, 1.6]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [1.6, 1.6]; bars.remove(['Wi-'])
    df = makeCombo(df, product(bars), product(vals), "4")
    # Combo: 5
    for j in [1, -1]:
        for i in ["EX", "EXP", "EXN"]:
            validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", i, "EY", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
            if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1]
            if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1]
            if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1]
            if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.5]
            if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if apply_30_flag and ("EY" and "EY" in orderedBars): indx = bars.index(['EY']); bars[indx] = ["EY", "EY",]; vals[indx] = [0.3, -0.3]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL",]; vals[indx] = [1.2+AI, 1.2-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV",]; vals[indx] = [1, -1]
            df = makeCombo(df, product(bars), product(vals), "5")
        for i in ["EY", "EYP", "EYN"]:
            validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", i, "EX", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
            if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1]
            if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1]
            if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1]
            if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.5]
            if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if apply_30_flag and ("EX" and "EX" in orderedBars): indx = bars.index(['EX']); bars[indx] = ["EX", "EX",]; vals[indx] = [0.3, -0.3]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL",]; vals[indx] = [1.2+AI, 1.2-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV",]; vals[indx] = [1, -1]
            df = makeCombo(df, product(bars), product(vals), "5")
    # Combo: 6
    validBars = ["DL", "SDL", "WALL", "WXP", "WYP", "Wi+", "Wi-"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.9]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.9]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.9]
    if "WXP" and "WYP" in orderedBars: indx = bars.index(['WXP']); bars[indx] = ["WXP", "WYP"]; vals[indx] = [1.6, 1.6]; bars.remove(['WYP'])
    if "Wi+" and "Wi-" in orderedBars: indx = bars.index(['Wi+']); bars[indx] = ["Wi+", "Wi-"]; vals[indx] = [1.6, 1.6]; bars.remove(['Wi-'])
    df = makeCombo(df, product(bars), product(vals), "6")
    # Combo: 7
    for j in [1, -1]:
        for i in ["EX", "EXP", "EXN"]:
            validBars = ["DL", "SDL", "WALL", i, "EY", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.9]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.9]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.9]
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if "EY" and "EY" in orderedBars: indx = bars.index(['EY']); bars[indx] = ["EY", "EY",]; vals[indx] = [0.3, -0.3]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL",]; vals[indx] = [0.9+AI, 0.9-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV",]; vals[indx] = [1, -1]
            df = makeCombo(df, product(bars), product(vals), "7")
        for i in ["EY", "EYP", "EYN"]:
            validBars = ["DL", "SDL", "WALL", i, "EX", "EV"]
            bars = [[i] for i in orderedBars if i in validBars]
            vals = [barsDic[i] for i in orderedBars if i in validBars]    
            if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [0.9]
            if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [0.9]
            if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [0.9]
            if i in orderedBars: indx = bars.index([i]); vals[indx] = [j]   
            if "EX" and "EX" in orderedBars: indx = bars.index(['EX']); bars[indx] = ["EX", "EX",]; vals[indx] = [0.3, -0.3]
            if AI:
                if "EV" in orderedBars: indx = bars.index(['DL']); bars[indx] = ["DL", "DL",]; vals[indx] = [0.9+AI, 0.9-AI]; bars.remove(['EV'])
            else:
                if "EV" in orderedBars: indx = bars.index(['EV']); bars[indx] = ["EV", "EV",]; vals[indx] = [1, -1]
            df = makeCombo(df, product(bars), product(vals), "7")
    # Combo: 8
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", "+T30", "-T30"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [0.5]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [0.5]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [0.5]
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [0.5]
    if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]    
    if "+T30" in orderedBars: indx = bars.index(['+T30']); bars[indx] = ["+T30", "-T30"]; vals[indx] = [1.2, 1.2]; bars.remove(['-T30'])
    df = makeCombo(df, product(bars), product(vals), "8")
    # Combo: 9
    validBars = ["DL", "SDL", "WALL", "LL1", "LL2", "LLPAR", "LLR", "PS0", "+T30", "-T30"]
    bars = [[i] for i in orderedBars if i in validBars]
    vals = [barsDic[i] for i in orderedBars if i in validBars]    
    if "DL" in orderedBars: indx = bars.index(['DL']); vals[indx] = [1.2]
    if "SDL" in orderedBars: indx = bars.index(['SDL']); vals[indx] = [1.2]
    if "WALL" in orderedBars: indx = bars.index(['WALL']); vals[indx] = [1.2]
    if "LL1" in orderedBars: indx = bars.index(['LL1']); vals[indx] = [1.6]
    if "LL2" in orderedBars: indx = bars.index(['LL2']); vals[indx] = [1.6]
    if "LLPAR" in orderedBars: indx = bars.index(['LLPAR']); vals[indx] = [1.6]
    if "LLR" in orderedBars: indx = bars.index(['LLR']); vals[indx] = [1.6]
    if "PS0" in orderedBars: indx = bars.index(['PS0']); vals[indx] = [1.6]        
    if "+T30" in orderedBars: indx = bars.index(['+T30']); bars[indx] = ["+T30", "-T30"]; vals[indx] = [1, 1]; bars.remove(['-T30'])
    df = makeCombo(df, product(bars), product(vals), "9")
    # Add Notional Bar
    if NL_flag:
        df["NL"] = [None for _ in range(len(df))]
        c = len(df)
        for i in range(len(df)):
            df.loc[len(df)] = df.iloc[i]
            df.at[df.index[i+c], "NL"] = 0.05
            df = df.rename(index={i+c:"N"+df.index[i]})
    return df

#_________LRFD

##orderedBars = ["DL", "SDL", "WALL","LL1", "LL2", "LLPAR", "LLR", "PS0", "WXP", "WYP", "Wi+", "Wi-", "EX", "EY", "EXP", "EYP", "EXN", "EYN", "EV", "+T30", "-T30", "NL"]
##df= getLRFD(orderedBars, True, True, None)
##df.to_excel("test.xls")

# LRFD-AMPLIFIED    
def getLRFD_AMP(orderedBars, apply_30_flag, NL_flag, omega, omega_x_flag, omega_y_flag, AI=None):
    bars = []
    if omega and omega_x_flag:
        bars = ["EX", "EXP", "EXN"]
    if omega and omega_x_flag and omega_y_flag:
        bars = ["EX", "EY", "EXP", "EYP", "EXN", "EYN"]
    df = getLRFD(orderedBars, apply_30_flag, NL_flag)
    for i in range(len(df)):
        for b in bars:
            if df.iloc[i][b]: df.iloc[i][b] *= omega
    return df

##orderedBars = ["DL", "SDL", "WALL","LL1", "LL2", "LLPAR", "LLR", "PS0", "WXP", "WYP", "Wi+", "Wi-", "EX", "EY", "EXP", "EYP", "EXN", "EYN", "EV", "+T30", "-T30"]
##df= getLRFD_AMP(orderedBars, True, True, 2.5, None)
##df.to_excel("test.xls")
