"""
..::Integral Numerical::..

Author : Alireza Molaee		Author Email : alirezamolaii@gmail.com
Professor : Dr.Ebrahimi

goal of this program is calculate integral by using numerical method.
this program input is an equation that we need integral of that or table of
x and f(x).
the out put is integral of equation or data of table.
"""

# using Tkinter and numpy library
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
from calculating import IntegralNumerical


class EntryField(Frame):
    def __init__(self, parent, label, labelwidth=12):
        Frame.__init__(self, parent)
        l = Label(self, text=label, anchor=W, width=labelwidth)
        l.pack(side=LEFT)
        self.str_var = StringVar(self)
        en = Entry(self, textvariable=self.str_var)
        en.pack(side=RIGHT, fill=X)
    
    def get_value(self):
        return self.str_var.get()


class EntryFloatField(Frame):
    def __init__(self, parent, label, labelwidth=12):
        Frame.__init__(self, parent)
        l = Label(self, text=label, anchor=W, width=labelwidth)
        l.pack(side=LEFT)
        self.float_var = DoubleVar(self)
        en = Entry(self, textvariable=self.float_var)
        en.pack(side=RIGHT, fill=X)

    def get_value(self):
        return self.float_var.get()
    

class RadioFieldVertical(Frame):
    def __init__(self, parent, label, choices, defult, labelwidth=12):
        Frame.__init__(self, parent)
        l = Label(self, text=label, anchor=N, width=labelwidth)
        l.pack(side=TOP)
        self.choice = StringVar(self, defult)
        for choice in choices:
            rb = Radiobutton(self, text=choice, variable=self.choice, value=choice)
            rb.pack(side=TOP, anchor=W, expand=True)
            
    def get_value(self):
        return self.choice.get()
            

class ButtonList(Frame):
    def __init__(self, parent, buttons):
        Frame.__init__(self, parent)
        for b in buttons:
            Button(self, text=b[0], command=b[1]).pack(side=TOP, fill=X, pady=1)
            
            
class CalculateSetting(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.rad1 = RadioFieldVertical(self, "solving methodes", ['left hand', 'right hand', 'mid point', 'trapezoidal', 'simpson'], 'simpson')
        self.rad1.pack(side=LEFT, anchor=W, fill=Y, pady=10, padx=5)

        self.rad2 = RadioFieldVertical(self, "data from", ['file', 'equation'], 'equation')
        self.rad2.pack(side=TOP, anchor=W, pady=10, padx=5)

        self.but = ButtonList(self, [('next', lambda:self.next()), ('close', lambda:self.close(),)])
        self.but.pack(side=BOTTOM, anchor=S, fill=X, expand=True, padx=5, pady=5)
        
        self.result_row = Frame(self).pack(side=BOTTOM, fill=X)

    solving_obj = None
    result_label = None        
        
    def next(self):
        rad1 = self.rad1.get_value()
        rad2 = self.rad2.get_value()
        if rad1 == 'mid point' and rad2 == 'file':
            tkMessageBox.showerror('file data error', message="for this method you can't use data from file. you can chose equation.", )
        else:
            if rad2 == 'file':
                path = askopenfilename()
                self.solving_obj = IntegralNumerical(path=path)
                self.show_result()
            else:
                self.show_eq_fram()

    def show_eq_fram(self):
        top = Toplevel()
        eq = EntryField(top, 'equation')
        eq.pack(side=TOP, fill=X, pady=5, padx=5)

        a = EntryField(top, 'a')
        a.pack(side=TOP, fill=X, pady=5, padx=5)

        b = EntryField(top, 'b')
        b.pack(side=TOP, fill=X, pady=5, padx=5)

        delta = EntryField(top, 'delta')
        delta.pack(side=TOP, fill=X, pady=5, padx=5)

        Button(top, text='ok', command=lambda:self.set_eq_to_obj(eq, a, b, delta, top)).pack(side=BOTTOM, fill=X, padx=30, pady=5)
        # top.mainloop()
        top.grab_set()
        
    def set_eq_to_obj(self, eq_w, a_w, b_w, d_w, top):
        eq = eq_w.get_value()
        a = a_w.get_value()
        b = b_w.get_value()
        d = d_w.get_value()
        top.grab_release()
        top.destroy()
        if eq:
            self.solving_obj = IntegralNumerical(equation=eq, a=a, b=b, delta=d)
            self.show_result()
               
    def get_result(self):
        method = self.rad1.get_value()
        result = 0
        if method == 'left hand':
            result = self.solving_obj.left_hand()
        elif method == 'right hand':
            result = self.solving_obj.right_hand()
        elif method == 'mid point':
            result = self.solving_obj.mid_point()
        elif method == 'trapezoidal':
            result = self.solving_obj.trapezoidal()
        elif method == 'simpson':
            result = self.solving_obj.simpson()
        return result
        
    def show_result(self):
        result = self.get_result()
        if self.result_label is None:
            self.result_label = Label(self.result_row, text=str(result), fg='blue')
            Label(self.result_row, text="result :").pack(side=LEFT, anchor=E, pady=10)
            self.result_label.pack(side=RIGHT, anchor=W, expand=TRUE, pady=10)
        else:
            self.result_label.configure(text=str(result))
    
    @staticmethod
    def close():
        root.destroy()
        
root = Tk()
root.wm_title("numerical integration")
root.resizable(width='FALSE', height='FALSE')

w = 440  # width for the Tk root
h = 200  # height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

logo = PhotoImage(file="logo.gif")
w1 = Label(root, image=logo).pack(side="left", anchor=N)

CalculateSetting(root).pack()

mainloop()


