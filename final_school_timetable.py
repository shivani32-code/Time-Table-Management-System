import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# -------------------------------
# Database Connection
# -------------------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shiv@ni123",  # 👈 change if needed
        database="timetable_db3"
    )

# -------------------------------
# Ensure Subjects Exist
# -------------------------------
def ensure_subjects():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM subjects")
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany(
            "INSERT INTO subjects (name, teacher) VALUES (%s, %s)",
            [
                ('English', 'Mr. Sharma'),
                ('Maths', 'Ms. Gupta'),
                ('Science', 'Mr. Verma'),
                ('Social Studies', 'Mrs. Mehta'),
                ('Hindi', 'Ms. Rani'),
                ('Computer', 'Mr. Raj'),
                ('Sanskrit', 'Ms. Kaur'),
                ('Physical Education', 'Mr. Singh')
            ]
        )
        con.commit()
    con.close()

# -------------------------------
# Generate Timetable for All Classes
# -------------------------------
def generate_all_timetables():
    ensure_subjects()
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT name, teacher FROM subjects")
    subjects = cur.fetchall()

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    classes = ["10th A", "10th B", "10th C", "10th D", "10th E"]

    cur.execute("TRUNCATE TABLE timetable")

    for class_name in classes:
        for day in days:
            selected = random.sample(subjects, 8)
            periods = [f"{s[0]}\n{s[1]}" for s in selected]
            cur.execute("""
                INSERT INTO timetable
                (class_name, day, period1, period2, period3, period4, break_time, period5, period6, period7, period8)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (class_name, day, periods[0], periods[1], periods[2], periods[3], "BREAK",
                  periods[4], periods[5], periods[6], periods[7]))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "All class timetables generated successfully!")
    show_timetable()

# -------------------------------
# Room Numbers per Class
# -------------------------------
room_numbers = {
    "10th A": "Room 101",
    "10th B": "Room 102",
    "10th C": "Room 103",
    "10th D": "Room 104",
    "10th E": "Room 105"
}

# -------------------------------
# Show Timetable for Selected Class
# -------------------------------
def show_timetable():
    for widget in frame_table.winfo_children():
        widget.destroy()

    selected_class = class_var.get()
    if not selected_class:
        messagebox.showwarning("Select", "Please select a class.")
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        SELECT day, period1, period2, period3, period4, break_time, period5, period6, period7, period8
        FROM timetable WHERE class_name=%s
    """, (selected_class,))
    data = cur.fetchall()
    con.close()

    if not data:
        messagebox.showwarning("Empty", "Please generate timetables first.")
        return

    # Class and room info
    room = room_numbers.get(selected_class, "Room 101")
    tk.Label(frame_table, text=f"Class {selected_class} - {room}",
             font=("Arial", 16, "bold"), bg="#E6F2F8", fg="#003366").pack(pady=10)

    table = tk.Frame(frame_table, bg="#E6F2F8")
    table.pack()

    timings = [
        "8:00–8:45", "8:45–9:30", "9:30–10:15", "10:15–11:00",
        "BREAK", "11:20–12:05", "12:05–12:50", "12:50–1:35", "1:35–2:20"
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {row[0]: row[1:] for row in data}

    # Header row
    tk.Label(table, text="Day", bg="#004466", fg="white", width=15, height=2,
             font=("Arial", 11, "bold"), relief="ridge").grid(row=0, column=0)

    col = 1
    for t in timings:
        bg_color = "#FF9933" if t == "BREAK" else "#0073E6"
        tk.Label(table, text=t, bg=bg_color, fg="white", width=18,
                 height=2, font=("Arial", 10, "bold"), relief="ridge").grid(row=0, column=col)
        col += 1

    # Rows
    for i, day in enumerate(days):
        tk.Label(table, text=day, bg="#009999", fg="white", width=15, height=3,
                 font=("Arial", 10, "bold"), relief="ridge").grid(row=i+1, column=0)
        row_data = timetable[day]
        col = 1
        for j, val in enumerate(row_data):
            # Just display "BREAK" as a normal cell
            if j == 4:
                tk.Label(table, text="BREAK", bg="#FFCC66", fg="black",
                         width=18, height=3, font=("Arial", 10, "bold"),
                         relief="ridge").grid(row=i+1, column=col)
            else:
                tk.Label(table, text=val, bg="#E6F2FF", fg="black", width=18,
                         height=5, font=("Arial", 9), relief="ridge",
                         wraplength=130, justify="center").grid(row=i+1, column=col)
            col += 1


# -------------------------------
# Export Timetable to PDF
# -------------------------------
def export_pdf():
    selected_class = class_var.get()
    if not selected_class:
        messagebox.showwarning("Select", "Please select a class to export.")
        return

    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        SELECT day, period1, period2, period3, period4, break_time, period5, period6, period7, period8
        FROM timetable WHERE class_name=%s
    """, (selected_class,))
    data = cur.fetchall()
    con.close()

    if not data:
        messagebox.showwarning("Empty", "Generate timetable first.")
        return

    c = canvas.Canvas(f"{selected_class.replace(' ', '')}_Timetable.pdf", pagesize=A4)
    width, height = A4

    room = room_numbers.get(selected_class, "Room 101")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height - 50, f"Class {selected_class} - {room} Timetable")

    timings = [
        "8:00–8:45", "8:45–9:30", "9:30–10:15", "10:15–11:00",
        "BREAK", "11:20–12:05", "12:05–12:50", "12:50–1:35", "1:35–2:20"
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {row[0]: row[1:] for row in data}

    x_start, y_start = 50, height - 100
    cell_w, cell_h = 65, 45

    c.setFont("Helvetica-Bold", 9)
    c.drawString(x_start, y_start, "Day")
    for i, t in enumerate(timings):
        c.drawString(x_start + (i+1)*cell_w, y_start, t)

    c.setFont("Helvetica", 8)
    y = y_start - 20
    for day in days:
        c.drawString(x_start, y, day)
        for i, val in enumerate(timetable[day]):
            if i == 4:
                c.drawString(x_start + cell_w, y, "BREAK")
            else:
                c.drawString(x_start + (i+1)*cell_w, y, val.replace("\n", " - ")[:40])
        y -= 40

    c.save()
    messagebox.showinfo("Exported", f"Saved as '{selected_class.replace(' ', '')}_Timetable.pdf' successfully!")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Class 10th Timetable Management System")
root.geometry("1350x650")
root.configure(bg="#E6F2F8")

tk.Label(root, text="Class 10th Timetable Management System",
         font=("Arial", 18, "bold"), bg="#E6F2F8", fg="#003366").pack(pady=10)

class_var = tk.StringVar()
tk.Label(root, text="Select Class:", font=("Arial", 12, "bold"), bg="#E6F2F8").pack()
class_dropdown = ttk.Combobox(root, textvariable=class_var, font=("Arial", 12), width=15,
                              values=["10th A", "10th B", "10th C", "10th D", "10th E"])
class_dropdown.pack(pady=5)

btn_frame = tk.Frame(root, bg="#E6F2F8")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Generate All Timetables", bg="#0073E6", fg="white",
          font=("Arial", 12, "bold"), command=generate_all_timetables, padx=20).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Show Timetable", bg="#009999", fg="white",
          font=("Arial", 12, "bold"), command=show_timetable, padx=20).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Export to PDF", bg="#006633", fg="white",
          font=("Arial", 12, "bold"), command=export_pdf, padx=20).pack(side=tk.LEFT, padx=10)

frame_table = tk.Frame(root, bg="#E6F2F8")
frame_table.pack(pady=10, fill="both", expand=True)

root.mainloop()
