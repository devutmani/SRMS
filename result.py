from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from create_db import connect_db


class ResultClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks = StringVar()
        self.var_full_marks = StringVar()

        self.roll_list = []
        self.fetch_roll()

        title = Label(self.root, text="Add Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        Label(self.root, text="Select Student", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=100)
        Label(self.root, text="Name", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=160)
        Label(self.root, text="Course", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=220)
        Label(self.root, text="Marks Obtained", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=280)
        Label(self.root, text="Full Marks", font=("goudy old style", 20, "bold"), bg="white").place(x=50, y=340)

        self.txt_student = ttk.Combobox(self.root, textvariable=self.var_roll, values=self.roll_list, font=("goudy old style", 15, "bold"), state="readonly", justify=CENTER)
        self.txt_student.place(x=280, y=100, width=200)
        self.txt_student.set("Select")

        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=500, y=100, width=100, height=30)

        txt_name = Entry(self.root, textvariable=self.var_name, font=("goudy old style", 20, "bold"), bg="lightyellow", state="readonly")
        txt_name.place(x=280, y=160, width=320)

        txt_course = Entry(self.root, textvariable=self.var_course, font=("goudy old style", 20, "bold"), bg="lightyellow", state="readonly")
        txt_course.place(x=280, y=220, width=320)

        txt_marks = Entry(self.root, textvariable=self.var_marks, font=("goudy old style", 20, "bold"), bg="lightyellow")
        txt_marks.place(x=280, y=280, width=320)

        txt_fullmarks = Entry(self.root, textvariable=self.var_full_marks, font=("goudy old style", 20, "bold"), bg="lightyellow")
        txt_fullmarks.place(x=280, y=340, width=320)

        btn_add = Button(self.root, text="Submit", font=("times new roman", 15), bg="lightgreen", activebackground="lightgreen", cursor="hand2", command=self.add)
        btn_add.place(x=300, y=420, width=120, height=35)

        btn_clear = Button(self.root, text="Clear", font=("times new roman", 15), bg="lightgray", activebackground="lightgray", cursor="hand2", command=self.clear)
        btn_clear.place(x=430, y=420, width=120, height=35)

        self.bg_image = Image.open("images/result.jpg")
        self.bg_image = self.bg_image.resize((500, 300), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        self.lbl_bg = Label(self.root, image=self.bg_image)
        self.lbl_bg.place(x=650, y=100)

    def fetch_roll(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT roll FROM student")
            rows = cur.fetchall()

            if rows:
                for row in rows:
                    self.roll_list.append(row[0])

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def search(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT name, course FROM student WHERE roll=%s", (self.var_roll.get(),))
            row = cur.fetchone()

            if row is not None:
                self.var_name.set(row[0])
                self.var_course.set(row[1])

            else:
                messagebox.showerror("Error", "No record found!", parent=self.root)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def add(self):
        try:
            con = connect_db()
            cur = con.cursor()

            if self.var_name.get() == "":
                messagebox.showerror("Error", "Please first search student record", parent=self.root)
                return

            if self.var_marks.get() == "" or self.var_full_marks.get() == "":
                messagebox.showerror("Error", "Please enter marks", parent=self.root)
                return

            cur.execute("SELECT * FROM result WHERE roll=%s AND course=%s", (self.var_roll.get(), self.var_course.get()))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Error", "Result already present", parent=self.root)

            else:
                per = (float(self.var_marks.get()) * 100) / float(self.var_full_marks.get())

                cur.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks, percent) VALUES(%s, %s, %s, %s, %s, %s)", (self.var_roll.get(), self.var_name.get(), self.var_course.get(), self.var_marks.get(), self.var_full_marks.get(), per))

                con.commit()

                messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)

                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        finally:
            con.close()

    def clear(self):
        self.var_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks.set("")
        self.var_full_marks.set("")


if __name__ == "__main__":
    root = Tk()
    obj = ResultClass(root)
    root.mainloop()