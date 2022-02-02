from cmath import nan
import tkinter as tk
from tkinter import ttk
from PyPDF2 import PdfFileReader, PdfFileWriter 
import os
import filetype


class app():
    def __init__(self):
        self.range_list = []
        self.list_pdf = []
        self.get_all_pdf()

        self.window = tk.Tk()
        self.window.title('Divide PDF App')
        self.window.geometry('280x550')
        self.window.resizable(0, 0)
        self.window.configure(background='white')


        self.header_label = tk.Label(self.window, text = 'Divide PDF')
        self.header_label.grid(row = 0, column= 0, sticky=tk.W)
        
        self.selected_frame = tk.Frame(self.window)
        self.selected_frame.grid(row = 1, column = 0, rowspan = 1 , columnspan = 2, sticky= tk.W)

        self.selectedPDF_label = tk.Label(self.selected_frame, text = "Choose PDF File")
        self.selectedPDF_label.grid(row = 1, column = 0, sticky = tk.W)

        self.selectedPDF = ttk.Combobox(self.selected_frame, values=self.list_pdf, width=23, state = "readonly")
        self.selectedPDF.grid(row = 1, column = 1)

        self.control_label_frame = tk.Frame(self.window)
        self.control_label_frame.grid(row = 2, column = 0, columnspan=2)

        self.start_range_label = tk.Label(self.control_label_frame, text='Starting Page :')
        self.start_range_label.grid(row = 2, column = 0, sticky=tk.N+tk.W)
        self.start_range_entry = tk.Entry(self.control_label_frame)
        self.start_range_entry.focus()
        self.start_range_entry.grid(row = 2, column = 1, sticky=tk.N+tk.W)

        self.end_range_label = tk.Label(self.control_label_frame, text= 'Ending Page :')
        self.end_range_label.grid(row = 3, column = 0, sticky = tk.N+tk.W)
        self.end_range_entry = tk.Entry(self.control_label_frame)
        self.end_range_entry.grid(row = 3, column = 1, sticky = tk.N+tk.W)


        self.control_range_frame = tk.Frame(self.window)
        self.control_range_frame.grid(row = 6, column= 0, columnspan = 2, sticky = tk.W)

        self.add_range_btn = tk.Button(self.control_range_frame, text = 'Add Range', command = self.add_range, width = 19)
        self.add_range_btn.grid(row = 6, column = 0, sticky=tk.W)

        self.remove_range_btn = tk.Button(self.control_range_frame, text = 'Remove Range', command = self.remove_range, width = 19)
        self.remove_range_btn.grid(row = 6, column = 1, sticky=tk.W)


        self.divide_btn = tk.Button(self.control_label_frame, text = 'Divide', command = self.divide, height = 2, width = 5)
        self.divide_btn.grid(row = 2, column = 2, rowspan= 2 , columnspan=2,  sticky = tk.E)

        self.text = tk.StringVar()

        self.result_label = tk.Label(self.window, textvariable = self.text, height=29, width=39, anchor=tk.NW)
        self.result_label.grid(row = 4, column = 0, sticky=tk.W + tk.N, rowspan=2, columnspan=2)
        
        self.text.set("Range :\nNone !")
        self.result_text = "Range :\n"

        self.widgets = [self.start_range_entry, self.end_range_entry, self.add_range_btn, self.remove_range_btn]
        for wl in self.widgets:
            wl.lift()

        self.window.mainloop()
    
    def get_all_pdf(self):
        allfile = os.listdir("./")
        for file in allfile:
            kind = filetype.guess(file)
            if (kind != None) and (kind.mime == 'application/pdf'):
                    self.list_pdf.append(file)

    def add_range(self):
        if self.start_range_entry.get() != nan and self.end_range_entry.get() != nan and self.start_range_entry.get().isdigit() and self.end_range_entry.get().isdigit():
            
            start = self.start_range_entry.get()
            end = self.end_range_entry.get()
            self.range_list.append([start, end])

            if len(self.range_list) == 0:
                self.result_text = "Range :\nNone !"
            else:
                self.result_text = "Range :\n"
            
            for i in self.range_list:
                self.result_text += "-".join(i) + "\n"
            self.text.set(self.result_text)

            self.end_range_entry.delete(0, 'end')
            self.start_range_entry.delete(0, 'end')
            self.start_range_entry.focus()

    def remove_range(self):
        if len(self.range_list) == 0:
            self.text.set("Range :\nNone !")
        else:
            self.range_list.pop()
            self.result_text = "Range :\n"
            for i in self.range_list:
                self.result_text += "-".join(i) + "\n"
            self.text.set(self.result_text)

    def divide(self):
        filename = self.selectedPDF.get()
        pdf_reader = PdfFileReader(filename)

        if filename.endswith(".pdf"):
            filename = filename.replace(".pdf", "")
        
        for r in self.range_list:
            pdf_writer = PdfFileWriter()
            for page in range(int(r[0])-1, int(r[1])):
                pdf_writer.addPage(pdf_reader.getPage(page))

            with open(filename + "{}".format("_" + r[0] + "-" + r[1]) +".pdf", 'wb') as out:
                pdf_writer.write(out)
    
if __name__ == '__main__':
    obj = app()