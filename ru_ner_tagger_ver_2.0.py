# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from tkinter import *
from tkinter import filedialog
import pandas as pd
import getpass

mainwindow = Tk()
mainwindow.title('RU NER - Tagging Tool')
mainwindow.geometry("575x450")
mainwindow.resizable(0,0)
mainwindow.config(bg='#1E1128')

class Tagger:
    def __init__(self):
        self.master = mainwindow
        self.max_rows = 0
        self.current = 0
        self.sentences = None
        self.persons = []
        self.per_entities = None
        self.organizations = []
        self.org_entities = None
        self.locations = []
        self.loc_entities = None
        self.sentence_text = Text(self.master, width=70, height=15, font=("Trebuchet MS",11), bg='#DFCBEE', wrap=WORD, selectbackground="black", selectforeground="white")
        self.button_openfile = Button(self.master, text="Open file", command=self.OpenFile, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 10, "bold"))
        self.button_back = Button(self.master, text="<<", state=DISABLED, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_forward = Button(self.master, text=">>", command=lambda: self.Forward(2), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_per = Button(self.master, text="PER", command=self.PER_NE, bg='#32a852', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_org = Button(self.master, text="ORG", command=self.ORG_NE, bg='#3267a8', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_loc = Button(self.master, text="LOC", command=self.LOC_NE, bg='#e8e15f', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_savefile = Button(self.master, text="Save File", command=self.SaveFile, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_openfile.grid(row=0,column=1, padx=5, pady=5)

    def OpenFile(self):
        username = getpass.getuser()
        try:
            self.master.filename = filedialog.askopenfilename(initialdir="/User/{}".format(username), title="Select a file...", filetypes=[('Excel Files', '*.xlsx')])
            self.ReadData()
        except:
            print("Choose File...")
            self.button_openfile.grid_forget()
            self.button_openfile.grid(row=0,column=1, padx=5, pady=5)
                
        
            
    def ReadData(self):
        data = pd.read_excel(self.master.filename)
        data  = pd.Series(data['sentences'])
        self.max_rows = len(data.index)
        self.sentences = data[0:]
        self.per_entities = [''] * (self.max_rows)
        self.org_entities = [''] * (self.max_rows) 
        self.loc_entities = [''] * (self.max_rows)
        self.button_openfile.grid_forget()
        self.status = Label(self.master, text="Sentence 1 of " + str(self.max_rows), bd=2, relief=SUNKEN, anchor=E, bg='#632E8B', fg='white')
        self.ShowSentences()

    def ShowSentences(self):
        self.sentence_text.insert(END, self.sentences[0])
        self.sentence_text.grid(row=0,column=0,columnspan=5, padx=5, pady=5)
        self.button_back.grid(row=1,column=0, padx=5, pady=5)
        self.button_per.grid(row=1,column=1, padx=5, pady=5)
        self.button_org.grid(row=1,column=2, padx=5, pady=5)
        self.button_loc.grid(row=1,column=3, padx=5, pady=5)
        self.button_forward.grid(row=1,column=4, padx=5, pady=5)
        self.button_savefile.grid(row=2,column=2, padx=5, pady=5)
        self.status.grid(row=3,column=0, columnspan=5, sticky=E+W, padx=5, pady=5)
        
    def Forward(self, sen_no):
        self.SaveTags()
        self.persons.clear()
        self.organizations.clear()
        self.locations.clear()
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.sentences[sen_no-1])
        self.current = sen_no-1
        self.sentence_text.grid(row=0,column=0,columnspan=5, padx=5, pady=5)
        if sen_no == self.max_rows:
            self.button_forward = Button(mainwindow, text=">>", state=DISABLED, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        else:
            self.button_forward = Button(mainwindow, text=">>", command=lambda: self.Forward(sen_no+1), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_back = Button(self.master, text="<<", command=lambda: self.Back(sen_no-1), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_back.grid(row=1,column=0, padx=5, pady=5)
        self.button_per.grid(row=1,column=1, padx=5, pady=5)
        self.button_org.grid(row=1,column=2, padx=5, pady=5)
        self.button_loc.grid(row=1,column=3, padx=5, pady=5)
        self.button_forward.grid(row=1,column=4, padx=5, pady=5)
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))

    def Back(self, sen_no):
        self.SaveTags()
        self.persons.clear()
        self.organizations.clear()
        self.locations.clear()
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.sentences[sen_no-1])
        self.current = sen_no-1
        self.sentence_text.grid(row=0,column=0,columnspan=5, padx=5, pady=5)
        self.button_forward = Button(mainwindow, text=">>", command=lambda: self.Forward(sen_no+1), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        if sen_no == 1:
            self.button_back = Button(mainwindow, text="<<", state=DISABLED, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        else:
            self.button_back = Button(mainwindow, text="<<", command=lambda: self.Back(sen_no-1), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_back.grid(row=1,column=0, padx=5, pady=5)
        self.button_per.grid(row=1,column=1, padx=5, pady=5)
        self.button_org.grid(row=1,column=2, padx=5, pady=5)
        self.button_loc.grid(row=1,column=3, padx=5, pady=5)
        self.button_forward.grid(row=1,column=4, padx=5, pady=5)
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))

    def PER_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            self.sentence_text.tag_configure("per", background="#32a852", foreground="black", selectbackground="black", selectforeground="#32a852")
            if "per" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("per","sel.first","sel.last")
                self.persons.remove(selected)
            elif "org" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("org","sel.first","sel.last")
                self.organizations.remove(selected)
                self.sentence_text.tag_add("per", "sel.first","sel.last")
                self.persons.append(selected)
            elif "loc" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("loc","sel.first","sel.last")
                self.locations.remove(selected)
                self.sentence_text.tag_add("per", "sel.first","sel.last")
                self.persons.append(selected)
            else:
                self.sentence_text.tag_add("per", "sel.first", "sel.last")
                self.persons.append(selected)
            print(selected)
        except:
            pass
    
    def ORG_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            self.sentence_text.tag_configure("org", background="#3267a8", foreground="black", selectbackground="black", selectforeground="#3267a8")
            if "org" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("org","sel.first","sel.last")
                self.organizations.remove(selected)
            elif "per" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("per","sel.first","sel.last")
                self.persons.remove(selected)
                self.sentence_text.tag_add("org", "sel.first","sel.last")
                self.organizations.append(selected)
            elif "loc" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("loc","sel.first","sel.last")
                self.locations.remove(selected)
                self.sentence_text.tag_add("org", "sel.first","sel.last")
                self.organizations.append(selected)
            else:
                self.sentence_text.tag_add("org", "sel.first", "sel.last")
                self.organizations.append(selected)
            print(selected)
        except:
            pass
    
    def LOC_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            self.sentence_text.tag_configure("loc", background="#e8e15f", foreground="black", selectbackground="black", selectforeground="#e8e15f")
            if "loc" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("loc","sel.first","sel.last")
                self.locations.remove(selected)
            elif "per" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("per","sel.first","sel.last")
                self.persons.remove(selected)
                self.sentence_text.tag_add("loc", "sel.first","sel.last")
                self.locations.append(selected)
            elif "org" in self.sentence_text.tag_names('sel.first'):
                self.sentence_text.tag_remove("org","sel.first","sel.last")
                self.organizations.remove(selected)
                self.sentence_text.tag_add("loc", "sel.first","sel.last")
                self.locations.append(selected)
            else:
                self.sentence_text.tag_add("loc", "sel.first", "sel.last")
                self.locations.append(selected)
            print(selected)
        except:
            pass
        
    def SaveTags(self):
        self.per_entities.pop(self.current)
        self.org_entities.pop(self.current)
        self.loc_entities.pop(self.current)
        self.per_entities.insert(self.current, ','.join(self.persons))
        self.org_entities.insert(self.current, ','.join(self.organizations))
        self.loc_entities.insert(self.current, ','.join(self.locations))
        print(self.current, self.per_entities, self.org_entities, self.loc_entities)

    def SaveFile(self):
        self.SaveTags()
        print("\n")
        print(len(self.per_entities), len(self.org_entities), len(self.loc_entities))
        print(self.per_entities, self.org_entities, self.loc_entities)
        tagged_data = pd.DataFrame({"Sentences":self.sentences, "PER":self.per_entities, "ORG":self.org_entities, "LOC":self.loc_entities})
        try:
            filename = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("excel files", '*.xlsx')], title="Choose filename")
            tagged_data.to_excel(filename)
            messagebox.showinfo("Alert!", "Tagged data have been saved.")
        except:
            self.SaveTags()
            self.button_savefile.grid_forget()
            self.button_savefile.grid(row=2,column=2, padx=5, pady=5)
            
tagger = Tagger()
mainwindow.mainloop()