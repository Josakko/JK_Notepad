import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import filedialog

class JK_Notepad:
    def __init__(self, master):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        window_width = 1300
        window_hight = 800
        
        monitor_width = master.winfo_screenwidth()
        monitor_hight = master.winfo_screenheight()
        
        x = (monitor_width / 2) - (window_width / 2)
        y = (monitor_hight / 2) - (window_hight / 2)

        master.geometry(f'{window_width}x{window_hight}+{int(x)}+{int(y)}')
        master.title("Untitled - JK Notepad")
        master.iconbitmap("JK.ico")
        
        self.y_scrollbar = tk.Scrollbar(master)
        self.y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.x_scrollbar = tk.Scrollbar(master, orient=tk.HORIZONTAL)
        self.x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.textarea = tk.Text(master, undo=True, wrap=tk.NONE, yscrollcommand=self.y_scrollbar.set, xscrollcommand=self.x_scrollbar.set, font=("Arial", 14), fg="black", insertbackground="black", bg="#dbdbdb") #(master, undo=True, yscrollcommand=self.scrollbar.set, font=("Arial", 14), bg="#272727", fg="#fff", insertbackground="#fff")
        self.textarea.pack(expand=True, fill='both')
        
        self.y_scrollbar.config(command=self.textarea.yview)
        self.x_scrollbar.config(command=self.textarea.xview)
        
        self.filename = None
        
        self.menubar = tk.Menu(master)
        
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        
        self.filemenu.add_command(label="New", command=self.new_file)
        self.filemenu.add_command(label="Open", command=self.open_file)
        self.filemenu.add_command(label="Save", command=self.save_file)
        self.filemenu.add_command(label="Save As", command=self.save_as)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.on_closing)
        
        
        self.editmenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        
        self.editmenu.add_command(label="Undo", command=self.textarea.edit_undo)
        self.editmenu.add_command(label="Redo", command=self.textarea.edit_redo)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Cut", command=self.cut)
        self.editmenu.add_command(label="Copy", command=self.copy)
        self.editmenu.add_command(label="Paste", command=self.paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Find", command=self.show_search_popup)
        
        self.viewmenu = tk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)
        
        self.viewmenu.add_command(label="Clear", command=self.clear)
        self.viewmenu.add_separator()
        self.viewmenu.add_command(label="Zoom In", command=self.zoom_in)
        self.viewmenu.add_command(label="Zoom Out", command=self.zoom_out)
        self.viewmenu.add_command(label="Reset Zoom", command=self.reset_zoom)
        

        master.config(menu=self.menubar)

        popup_width = 320
        popup_hight = 70
        
        xp = (monitor_width / 2) - (popup_width / 2)
        yp = (monitor_hight / 2) - (popup_hight / 2) - 300
        
        self.search_popup = tk.Toplevel(self.master)
        self.search_popup.withdraw()
        self.search_popup.iconbitmap("JK.ico")
        self.search_popup.resizable(False, False)
        self.search_popup.geometry(f'{popup_width}x{popup_hight}+{int(xp)}+{int(yp)}')
        self.search_popup.title("Find")

        self.search_label = tk.Label(self.search_popup, text="Find:")
        self.search_label.pack(side=tk.LEFT, padx=(5, 0), pady=5)

        self.search_entry = tk.Entry(self.search_popup, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        self.search_entry.bind("<Return>", self.find_text)
        self.search_entry.bind("<Escape>", self.close_search_popup)

        self.find_button = tk.Button(self.search_popup, text="Find", command=self.find_text)
        self.find_button.pack(side=tk.LEFT, pady=20)

        #self.find_prev_button = tk.Button(self.search_popup, text="Find Previous", command=self.find_previous)
        #self.find_prev_button.pack(side=tk.LEFT, pady=20)

        self.close_search_popup_button = tk.Button(self.search_popup, text="Close", command=self.close_search_popup)
        self.close_search_popup_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        
    base_font_size = 14
    zoom_factor = 0
    #print(zoom_factor)

    def zoom_in(self, event=None):
        self.zoom_factor += 0.9
        #print("factor", self.zoom_factor)
        zoom = int(self.base_font_size * self.zoom_factor)
        #print("zoom", zoom)
        self.textarea.config(font=("Arial", zoom))#int(self.base_font_size * zoom_factor))) 

    def zoom_out(self, event=None):
        self.zoom_factor -= 0.3
        #print("factor", self.zoom_factor)
        if self.zoom_factor < 0:
            zoom = 5
            #print("zoom", zoom)
        else:
            zoom = int(self.base_font_size * self.zoom_factor)
            #print("zoom", zoom)
            
        self.textarea.config(font=("Arial", zoom))#int(self.base_font_size * zoom_factor)))

    def reset_zoom(self):
        self.zoom_factor = 0.9
        self.textarea.config(font=("Arial", self.base_font_size)) 

    def show_search_popup(self):
        self.search_popup.deiconify()
        self.search_entry.focus_set()

    def close_search_popup(self, event=None):
        self.search_popup.withdraw()
        self.textarea.focus_set()

    def find_text(self):
        search_term = self.search_entry.get()
        text_widget = self.textarea
        text_widget.tag_remove("search", "1.0", "end")

        if search_term:
            idx = "1.0"
            while True:
                idx = text_widget.search(search_term, idx, nocase=1, stopindex="end")
                if not idx:
                    break

                end_idx = f"{idx}+{len(search_term)}c"
                text_widget.tag_add("search", idx, end_idx)
                idx = end_idx

            text_widget.tag_config("search", background="yellow")

        self.search_entry.focus_set()

    def clear(self):
        text_widget = self.textarea
        text_widget.tag_remove("search", "1.0", "end")
        text_widget.tag_config("search", background="white")

    #def find_previous(self):
    #    search_term = self.search_entry.get()
    #    text_widget = self.textarea
    #    text_widget.tag_remove("search", "1.0", "end")
    #
    #    if search_term:
    #        idx = "1.0"
    #        while True:
    #            idx = text_widget.search(search_term, idx, nocase=1, stopindex="end", backwards=True)
    #            if not idx:
    #                break
    #
    #            end_idx = f"{idx}+{len(search_term)}c"
    #            text_widget.tag_add("search", idx, end_idx)
    #            idx = idx
    #
    #       text_widget.tag_config("search", background="yellow")
    #
    #    self.search_entry.focus_set()

    def on_closing(self):
        if self.is_saved():
            self.master.destroy()
    
    def is_saved(self):
        if self.filename is not None:
            try:
                with open(self.filename,  encoding="utf-8") as f:
                    if self.textarea.get(1.0, tk.END) == f.read():
                        return True
                    else:
                        answer = messagebox.askyesnocancel(title="Notepad", message="Do you want to save changes to " + self.filename + "?")
                        if answer is not None:
                            if answer:
                                self.save_file()
                                return True
                            else:
                                return True
                        else:
                            return False
            except:
                answer = messagebox.askyesno("Error", "Encoding of selected file is not correct, do you want to exit?")
                if answer is not False:
                    exit()
                else:
                    return
        else:
            if len(self.textarea.get(1.0, tk.END).strip()) == 0:
                return True
            else:
                answer = messagebox.askyesnocancel(title="Notepad", message="Do you want to save changes to Untitled?")
                if answer is not None:
                    if answer:
                        self.save_as()
                        return True
                    else:
                        return True
                else:
                    return False
    
    def new_file(self):
        if self.is_saved():
            self.filename = None
            self.master.title("Untitled - Notepad")
            self.textarea.delete(1.0, tk.END)

    def open_file(self):
        if self.is_saved():
            file = filedialog.askopenfile(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
            if file:
                self.filename = file.name
                self.master.title(f"{self.filename} - Notepad")
                self.textarea.delete(1.0, tk.END)
                #self.textarea.insert(tk.END, file.read())
                try:
                    with open(self.filename, "r", encoding="utf-8") as f:
                        self.textarea.insert(tk.END, f.read())
                except:
                    messagebox.showerror("Error", "Encoding of selected file is not correct!")

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.textarea.get(1.0, tk.END))
            self.master.title(self.filename + " - Notepad")
        else:
            self.save_as()

    def save_as(self):
        file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if file:
            self.filename = file.name
            with open(self.filename, "w", encoding="utf-8") as f:
                f.write(self.textarea.get(1.0, tk.END))
            self.master.title(self.filename + " - Notepad")

    def cut(self):
        self.textarea.event_generate("<<Cut>>")

    def copy(self):
        self.textarea.event_generate("<<Copy>>")

    def paste(self):
        self.textarea.event_generate("<<Paste>>")
    

root = tk.Tk()
JK_Notepad = JK_Notepad(root)
root.mainloop()
