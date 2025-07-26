#Author: João Victor Lima da Silva
import RSA
import random
import json
from sympy import randprime
import tkinter as tk
import customtkinter as ctk

#Global variables
privateKey = RSA.CHAVE_PRIVADA
publicKey = RSA.CHAVE_PUBLICA
currentLang = "en"
currentFrame = "mainWindow" 
with open('translations.json', 'r', encoding='utf-8') as f: #Sets the traslations dict from the translations json file
    translations = json.load(f)

#Global functions
def t(key): #Traslates text based on the selected language, current frame and selected key using the traslations dict
    return translations[currentLang][currentFrame].get(key, key)
def setCurrentF(frame):
    global currentFrame
    currentFrame = frame.__class__.__name__
#Appearance setting
ctk.set_appearance_mode("light")
#Encryption frame
class encryptionGUI(ctk.CTkFrame):
    def __init__(self, master, copyCallback, pasteCallback):
        super().__init__(master, fg_color="lightblue")
        setCurrentF(self) #Sets current frame in the first call *important
        #Field creation

        ctk.CTkLabel(self, text=t("label1"), font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox1 = ctk.CTkTextbox(self, width=400, font=("Helvetica", 18), wrap="word")
        self.tBox1.pack(pady=(10, 20))

        self.frame2 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        
        ctk.CTkButton(self.frame2, text=t("button1"), font=("Helvetica", 18), width=140, height=40, command=lambda: pasteCallback(self.tBox1)).grid(row=0, column=0)
        ctk.CTkButton(self.frame2, text=t("button2"), font=("Helvetica", 18), width=140, height=40, command=self.Encript).grid(padx=(30, 0), row=0, column=1)
        
        self.frame2.pack(pady=(0, 20))
        
        self.frame1 = ctk.CTkFrame(self, fg_color="#8CAFBB")
        
        ctk.CTkLabel(self.frame1, text=t("label2"), font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox2 = ctk.CTkTextbox(self.frame1, width=400, height= 120, font=("Helvetica", 18), wrap="word")
        self.tBox2.pack(padx=15, pady=10)
        
        ctk.CTkButton(self.frame1, text=t("button3"), width=100, height=30, font=("Helvetica", 18), command=lambda: copyCallback(self.tBox2)).pack(pady=(0, 10))
        
        self.frame1.pack(pady=10, padx=10)
        self.pack(fill="both", expand=1)
    #Functions
    def Encript(self):
        text = self.tBox1.get("0.0", "end")
        text = text[:-1]

        self.tBox2.configure(state="normal")
        self.tBox2.delete("0.0", "end")
        self.tBox2.configure(state="disabled")

        try:
            textE = RSA.cifraDeBlocosE(text, publicKey)
            
            self.tBox2.configure(state="normal")
            self.tBox2.insert("0.0", textE)
            self.tBox2.configure(state="disabled")
        except Exception as e:
            print("Error: ", e)
            
            self.tBox2.configure(state="normal")
            self.tBox2.insert("0.0", f"Error: \" {e} \"")
            self.tBox2.configure(state="disabled")
#Decryption frame
class decryptionGUI(ctk.CTkFrame):
    def __init__(self, master, copyCallback, pasteCallback):
        super().__init__(master, fg_color="lightblue")
        #Field creation
        ctk.CTkLabel(self, font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox1 = ctk.CTkTextbox(self, width=400, font=("Helvetica", 18), wrap="word")
        self.tBox1.pack(pady=(10, 20))

        self.frame2 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        
        ctk.CTkButton(self.frame2, font=("Helvetica", 18), width=140, height=40, command=lambda: pasteCallback(self.tBox1)).grid(row=0, column=0)
        ctk.CTkButton(self.frame2, font=("Helvetica", 18), width=140, height=40, command=self.Decript).grid(padx=(30, 0), row=0, column=1)
        
        self.frame2.pack(pady=(0, 20))

        self.frame1 = ctk.CTkFrame(self, fg_color="#8CAFBB")
        
        ctk.CTkLabel(self.frame1, font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox2 = ctk.CTkTextbox(self.frame1, width=400, height= 120, font=("Helvetica", 18), wrap="word")
        self.tBox2.pack(padx=15, pady=10)
        
        ctk.CTkButton(self.frame1, width=100, height=30, font=("Helvetica", 18), command=lambda: copyCallback(self.tBox2)).pack(pady=(0, 10))
        
        self.frame1.pack(pady=10, padx=10)
        self.pack(fill="both", expand=1)
    #Functions
    def Decript(self):
        text = self.tBox1.get("0.0", "end")
        text = text[:-1]

        self.tBox2.configure(state="normal")
        self.tBox2.delete("0.0", "end")
        self.tBox2.configure(state="disabled")

        try:
            textD = RSA.cifraDeBlocosD(text, privateKey)
            
            self.tBox2.configure(state="normal")
            self.tBox2.insert("0.0", textD)
            self.tBox2.configure(state="disabled")
        except Exception as e:
            print("Error: ", e)
            
            self.tBox2.configure(state="normal")
            self.tBox2.insert("0.0", f"Error: \" {e} \"")
            self.tBox2.configure(state="disabled")
#Key generator Frame
class keyGenGUI(ctk.CTkFrame):
    def __init__(self, master, copyCallback, popupCallback):
        super().__init__(master, fg_color="lightblue")
        setCurrentF(self)
        vcmd = self.register(self.isNum)
        #Field creation
        ctk.CTkLabel(self, font=("Helvetica", 26, "bold")).pack(pady=20)

        ctk.CTkLabel(self, font=("Helvetica", 15)).pack()

        ctk.CTkLabel(self, font=("Helvetica", 18, "bold")).pack()

        ctk.CTkLabel(self, font=("Helvetica", 15)).pack()

        self.frame1 = ctk.CTkFrame(self, fg_color="#8CAFBB")

        ctk.CTkLabel(self.frame1, font=("Helvetica", 18)).grid(padx=(20, 0), pady=20, row=0, column=0)
        self.entry1 = ctk.CTkEntry(self.frame1, font=("Helvetica", 18), placeholder_text="E.g., 10427", validate="key", validatecommand=(vcmd, "%P"))
        self.entry1.grid(padx=(10, 0), pady=20, ipadx=5, ipady=5, row=0, column=1)
        ctk.CTkLabel(self.frame1, font=("Helvetica", 18)).grid(padx=(20, 0), pady=10,row=1, column=0)
        self.entry2 = ctk.CTkEntry(self.frame1, font=("Helvetica", 18), placeholder_text="E.g., 19997", validate="key", validatecommand=(vcmd, "%P"))
        self.entry2.grid(padx=(10, 0), pady=10,ipadx=5, ipady=5, row=1, column=1)

        self.frame1.pack(padx=20 ,pady=10, ipadx=10, ipady=5)

        self.frame2 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        
        ctk.CTkButton(self.frame2, font=("Helvetica", 18), width=130, height=50, command=self.randPrime).grid(row=0, column=0)
        ctk.CTkButton(self.frame2, font=("Helvetica", 18), width=130, height=50, command=lambda: self.confirm(popupCallback)).grid(padx=(30, 0), pady=10 ,row=0, column=1)
        
        self.frame2.pack(pady=5)

        self.frame3 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.frame3_1 = ctk.CTkFrame(self.frame3, fg_color="#8CAFBB")

        ctk.CTkLabel(self.frame3_1, font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox1 = ctk.CTkTextbox(self.frame3_1, width=170, height=60, font=("Helvetica", 18), wrap="word", state="disabled")
        self.tBox1.pack(padx=15, pady=10)
        
        ctk.CTkButton(self.frame3_1, width=25, height=15, font=("Helvetica", 18), command=lambda: copyCallback(self.tBox1)).pack()

        self.frame3_1.grid(ipadx=5, ipady=5, row=0, column=0)

        self.frame3_2 = ctk.CTkFrame(self.frame3, fg_color="#8CAFBB")

        ctk.CTkLabel(self.frame3_2, font=("Helvetica", 18)).pack(pady=(10, 0))

        self.tBox2 = ctk.CTkTextbox(self.frame3_2, width=170, height=60, font=("Helvetica", 18), wrap="word", state="disabled")
        self.tBox2.pack(padx=15, pady=10)
        
        ctk.CTkButton(self.frame3_2, width=25, height=15, font=("Helvetica", 18), command=lambda: copyCallback(self.tBox2)).pack()

        self.frame3_2.grid(padx=(20, 0), ipadx=5, ipady=5, row=0, column=1)

        self.frame3.pack(pady=5)

        self.pack(fill="both", expand=1)
    #Functions
    def isNum(self, text):#Certifies that the entry text is either a number or a placeholder text
        if text.isdigit() or text == "":
            return True
        if text == "E.g., 10427" or text == "E.g., 19997":
            return True
        return False 
    def randPrime(self): #Generates random prime numbers for the keys
        prime1 = str(randprime(10000, 100000))
        prime2 = str(randprime(10000, 100000))
        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.entry1.insert(0, prime2)
        self.entry2.insert(0, prime1)
    def confirm(self, popupCallback): #Certifies that the typed in numbers are valid
        prime2 = int(self.entry1.get())
        prime1 = int(self.entry2.get())

        if (prime2 * prime1) < len(RSA.ALFABETO): 
            popupCallback(t("warning1") + f"({len(RSA.ALFABETO)})")
            return
        if not(RSA.ehPrimo(prime1) and RSA.ehPrimo(prime2)):
            popupCallback(t("warning2"))
            return
        if prime1 == prime2 :
            popupCallback(t("warning3"))
            return
        try:
            keys = RSA.geraChaves(prime1, prime2)
            self.tBox1.configure(state="normal")
            self.tBox1.delete("0.0", "end")
            self.tBox1.insert("0.0", f"{keys[0][0]},{keys[0][1]}")
            self.tBox1.configure(state="disabled")
            self.tBox2.configure(state="normal")
            self.tBox2.delete("0.0", "end")
            self.tBox2.insert("0.0", f"{keys[1][0]},{keys[1][1]}")
            self.tBox2.configure(state="disabled")
        except Exception as e:
            print("Error:", e)
            tk.messagebox.showerror("Error", e)
#Settings frame
class settingsGUI(ctk.CTkFrame):
    def __init__(self, master, popupCallback, copyCallback, pasteCallback, updateLangCallback):
        super().__init__(master, fg_color="lightblue")
        setCurrentF(self)
        #Field creation
        ctk.CTkLabel(self, font=("Helvetica", 22, "bold")).pack(pady=(50, 10))
        self.entry1 = ctk.CTkEntry(self, font=("Helvetica", 22), placeholder_text="E.g., '7990271,5'", width=260, height=50)
        self.entry1.pack(pady=10, ipadx=5, ipady=5)

        self.frame1 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        
        ctk.CTkButton(self.frame1, font=("Helvetica", 20), width=120, height=40, command=lambda: copyCallback(self.entry1)).grid(row=0, column=0)
        ctk.CTkButton(self.frame1, font=("Helvetica", 20), width=120, height=40, command=lambda: pasteCallback(self.entry1)).grid(padx=(30, 0), row=0, column=1)
        ctk.CTkButton(self.frame1, font=("Helvetica", 20), width=120, height=40, command=lambda: self.publicKeyValidation(popupCallback)).grid(padx=(30, 0), row=0, column=2)

        self.frame1.pack(pady=(10, 50))

        ctk.CTkLabel(self, font=("Helvetica", 22, "bold")).pack(pady=10)
        self.entry2 = ctk.CTkEntry(self, font=("Helvetica", 22), placeholder_text="E.g., '7990271,1596269'", width=260, height=50)
        self.entry2.pack(pady=10, ipadx=5, ipady=5)
        
        self.frame2 = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        
        ctk.CTkButton(self.frame2, font=("Helvetica", 20), width=120, height=40, command=lambda: copyCallback(self.entry2)).grid(row=0, column=0)
        ctk.CTkButton(self.frame2, font=("Helvetica", 20), width=120, height=40, command=lambda: pasteCallback(self.entry2)).grid(padx=(30, 0), row=0, column=1)
        ctk.CTkButton(self.frame2, font=("Helvetica", 20), width=120, height=40, command=lambda: self.privateKeyValidation(popupCallback)).grid(padx=(30, 0), row=0, column=2)

        self.frame2.pack(pady=(10, 30))

        self.radioVar = tk.IntVar(value=0)
        ctk.CTkRadioButton(self, text="English", command=lambda: self.toggleLang(master, updateLangCallback), variable=self.radioVar, value=0).pack(pady=(0, 10))
        ctk.CTkRadioButton(self, text="Português", command=lambda: self.toggleLang(master, updateLangCallback), variable=self.radioVar, value=1).pack()
        
        self.pack(fill="both", expand=1)
    #Functions
    def publicKeyValidation(self, popupCallback):
        try:
            text = self.entry1.get()
            text = text.split(",")
            if len(text) != 2:
                popupCallback(t("warning1"))
                return
            if not(text[0].isdigit() and text[1].isdigit()):
                popupCallback(t("warning1"))
                return
            text = [int(text[0]), int(text[1])]
            if not(RSA.checaChavePub(text)):
                popupCallback(t("warning1"))
                return
            global publicKey
            publicKey = text
            self.entry1.delete(0, "end")
            self.entry1.insert(0, f"{publicKey[0]},{publicKey[1]}")
        except Exception as e:
            print("Error: ", e)
            tk.messagebox.showerror(title="Error", message=f"Error: '{e}'")
    def privateKeyValidation(self, popupCallback):
        text = self.entry2.get()
        text = text.split(",")
        if len(text) != 2:
            popupCallback("Invalid format")
            return
        if not(text[0].isdigit() and text[1].isdigit()):
            popupCallback("Invalid format")
            return
        text = [int(text[0]), int(text[1])]
        global privateKey
        privateKey = text
        self.entry2.delete(0, "end")
        self.entry2.insert(0, f"{privateKey[0]},{privateKey[1]}")
    def toggleLang(self, master, updateLangCallback): #Toggles current language
        global currentLang
        option = self.radioVar.get()
        if option:
            currentLang = "pt-br"
        else:
            currentLang = "en"
        updateLangCallback(self)
        self.toggleMainWindowLang(master)
    def toggleMainWindowLang(self, master): #Toggles menu bar and title language
        setCurrentF(master)
        master.title(t("title"))
        for i in range(1, master.myMenu.index("end") + 1):
            master.myMenu.entryconfigure(i, label=t(f"mb{i}"))
        setCurrentF(self)
#Info frame
class info(ctk.CTkFrame):   
    def __init__(self, master):
        super().__init__(master, fg_color="lightblue")
        #Field creation
        
        self.tBox1 = ctk.CTkTextbox(self, font=("Helvetica", 22, "bold"), wrap="word")
    
        self.tBox1.pack(fill="both", expand=1)

        self.readFile()

        self.pack(fill="both", expand=1)
    #Functions
    def readFile(self):
        filename = './help.txt'
        with open(filename, 'r', encoding='utf-8') as f:
            self.tBox1.insert("0.0", f.read())
#Main window
class mainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Field creation
        self.update_idletasks()

        self.width = 500
        self.height = 600

        self.x = (self.winfo_screenwidth() // 2) - (self.width //2)
        self.y = (self.winfo_screenheight() // 2) - (self.height //2)

        self.title(t("title"))
        self.resizable(False, False)

        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        
        #Menu bar
        self.myMenu = tk.Menu(self)
        self.config(menu=self.myMenu) 

        self.myMenu.add_command(label=t("mb1"), command=self.showFrame1)
        self.myMenu.add_command(label=t("mb2"), command=self.showFrame2)
        self.myMenu.add_command(label=t("mb3"), command=self.showFrame3)
        self.myMenu.add_command(label=t("mb4"), command=self.showFrame4)
        self.myMenu.add_command(label=t("mb5"), command=self.showFrame5)
        self.myMenu.add_command(label=t("mb6"), command=self.quit)

        #Frames
        self.frames = [encryptionGUI(self, self.copy, self.paste), decryptionGUI(self, self.copy, self.paste), keyGenGUI(self, self.copy, self.warningPopup), settingsGUI(self, self.warningPopup, self.copy, self.paste, self.updateFrameLang), info(self)]
        self.frames[1].forget()
        self.frames[2].forget()
        self.frames[3].forget()
        self.frames[4].forget()
    #Functions
    def showFrame1(self):
        encryptionGUI = self.frames[0]
        setCurrentF(encryptionGUI)
        self.updateFrameLang(encryptionGUI)
        encryptionGUI.tBox1.delete("0.0", "end")
        encryptionGUI.tBox2.configure(state="normal")
        encryptionGUI.tBox2.delete("0.0", "end")
        encryptionGUI.tBox2.configure(state="disabled")
        self.switchFrame(0)
    def showFrame2(self):
        decryptionGUI = self.frames[1]
        setCurrentF(decryptionGUI)
        self.updateFrameLang(decryptionGUI)
        decryptionGUI.tBox1.delete("0.0", "end")
        decryptionGUI.tBox2.configure(state="normal")
        decryptionGUI.tBox2.delete("0.0", "end")
        decryptionGUI.tBox2.configure(state="disabled")
        self.switchFrame(1)
    def showFrame3(self):
        keyGenGUI = self.frames[2]
        setCurrentF(keyGenGUI)
        self.updateFrameLang(keyGenGUI)
        self.switchFrame(2)
    def showFrame4(self):
        settingsGUI = self.frames[3]
        setCurrentF(settingsGUI)
        self.updateFrameLang(settingsGUI)
        settingsGUI.entry1.delete(0, "end")
        settingsGUI.entry1.insert(0, f"{publicKey[0]},{publicKey[1]}")
        settingsGUI.entry2.delete(0, "end")
        settingsGUI.entry2.insert(0, f"{privateKey[0]},{privateKey[1]}")
        self.switchFrame(3)
    def showFrame5(self):
        info = self.frames[4]
        text = self.infoText()
        info.tBox1.configure("normal")
        info.tBox1.delete("0.0", "end")
        info.tBox1.insert("0.0", text)
        info.tBox1.configure("disabled")
        self.switchFrame(4)
    def switchFrame(self, index):
        for frame in self.frames:
            frame.forget()
        self.frames[index].tkraise()
        self.frames[index].pack(fill="both", expand=1)
    def copy(self, element): #Copy to clipboar function
        if isinstance(element, ctk.CTkEntry):
            textCopy = element.get()
            self.clipboard_clear()
            self.clipboard_append(textCopy)
            return
        textCopy = element.get("0.0", "end")
        textCopy = textCopy[:-1]
        self.clipboard_clear()
        self.clipboard_append(textCopy)
    def warningPopup(self, warningmessage): #Shows a popup warning message
        tk.messagebox.showwarning("Warning", warningmessage)
    def paste(self, element): #Paste from clipboard function
        textPaste = self.clipboard_get()
        if isinstance(element, ctk.CTkEntry):
            element.delete(0, "end")
            element.insert(0, textPaste)
            return
        element.delete("0.0", "end")
        element.insert("0.0", textPaste)
    def updateFrameLang(self, frame, labelCount=0, buttonCount=0): #Parses trough all labels and buttons of a specific frame and translates the text acording to the translation function t()
        for widget in frame.winfo_children():           
            if isinstance(widget, ctk.CTkLabel):
                labelCount += 1
                widget.configure(text=t(f"label{labelCount}"))
            elif isinstance(widget, ctk.CTkButton):
                buttonCount += 1
                widget.configure(text=t(f"button{buttonCount}"))
            elif isinstance(widget, ctk.CTkFrame):
                labelCount, buttonCount = self.updateFrameLang(widget, labelCount, buttonCount)
        return labelCount, buttonCount
    def infoText(self): #Returns info tab text based on the current language
        if currentLang == "en":
           byteStart = 0
           byteEnd = 2206
        else:
            byteStart = 2210
            byteEnd = -1
        with open("./help.txt", "rb") as f: 
            f.seek(byteStart)
            text = f.read(byteEnd)
        return text.decode("utf-8", errors="ignore")
#Start the app
if __name__=="__main__":
    app = mainWindow()  
    app.mainloop()