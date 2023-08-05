import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import ttk
from tkinter import font
from reportlab.pdfgen import canvas
import winsound

class Notepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad")
        self.master.geometry("800x600")
        self.master.configure(bg="#2b2b2b")

        self.text = tk.Text(self.master, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
        self.text.pack(expand=True, fill="both")
        self.text.bind("<Key>", self.play_typing_sound)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Export to PDF", command=self.export_to_pdf)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Change Background", command=self.change_background)
        self.settings_menu.add_command(label="Toggle Typing Sound", command=self.toggle_typing_sound)
        self.settings_menu.add_command(label="Change Font", command=self.change_font)
        self.settings_menu.add_command(label="Set Background Image", command=self.set_background_image)

        self.filename = None
        self.typing_sound_enabled = True

    def new_file(self):
        self.text.delete("1.0", tk.END)
        self.filename = None

    def open_file(self):
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Open file", filetypes=filetypes)
        if filename:
            with open(filename, "r") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert("1.0", f.read())
            self.filename = filename

    def save_file(self):
        if self.filename:
            with open(self.filename, "w") as f:
                f.write(self.text.get("1.0", tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
        filename = filedialog.asksaveasfilename(title="Save file as", filetypes=filetypes)
        if filename:
            with open(filename, "w") as f:
                f.write(self.text.get("1.0", tk.END))
            self.filename = filename

    def export_to_pdf(self):
        if not self.filename:
            messagebox.showerror("Error", "Please save the file first.")
            return

        pdf_filename = filedialog.asksaveasfilename(title="Export to PDF", defaultextension=".pdf")
        if pdf_filename:
            c = canvas.Canvas(pdf_filename)
            text_lines = self.text.get("1.0", tk.END).split("\n")
            text_lines = [line.strip() for line in text_lines]
            text_lines = [line for line in text_lines if line]
            c.drawString(50, 750, self.filename)
            c.drawString(50, 700, "\n".join(text_lines))
            c.save()

    def play_typing_sound(self, event):
        if self.typing_sound_enabled:
            winsound.PlaySound("keyboard.wav", winsound.SND_ASYNC)

    def change_background(self):
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            self.text.configure(bg=color[1])

    def toggle_typing_sound(self):
        self.typing_sound_enabled = not self.typing_sound_enabled

    def change_font(self):
        font = tk.font.Font(family="Arial", size=12)
        font_tuple = tk.font.families()
        selected_font = tk.font.Font(family=font.cget("family"), size=font.cget("size"))
        font_dialog = tk.Toplevel(self.master)
        font_dialog.title("Choose Font")
        font_dialog.geometry("400x300")
        font_dialog.configure(bg="#2b2b2b")

        font_family_label = tk.Label(font_dialog, text="Font Family:", bg="#2b2b2b", fg="white")
        font_family_label.pack()

        font_family_combobox = ttk.Combobox(font_dialog, values=font_tuple, font=selected_font)
        font_family_combobox.pack()

        font_size_label = tk.Label(font_dialog, text="Font Size:", bg="#2b2b2b", fg="white")
        font_size_label.pack()

        font_size_entry = tk.Entry(font_dialog, font=selected_font)
        font_size_entry.pack()

        def apply_font():
            selected_family = font_family_combobox.get()
            selected_size = font_size_entry.get()
            if selected_family and selected_size:
                self.text.configure(font=(selected_family, int(selected_size)))
            font_dialog.destroy()

        apply_button = tk.Button(font_dialog, text="Apply", command=apply_font)
        apply_button.pack()

    def set_background_image(self):
        image_filetypes = (("Image files", "*.jpg;*.jpeg;*.png;*.gif"), ("All files", "*.*"))
        image_filename = filedialog.askopenfilename(title="Choose Background Image", filetypes=image_filetypes)
        if image_filename:
            try:
                image = tk.PhotoImage(file=image_filename)
                self.text.image_create(tk.END, image=image)
                self.text.configure(bg="white")
            except tk.TclError:
                messagebox.showerror("Error", "Invalid image file.")


if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()