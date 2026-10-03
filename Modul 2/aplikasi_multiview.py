import tkinter as tk
from tkinter import messagebox
import datetime
import logging
import json
import re

# Setup logging
logging.basicConfig(
    filename='aplikasi_biodata.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk


class AplikasiBiodata(tk.Tk):

    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        # Memanggil constructor dari kelas induk (tk.Tk)
        super().__init__()
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

    # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        # Status login
        self.current_user = None

        # Atribut entry
        self.entry_bg = "white"
        self.entry_border = "grey"

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Sembunyikan password
        self.password_tampil = False

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

        # Log aplikasi start
        logging.info("Aplikasi dimulai")

        # Simpan username login
        self.ingat_username = "remember_me.json"
        self._remember_me()

    def submit_data(self):
        #   """Submit data biodata dengan validasi lengkap"""
        try:
            # Cek checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning(
                    "Peringatan", "Anda harus menyetujui pengumpulan data!")
                return

            # Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()
            email = self.var_email.get().strip()
            telepon = self.var_telepon.get().strip()
            tgl_lahir = self.var_tgl_lahir.get().strip()

            # Validasi field kosong
            if not nama or not nim or not jurusan:
                messagebox.showwarning(
                    "Input Kosong", "Nama, NIM, dan Jurusan harus diisi!")
                return

            # Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning(
                    "Format NIM Salah", "NIM harus berupa angka minimal 8 digit!")
                self.entry_nim.config(bg="red", highlightbackground="red")
                self.entry_nim.focus_set()
                return

            # Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning(
                    "Format Nama Salah", "Nama tidak boleh hanya berupa angka!")
                self.entry_nama.config(bg="red", highlightbackground="red")
                self.entry_nama.focus_set()
                return

            pola_email = r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$'
            if not re.match(pola_email, email):
                messagebox.showwarning(
                    "Format Email Salah",
                    "Format email tidak valid!\nContoh: nama@gmail.com")
                self.entry_email.config(bg="red", highlightbackground="red")
                self.entry_email.focus_set()
                return

            telepon_format = telepon.replace(" ", "").replace("-", "")
            pola_telepon = r'^(\+62|62|0)8[1-9][0-9]{7,10}$'
            if not re.match(pola_telepon, telepon_format):
                messagebox.showwarning(
                    "Format Telepon Salah",
                    "Nomor telepon tidak valid!\nContoh: 081234567890")
                self.entry_telepon.config(bg="red", highlightbackground="red")
                self.entry_telepon.focus_set()
                return

            try:
                tgl_obj = datetime.datetime.strptime(tgl_lahir, "DD-MM-YYYY")
            except ValueError:
                messagebox.showwarning(
                    "Format Tanggal Salah",
                    "Gunakan format DD-MM-YYYY dengan tanggal yang valid.")
                self.entry_tgl_lahir.config(
                    bg="red", highlightbackground="red")
                self.entry_tgl_lahir.focus_set()
                return

            if tgl_obj > datetime.datetime.now():
                messagebox.showwarning(
                    "Tanggal Tidak Valid",
                    "Tanggal lahir tidak boleh di masa depan!")
                self.entry_tgl_lahir.config(
                    bg="red", highlightbackground="red")
                self.entry_tgl_lahir.focus_set()
                return
                        
            # Tampilkan hasil
            hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nAlamat: {alamat}\nEmail: {email}\nTanggal Lahir: {tgl_lahir}\nJenis Kelamin: {jenis_kelamin}\nTelepon: {telepon_format}"
            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            self.label_hasil.config(text=hasil_lengkap)

            logging.info(
                f"Data submitted by user: {self.current_user} - NIM: {nim}")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}")

        # Log successful data submission
    def _reset_color(self, entry):
        entry.config(bg=self.entry_bg, highlightbackground=self.entry_border)

    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning(
                    "Peringatan", "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.")
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(
                    f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo(
                "Info", f"Data berhasil disimpan ke file '{filename}'.")

        except PermissionError:
            messagebox.showerror(
                "Error", "Tidak memiliki izin untuk menyimpan file di lokasi ini.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}")

    def on_enter(self, event):
        if self.btn_submit['state'] == tk.NORMAL:
            self.btn_submit.config(bg="lightblue")

    def on_leave(self, event):
        self.btn_submit.config(bg="SystemButtonFace")

    def submit_shortcut(self, event=None):
        if self.btn_submit['state'] == tk.NORMAL:
            self.submit_data()

    def validate_form(self, *args):
        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        email_valid = self.var_email.get().strip() != ""
        telepon_valid = self.var_telepon.get().strip() != ""
        tgl_lahir_valid = self.var_tgl_lahir.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1


        if nama_valid and nim_valid and jurusan_valid and email_valid and telepon_valid and tgl_lahir_valid and setuju_valid:
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def _buat_tampilan_biodata(self):
        # Variabel-variabel berikut sekarang menjadi atribut dari instance kelas
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl_lahir = tk.StringVar()
        
        # --- Frame Utama ---
        # Frame utama juga menjadi atribut
        self.frame_biodata = tk.Frame(
            master=self, padx=20, pady=20, bg="#cf4e4e")
        # self.frame_biodata.pack(fill=tk.BOTH, expand=True)
        self.frame_biodata.columnconfigure(1, weight=1)

        # Aktifkan trace untuk validasi real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_tgl_lahir.trace_add("write", self.validate_form)

        self.var_nama.trace_add(
            "write", lambda *a: self._reset_color(self.entry_nama))
        self.var_nim.trace_add(
            "write", lambda *a: self._reset_color(self.entry_nim))
        self.var_jurusan.trace_add(
            "write", lambda *a: self._reset_color(self.entry_jurusan))
        self.var_email.trace_add( "write", lambda *a: self._reset_color(self.entry_nama))
        self.var_telepon.trace_add( "write", lambda *a: self._reset_color(self.entry_nama))
        self.var_tgl_lahir.trace_add( "write", lambda *a: self._reset_color(self.entry_nama))

        # (Di sini kita akan meletakkan semua kode GUI nantinya)
        # --- Membuat dan Menempatkan Widget ---
        # Judul
        self.label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 16, "bold"),
            bg="#deb887"
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame khusus untuk input dengan border
        self.frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=10,
            pady=10,
            bg="#deb887"
        )

        # Input Nama
        self.label_nama = tk.Label(
            master=self.frame_input,
            text="Nama Lengkap:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_nama.grid(row=0, column=0, sticky="W", pady=2)
        self.entry_nama = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, pady=2)

        # Input NIM
        self.label_nim = tk.Label(
            master=self.frame_input,
            text="NIM:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_nim.grid(row=1, column=0, sticky="W", pady=2)
        self.entry_nim = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, pady=2)

        # Input Jurusan
        self.label_jurusan = tk.Label(
            master=self.frame_input,
            text="Jurusan:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_jurusan.grid(row=2, column=0, sticky="W", pady=2)
        self.entry_jurusan = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, pady=2)

        # Input alamat dengan Text widget
        self.label_alamat = tk.Label(
            master=self.frame_input,
            text="Alamat:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_alamat.grid(row=3, column=0, sticky="NW", pady=2)

        # Frame untuk Text dan Scrollbar
        self.frame_alamat = tk.Frame(
            master=self.frame_input,
            relief=tk.SUNKEN,
            borderwidth=1
        )

        # Scrollbar untuk alamat
        self.scrollbar_alamat = tk.Scrollbar(master=self.frame_alamat)
        self.scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk alamat
        self.text_alamat = tk.Text(
            master=self.frame_alamat,
            height=5,
            width=28,
            font=("Arial", 12)
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Hubungkan scrollbar dengan text
        self.scrollbar_alamat.config(command=self.text_alamat.yview)
        self.text_alamat.config(yscrollcommand=self.scrollbar_alamat.set)

        self.frame_alamat.grid(row=3, column=1, pady=2)

        # Jenis kelamin
        self.label_jk = tk.Label(
            master=self.frame_input,
            text="Jenis Kelamin:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_jk.grid(row=4, column=0, sticky="W", pady=2)

        self.frame_jk = tk.Frame(master=self.frame_input)
        self.frame_jk.grid(row=4, column=1, sticky="W")

        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk,
            text="Pria",
            variable=self.var_jk,
            value="Pria"
        )
        self.radio_pria.pack(side=tk.LEFT)
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita"
        )
        self.radio_wanita.pack(side=tk.LEFT)

        self.label_email = tk.Label(
            master=self.frame_input, 
            text="Email:", 
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_email.grid(row=5, column=0, sticky="W", pady=2)
        self.entry_email = tk.Entry(
            master=self.frame_input, 
            width=30,
            font=("Arial", 12),
            textvariable=self.var_email
        )
        self.entry_email.grid(row=5, column=1, pady=2)

        self.label_telepon=tk.Label(
            master=self.frame_input, 
            text="Telepon:",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_telepon.grid(row=6, column=0, sticky="W", pady=2)
        self.entry_telepon = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_telepon
        )
        self.entry_telepon.grid(row=6, column=1, pady=2)

        self.label_tgl_lahir = tk.Label(
            master=self.frame_input,
            text="Tanggal Lahir (YYYY-MM-DD):",
            font=("Arial", 12),
            bg="#deb887"
        )
        self.label_tgl_lahir.grid(row=7, column=0, sticky="W", pady=2)
        self.entry_tgl_lahir = tk.Entry(
            master=self.frame_input,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_tgl_lahir
        )
        self.entry_tgl_lahir.grid(row=7, column=1, pady=2)

        # Checkbox persetujuan
        self.check_setuju = tk.Checkbutton(
            master=self.frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form)
        
        self.check_setuju.grid(
            row=8, column=0, columnspan=2, pady=10, sticky="W")

        self.frame_input.grid(row=1, column=0, columnspan=2, sticky="EW")

        # Tombol submit
        self.btn_submit = tk.Button(
            master=self.frame_biodata,
            text="Submit Biodata",
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )
        self.btn_submit.grid(row=6, column=0, columnspan=2,
                             pady=20, sticky="EW")

        # Event bindings untuk hover dan keyboard shortcuts
        self.btn_submit.bind("<Enter>", self.on_enter)
        self.btn_submit.bind("<Leave>", self.on_leave)

        # Keyboard shortcuts
        self.entry_nama.bind("<Return>", self.submit_shortcut)
        self.entry_nim.bind("<Return>", self.submit_shortcut)
        self.entry_jurusan.bind("<Return>", self.submit_shortcut)
        self.text_alamat.bind("<Return>", self.submit_shortcut)

        self.btn_reset = tk.Button(
            master=self.frame_biodata, 
            text="Reset", 
            font=("Arial", 10, "bold"),
            command=self._tombol_reset
        )
        self.btn_reset.grid(row=7, column=0, columnspan=2, pady= (0,20), sticky="W")

        # Label hasil
        self.label_hasil = tk.Label(
            master=self.frame_biodata,
            text="",
            font=("Arial", 12, "italic"),
            justify=tk.LEFT
        )
        self.label_hasil.grid(
            row=8, column=0, columnspan=2, sticky="W", padx=10)

        # Membuat menu
        self._buat_menu()

    def _tampilan_user(self):
        warna_user = {
            "admin": "#e9edc9",
            "user1": "#faedcd",
            "mahasiswa": "#f07167"
        }
        warna = warna_user.get(self.current_user, "#deb887")
        self._terapkan_warna(self.frame_biodata, warna)

    def _terapkan_warna(self, widget, warna):
        if isinstance(widget, (tk.Frame, tk.Label, tk.Checkbutton, tk.Radiobutton)):
            widget.config(bg=warna)

        for child in widget.winfo_children():
            self._terapkan_warna(child, warna)

    def keluar_aplikasi(self):
        if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()

    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Log attempt login
        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(
                f"Empty credentials attempt for username: {username}")
            messagebox.showwarning(
                "Login Gagal", "Username dan Password tidak boleh kosong.")
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning(
                "Login Gagal", "Username minimal 3 karakter.")
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username
            logging.info(f"Successful login for user: {username}")
            self._remember_me(simpan=True)
            messagebox.showinfo(
                "Login Berhasil", f"Selamat Datang, {username}!")
            self._reset_form_biodata()
            self._update_title_with_user()
            self._tampilan_user()
            self._pindah_ke(self.frame_biodata)
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror(
                "Login Gagal", "Username atau Password salah.")
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _tombol_reset(self):
        self._reset_form_biodata()
        self.validate_form()
        self.entry_nama.focus_set()

        logging.info(f"Form biodata telah direset")

    def _reset_form_biodata(self):
        """Reset semua field di form biodata"""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl_lahir.set("")
        self.label_hasil.config(text="")

    def _update_title_with_user(self):
        """Update judul window dengan nama user yang login"""
        if self.current_user:
            self.title(
                f"Aplikasi Biodata Mahasiswa - User: {self.current_user}")
        else:
            self.title("Aplikasi Biodata Mahasiswa")

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno("Logout", f"Apakah {self.current_user} yakin ingin logout?"):
            logging.info(f"User logout: {self.current_user}")
            # Reset status user
            self.current_user = None
            # Update title
            self._update_title_with_user()
            # Bersihkan field login
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
            self._remember_me()
            # Reset form biodata
            self._reset_form_biodata()
            # Kembali ke halaman login
            self._pindah_ke(self.frame_login)
            # Focus ke username field
            self.entry_username.focus_set()

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _remember_me(self, simpan=False):
        try:
            if simpan:
                if self.var_ingat.get() == 1:
                    data = {"username": self.entry_username.get().strip()}
                else:
                    data = {"username": ""}

                with open(self.ingat_username, "w", encoding="utf-8") as file:
                    json.dump(data, file)
                logging.info(f"username '{data['username']}' disimpan")

            else:
                self.entry_username.delete(0, tk.END)
                self.var_ingat.set(0)

                with open(self.ingat_username, "r", encoding="utf-8") as file:
                    data = json.load(file)

                username = data.get("username", "")
                if username != "":
                    self.entry_username.insert(0, username)
                    self.var_ingat.set(1)
                    logging.info(f"'{username}' dimuat")

        except FileNotFoundError:
            logging.warning(
                f"File '{self.ingat_username}' tidak ditemukan. Tidak ada username yang diingat.")
        except Exception as e:
            logging.error(f"Remember Me error: {e}")            

    def _hiding_password(self):
        self.password_tampil = not self.password_tampil
        if self.password_tampil:
            self.entry_password.config(show="")
            self.btn_hide.config(text="Hide")
        else: 
            self.entry_password.config(show="*")
            self.btn_hide.config(text="Show")
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=20, pady=100)

        # Konfigurasi grid untuk frame login agar terpusat
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_columnconfigure(1, weight=1)
        # Judul Login
        tk.Label(
            self.frame_login,
<<<<<<< HEAD
            text="LOGIN",
=======
            text="HALAMAN LOGIN",
>>>>>>> 514a176fc2a8755a64817b6b2a0dd6b2f4abe2cd
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=20)

        # Input Username
        tk.Label(
            self.frame_login,
            text="Username:",
            font=("Arial", 12)
        ).grid(row=1, column=0, sticky="W", pady=5)

        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_username.grid(row=1, column=1, pady=5, sticky="EW")

        self.var_ingat = tk.IntVar()
        self.ck_ingat = tk.Checkbutton(
            self.frame_login, 
            text="Remember me", 
            variable=self.var_ingat,
            font=("Arial", 10)
        )
        self.ck_ingat.grid(row=3, column=1, sticky="W")

        # Input Password
        tk.Label(
            self.frame_login,
            text="Password:",
            font=("Arial", 12)
        ).grid(row=2, column=0, sticky="W", pady=5)

        self.entry_password = tk.Entry(
            self.frame_login,
            font=("Arial", 12),
            show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=5, sticky="EW")

        self.btn_hide = tk.Button(
            self.frame_login,
            text="Show",
            font=("Arial", 8),
            width=5,
            command=self._hiding_password
        )
        self.btn_hide.grid(row=2, column=2, padx=5)

        # Tombol Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(row=4, column=0, columnspan=3,
                            pady=20, sticky="EW")

        # Keyboard shortcuts untuk login
        self.entry_username.bind(
            "<Return>", lambda e: self.entry_password.focus_set())
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Info untuk user
        info_label = tk.Label(
            self.frame_login,
            text="Info: Username yang tersedia:\nadmin (password: 123)\nuser1 (password: password1)\nmahasiswa (password: 123456)",
            font=("Arial", 9),
            fg="gray",
            justify=tk.LEFT
        )
        info_label.grid(row=5, column=0, columnspan=3, pady=10)
<<<<<<< HEAD
        self._terapkan_warna(self.frame_login, "#eef4ed")
        
=======

>>>>>>> 514a176fc2a8755a64817b6b2a0dd6b2f4abe2cd
    def _pindah_ke(self, frame_tujuan):
        """Method untuk berpindah antar tampilan"""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Auto-focus berdasarkan frame yang ditampilkan
        if frame_tujuan == self.frame_login:
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self.after(100, lambda: self.entry_nama.focus_set())


# Blok berikut hanya akan dieksekusi jika file ini dijalankan secara langsung
if __name__ == "__main__":
    # Membuat instance dari kelas aplikasi kita
    app = AplikasiBiodata()

    # Menjalankan mainloop dari instance tersebut
    app.mainloop()
