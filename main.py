import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.pdfgen import canvas


# Define the Notepad along with its functionalities
class Notepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad")
        self.master.geometry("800x600")
        self.master.configure(bg="#2b2b2b")

        self.text = tk.Text(self.master, bg="#1e1e1e", fg="white", insertbackground="white", font=("Arial", 12))
        self.text.pack(expand=True, fill="both")

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

        self.filename = None

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

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()