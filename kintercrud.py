import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database SQLite (akan membuat file db jika belum ada)
    cursor = conn.cursor()
    # Membuat tabel 'nilai_siswa' jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    # Menjalankan query untuk mengambil semua data dari tabel 'nilai_siswa'    
    cursor.execute("SELECT * FROM nilai_siswa")  
    rows = cursor.fetchall()  # Mengambil semua hasil query
    conn.close()  # Menutup koneksi ke database
    return rows  # Mengembalikan data yang diambil

# Fungsi untuk menyimpan data ke dalam database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()    
    # Menyimpan data siswa ke dalam tabel 'nilai_siswa'
    cursor.execute(''' 
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk memperbarui data siswa dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()    
    # Menjalankan query untuk memperbarui data siswa berdasarkan ID
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghapus data siswa dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()    
    # Menjalankan query untuk menghapus data siswa berdasarkan ID
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai siswa
def calculate_prediction(biologi, fisika, inggris):
    # Prediksi fakultas berdasarkan nilai tertinggi
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"  # Jika ada nilai yang sama atau tidak ada nilai tertinggi yang jelas

# Fungsi untuk menangani aksi saat tombol 'Add' ditekan
def submit():
    try:
        # Mengambil input dari form
        nama = nama_var.get()
        biologi = int(biologi_var.get())  # Mengonversi nilai Biologi menjadi integer
        fisika = int(fisika_var.get())    # Mengonversi nilai Fisika menjadi integer
        inggris = int(inggris_var.get())  # Mengonversi nilai Inggris menjadi integer

        if not nama:  # Validasi jika nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        # Menghitung prediksi fakultas berdasarkan nilai
        prediksi = calculate_prediction(biologi, fisika, inggris)

        # Menyimpan data siswa ke dalam database
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        
        # Menghapus input form setelah data disimpan
        clear_inputs()
        
        # Memperbarui tabel dengan data terbaru
        populate_table()
    
    except ValueError as e:  # Menangani kesalahan jika input tidak valid
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk menangani aksi saat tombol 'Update' ditekan
def update():
    try:
        if not selected_record_id.get():  # Memeriksa apakah ada ID yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        # Menghitung kembali prediksi fakultas setelah data diperbarui
        prediksi = calculate_prediction(biologi, fisika, inggris)

        # Memperbarui data siswa di database
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")

        # Menghapus input form setelah data diperbarui
        clear_inputs()
        
        # Memperbarui tabel dengan data terbaru
        populate_table()

    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menangani aksi saat tombol 'Delete' ditekan
def delete():
    try:
        if not selected_record_id.get():  # Memeriksa apakah ada ID yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID record yang dipilih

        # Menghapus data siswa dari database
        delete_database(record_id)

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")

        # Menghapus input form setelah data dihapus
        clear_inputs()

        # Memperbarui tabel dengan data terbaru
        populate_table()
    
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus input form setelah operasi selesai
def clear_inputs():
    nama_var.set("")  # Mengosongkan input Nama
    biologi_var.set("")  # Mengosongkan input Nilai Biologi
    fisika_var.set("")  # Mengosongkan input Nilai Fisika
    inggris_var.set("")  # Mengosongkan input Nilai Inggris
    selected_record_id.set("")  # Mengosongkan ID record yang dipilih

# Fungsi untuk memperbarui tampilan tabel dengan data terbaru
def populate_table():
    # Menghapus semua baris yang ada di tabel
    for row in tree.get_children():
        tree.delete(row)
    
    # Mengambil data terbaru dari database dan menambahkannya ke tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form input berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil ID dari baris yang dipilih
        selected_row = tree.item(selected_item)['values']  # Mengambil nilai dari baris yang dipilih

        # Mengisi input form dengan data yang dipilih
        selected_record_id.set(selected_row[0])  # Mengisi ID record yang dipilih
        nama_var.set(selected_row[1])  # Mengisi Nama Siswa
        biologi_var.set(selected_row[2])  # Mengisi Nilai Biologi
        fisika_var.set(selected_row[3])  # Mengisi Nilai Fisika
        inggris_var.set(selected_row[4])  # Mengisi Nilai Inggris
    
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menangani jika tidak ada data yang dipilih

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter untuk menyimpan data dari input form
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Label dan Entry untuk input Nama Siswa
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

# Label dan Entry untuk input Nilai Biologi
Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

# Label dan Entry untuk input Nilai Fisika
Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

# Label dan Entry untuk input Nilai Inggris
Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol untuk Add, Update, dan Delete data
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur header tabel
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Binding untuk memilih data dari tabel dan mengisi form
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Memperbarui tabel dengan data dari database
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()