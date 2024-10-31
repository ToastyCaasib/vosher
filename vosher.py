import sys, re
from phonemizer import phonemize
from phonemizer.backend.espeak.wrapper import EspeakWrapper
EspeakWrapper.set_library("C:\Program Files\eSpeak NG\libespeak-ng.dll")

#Phoneme to Vosh Character dictionary
voshDict = {
    "b":":vosh14:",     #1 X -> 14
    "d":":vosh12:",     #2 X -> 12
    "f":":vosh21:",     #3 X -> 21
    "g":":vosh16:",     #4 X -> 16
    "ɡ":":vosh16:",
    "h":":vosh28:",     #5 X -> 28
    "dʒ":":vosh18:",    #6 ~ -> 18
    "k":":vosh15:",     #7 ? -> 15
    "l":":vosh29:",     #8 X -> 29
    "m":":vosh27:",     #9 X -> 27
    "n":":vosh30:",     #10 X -> 30
    "p":":vosh13:",     #11 X -> 13
    "r":":vosh06:",     #12 X -> 06
    "ɹ":":vosh06:",
    "ɚ":":vosh06:",
    "s":":vosh19:",     #13 X -> 19
    "t":":vosh11:",     #14 X -> 11
    "v":":vosh22:",     #15 X -> 22
    "w":":vosh10:",     #16 ? -> 05
    "z":":vosh20:",     #17 X -> 20
    "ʒ":":vosh18:",     #18 ~ -> 18
    "tʃ":":vosh17:",    #19 X -> 17
    "ʃ":":vosh23:",     #20 X -> 23
    "θ":":vosh25:",     #21 X -> 25
    "ð":":vosh26:",     #22 X -> 26
    "ŋ":":vosh16:",     #23 X -> 16
    "j":":vosh18:",     #24 X -> 18
    "æ":":vosh01:",     #25 X -> 01
    "eɪ":":vosh07:",    #26 X -> 07
    "ɛ":":vosh02:",     #27 X -> 02
    "iː":":vosh08:",    #28 X -> 08
    "ɪ":":vosh03:",     #29 X -> 03
    "aɪ":":vosh01::vosh08:",    #30 X -> 04+08
    "ɒ":":vosh05:",     #31 X -> 05
    "ɐ":":vosh07:",      #   X -> 07
    "oʊ":":vosh09:",    #32 X -> 09
    "ʊ":":vosh10:",     #33 ? -> "oo" 10?
    "ʌ":":vosh05:",     #34 X -> 05
    "uː":":vosh10:",    #35 X -> 10
    "ɔɪ":":vosh09::vosh08:",    #36 ? -> 09+08 "Oi!"
    "aʊ":":vosh01::vosh09:",    #37 ? -> "Ow"
    "ə":":vosh10:",     #38 X -> 10
    "eəʳ":":vosh01:",   #39 ? -> 
    "ɑː":":vosh04:",    #40 X -> 04
    "ɜː":":vosh06:",   #41 X -> 6
    "ɔː":":vosh19:",    #42 X -> 19
    "ɔ":":vosh04:",      # X -> 04 wrOng
    "ɪəɾ":":vosh07:",   #43 ~ -> 07
    "ʊəʳ":":vosh01:",   #44 ?
    "oː":":vosh09:",
    "ᵻ":":vosh02:",
    " ":":vosh00:"      #Space
}

def vosh(string): #Converts English text to Vosh Character String 
    #Phonemize String
    string = phonemize(string).strip()
    print(string)
    #Look up character sets in dict
    twoChar = {"d","e","ɑ","t","i","a","o","u","ɔ","ɜ"}
    threeChar = {"ɪ","r","e","ʊ"}
    ignore = {".",",","?","!"}
    voshed = ""
    vosh = ""
    cur = 0
    while cur < len(string):
        segment=string[cur]
        if segment in ignore:
            vosh = segment
            cur+=1 #Move to next
        #If Character in 3, Check next 3
        elif segment in threeChar and string[cur:(cur+3)] in voshDict.keys():
            segment=string[cur:(cur+3)]
            #print(f"Three Chars: \"{segment}\"")
            vosh = str(voshDict.get(segment))
            cur +=3 #Skip used characters
        #If Charcter in 2, Check 2
        elif segment in twoChar and string[cur:(cur+2)] in voshDict.keys():
            segment=string[cur:(cur+2)]
            #print(f"Two Chars: \"{segment}\"")
            vosh = str(voshDict.get(segment))
            cur +=2 #Skip used characters
        #Else, treat as one
        else: 
            vosh = str(voshDict.get(segment))
            cur+=1 #Move to next
        voshed += vosh #Assemble voshed string
        
    return voshed

washDict = {
    ":vosh00:":" ",
    ":vosh01:":"a",#Short Vowels
    ":vosh02:":"e",
    ":vosh03:":"i",
    ":vosh04:":"o",
    ":vosh05:":"u",
    ":vosh06:":"r",
    ":vosh07:":"ay",#Long Vowels
    ":vosh08:":"ee",
    ":vosh09:":"oh",
    ":vosh10:":"ou",
    ":vosh11:":"t",#Short Con
    ":vosh12:":"d",
    ":vosh13:":"p",
    ":vosh14:":"b",
    ":vosh15:":"k",
    ":vosh16:":"g",
    ":vosh17:":"ch",
    ":vosh18:":"jh",
    ":vosh19:":"s",#Long Con
    ":vosh20:":"z",
    ":vosh21:":"f",
    ":vosh22:":"v",
    ":vosh23:":"sh",
    ":vosh24:":"zh",
    ":vosh25:":"th",
    ":vosh26:":"th", #tvh
    ":vosh27:":"m",#Extra
    ":vosh28:":"h",
    ":vosh29:":"L",
    ":vosh30:":"n",
    ":vosh31:":"God",
}

def sanitize(string):#Remove Discord Artifacts
    return re.sub(r"<|\d+>\s?","",string)

def wash(string): #Converts Vosh Character String to Human readable text
    washed = ""
    #Translate each Vosh character backwards from Vosh Dict
    #Assemble wahsed string
    for char in washDict.keys():
        string = str.replace(sanitize(string),char,washDict[char])
    return string

def main():
    if len(sys.argv) < 2:
        #Do Menu Verson
        print("Choose an Option:")
        print("Format: V/W \"Text Here\"")
        print("(W)ash - Convert Vosh to Human Readable Text")
        print("(V)osh - Convert English Text to Vosh Characters")
        print("(Q)uit - Exit the program")
        while True:
            string = input()
            cmd=str.upper(string[0])
            string=string[2:]#Keep rest of string
            print()#Break
            if cmd == "W":
                print(f"Washed String: {wash(string)}")
            elif cmd == "V":
                print(f"Voshed String: {vosh(string)}") 
            elif cmd == "Q":
                print("Quitting...")
                return
            else:
                print("Invalid Args. Please use fortmat \"[W/V] [String]\"")    


    else:
        #Do Command Line Version
        '''vosher.py [W/V] "String" '''
        #1st Arg, (W)ash or (V)osh
        cmd = str.upper(sys.argv[1])
        #String to translate
        string = sys.argv[2]
        print(f"Text to translate: {string}")
        if cmd == "W":
            print(f"Washed String: {wash(string)}")
        elif cmd == "V":
            print(f"Voshed String: {vosh(string)}") 
        else:
            print("Invalid Args. Please use fortmat \"vosher.py [W/V] [String]\"")
    pass

if __name__ == "__main__":
    main()