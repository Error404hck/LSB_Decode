'''
    function program

    Write by : 
             _____                     _  _    ___  _  _   
            | ____|_ __ _ __ ___  _ __| || |  / _ \| || |  
            |  _| | '__| '__/ _ \| '__| || |_| | | | || |_ 
            | |___| |  | | | (_) | |  |__   _| |_| |__   _|
            |_____|_|  |_|  \___/|_|     |_|  \___/   |_|  
                                             
    
    Descrition: This code allows to find hidden data in lsb files
                This file contains the function and variable for the search


        setup.py
            lsbFunction/
             |_________: __init__.py
             |_________: convertLsb.py
            ascciDir/
             |_________: *.txt   

''' 




from PIL import Image
from sys import argv
from setup import pic
import time

# FONCTION POUR TROUVER LE FLAG :
def writeFile(typePixel="rvb", pic="",jump=1, turnImage=False, switchBit=False, notBit=False, x_depart=0, x_fin=pic.height, y_depart=0 , y_fin=pic.width):
    nameFile = "asciiDir/" + (typePixel.upper().replace(" ","")) + str(x_depart) + "x" + str(y_fin) + ".txt"
    asciiTab = ""
    flag = ""

    fichier = open(nameFile, "w")

    #jumpSize = 1
    #jump = 0

    # PARCOUR DE L'IMAGE
    
    for largeur in range (x_depart, x_fin):
        for hauteur in range (y_depart, y_fin, int(jump)):

            if turnImage == False :
                pixel = pic.getpixel((hauteur,largeur))
            elif turnImage == True :
                try :
                    pixel = pic.getpixel((largeur,hauteur))
                except :
                    print("the dimensions of your image are too large")
                    print("Use the '-d' for define a fix dimension")
                    exit()
            # RECUPERATION PIXEL DANS DES VARIABLES
            r = pixel[0]
            v = pixel[1]
            b = pixel[2]


            if len(pixel) > 3 : #--> check if transparency is present
                a = pixel[3]
                    
                  
            for check in typePixel :
                # RED PIXEL :
                if check == "r":    
                    asciiTab+=(lsbPixel(r, notBit))#--> Get lsb and adding to the list for red color
                    if len(asciiTab) == 8 :
                        if switchBit == False :
                            wrAsc , wrDec = convertBinToAscii(asciiTab)#--> Get the binary conversion to ASCII and binary to decimal               
                        elif switchBit == True :
                            wrAsc , wrDec = convertBinToAsciiSwitchBit(asciiTab)#--> Make a reverse bit and get the binary conversion to ASCII and binary to decimal

                        # Print Flag :
                        flag = printFlag(flag, wrDec, wrAsc)

                        # Write File :
                        fichier.write(wrAsc)
                        asciiTab = ""

                # GREEN PIXEL :
                if check == "v":
                    asciiTab+=(lsbPixel(v, notBit))#--> Get lsb and adding to the list for green color
                    if len(asciiTab) == 8 :
                        
                        if switchBit == False :
                            wrAsc , wrDec = convertBinToAscii(asciiTab)#--> Get the binary conversion to ASCII and binary to decimal               
                        elif switchBit == True :
                            wrAsc , wrDec = convertBinToAsciiSwitchBit(asciiTab)#--> Make a reverse bit and get the binary conversion to ASCII and binary to decimal
                        
                        # Print Flag :
                        flag = printFlag(flag, wrDec, wrAsc)

                        # Write File :
                        fichier.write(wrAsc)
                        asciiTab = ""

                # BLUE PIXEL :
                if check == "b":
                    asciiTab += (lsbPixel(b, notBit))#--> Get lsb and adding to the list for blue color
                    if len(asciiTab) == 8 :
                        
                        if switchBit == False :
                            wrAsc , wrDec = convertBinToAscii(asciiTab)#--> Get the binary conversion to ASCII and binary to decimal               
                        elif switchBit == True :
                            wrAsc , wrDec = convertBinToAsciiSwitchBit(asciiTab)#--> Make a reverse bit and get the binary conversion to ASCII and binary to decimal

                        # Print Flag :
                        flag = printFlag(flag, wrDec, wrAsc)

                        # Write File :
                        fichier.write(wrAsc)
                        asciiTab = ""


                # TRANSPARENCY :
                if check == "a" and len(pixel) > 3: 
                    asciiTab += (lsbPixel(a, notBit))#--> Get lsb and adding to the list for transparency
                    if len(asciiTab) == 8 :
                        
                        if switchBit == False :
                            wrAsc , wrDec = convertBinToAscii(asciiTab)#--> Get the binary conversion to ASCII and binary to decimal               
                        elif switchBit == True :
                            wrAsc , wrDec = convertBinToAsciiSwitchBit(asciiTab)#--> Make a reverse bit and get the binary conversion to ASCII and binary to decimal

                        # Print Flag :
                        flag = printFlag(flag, wrDec, wrAsc)

                        # Write File :
                        fichier.write(wrAsc)
                        asciiTab = ""
                

    print(nameFile + " : " + flag)
    fichier.close()

# Function to get LSB with modulo
def lsbPixel(pix, notBit):
    if notBit == False :
        if pix % 2 == 0 :
            return "0"
        
        elif pix % 2 == 1 :
            return "1"

    elif notBit == True : 
        #print("notBit")
        if pix % 2 == 0 :
            return "1"
        
        elif pix % 2 == 1 :
            return "0"


    
# Function to convert bin to ascii and bin to decimal
def convertBinToAscii(pix):
    wrDec = int(pix,2)
    wrAsc = chr(wrDec)
    return wrAsc , wrDec

def convertBinToAsciiSwitchBit(pix):
    pix = "".join(reversed(pix))
    wrDec = int(pix,2)
    wrAsc = chr(wrDec)
    return wrAsc , wrDec



# Function to print flag
def printFlag(flag, wrDec, wrAsc):
    lenFlag = 100
    if wrDec in range(48,57) and len(flag) < lenFlag: #--> char (1-9)
        flag+= wrAsc
    elif wrDec in range(65,90) and len(flag) < lenFlag : #--> char (A-Z)
        flag+= wrAsc
    elif wrDec in range(97,122) and len(flag) < lenFlag : #--> char (a-z)
        flag+= wrAsc
    elif wrDec in range (123,125) and len(flag) < lenFlag: #--> char ({|})
        flag+= wrAsc
    elif wrDec == 61 and len(flag) < lenFlag: #--> char ({|})
        flag+= wrAsc

    return flag
 


# VERIFICATION DU MAIN
if __name__ == "__main__" : 
    print("Fin du programme") 