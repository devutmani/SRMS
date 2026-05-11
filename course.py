from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow

from create_db import connect_db


class CourseClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= Title =================
        title = Label(
            self.root,
            text="Manage Course Details",
            font=("goudy old style", 20, "bold"),
            bg="#033054",
            fg="white"
        )
        title.place(x=10, y=15, width=1180, height=35)

        # ================= Variables =================
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()

        # ================= Labels =================
        Label(self.root, text="Course Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        Label(self.root, text="Duration", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        Label(self.root, text="Charges", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        Label(self.root, text="Description", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)

        # ================= Entry Fields =================
        self.txt_courseName = Entry(self.root, textvariable=self.var_course,
                                    font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_courseName.place(x=150, y=60, width=200)

        Entry(self.root, textvariable=self.var_duration,
              font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=100, width=200)

        Entry(self.root, textvariable=self.var_charges,
              font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=150, y=140, width=200)

        self.txt_description = Text(self.root, font=("goudy old style", 15, "bold"), bg="lightyellow")
        self.txt_description.place(x=150, y=180, width=500, height=130)

        # ================= Buttons =================
        Button(self.root, text="Save", command=self.add,
               font=("goudy old style", 15, "bold"),
               bg="#2196f3", fg="white", cursor="hand2").place(x=150, y=400, width=110, height=40)

        Button(self.root, text="Update", command=self.update,
               font=("goudy old style", 15, "bold"),
               bg="#4caf50", fg="white", cursor="hand2").place(x=270, y=400, width=110, height=40)

        Button(self.root, text="Delete", command=self.delete,
               font=("goudy old style", 15, "bold"),
               bg="#f44336", fg="white", cursor="hand2").place(x=390, y=400, width=110, height=40)

        Button(self.root, text="Clear", command=self.clear,
               font=("goudy old style", 15, "bold"),
               bg="#607d8b", fg="white", cursor="hand2").place(x=510, y=400, width=110, height=40)

        # ================= Search =================
        Entry(self.root, textvariable=self.var_search,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=870, y=60, width=180)

        Button(self.root, text="Search", command=self.search,
               font=("goudy old style", 15, "bold"),
               bg="#2196f3", fg="white", cursor="hand2").place(x=1070, y=60, width=120, height=28)

        # ================= Table =================
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        Scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)
        Scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)

        self.CourseTable = ttk.Treeview(
            self.C_Frame,
            columns=("cid", "name", "duration", "charges", "description"),
            xscrollcommand=Scrollx.set,
            yscrollcommand=Scrolly.set
        )

        Scrollx.pack(side=BOTTOM, fill=X)
        Scrolly.pack(side=RIGHT, fill=Y)

        Scrollx.config(command=self.CourseTable.xview)
        Scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="ID")
        self.CourseTable.heading("name", text="Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")

        self.CourseTable["show"] = "headings"

        self.CourseTable.column("cid", width=50)
        self.CourseTable.column("name", width=100)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= Get Data =================
    def get_data(self, ev):
        f = self.CourseTable.focus()
        row = self.CourseTable.item(f).get("values")

        if not row:
            return

        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])

        self.txt_description.delete("1.0", END)
        self.txt_description.insert(END, row[4])

        self.txt_courseName.config(state='readonly')

    # ================= Add =================
    def add(self):
        try:
            con = connect_db()
            cur = con.cursor()

            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course Name required", parent=self.root)
                return

            cur.execute(
                "INSERT INTO course(name, duration, charges, description) VALUES(%s,%s,%s,%s)",
                (
                    self.var_course.get(),
                    self.var_duration.get(),
                    self.var_charges.get(),
                    self.txt_description.get("1.0", END)
                )
            )

            con.commit()
            con.close()

            messagebox.showinfo("Success", "Course Added Successfully", parent=self.root)
            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ================= Update =================
    def update(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE course 
                SET duration=%s, charges=%s, description=%s 
                WHERE name=%s
            """, (
                self.var_duration.get(),
                self.var_charges.get(),
                self.txt_description.get("1.0", END),
                self.var_course.get()
            ))

            con.commit()
            con.close()

            messagebox.showinfo("Success", "Course Updated Successfully", parent=self.root)
            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ================= Delete =================
    def delete(self):
        try:
            con = connect_db()
            cur = con.cursor()

            op = messagebox.askyesno("Confirm", "Do you want to delete?", parent=self.root)

            if op:
                cur.execute("DELETE FROM course WHERE name=%s", (self.var_course.get(),))
                con.commit()
                con.close()

                messagebox.showinfo("Deleted", "Course Deleted Successfully", parent=self.root)
                self.show()
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ================= Show =================
    def show(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()

            self.CourseTable.delete(*self.CourseTable.get_children())

            for row in rows:
                self.CourseTable.insert("", END, values=row)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ================= Search =================
    def search(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM course WHERE name LIKE %s",
                        ('%' + self.var_search.get() + '%',))

            rows = cur.fetchall()

            self.CourseTable.delete(*self.CourseTable.get_children())

            for row in rows:
                self.CourseTable.insert("", END, values=row)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)

    # ================= Clear =================
    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0", END)
        self.txt_courseName.config(state='normal')


if __name__ == "__main__":
    root = Tk()
    obj = CourseClass(root)
    root.mainloop()