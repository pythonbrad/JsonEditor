from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showinfo
import json
import json_editor_toolkit as toolkit
import sys

class Gui:
    def __init__(self):
        self.master = Tk()
        self.master.title('Json editor.')

        self.tabs = 40
        self.file = None

        self.frame = Frame()
        self.frame.pack()

        self.text = Text(self.frame, tabs=self.tabs)
        self.text.pack(side=LEFT, fill=Y)
        self.text.tag_config('red', foreground='red')
        self.text.tag_config('blue', foreground='blue')
        self.text.tag_config('green', foreground='green')
        self.text.tag_config('orange', foreground='orange')

        self.yscrollbar = Scrollbar(self.frame, command=self.text.yview)
        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=self.yscrollbar.set)

        self.menubar = Menu()
        self.menufile = Menu(tearoff=False)
        self.menufile.add_command(label='Open', command=self.open)
        self.menufile.add_command(label='Save as', command=self.saveas)
        self.menufile.add_command(label='Save', command=self.save)

        self.menutext = Menu(tearoff=False)
        self.menutext.add_command(label='Verify the Json', command=self.json_verify)
        self.menutext.add_command(label='Correct errors Double quotes', command=self.json_correct_error_double_quote)
        self.menutext.add_command(label='Restore the original json', command=self.restore)

        self.menuconfig_indent_width = Menu(tearoff=False)
        self.menuconfig_indent_width.add_radiobutton(label='1 spaces', command=lambda:self.config_indent_width(1))
        self.menuconfig_indent_width.add_radiobutton(label='2 spaces', command=lambda:self.config_indent_width(2))
        self.menuconfig_indent_width.add_radiobutton(label='3 spaces', command=lambda:self.config_indent_width(3))
        self.menuconfig_indent_width.add_radiobutton(label='4 spaces', command=lambda:self.config_indent_width(4))
        self.menuconfig_indent_width.add_radiobutton(label='5 spaces', command=lambda:self.config_indent_width(5))
        self.menuconfig_indent_width.add_radiobutton(label='6 spaces', command=lambda:self.config_indent_width(6))
        self.menuconfig_indent_width.add_radiobutton(label='7 spaces', command=lambda:self.config_indent_width(7))
        self.menuconfig_indent_width.add_radiobutton(label='8 spaces', command=lambda:self.config_indent_width(8))
        self.menuconfig_indent_width.add_radiobutton(label='9 spaces', command=lambda:self.config_indent_width(9))
        self.menuconfig_indent_width.add_radiobutton(label='10 spaces', command=lambda:self.config_indent_width(10))
        
        self.menutext.add_cascade(label='config_indent_width', menu=self.menuconfig_indent_width)
        
        self.menubar.add_cascade(label='File', menu=self.menufile)
        self.menubar.add_cascade(label='Json', menu=self.menutext)

        self.auto_resize()

        self.master.geometry("200x200")

        self.master.config(menu=self.menubar)

    def auto_resize(self):
        self.text.config(
            width=int(self.master.winfo_width())-100,
            height=int(self.master.winfo_height())-100
            )
        self.master.after(500, self.auto_resize)

    def open(self):
        file = askopenfile(filetypes=[('Json','.json')], mode='rb')
        self.file = file
        if file:
            self.data_json = file.read().decode()
            self.write_json(self.data_json)
            file.close()
        
    def saveas(self):
        filename = asksaveasfilename(filetypes=[('Json','.json')], confirmoverwrite=True)
        if not '.json' in filename:
            filename += '.json'
        if filename:
            data_json = self.text.get(1.0,END)
            f = open(filename, 'wb')
            f.write(data_json.encode())
            f.close()

    def save(self):
        if self.file:
            data_json = self.text.get(1.0,END)
            f = open(self.file.name, 'wb')
            f.write(data_json.encode())
            f.close()
        else:
            showinfo(message='File not open')

    def restore(self):
        self.write_json(self.data_json)

    def organise(self, data_json):
        data_json = toolkit.del_space(data_json)
        data_json = toolkit.indent(data_json)
        return data_json

    def write_json(self, data_json):
        self.text.delete(1.0, END)
        data_json = self.organise(data_json)
        ####gu guillemet
        gu = False
        tag_color = None
        for i in data_json:
            if i in ['"']:
                self.text.insert(END, i, 'green')
                if gu:
                    tag_color = None
                    gu = False
                else:
                    tag_color = 'green'
                    gu = True
            elif i in ['{','}']:
                self.text.insert(END, i, 'red')
            elif i in ['[',']']:
                self.text.insert(END, i, 'blue')
            else:
                self.text.insert(END, i, tag_color)

    def json_verify(self):
        data_json = self.text.get(1.0,END)
        result = toolkit.verify(data_json)
        if result == True:
            showinfo(message="Json verify :\nSucceed")
        else:
            showinfo(message="Json verify Error:\n%s"%result)

    def config_indent_width(self, tabs):
        self.tabs = tabs * 10
        self.text.config(tabs=self.tabs)

    def json_correct_error_double_quote(self):
        data_json = self.text.get(1.0,END)
        new_data_json = toolkit.correct_error_double_quote(data_json)
        self.text.delete(1.0, END)
        self.write_json(new_data_json)

    def mainloop(self):
        self.master.mainloop()
        
if __name__ == '__main__':
    w=Gui()
    try:
        f = open(sys.argv[1], 'rb')
        w.data_json = f.read().decode()
        f.close()
        w.write_json(w.data_json)
    except Exception as e:
        print(e)
    w.mainloop()
