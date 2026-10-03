import tkinter as tk
window = tk.Tk()

window.resizable(False, False)

window.title("Form Biodata Mahasiswa")

window.geometry("500x600")

label_judul = tk.Label(
    master=window,
    text="FORM BIODATA MAHASISWA",
    font=("Arial", 16, "bold"),
    bg="ivory"
)

label_judul.pack(pady=25)

# Label untuk input nama
label_nama = tk.Label(master=window, text="Nama Lengkap:",
                      font=("Arial", 12), bg="ivory")
label_nama.pack(pady=5)

# Entry untuk input nama
entry_nama = tk.Entry(master=window, width=50)
entry_nama.pack(pady=5)


label_nim = tk.Label(master=window, text="NIM:",
                     font=("Arial", 12), bg="ivory")

label_nim.pack(pady=5)
entry_nim = tk.Entry(master=window, width=50)
entry_nim.pack(pady=5)

label_jurusan = tk.Label(master=window, text="Jurusan:",
                         font=("Arial", 12), bg="ivory")
label_jurusan.pack(pady=5)
entry_jurusan = tk.Entry(master=window, width=50)
entry_jurusan.pack(pady=5)


window.configure(bg="ivory")
window.mainloop()
