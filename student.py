from tkinter import *
from tkinter import ttk, messagebox
from create_db import connect_db


class StudentClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= Variables =================
        self.var_roll = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_course = StringVar()
        self.var_admission = StringVar()
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        self.var_search = StringVar()

        # ================= Title =================
        title = Label(
            self.root,
            text="Manage Student Details",
            font=("goudy old style", 20, "bold"),
            bg="#033054",
            fg="white"
        )
        title.place(x=10, y=15, width=1180, height=35)

        # ================= Labels =================
        Label(self.root, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        Label(self.root, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=100)
        Label(self.root, text="Email", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=140)
        Label(self.root, text="Gender", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=180)

        Label(self.root, text="D.O.B", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=60)
        Label(self.root, text="Contact", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=100)
        Label(self.root, text="Admission", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=140)
        Label(self.root, text="Course", font=("goudy old style", 15, "bold"), bg="white").place(x=360, y=180)

        Label(self.root, text="State", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=220)
        Label(self.root, text="City", font=("goudy old style", 15, "bold"), bg="white").place(x=310, y=220)
        Label(self.root, text="Pin", font=("goudy old style", 15, "bold"), bg="white").place(x=500, y=220)
        Label(self.root, text="Address", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=260)

        # ================= Entries =================
        self.txt_roll = Entry(self.root, textvariable=self.var_roll,
                              font=("goudy old style", 15, "bold"),
                              bg="lightyellow")
        self.txt_roll.place(x=150, y=60, width=200)

        Entry(self.root, textvariable=self.var_name,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=150, y=100, width=200)

        Entry(self.root, textvariable=self.var_email,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=150, y=140, width=200)

        self.txt_gender = ttk.Combobox(
            self.root,
            textvariable=self.var_gender,
            values=("Select", "Male", "Female", "Other"),
            font=("goudy old style", 15, "bold"),
            state="readonly",
            justify=CENTER
        )
        self.txt_gender.place(x=150, y=180, width=200)
        self.txt_gender.current(0)

        Entry(self.root, textvariable=self.var_dob,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=480, y=60, width=200)

        Entry(self.root, textvariable=self.var_contact,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=480, y=100, width=200)

        Entry(self.root, textvariable=self.var_admission,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=480, y=140, width=200)

        # ================= Course Combobox =================
        self.course_list = []
        self.fetch_course()

        self.txt_course = ttk.Combobox(
            self.root,
            textvariable=self.var_course,
            values=self.course_list,
            font=("goudy old style", 15, "bold"),
            state="readonly",
            justify=CENTER
        )
        self.txt_course.place(x=480, y=180, width=200)
        self.txt_course.set("Select")

        Entry(self.root, textvariable=self.var_state,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=150, y=220, width=150)

        Entry(self.root, textvariable=self.var_city,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=380, y=220, width=100)

        Entry(self.root, textvariable=self.var_pin,
              font=("goudy old style", 15, "bold"),
              bg="lightyellow").place(x=560, y=220, width=120)

        self.txt_address = Text(
            self.root,
            font=("goudy old style", 15, "bold"),
            bg="lightyellow"
        )
        self.txt_address.place(x=150, y=260, width=540, height=100)

        # ================= Buttons =================
        Button(self.root, text="Save", command=self.add, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white").place(x=150, y=400, width=110, height=40)
        Button(self.root, text="Update", command=self.update, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white").place(x=270, y=400, width=110, height=40)
        Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15, "bold"), bg="#f44336", fg="white").place(x=390, y=400, width=110, height=40)
        Button(self.root, text="Clear", command=self.clear, font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white").place(x=510, y=400, width=110, height=40)

        # ================= Search =================
        Entry(self.root, textvariable=self.var_search, font=("goudy old style", 15, "bold"), bg="lightyellow").place(x=870, y=60, width=180)
        Button(self.root, text="Search", command=self.search, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white").place(x=1070, y=60, width=120, height=28)

        # ================= Table =================
        self.C_Frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_Frame.place(x=720, y=100, width=470, height=340)

        scrolly = Scrollbar(self.C_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_Frame, orient=HORIZONTAL)

        self.StudentTable = ttk.Treeview(
            self.C_Frame,
            columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        for col in ("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"):
            self.StudentTable.heading(col, text=col.title())
            self.StudentTable.column(col, width=100)

        self.StudentTable["show"] = "headings"
        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= Fetch Course =================
    def fetch_course(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT name FROM course")
            rows = cur.fetchall()

            self.course_list.clear()

            for row in rows:
                self.course_list.append(row[0])

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # ================= Add =================
    def add(self):
        try:
            con = connect_db()
            cur = con.cursor()

            # ===== Validation =====
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Roll Number is required", parent=self.root)
                return

            # ===== Check Roll Number =====
            if not self.var_roll.get().isdigit():
                messagebox.showerror("Error", "Roll Number must be numeric only", parent=self.root)
                return

            # ===== Duplicate Check =====
            cur.execute("SELECT * FROM student WHERE roll=%s", (self.var_roll.get(),))
            row = cur.fetchone()

            if row is not None:
                messagebox.showerror("Error", "Roll Number already exists", parent=self.root)
                return

            # ===== Insert =====
            cur.execute("""
                INSERT INTO student
                (roll, name, email, gender, dob, contact,
                 admission, course, state, city, pin, address)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                self.var_roll.get(),
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_admission.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0", END)
            ))

            con.commit()

            messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
            self.show()
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================= Update =================
    def update(self):
        try:
            con = connect_db()
            cur = con.cursor()

            # ===== Validation =====
            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Please select student first", parent=self.root)
                return

            if not self.var_roll.get().isdigit():
                messagebox.showerror("Error", "Invalid Roll Number", parent=self.root)
                return

            # ===== Check Student Exists =====
            cur.execute("SELECT * FROM student WHERE roll=%s", (int(self.var_roll.get()),))
            row = cur.fetchone()

            if row is None:
                messagebox.showerror("Error", "Student record not found", parent=self.root)
                return

            # ===== Update Record =====
            cur.execute("""
                UPDATE student SET
                name=%s,
                email=%s,
                gender=%s,
                dob=%s,
                contact=%s,
                admission=%s,
                course=%s,
                state=%s,
                city=%s,
                pin=%s,
                address=%s
                WHERE roll=%s
            """, (
                self.var_name.get(),
                self.var_email.get(),
                self.var_gender.get(),
                self.var_dob.get(),
                self.var_contact.get(),
                self.var_admission.get(),
                self.var_course.get(),
                self.var_state.get(),
                self.var_city.get(),
                self.var_pin.get(),
                self.txt_address.get("1.0", END),
                int(self.var_roll.get())
            ))

            con.commit()

            # ===== Success Message =====
            messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)

            # ===== Refresh Table =====
            self.show()

            # ===== Clear Fields =====
            self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            if 'con' in locals():
                con.close()

    # ================= Delete =================
    def delete(self):
        try:
            con = connect_db()
            cur = con.cursor()

            if self.var_roll.get() == "":
                messagebox.showerror("Error", "Please select student first", parent=self.root)
                return

            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op:
                cur.execute("DELETE FROM student WHERE roll=%s", (self.var_roll.get(),))
                con.commit()
                messagebox.showinfo("Deleted", "Student Deleted Successfully", parent=self.root)
                self.show()
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)
        finally:
            con.close()

    # ================= Show =================
    def show(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()

            self.StudentTable.delete(*self.StudentTable.get_children())

            for row in rows:
                self.StudentTable.insert("", END, values=row)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # ================= Get Data =================
    def get_data(self, ev):
        f = self.StudentTable.focus()
        content = self.StudentTable.item(f)
        row = content["values"]

        if row:
            self.var_roll.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_admission.set(row[6])
            self.var_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])

            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[11])
            self.txt_roll.config(state='readonly')

    # ================= Search =================
    def search(self):
        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute("SELECT * FROM student WHERE roll=%s",
                        (self.var_search.get(),))

            rows = cur.fetchall()

            self.StudentTable.delete(*self.StudentTable.get_children())

            for row in rows:
                self.StudentTable.insert("", END, values=row)

            con.close()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    # ================= Clear =================
    def clear(self):
        self.var_roll.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_admission.set("")
        self.var_course.set("Select")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.var_search.set("")

        self.txt_address.delete("1.0", END)


if __name__ == "__main__":
    root = Tk()
    obj = StudentClass(root)
    root.mainloop()