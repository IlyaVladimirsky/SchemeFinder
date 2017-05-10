import threading
from tkinter import Tk, Label, Button, Entry, Frame, StringVar, RIDGE, LEFT
from tkinter.ttk import Combobox

from src.finder import SchemeFinder
from src.operations import Operation
from src.schema import Node


class FinderGUI:
    def __init__(self, master):
        self.master = master
        self.working_thread = None
        self.wf_text_var = StringVar()

        self.input_frame = Frame(master)
        self.button_frame = Frame(master)
        self.output_frame = Frame(master)

        master.title("Schema finder")
        master.geometry('{}x{}'.format(1000, 500))
        master.resizable(width=False, height=False)

        wf_label = Label(self.input_frame, text='w(f): ')
        self.wf_input = Entry(self.input_frame, width=50, textvariable=self.wf_text_var)
        self.wf_text_var.set('00000000')
        wf_label.grid(row=0, column=0)
        self.wf_input.grid(row=0, column=1)

        basis_label = Label(self.input_frame, text='базис: ')
        self.basis_box = Combobox(self.input_frame, values=('K2', 'K2 + M2'))
        self.basis_box.set('K2')
        basis_label.grid(row=1, column=0)
        self.basis_box.grid(row=1, column=1)

        var_label = Label(self.input_frame, text='количество переменных: ')
        self.var_box = Combobox(self.input_frame, values=('3', '4'))
        self.var_box.set('4')
        var_label.grid(row=2, column=0)
        self.var_box.grid(row=2, column=1)

        self.resume_button = Button(self.input_frame, text="далее", command=self.resume)
        self.pause_button = Button(self.input_frame, text="пауза", command=self.pause)
        self.close_button = Button(self.input_frame, text="закрыть", command=self.on_close)
        self.find_button = Button(self.input_frame, text="поиск", command=self.find_click)

        self.output_label = Label(self.output_frame, height=20, text='', justify=LEFT, anchor='nw', relief=RIDGE, width=80)
        self.output_label.grid(row=0, sticky='nw')

        self.resume_button.grid(row=1, column=3, padx=20)
        self.pause_button.grid(row=1, column=4, padx=20)
        self.close_button.grid(row=1, column=5, padx=20)
        self.find_button.grid(row=2, column=4, padx=20)

        self.input_frame.grid(row=0, padx=50, pady=50)
        self.output_frame.grid(row=2)

        self.state = False
        master.bind("<F11>", self.toggle_fullscreen)
        master.bind("<Escape>", self.end_fullscreen)

        conj = Operation('conjunction', 2)
        disj = Operation('disjunction', 2)
        mod = Operation('mod', 2)
        neg = Operation('negation', 1)

        classic_basis = [
            Node(conj.func, conj.in_count),
            Node(disj.func, disj.in_count),
            Node(neg.func, neg.in_count),
        ]

        self.basises = {
            'K2': classic_basis,
            'K2 + M2': classic_basis + [Node(mod.func, mod.in_count)]
        }

        self.finder = SchemeFinder(
            basis=classic_basis,
            unipolar=True,
            var_count=int(self.var_box.get()),
            wf=self.wf_input.get(),
            output=self.output_label
        )

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.master.attributes('-zoomed', self.state)

        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.master.attributes('-zoomed', False)

        return "break"

    def resume(self):
        self.finder.running = True

    def pause(self):
        self.finder.running = False

    def on_close(self):
        if self.finder.all_minimal_file:
            self.finder.all_minimal_file.close()
            self.finder.save_state()

        self.master.quit()

    def find_click(self):
        def worker():
            # global self
            self.finder.find()

        self.finder.var_count = int(self.var_box.get())
        self.finder.basis = self.basises[self.basis_box.get()]
        self.finder.wf = self.wf_input.get()

        self.working_thread = threading.Thread(target=worker, daemon=True)
        self.working_thread.start()


root = Tk()
# root.resizable(width=False, height=False)
my_gui = FinderGUI(root)
root.mainloop()