
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def pdf_split():

    path = archive_var.get()

    if not path:
        status_label.configure(text="Selecione um PDF primeiro", text_color="red")
        return

    if not os.path.exists(path):
        status_label.configure(text="Arquivo não encontrado", text_color="red")
        return

    try:
        reader = PdfReader(path)
    except:
        status_label.configure(text="Erro ao abrir PDF.", text_color="red")
        return

    pages_total = len(reader.pages)

    try:
        pages_per_pdf = int(pages_entry.get())
        if pages_per_pdf <= 0:
            raise ValueError
    except:
        status_label.configure(text="Número inválido.", text_color="red")
        return

    interval = interval_var.get()

    if interval:
        try:
            page_start = int(start_entry.get()) - 1
            page_end = int(end_entry.get())

            if page_start < 0 or page_end > pages_total or page_start >= page_end:
                raise ValueError

        except:
            status_label.configure(text="Intervalo inválido.", text_color="red")
            return
    else:
        page_start = 0
        page_end = pages_total

    base_name = os.path.splitext(os.path.basename(path))[0]
    parent_dir = os.path.dirname(path)
    output_folder = os.path.join(parent_dir, base_name)

    os.makedirs(output_folder, exist_ok=True)

    count = 1

    for i in range(page_start, page_end, pages_per_pdf):

        writer = PdfWriter()

        for j in range(i, i + pages_per_pdf):
            if j < page_end:
                writer.add_page(reader.pages[j])

        exit_name = os.path.join(
            output_folder,
            f"{base_name}_page_{count}.pdf"
        )

        with open(exit_name, "wb") as new_pdf:
            writer.write(new_pdf)

        count += 1

    status_label.configure(
        text=f"PDF separado com sucesso em {output_folder}! ({count-1} arquivos criados)",
        text_color="green"
    )

def drop(event):
        archive_var.set(event.data.strip("{}"))
    

root = TkinterDnD.Tk()
root.geometry("820x820")
root.title("PDF Splitter")

root.configure(bg="#1f1f1f")
frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(pady=30, padx=30, fill="both", expand=True)

title = ctk.CTkLabel(
    frame,
    text="PDF Splitter",
    font=("Arial", 26, "bold")
)
title.pack(pady=20)

archive_var = ctk.StringVar()
interval_var = ctk.BooleanVar()

drop_frame = ctk.CTkFrame(
    frame,
    width=420,
    height=250,
    corner_radius=15
)
drop_frame.pack(pady=15)

drop_frame.pack_propagate(False)

drop_text = ctk.CTkLabel(
    drop_frame,
    text="📂\nArraste seu PDF aqui",
    font=("Arial", 16),
    justify="center"
)
drop_text.pack(expand=True)

archive_var = ctk.StringVar()

def drop(event):
    file_path = event.data.strip("{}")
    archive_var.set(file_path)
    drop_text.configure(text=f"Arquivo selecionado:\n{os.path.basename(file_path)}")

drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind("<<Drop>>", drop)

paginas_label = ctk.CTkLabel(
    frame,
    text="Páginas por arquivo"
)
paginas_label.pack(pady=(20, 5))

pages_entry = ctk.CTkEntry(frame, width=120)
pages_entry.pack()

interval_check = ctk.CTkCheckBox(
    frame,
    text="Usar intervalo específico",
    variable=interval_var
)
interval_check.pack(pady=20)

start_label = ctk.CTkLabel(frame, text="Página inicial")
start_label.pack()

start_entry = ctk.CTkEntry(frame, width=120)
start_entry.pack(pady=5)

end_label = ctk.CTkLabel(frame, text="Página final")
end_label.pack()

end_entry = ctk.CTkEntry(frame, width=120)
end_entry.pack(pady=5)

botao = ctk.CTkButton(
    frame,
    text="Separar PDF",
    height=45,
    command=pdf_split
)
botao.pack(pady=30)

status_label = ctk.CTkLabel(frame, text="")
status_label.pack()

root.mainloop()