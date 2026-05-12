from tkinter import *
from tkinter import messagebox
from create_db import connect_db


class ReportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_search = StringVar()
        self.var_id = ""

        title = Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"), bg="orange", fg="#262626")
        title.place(x=10, y=15, width=1180, height=50)

        Label(self.root, text="Search By Roll Number", font=("goudy old style", 18, "bold"), bg="white").place(x=280, y=100)

        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20), bg="lightyellow").place(x=580, y=100, width=180)

        Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#03a9f4", fg="white", cursor="hand2").place(x=780, y=100, width=100, height=35)

        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="gray", fg="white", cursor="hand2").place(x=900, y=100, width=100, height=35)

        Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=150, y=230, width=150, height=50)

        Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=300, y=230, width=150, height=50)

        Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=450, y=230, width=150, height=50)

        Label(self.root, text="Marks Obtained", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=600, y=230, width=150, height=50)

        Label(self.root, text="Total Marks", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=750, y=230, width=150, height=50)

        Label(self.root, text="Percentage", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=900, y=230, width=150, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)

        self.name = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)

        self.course = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)

        self.marks = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.marks.place(x=600, y=280, width=150, height=50)

        self.full = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.full.place(x=750, y=280, width=150, height=50)

        self.per = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)

        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2").place(x=500, y=360, width=150, height=40)

    def search(self):
        try:
            con = connect_db()
            cur = con.cursor()

            if self.var_search.get() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return

            cur.execute("SELECT * FROM result WHERE roll=%s", (self.var_search.get(),))
            row = cur.fetchone()

            if row is not None:
                self.var_id = row[0]

                self.roll.config(text=row[1])
                self.name.config(text=row[2])
                self.course.config(text=row[3])
                self.marks.config(text=row[4])
                self.full.config(text=row[5])
                self.per.config(text=row[6])

            else:
                messagebox.showerror("Error", "No Record Found", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        finally:
            if 'con' in locals():
                con.close()

    def delete(self):
        try:
            con = connect_db()
            cur = con.cursor()

            if self.var_id == "":
                messagebox.showerror("Error", "Search Result First", parent=self.root)
                return

            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)

            if op:
                cur.execute("DELETE FROM result WHERE rid=%s", (self.var_id,))
                con.commit()

                messagebox.showinfo("Deleted", "Result Deleted Successfully", parent=self.root)

                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

        finally:
            if 'con' in locals():
                con.close()

    def clear(self):
        self.var_search.set("")
        self.var_id = ""

        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")


if __name__ == "__main__":
    root = Tk()
    obj = ReportClass(root)
    root.mainloop()