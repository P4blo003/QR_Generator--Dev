# ---- LIBS ----
import sys
import os
import qrcode
import qrcode.constants
import traceback

# ---- GLOBAL VARIABLES ----
_MAX_ARGUMENTS_ = 3  # Max number of arguments.
_ALLOWED_ARGS = ["url","sp"]
_URL_TAG = "url"
_SAVE_PATH_TAG = "sp"
_ARGUMENTS_ = {}

# ---- FUNCTIONS ----
"""
Print the program information.
"""
def PrintProgInfo():
    print()
    print(f"Information\n{"*"*len("Information")}")
    print("Usage: <main.py [Options]>")
    print("[Options] : ")
    print("\t--url=[url] : The url to generate the qr code.")
    print("\t--sp=[savePath] : The save path where the program will save the qr code.")
"""
Finish the program with the given exit code.
"""
def FinishProg(exitCode : int = 0):
    print("---- End program ----")
    print()
    exit(exitCode)
""" 
Check the given arguments.
"""
def CheckArgs(argv:list):
    
    global _ARGUMENTS_
    
    if len(argv) > _MAX_ARGUMENTS_:  # It the number of arguments is incorrect.
        print("-- [ERROR] : Number of arguments incorrect.")
        PrintProgInfo()     # Print program information.
        FinishProg(1)   # Finish the program.
        
    if len(argv) > 1:   # If there is arguments.
        
        for arg in argv[1:]:    # For each argument.
            
            values = arg.split("=")     # Split like: [--url, value]
            if len(values) != 2:
                print(f"-- [ERROR] : Incorrect argument. Given <{arg}>")
                PrintProgInfo()     # Print program information.
                FinishProg(1)   # Finish the program.
                
            properties = values[0].split("--")  # Split like: [, url]
            if len(properties) != 2:
                print(f"-- [ERROR] : Incorrect argument. Given <{arg}>")
                PrintProgInfo()     # Print program information.
                FinishProg(1)   # Finish the program.
                
            if properties[1] not in _ALLOWED_ARGS:
                print(f"-- [ERROR] : Incorrect argument. Given <{arg}>")
                PrintProgInfo()     # Print program information.
                FinishProg(1)   # Finish the program.
                
        _ARGUMENTS_[properties[1]] = values[1]  # Save the properties.
        
    
# ---- MAIN ----
if __name__ == "__main__":
    print()
    print("---- Running program ----")
    
    # Check the arguments:
    CheckArgs(sys.argv)     # Check the arguments.
    
    if _URL_TAG not in _ARGUMENTS_.keys():  # If the user didn't give an url in the arguments.
        print("You don't give an URL. Please give one:")
        m_url = input("URL: ")
        _ARGUMENTS_[_URL_TAG] = m_url
        
    if _SAVE_PATH_TAG not in _ARGUMENTS_.keys():    # If the user didn't give a save path in the arguments.
        
        validPath = False
        
        print("You don't give a save path. Please give one.") 
        while not validPath:    # Will the user give a bad directory.
            
            m_savePath = input("SavePath: ")    # Ask for a directory.
            
            if not os.path.exists(m_savePath):
                print("-- [WARNING] : The directory doesn't exist.")
            else:
                validPath = True
            
        _ARGUMENTS_[_SAVE_PATH_TAG] = m_savePath    # Save the path.
        
    try:
        # Generate the qr code.
        qr = qrcode.QRCode (version = 1, error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10, border=2)
        qr.add_data(_ARGUMENTS_[_URL_TAG])
        qr.make(fit=True)
        
        # Create the qr image.
        qr_image = qr.make_image(fill_color = "black", back_color = "white")
        
        # Save the qr in the specific path.
        qr_image.save(os.path.join(_ARGUMENTS_[_SAVE_PATH_TAG],"generatedQR.png"))
        
    except Exception as ex:
        print(f"-- [ERROR] : Some error in qr generation.\nException:\n{"*"*len("Exception:")}\n{ex.print_exc()}")
    
    FinishProg(0)   # Finish the program.