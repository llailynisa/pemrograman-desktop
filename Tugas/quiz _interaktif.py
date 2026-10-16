import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

BG = "#FFF4DE"

class QuizApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Quiz Interaktif - Tugas Akhir")
        self.window.geometry("610x550")

        # Data quiz
        self.questions = [
            # 1
            {
                "question": "Apa itu event-driven programming?",
                "options": ["Program yang berjalan berurutan", "Program yang merespons kejadian", "Program tanpa GUI", "Program berbasis web"],
                "correct": 1
            },
            # 2
            {
                "question": "Apa fungsi dari widget dalam GUI?",
                "options": ["Menyimpan data", "Menampilkan informasi dan menerima input", "Mengatur alur program", "Membuat koneksi database"],
                "correct": 1
            },
            # 3
            {
                "question": "Apa yang tidak termasuk dalam jenis event?",
                "options": ["Mouse Events", "Keyboard Events", "Widget Events", "Function"],
                "correct": 3
            },
            # 4
            {
                "question": "Apa yang dimaksud dengan callback function?",
                "options": ["Fungsi yang dijalankan secara otomatis ketika suatu event atau kondisi tertentu terjadi",
                            "Fungsi yang digunakan untuk membuat widget baru",
                            "Fungsi yang digunakan untuk menyimpan data ke dalam variabel",
                            "Fungsi yang hanya dapat dipanggil satu kali"],
                "correct": 0
            },
            # 5
            {
                "question": "Pada Tkinter, callback function biasanya digunakan pada parameter...",
                "options": ["command", "event", "callback", "function"],
                "correct": 0
            },
            # 6
            {
                "question": "Keyword yang digunakan untuk membuat fungsi di Python adalah...",
                "options": ["function", "define", "def", "func"],
                "correct": 2
            },
            # 7
            {
                "question": "Keyword yang digunakan untuk membuat kelas dalam Python adalah...",
                "options": ["object", "class", "define", "struct"],
                "correct": 1
            },
            # 8
            {
                "question": "Manakah yang merupakan nilai bertipe data Boolean?",
                "options": ["True", "'True'", "1.5", "None"],
                "correct": 0
            },
            # 9
            {
                "question": "Fungsi dari perintah 'import' dalam Python adalah...",
                "options": ["Membuat variabel baru", "Menjalankan program", "Mengimpor modul atau library", "Membuat fungsi baru"],
                "correct": 2
            },
            # 10
            {
                "question": "Method pertama yang biasanya digunakan untuk menginisialisasi objek dalam class Python adalah...",
                "options": ["__init__", "__start__", "__create__", "__new__"],
                "correct": 0
            }
        ]

        # State management
        self.current_question = 0
        self.score = 0
        self.time_left = 30
        self.timer_id = None
        self.locked = False
        self.selected_answer = tk.IntVar(value=-1)

        self.buat_interface()
        self.load_question()

    def buat_interface(self):
        # Frame utama
        self.frame_quiz = tk.Frame(
            master=self.window,
            padx=20,
            pady=20,
            bg=BG
        )
        self.frame_quiz.pack(fill="both", expand=True)

        # Judul
        self.label_judul = tk.Label(
            master=self.frame_quiz,
            text="Quiz Interaktif",
            font=("Arial", 16, "bold"),
            bg=BG
        )
        self.label_judul.pack(pady=10)

        # Informasi nomor soal dan skor
        self.count_question = tk.Label(
            master=self.frame_quiz,
            text="Soal 1 dari 10 | Skor: 0",
            font=("Arial", 12),
            bg=BG
        )
        self.count_question.pack()

        # Timer
        self.timer_label = tk.Label(
            master=self.frame_quiz,
            text="Waktu tersisa: 30 detik",
            font=("Arial", 12),
            bg=BG
        )
        self.timer_label.pack(pady=5)

        # Pertanyaan
        self.question_label = tk.Label(
            master=self.frame_quiz,
            text="Pertanyaan",
            font=("Arial", 12),
            wraplength=600,
            bg=BG
        )
        self.question_label.pack(pady=20)

        # Tempat untuk radio button
        self.option_buttons = []

        for i in range(4):
            option = tk.Radiobutton(
                master=self.frame_quiz,
                text=f"Pilihan {i+1}",
                variable=self.selected_answer,
                value=i,
                bg=BG,
                activebackground=BG,
                font=("Arial", 12),
                wraplength=580,
                justify="left"
            )

            option.pack(anchor="w")
            self.option_buttons.append(option)

        # Tombol submit
        self.submit_button = tk.Button(
            master=self.frame_quiz,
            text="Submit Jawaban",
            command=self.submit_answer
        )
        self.submit_button.pack(pady=20)

        # Feedback benar/salah
        self.feedback_label = tk.Label(
            master=self.frame_quiz,
            text="",
            font=("Arial", 12, "bold"),
            wraplength=600,
            bg=BG
        )
        self.feedback_label.pack()

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            master=self.frame_quiz,
            length=400,
            mode="determinate"
        )
        self.progress_bar.pack(pady=10)

        # Keyboard shortcut: Enter = submit, Esc = skip
        self.window.bind("<Return>", self.submit_answer)
        self.window.bind("<Escape>", lambda e: self.submit_answer(status="skip"))

    def load_question(self):
        # Kalau semua soal sudah selesai, tampilkan hasil
        if self.current_question >= len(self.questions):
            self.show_result()
            return

        soal = self.questions[self.current_question]
        total = len(self.questions)

        self.locked = False
        self.selected_answer.set(-1)
        self.time_left = 30

        self.count_question.config(text=f"Soal {self.current_question + 1} dari {total} | Skor: {self.score}")
        self.question_label.config(text=soal["question"])
        self.feedback_label.config(text="", bg=BG)
        self.progress_bar["maximum"] = total
        self.progress_bar["value"] = self.current_question

        for i, tombol in enumerate(self.option_buttons):
            tombol.config(text=soal["options"][i], state="normal")
        self.submit_button.config(state="normal")

        self.start_timer()

    def start_timer(self):
        if self.locked:
            return

        self.timer_label.config(
            text=f"Waktu tersisa: {self.time_left} detik",
            fg="red" if self.time_left <= 10 else "black"
        )

        if self.time_left <= 0:
            self.submit_answer(status="timeout")
            return

        self.time_left -= 1
        self.timer_id = self.window.after(1000, self.start_timer)

    def submit_answer(self, event=None, status="submit"):
        if self.locked:
            return

        pilihan = self.selected_answer.get()

        # Validasi: harus memilih dulu sebelum submit
        if status == "submit" and pilihan == -1:
            messagebox.showwarning("Belum memilih", "Pilih salah satu jawaban dulu.")
            return

        self.locked = True
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)

        soal = self.questions[self.current_question]
        jawaban_benar = soal["options"][soal["correct"]]

        if status == "submit" and pilihan == soal["correct"]:
            self.score += 1
            pesan = "Benar!"
            warna = "#2e8b57"
        else:
            if status == "skip":
                pesan = "Soal dilewati."
            elif status == "timeout":
                pesan = "Waktu habis."
            else:
                pesan = "Salah."
            pesan += f" Jawaban: {jawaban_benar}"
            warna = "#d9534f"

        for tombol in self.option_buttons:
            tombol.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.feedback_label.config(text=pesan, fg="white", bg=warna)
        self.animasi_feedback(warna)
        # Update skor & progress bar, lalu lanjut ke soal berikutnya
        self.current_question += 1
        self.progress_bar["value"] = self.current_question
        self.count_question.config(
            text=f"Soal {self.current_question} dari {len(self.questions)} | Skor: {self.score}"
        )
        self.window.after(1800, self.load_question)

    def animasi_feedback(self, warna, jumlah=4):
        if jumlah <= 0:
            self.feedback_label.config(bg=BG)
            return

        # tampilkan warna feedback
        self.feedback_label.config(bg=warna)

        # setelah 300 ms ubah ke warna normal
        self.window.after(
            300,
            lambda: self.kedip_feedback(warna, jumlah)
        )


    def kedip_feedback(self, warna, jumlah):
        self.feedback_label.config(bg=BG)

        # setelah 300 ms tampilkan warna lagi
        self.window.after(
            300,
            lambda: self.animasi_feedback(warna, jumlah - 1)
        )

    def show_result(self):
        total = len(self.questions)
        messagebox.showinfo(
            "Hasil Quiz",
            f"Skor akhir kamu: {self.score} dari {total} ({self.score / total * 100:.0f}%)"
        )
        self.window.destroy()

if __name__ == "__main__":
    app = QuizApp()
    app.window.mainloop()