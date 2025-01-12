import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import pickle
import numpy as np
import pandas as pd

# 1. Load dataset tim dan logo
def load_team_data():
    try:
        df = pd.read_csv('premier-league-matches.csv')
        home_team_mapping = {team: idx for idx, team in enumerate(df['Home'].unique())}
        away_team_mapping = {team: idx for idx, team in enumerate(df['Away'].unique())}
    except FileNotFoundError:
        # Mapping manual jika dataset tidak ditemukan
        home_team_mapping = {'Team A': 0, 'Team B': 1, 'Team C': 2}
        away_team_mapping = {'Team A': 0, 'Team B': 1, 'Team C': 2}
    return home_team_mapping, away_team_mapping

def load_logo_mapping():
    try:
        logo_df = pd.read_csv('premier_league/logo_tim.csv')
        return dict(zip(logo_df['nama_tim'], logo_df['logo']))
    except FileNotFoundError:
        messagebox.showerror("Error", "File logo_tim.csv tidak ditemukan.")
        return {}

home_team_mapping, away_team_mapping = load_team_data()
logo_mapping = load_logo_mapping()

# 2. Fungsi prediksi skor
def predict_match_score(home_team, away_team):
    try:
        with open('random_forest_model.pkl', 'rb') as file:
            model = pickle.load(file)

        if home_team not in home_team_mapping or away_team not in away_team_mapping:
            return "Nama tim tidak valid. Periksa kembali input Anda."

        home_team_code = home_team_mapping[home_team]
        away_team_code = away_team_mapping[away_team]
        input_data = np.array([[home_team_code, away_team_code]])

        probabilities = model.predict_proba(input_data)[0]
        classes = model.classes_

        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        return [(classes[i], probabilities[i]) for i in top_3_indices]
    except Exception as e:
        return f"Kesalahan dalam prediksi: {e}"

# 3. Fungsi untuk menampilkan logo
def display_logo(team_name, logo_label):
    if team_name in logo_mapping:
        try:
            logo_path = logo_mapping[team_name]
            img = Image.open(logo_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            logo_label.config(image=img, text="")
            logo_label.image = img
        except Exception as e:
            logo_label.config(text=f"Error: {e}", image="")
    else:
        logo_label.config(text=f"Logo {team_name} tidak tersedia.", image="")

# 4. Fungsi tombol prediksi
def predict_button_action():
    home_team = home_team_entry.get().strip()
    away_team = away_team_entry.get().strip()

    if not home_team or not away_team:
        result_label.config(text="Harap masukkan nama tim.", fg="red")
        return

    result = predict_match_score(home_team, away_team)
    display_result(result)

    display_logo(home_team, home_team_logo_label)
    display_logo(away_team, away_team_logo_label)

# 5. Tampilkan hasil prediksi dalam tabel
def display_result(result):
    for row in treeview.get_children():
        treeview.delete(row)

    if isinstance(result, list):
        for i, (score, prob) in enumerate(result):
            treeview.insert("", "end", values=(i + 1, score, f"{prob * 100:.2f}%"))
    else:
        result_label.config(text=result, fg="red")

# 6. GUI dengan Tkinter
root = tk.Tk()
root.title("Prediksi Skor Pertandingan")
root.geometry("700x700")

# Input tim tuan rumah
home_team_label = tk.Label(root, text="Nama Tim Tuan Rumah:", font=("Verdana", 12))
home_team_label.pack(pady=10)
home_team_entry = tk.Entry(root, font=("Verdana", 12), width=30)
home_team_entry.pack(pady=5)

home_team_logo_label = tk.Label(root,  font=("Verdana", 10))
home_team_logo_label.pack(pady=5)

# Input tim tandang
away_team_label = tk.Label(root, text="Nama Tim Tandang:", font=("Verdana", 12))
away_team_label.pack(pady=10)
away_team_entry = tk.Entry(root, font=("Verdana", 12), width=30)
away_team_entry.pack(pady=5)

away_team_logo_label = tk.Label(root, font=("Verdana", 10))
away_team_logo_label.pack(pady=5)

# Tombol prediksi
predict_button = tk.Button(root, text="Prediksi", font=("Verdana", 12), command=predict_button_action, bg="#8174A0", fg="white")
predict_button.pack(pady=20)

result_label = tk.Label(root, text="", font=("Verdana", 12))
result_label.pack(pady=10)

# Tabel hasil prediksi
result_frame = tk.Frame(root, bd=2, relief="solid", padx=10, pady=10)
result_frame.pack(fill="both", expand=True, padx=10, pady=10)


columns = ("Rank", "Prediksi Skor", "Probabilitas")
treeview = ttk.Treeview(result_frame, columns=columns, show="headings", height=5)

treeview.heading("Rank", text="Rank", anchor="center")
treeview.heading("Prediksi Skor", text="Prediksi Skor", anchor="center")
treeview.heading("Probabilitas", text="Probabilitas", anchor="center")

treeview.column("Rank", anchor="center", width=50)
treeview.column("Prediksi Skor", anchor="center", width=150)
treeview.column("Probabilitas", anchor="center", width=150)

scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)

treeview.pack(side="top", fill="x", padx=10, pady=10)
scrollbar.pack(side="right", fill="y")

root.mainloop()
