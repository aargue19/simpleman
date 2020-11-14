import numpy as np
import pandas as pd
import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import IntVar, Tk, Frame, Label, Button, Checkbutton, Entry, Canvas, Scrollbar, Text, ttk, Listbox

# SET UP WINDOW
root = Tk()

# GLOBAL VARIABLES
global currentRow
currentRow = 0
global skipVar
global cartList
cartList = []
global end_pos
end_pos = ''
global start_pos
start_pos = 0
global numInfo
global idInfo
global wordInfo
global gameDescInfo
global gameDescTxt
global searchInput
global searchCanvas
global searchListBox
global cartCanvas
global cartListBox

# METHODS
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = "black"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.configure(background = "black", foreground="white", activebackground = "grey66")

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# FUNCTIONS
def load():
    global df
    df = pd.read_csv("test_df.csv", index_col ="index")
    df = df.astype({"id": int, 
                    "game_num": int, 
                    "word": str, 
                    "game_name": str, 
                    "game_description": str,
                    "stemmed_word": str,
                    "changed_word": str, 
                    "remark": str, 
                    "std_word": str,
                    "std2": str})

def prev_row():
    global currentRow
    keepSkipping = True
    skipNum = 0
    count = 0
    wantSkip = skipVar.get()
    if wantSkip == 1:
        while keepSkipping == True:
            count += 1
            if df.iloc[currentRow + count].std_word != "nan":
                skipNum+=1
            else:
                keepSkipping = False
    currentRow = currentRow - 1 - skipNum
    destroy_info()
    update_info()
    update_std_words()

def next_row():
    global currentRow
    keepSkipping = True
    skipNum = 0
    count = 0
    wantSkip = skipVar.get()
    if wantSkip == 1:
        while keepSkipping == True:
            count += 1
            if df.iloc[currentRow + count].std_word != "nan":
                skipNum+=1
            else:
                keepSkipping = False
    currentRow = currentRow + 1 + skipNum    
    destroy_info()
    update_info()
    update_std_words()

def destroy_info():
    global numInfo
    global idInfo
    global wordInfo
    global gameDescInfo
    global gameDescTxt
    global searchInput
    global cartCanvas
    global cartListBox
    global searchCanvas
    global searchListBox
    numInfo.destroy()
    idInfo.destroy()
    wordInfo.destroy()
    gameDescInfo.destroy()
    gameDescTxt.delete('1.0', tk.END)
    searchInput.delete(0, 'end')

def update_info():
    global numInfo
    global idInfo
    global wordInfo
    global gameDescInfo
    global gameDescTxt
    global searchInput
    numInfo = Label(frame1, text=df.iloc[currentRow].game_num)
    numInfo.place(x=10, y=35)
    numInfo.configure(background = "black", foreground="white")
    idInfo = Label(frame1, text=df.iloc[currentRow].id)
    idInfo.place(x=100, y=35)
    idInfo.configure(background = "black", foreground="white")    
    wordInfo = Label(frame1, text=df.iloc[currentRow].changed_word)
    wordInfo.place(x=200, y=35)
    wordInfo.configure(background = "black", foreground="white")
    gameDescInfo = Label(frame1, text=df.iloc[currentRow].game_name)
    gameDescInfo.place(x=10, y=130)
    gameDescInfo.configure(background = "black", foreground="white")
    gameDescTxt.insert(1.0, "{}".format(df.iloc[currentRow].game_description))
    searchInput.insert(0, df.iloc[currentRow].changed_word)
    highlight_word()

def highlight_word():
    global start_pos
    start_pos = 0
    global end_pos
    end_pos = ''
    gameDescTxt.delete('1.0', tk.END)
    gameDescTxt.insert(1.0, df.iloc[currentRow].game_description, 'warning')
    h_word = df.iloc[currentRow].word.replace(" ","_")
    start_pos = gameDescTxt.search(h_word, '1.0', stopindex=tk.END)
    if not start_pos:   #in case the word is capitalized b/c it's first word in sentence
        start_pos = gameDescTxt.search(h_word.capitalize(), '1.0', stopindex=tk.END)
    if not start_pos:   #in case the word is all uppercase letters  
        start_pos = gameDescTxt.search(h_word.upper(), '1.0', stopindex=tk.END)
    if not start_pos:   #in case the word has hyphens
        start_pos = gameDescTxt.search(h_word.replace(" ","-"), '1.0', stopindex=tk.END)
    if start_pos:
        if end_pos:
            gameDescTxt.tag_remove('highlight', start_pos, end_pos)
        end_pos = '{}+{}c'.format(start_pos, len(h_word))            
        gameDescTxt.tag_add('highlight', start_pos, end_pos)
        gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")

def search_word():
    global checkBoxList
    global checkBoxes
    global labelList
    global matchList
    global searchCanvas
    global searchListBox
    search_term = searchInput.get()
    searchCanvas = Canvas(frame2, bg='black', width=420, height=800)
    searchCanvas.place(x=10,y=160)
    searchListBox = st.ScrolledText(searchCanvas, width=50, height=50, wrap="none")
    searchListBox.configure(background = "black")
    searchListBox.pack() 
    wantSkip = skipVar.get()
    if wantSkip == 1:
        matchDf = df['changed_word'][df['changed_word'].str.contains(search_term, na=False) & df['std_word'].str.contains("nan")].unique()
    else:
        matchDf = df['changed_word'][df['changed_word'].str.contains(search_term, na=False)].unique()
    matchList = []
    for i in range(len(matchDf)):
        matchList.append(matchDf[i])
    checkBoxList = []
    checkBoxes = []
    labelList = []
    for i in range(len(matchList)):
        labelList.append(Label(searchListBox, text=matchList[i]))
        labelList[i].changed_word = matchList[i]
        labelList[i].config(background = "black", foreground= 'white', font = ('Consolas', 10, 'bold'))
        labelList[i].bind("<Enter>", on_enter)
        labelList[i].bind("<Leave>", on_leave)
        checkBoxList.append(IntVar())
        checkBoxes.append(Checkbutton(searchListBox, text='', variable=checkBoxList[i], selectcolor="grey88", background='black'))
        searchListBox.window_create("end", window=checkBoxes[i])
        searchListBox.window_create("end", window=labelList[i])
        searchListBox.insert("end", "\n")

def on_enter(event):
    global start_pos
    global end_pos
    descriptions_list = []
    target = getattr(event.widget, "changed_word", "")
    search_term = searchInput.get()
    for i in range(len(df['game_description'][df['changed_word'].str.match(str(target))])):
        descriptions_list.append(str(df['game_description'][df['changed_word'].str.match(str(target))].iloc[i]))
        descriptions_list.append("\n\n\n\n")
    gameDescTxt.delete('1.0', tk.END)
    gameDescTxt.insert(1.0, descriptions_list, 'warning')
    start_pos = gameDescTxt.search(search_term, '1.0', stopindex=tk.END)
    if not start_pos:       #in case the word is capitalized b/c first word in sentence
        start_pos = gameDescTxt.search(search_term.capitalize(), '1.0', stopindex=tk.END)
    if not start_pos:       #in case the word is all uppercase letters
        start_pos = gameDescTxt.search(search_term.upper(), '1.0', stopindex=tk.END)
    if not start_pos:       #in case the word has hyphens   
        start_pos = gameDescTxt.search(search_term.replace(" ","-"), '1.0', stopindex=tk.END)
    if start_pos:
        if end_pos:
            gameDescTxt.tag_remove('highlight', start_pos, end_pos)
        end_pos = '{}+{}c'.format(start_pos, len(search_term))            
        gameDescTxt.tag_add('highlight', start_pos, end_pos)
        gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")
    for i in range(len(df['game_description'][df['changed_word'].str.match(str(target))])):
        start_pos = gameDescTxt.search(search_term, end_pos, stopindex=tk.END)
        if start_pos:
            if end_pos:
                gameDescTxt.tag_remove('highlight', start_pos, end_pos)
            end_pos = '{}+{}c'.format(start_pos, len(search_term))            
            gameDescTxt.tag_add('highlight', start_pos, end_pos)
            gameDescTxt.tag_config('highlight', background='yellow', foreground = "black")

def on_leave(event):
    pass

def add_to_cart():
    global cartList
    finalValue = []
    for x in checkBoxList:
        finalValue.append(x.get())
    for i in range(len(finalValue)):
        if finalValue[i] == 1:
            cartList.append(matchList[i])
    update_cart()

def update_cart():
    global cartCheckBoxList
    global cartCheckBoxes
    cartCanvas = Canvas(frame3, bg='black', width=420, height=800)
    cartCanvas.place(x=10,y=160)
    cartListBox = st.ScrolledText(cartCanvas, width=50, height=50, wrap="none")
    cartListBox.configure(background = "black")
    cartListBox.pack()
    cartCheckBoxList = []
    cartCheckBoxes = []
    cartLabelList = []
    for i in range(len(cartList)):
        cartLabelList.append(Label(cartListBox, text=cartList[i]))
        cartLabelList[i].description = cartList[i]
        cartLabelList[i].config(background = "black", foreground= 'white', font = ('Consolas', 10, 'bold'))
        cartCheckBoxList.append(IntVar())
        cartCheckBoxes.append(Checkbutton(cartListBox, text='', variable=cartCheckBoxList[i], selectcolor="grey88", background='black'))
        cartListBox.window_create("end", window=cartCheckBoxes[i])
        cartListBox.window_create("end", window=cartLabelList[i])
        cartListBox.insert("end", "\n") 

def remove_from_cart(): 
    global cartList
    whichChecked = []
    for x in cartCheckBoxList:
        whichChecked.append(x.get())
    keepList = []
    for i in range(len(whichChecked)):
        if whichChecked[i] != 1:
            keepList.append(cartList[i])
    cartList = keepList
    update_cart()

def update_std_words():
    stdListBox.delete(0, tk.END)
    bwList = df['std_word'][df['std_word'] != "nan"].tolist()
    for item in sorted(list(set(bwList))):
        stdListBox.insert(tk.END, item)
    data_output()

def set_std():
    newStdWord = stdListBox.get(tk.ACTIVE)
    newStd2Word = specInput.get()
    for cartWord in cartList:
        df['std_word'][df['changed_word'].str.match(cartWord)] = newStdWord
        df['std2'][df['changed_word'].str.match(cartWord)] = newStd2Word
    update_std_words()

def new_std_word():
    newStdWord = newStdInput.get()
    newStd2Word = specInput.get()
    for cartWord in cartList:
        df['std_word'][df['changed_word'].str.match(cartWord)] = newStdWord
        df['std2'][df['changed_word'].str.match(cartWord)] = newStd2Word
    update_std_words()

def select_all_search():
    for x in checkBoxes:
        x.select()

def deselect_all_search():
    for x in checkBoxes:
        x.deselect()

def select_all_cart():
    for x in cartCheckBoxes:
        x.select()

def deselect_all_cart():
    for x in cartCheckBoxes:
        x.deselect()

def data_output():
    df.to_csv('data_output.csv', index=True, index_label="index")

def save_file():
    df.to_csv('C:/Users/gaoan/Code/Freebird/{}.csv'.format(saveFileInput.get()), index=True, index_label="index")

###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################

# SET WINDOW SIZE
rootWidth = 1800
rootHeight = 1000
root.geometry('{}x{}+25+25'.format(rootWidth, rootHeight))
root.resizable(width=False, height=False)

# SET FRAME DIMENSIONS
frame1 = Frame(root, width=450, height=1000)
frame1.place(x=0,y=0)
frame1.config(bg="grey22")
frame2 = Frame(root, width=450, height=1000)
frame2.place(x=450,y=0)
frame2.config(bg="grey44")
frame3 = Frame(root, width=450, height=1000)
frame3.place(x=900,y=0)
frame3.config(bg="grey66")
frame4 = Frame(root, width=450, height=1000)
frame4.place(x=1350,y=0)
frame4.config(bg="grey88")

# FRAME 1
numTitle = Label(frame1, text="Game number:")
numTitle.place(x=10, y=10)
numTitle.configure(background = "black", foreground="white")
numInfo = Label(frame1, text="")
numInfo.place(x=10, y=35)
numInfo.configure(background = "black", foreground="white")
idTitle = Label(frame1, text="Game ID:")
idTitle.place(x=100, y=10)
idTitle.configure(background = "black", foreground="white")
idInfo = Label(frame1, text="")
idInfo.place(x=100, y=35)
idInfo.configure(background = "black", foreground="white")
wordTitle = Label(frame1, text="Word:")
wordTitle.place(x=200, y=10)
wordTitle.configure(background = "black", foreground="white")
wordInfo = Label(frame1, text="")
wordInfo.place(x=200, y=35)
wordInfo.configure(background = "black", foreground="white")
prevBtn= HoverButton(frame1, text="Previous", command=prev_row, padx=2, pady=2)
prevBtn.place(x=10,y=65)
prevBtn.configure(background = "black", foreground="white")
nextBtn = HoverButton(frame1, text="Next", command=next_row, padx=2, pady=2)
nextBtn.place(x=85,y=65)
nextBtn.configure(background = "black", foreground="white")
skipVar = IntVar()
skipBtn = Checkbutton(frame1, text='', variable=skipVar, selectcolor="grey88", background='black')
skipBtn.place(x=145,y=65)
navTitle = Label(frame1, text="Skip/Hide Standardized Words")
navTitle.place(x=180, y=65)
navTitle.configure(background = "black", foreground="white")
gameDescTitle = Label(frame1, text="Game:")
gameDescTitle.place(x=10, y=100)
gameDescTitle.configure(background = "black", foreground="white")
gameDescInfo = Label(frame1, text="")
gameDescInfo.place(x=10, y=130)
gameDescInfo.configure(background = "black", foreground="white")
gameDescTxt = st.ScrolledText(frame1, undo=True, width=50, height=40, wrap="word", bg = "black", fg = "white")
gameDescTxt.place(x=10, y=160)
gameDescTxt.insert(1.0, "DESCRIPTION GOES HERE..")
saveFileBtn = HoverButton(frame1, text="Save", command=save_file, padx=2, pady=2)
saveFileBtn.place(x=10,y=940)
saveFileBtn.configure(background = "black", foreground="white")
saveFileInput = Entry(frame1, width=42, justify = "left", font=('Consolas', 10, 'bold'))
saveFileInput.place(x=75,y=942)

# FRAME 2
searchBtn = HoverButton(frame2, text="Search", command=search_word, padx=2, pady=2)
searchBtn.place(x=10,y=40)
searchBtn.configure(background = "black", foreground="white")
searchInput = Entry(frame2, width=42, justify = "left", font=('Consolas', 10, 'bold'))
searchInput.place(x=75,y=42)
addCartBtn = HoverButton(frame2, text="Add", command=add_to_cart, padx=2, pady=2)
addCartBtn.place(x=10,y=120)
addCartBtn.configure(background = "black", foreground="white")
selectAllSearchBtn = HoverButton(frame2, text="Select All", command=select_all_search, padx=2, pady=2)
selectAllSearchBtn.place(x=275,y=120)
selectAllSearchBtn.configure(background = "black", foreground="white")
deselectAllSearchBtn = HoverButton(frame2, text="Deselect All", command=deselect_all_search, padx=2, pady=2)
deselectAllSearchBtn.place(x=350,y=120)
deselectAllSearchBtn.configure(background = "black", foreground="white")
searchCanvas = Canvas(frame2, bg='black', width=420, height=800)
searchCanvas.place(x=10,y=160)
searchListBox = st.ScrolledText(searchCanvas, width=50, height=50, wrap="none")
searchListBox.configure(background = "black")
searchListBox.pack() 

# FRAME 3

removeCartBtn = HoverButton(frame3, text="Remove", command=remove_from_cart, padx=2, pady=2)
removeCartBtn.place(x=10,y=120)
removeCartBtn.configure(background = "black", foreground="white")
selectAllSearchBtn = HoverButton(frame3, text="Select All", command=select_all_cart, padx=2, pady=2)
selectAllSearchBtn.place(x=275,y=120)
selectAllSearchBtn.configure(background = "black", foreground="white")
deselectAllSearchBtn = HoverButton(frame3, text="Deselect All", command=deselect_all_cart, padx=2, pady=2)
deselectAllSearchBtn.place(x=350,y=120)
deselectAllSearchBtn.configure(background = "black", foreground="white")
cartCanvas = Canvas(frame3, bg='black', width=420, height=800)
cartCanvas.place(x=10, y=160)
cartListBox = st.ScrolledText(cartCanvas, width=50, height=50, wrap="none")
cartListBox.configure(background = "black")
cartListBox.pack() 

# FRAME 4
newStdBtn = HoverButton(frame4, text="New", command=new_std_word, padx=2, pady=2)
newStdBtn.place(x=10,y=40)
newStdBtn.configure(background = "black", foreground="white")
newStdInput = Entry(frame4, width=42, justify = "left", font=('Consolas', 10, 'bold'))
newStdInput.place(x=75,y=42)

stdSetBtn = HoverButton(frame4, text="Existing", command=set_std, padx=2, pady=2)
stdSetBtn.place(x=10, y=80)
stdSetBtn.configure(background = "black", foreground="white")

specLabel = Label(frame4, text="Specify", padx=4, pady=4)
specLabel.place(x=10,y=120)
specLabel.configure(background = "black", foreground="white")
specInput = Entry(frame4, width=42, justify = "left", font=('Consolas', 10, 'bold'))
specInput.place(x=75,y=120)

stdCanvas = Canvas(frame4, bg='green', width=420, height=900)
stdCanvas.place(x=10,y=160)

stdScrollbar = Scrollbar(stdCanvas, orient="vertical")
stdScrollbar.pack(side="right", fill="y")
stdListBox = Listbox(stdCanvas, width=56, height=50, background = "black", foreground="white", font = ('Consolas', 10, 'bold'))
stdListBox.pack()
stdListBox.insert(tk.END, "std words go here")
stdListBox.configure(yscrollcommand=stdScrollbar.set)
stdScrollbar.config(command=stdListBox.yview)

# EXECUTE ON STARTUP
load()
update_info()
update_std_words()

# MAIN LOOP
root.mainloop()