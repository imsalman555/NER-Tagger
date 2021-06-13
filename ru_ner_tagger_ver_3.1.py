# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 16:06:19 2021

@author: salmanmirza
"""

from tkinter import *
from tkinter import filedialog
import pandas as pd
import getpass
import os
import copy

mainwindow = Tk()
mainwindow.title('RU NER - Tagging Tool')
mainwindow.geometry("800x440")
mainwindow.resizable(0,0)
mainwindow.config(bg='#1E1128')

class Tagger:
    def __init__(self):
        self.master = mainwindow
        self.max_rows = 0
        self.current = 0
        self.sentences = None
        self.tagged_sentences = None
        #self.persons = []
        #self.per_entities = None
        #self.organizations = []
        #self.org_entities = None
        #self.locations = []
        #self.loc_entities = None
        self.isTagged = None
        # self.per_count = None
        # self.org_count = None
        # self.loc_count = None
        self.sentence_text = Text(self.master, width=70, height=13, font=("Trebuchet MS",13), bg='#DFCBEE', wrap=WORD, selectbackground="black", selectforeground="white")
        self.button_openfile = Button(self.master, text="Start Tagging", command=self.OpenFile, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 10, "bold"))
        #self.button_editfile = Button(self.master, text="Edit Tagging", command=lambda:self.OpenFile(2), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 10, "bold"))
        self.button_back = Button(self.master, text="<<", state=DISABLED, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_forward = Button(self.master, text=">>", command=lambda: self.Forward(2), bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_per = Button(self.master, text="PER", command=self.PER_NE, bg='#32a852', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_org = Button(self.master, text="ORG", command=self.ORG_NE, bg='#3267a8', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_loc = Button(self.master, text="LOC", command=self.LOC_NE, bg='#e8e15f', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_removetags = Button(self.master, text="Remove Tags", command=self.RemoveTags, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_savefile = Button(self.master, text="Save File", command=self.SaveFile, bg='#9657C7', fg='white', height=2, width=10, font=("Verdana", 8, "bold"))
        self.button_openfile.grid(row=0,column=1, padx=265, pady=195, columnspan=2)
        #self.button_editfile.grid(row=1,column=1, padx=5, pady=5, columnspan=2)

    def OpenFile(self):
        username = getpass.getuser()
        try:
            self.master.filename = filedialog.askopenfilename(initialdir="/User/{}".format(username), title="Select a file...", filetypes=[('Excel file', '*.xlsx'),('csv file','*.csv')])
            #if id==1:
            self.ReadData()
            # elif id==2:
            #     self.EditData()
        except:
            print("Choose File...")
            self.button_openfile.grid_forget()
            #self.button_editfile.grid_forget()
            self.button_openfile.grid(row=0,column=1, padx=5, pady=5, columnspan=2)
            #self.button_editfile.grid(row=1,column=1, padx=5, pady=5, columnspan=2)
        
            
    def ReadData(self):
        data = pd.read_excel(self.master.filename)
        data  = pd.Series(data['Sentences'])
        self.max_rows = len(data.index)
        self.sentences = data[0:]
        self.tagged_sentences = copy.copy(data[0:])
        #self.per_entities = [''] * (self.max_rows)
        #self.org_entities = [''] * (self.max_rows) 
        #self.loc_entities = [''] * (self.max_rows)
        self.isTagged = [False] * (self.max_rows)
        # self.per_count = [0] * (self.max_rows)
        # self.org_count = [0] * (self.max_rows)
        # self.loc_count = [0] * (self.max_rows)
        self.button_openfile.grid_forget()
        #self.statustags = Label(self.master, text="PER: , ORG: , LOC: ", bd=2, relief=SUNKEN, anchor=W, bg='#632E8B', fg='white', justify=LEFT, wraplength=550)
        self.status = Label(self.master, text="Sentence 1 of " + str(self.max_rows), bd=2, relief=SUNKEN, anchor=E, bg='#632E8B', fg='white')
        self.ShowSentences()
        

    def ShowSentences(self):
        self.sentence_text.insert(END, self.tagged_sentences[0])
        self.sentence_text.grid(row=0,column=0,columnspan=5, padx=5, pady=5)
        self.button_back.grid(row=1,column=0, padx=5, pady=5)
        self.button_per.grid(row=1,column=1, padx=5, pady=5)
        self.button_org.grid(row=1,column=2, padx=5, pady=5)
        self.button_loc.grid(row=1,column=3, padx=5, pady=5)
        self.button_forward.grid(row=1,column=4, padx=5, pady=5)
        self.button_removetags.grid(row=2,column=1, padx=5, pady=5)
        self.button_savefile.grid(row=2,column=3, padx=5, pady=5)
        #self.statustags.grid(row=3,column=0, columnspan=5, sticky=E+W, padx=5, pady=5)
        self.status.grid(row=3,column=0, columnspan=5, sticky=E+W, padx=5, pady=5)
        
    def Forward(self, sen_no):
        self.SaveTags()
        self.current = self.current + 1
        # if self.per_entities[self.current] == '':
        #     self.persons.clear()
        # else:
        #     self.persons = self.per_entities[self.current].split(',')
        # if self.org_entities[self.current] == '':
        #     self.organizations.clear()
        # else:
        #     self.organizations = self.org_entities[self.current].split(',')
        # if self.loc_entities[self.current] == '':
        #     self.locations.clear()
        # else:
        #     self.locations = self.loc_entities[self.current].split(',')
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.tagged_sentences[sen_no-1])
        if self.isTagged[self.current] == True:
            self.sentence_text.configure(fg="gray")
            self.sentence_text.bindtags((str(self.sentence_text), str(self.master), "all"))
            self.button_removetags["state"]="normal"
        else:
            self.sentence_text.configure(fg="black")
            self.sentence_text.bindtags((self.sentence_text, "Text", self.master, "all"))
            self.button_removetags["state"]="disabled"
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
        #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(self.per_entities[self.current], self.org_entities[self.current], self.loc_entities[self.current]))
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))

    def Back(self, sen_no):
        self.SaveTags()
        self.current = self.current - 1
        # if self.per_entities[self.current] == '':
        #     self.persons.clear()
        # else:
        #     self.persons = self.per_entities[self.current].split(',')
        # if self.org_entities[self.current] == '':
        #     self.organizations.clear()
        # else:
        #     self.organizations = self.org_entities[self.current].split(',')
        # if self.loc_entities[self.current] == '':
        #     self.locations.clear()
        # else:
        #     self.locations = self.loc_entities[self.current].split(',')
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.tagged_sentences[sen_no-1])
        if self.isTagged[self.current] == True:
            self.sentence_text.configure(fg="gray")
            self.sentence_text.bindtags((str(self.sentence_text), str(self.master), "all"))
            self.button_removetags["state"]="normal"
        else:
            self.sentence_text.configure(fg="black")
            self.sentence_text.bindtags((self.sentence_text, "Text", self.master, "all"))
            self.button_removetags["state"]="disabled"
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
        #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(self.per_entities[self.current], self.org_entities[self.current], self.loc_entities[self.current]))
        self.status.config(text="Sentence " + str(sen_no) + " of " + str(self.max_rows))
        
    def float(self, num):
        return num

    def PER_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            first = int(str(self.sentence_text.index("sel.first"))[2:])
            last = int(str(self.sentence_text.index("sel.last"))[2:])
            #self.persons.append(selected)
            if selected.startswith('<PER--')==True and selected.endswith('>')==True:
                selected = selected.replace('<PER--','')
                selected = selected.replace('>','')
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + selected + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            elif selected.startswith('<PER--')==False and selected.endswith('>')==False:
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + "<PER--" + selected + ">" + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(','.join(self.persons),','.join(self.organizations),','.join(self.locations)))
        except:
            pass
    
    def ORG_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            first = int(str(self.sentence_text.index("sel.first"))[2:])
            last = int(str(self.sentence_text.index("sel.last"))[2:])
            #self.organizations.append(selected)
            if selected.startswith('<ORG--')==True and selected.endswith('>')==True:
                selected = selected.replace('<ORG--','')
                selected = selected.replace('>','')
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + selected + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            elif selected.startswith('<ORG--')==False and selected.endswith('>')==False:
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + "<ORG--" + selected + ">" + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(','.join(self.persons),','.join(self.organizations),','.join(self.locations)))
        except:
            pass
    
    def LOC_NE(self):
        try:
            selected = self.sentence_text.selection_get()
            first = int(str(self.sentence_text.index("sel.first"))[2:])
            last = int(str(self.sentence_text.index("sel.last"))[2:])
            #self.locations.append(selected)
            if selected.startswith('<LOC--')==True and selected.endswith('>')==True:
                selected = selected.replace('<LOC--','')
                selected = selected.replace('>','')
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + selected + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            elif selected.startswith('<LOC--')==False and selected.endswith('>')==False:
                self.tagged_sentences[self.current] = self.tagged_sentences[self.current][:first] + "<LOC--" + selected + ">" + self.tagged_sentences[self.current][last:]
                self.sentence_text.delete(1.0,END)
                self.sentence_text.insert(END, self.tagged_sentences[self.current])
            #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(','.join(self.persons),','.join(self.organizations),','.join(self.locations)))
        except:
            pass
        
    def SaveTags(self):
        # self.per_entities[self.current] = ','.join(self.persons)
        # if self.per_entities[self.current] != '':
        #     self.per_count[self.current] = len(self.per_entities[self.current].split(','))
        # else:
        #     self.per_count[self.current] = 0
        # self.org_entities[self.current] = ','.join(self.organizations)
        # if self.org_entities[self.current] != '':
        #     self.org_count[self.current] = len(self.org_entities[self.current].split(','))
        # else:
        #     self.org_count[self.current] = 0
        # self.loc_entities[self.current] = ','.join(self.locations)
        # if self.loc_entities[self.current] != '':
        #     self.loc_count[self.current] = len(self.loc_entities[self.current].split(','))
        # else:
        #     self.loc_count[self.current] = 0
        self.isTagged[self.current] = True
        
    def RemoveTags(self):
        # self.persons.clear()
        # self.organizations.clear()
        # self.locations.clear()
        self.tagged_sentences[self.current] = self.sentences[self.current]
        self.sentence_text.delete(1.0,END)
        self.sentence_text.insert(END, self.tagged_sentences[self.current])
        self.sentence_text.bindtags((self.sentence_text, "Text", self.master, "all"))
        self.sentence_text.configure(fg="black")
        self.button_removetags["state"]="disabled"
        self.isTagged[self.current] = False
        #self.statustags.config(text="PER: {}, ORG: {}, LOC: {}".format(','.join(self.persons),','.join(self.organizations),','.join(self.locations)))

    def SaveFile(self):
        self.SaveTags()
        #print("\n")
        #print(len(self.per_entities), len(self.org_entities), len(self.loc_entities))
        #print(self.per_entities, self.org_entities, self.loc_entities)
        tagged_data = pd.DataFrame({"Sentences":self.sentences, "Tagged":self.tagged_sentences})
        try:
            filename = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("excel files", '*.xlsx')], title="Choose filename")
            tagged_data.to_excel(filename)
            messagebox.showinfo("Alert!", "Tagged data have been saved.")
        except:
            self.SaveTags()
            self.button_savefile.grid_forget()
            self.button_savefile.grid(row=2,column=3, padx=5, pady=5)
            
tagger = Tagger()
mainwindow.mainloop()