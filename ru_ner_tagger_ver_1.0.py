# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from tkinter import *
from tkinter import filedialog
import pandas as pd

mainwindow = Tk()
mainwindow.title('RU NER - Tagging Tool')
mainwindow.geometry("525x300")

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
        self.sentence_text = Text(self.master, width=65, height=5)
        self.button_openfile = Button(self.master, text="Open file", command=self.OpenFile)
        self.button_back = Button(self.master, text="<<", state=DISABLED)
        self.button_forward = Button(self.master, text=">>", command=lambda: self.Forward(2))
        self.button_per = Button(self.master, text="PER", command=self.PER_NE)
        self.button_org = Button(self.master, text="ORG", command=self.ORG_NE)
        self.button_loc = Button(self.master, text="LOC", command=self.LOC_NE)
        self.button_savetags = Button(self.master, text="Save Current Tags", command=self.SaveTags)
        self.button_savefile = Button(self.master, text="Save File", command=self.SaveFile)
        self.button_openfile.grid(row=0,column=1)

    def OpenFile(self):
        self.master.filename = filedialog.askopenfilename(initialdir="/User/salmanmirza/FYP", title="Select a file...", filetypes=[('Excel Files', '*.xlsx')])
        data = pd.read_excel(self.master.filename, 'Sheet1')
        data  = pd.Series(data['sentences'])
        self.max_rows = len(data.index)
        self.sentences = data[0:]
        self.per_entities = [''] * (self.max_rows)
        self.org_entities = [''] * (self.max_rows) 
        self.loc_entities = [''] * (self.max_rows)
        self.button_openfile.grid_forget()
        self.status = Label(self.master, text="Sentence 1 of " + str(self.max_rows), bd=2, relief=SUNKEN, anchor=E)
        self.ShowSentences()

    def ShowSentences(self):
        self.sentence_text.insert(END, self.sentences[0])
        self.sentence_text.grid(row=0,column=0,columnspan=5)
        self.button_back.grid(row=1,column=0)
        self.button_per.grid(row=1,column=1)
        self.button_org.grid(row=1,column=2)
        self.button_loc.grid(row=1,column=3)
        self.button_forward.grid(row=1,column=4)
        self.button_savetags.grid(row=2,column=0)
        self.button_savefile.grid(row=2,column=1)
        self.status.grid(row=3,column=0, columnspan=5, sticky=E+W)
        
    def Forward(self, sen_no):
        self.SaveTags()
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.sentences[sen_no-1])
        self.current = sen_no-1
        self.sentence_text.grid(row=0,column=0,columnspan=5)
        if sen_no == self.max_rows:
            self.button_forward = Button(mainwindow, text=">>", state=DISABLED)
        else:
            self.button_forward = Button(mainwindow, text=">>", command=lambda: self.Forward(sen_no+1))
        self.button_back = Button(self.master, text="<<", command=lambda: self.Back(sen_no-1))
        self.button_back.grid(row=1,column=0)
        self.button_per.grid(row=1,column=1)
        self.button_org.grid(row=1,column=2)
        self.button_loc.grid(row=1,column=3)
        self.button_forward.grid(row=1,column=4)
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))

    def Back(self, sen_no):
        self.SaveTags()
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.sentences[sen_no-1])
        self.current = sen_no-1
        self.sentence_text.grid(row=0,column=0,columnspan=5)
        self.button_forward = Button(mainwindow, text=">>", command=lambda: self.Forward(sen_no+1))
        if sen_no == 1:
            self.button_back = Button(mainwindow, text="<<", state=DISABLED)
        else:
            self.button_back = Button(mainwindow, text="<<", command=lambda: self.Back(sen_no-1))
        self.button_back.grid(row=1,column=0)
        self.button_per.grid(row=1,column=1)
        self.button_org.grid(row=1,column=2)
        self.button_loc.grid(row=1,column=3)
        self.button_forward.grid(row=1,column=4)
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))

    def PER_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            self.persons.append(selected)
            print(selected)
        except:
            pass
    
    def ORG_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            self.organizations.append(selected)
            print(selected)
        except:
            pass
    
    def LOC_NE(self):
        try:
            selected = self.sentence_text.selection_get()
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
        self.persons.clear()
        self.organizations.clear()
        self.locations.clear()

    def SaveFile(self):
        self.SaveTags()
        print("\n")
        print(self.per_entities, self.org_entities, self.loc_entities)
        print(len(self.sentences),len(self.per_entities),len(self.org_entities),len(self.loc_entities))
        tagged_data = pd.DataFrame({"Sentences":self.sentences, "PER":self.per_entities, "ORG":self.org_entities, "LOC":self.loc_entities})
        tagged_data.to_excel("Tagged Data.xlsx")
        
        

#my_text = Text(root, width=40, height=10, selectbackground="yellow", selectforeground="black")
tagger = Tagger()
mainwindow.mainloop()