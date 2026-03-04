from tkinter import *
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter
import os

def pdf_split():

    path = archive_var.get()

    if not path:
        messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        return
    
    try:
        reader = PdfReader(path)
    except:
        messagebox.showerror("Erro", "Não foi possível abrir o PDF")
        return
    
    pages_total = len(reader.pages)

    try:
        pages_per_pdf = int(pages_entry.get())
    except:
        messagebox.showerror("Erro", "Digite um número válido.")
        return
    
    interval = interval_var.get()

    if interval:
        try:
            page_start = int(start_entry.get()) - 1
            page_end = int(end_entry.get())
        except:
            messagebox.showerror("Erro", "Intervalo inválido.")
            return
        
        if page_end > pages_total:
            page_end = pages_total
    else:
        page_start = 0
        page_end = pages_total
    
    count = 1

    for i in range(page_start, page_end, pages_per_pdf):

        writer = PdfWriter()

        for j in range(i, i + pages_per_pdf):
            if j < page_end:
                writer.add_page(reader.pages[j])
        
        exit_name = f"arquivo_separado_{count}.pdf"

        with open(exit_name, "wb") as new_pdf:
            writer.write(new_pdf)

        count += 1

    messagebox.showinfo("Sucesso!", "Seu PDF foi separado!")

def drop(event):
        archive_var.set(event.data.strip("{}"))
    

root = TkinterDnD.Tk()
root.title("Separador de PDF")
root.geometry("400x400")

archive_var = StringVar()
interval_var = BooleanVar()

Label(root, text = "Arraste o PDF aqui").pack(pady=10)

archive_entry = Entry(root, textvariable=archive_var, width=40)
archive_entry.pack(pady=5)

archive_entry.drop_target_register(DND_FILES)
archive_entry.dnd_bind("<<Drop>>", drop)

Label(root, text="Páginas por arquivo:").pack()
pages_entry = Entry(root)
pages_entry.pack(pady=5)

Checkbutton(root, text="Usar intervalo especifico", variable=interval_var).pack(pady=5)

Label(root, text="Página inicial:").pack()
start_entry = Entry(root)
start_entry.pack()

Label(root, text="Página final:").pack()
end_entry = Entry(root)
end_entry.pack()

Button(root, text="Separar PDF", command=pdf_split).pack(pady=20)

root.mainloop()

 


