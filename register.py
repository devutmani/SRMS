from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk   # pip install pillow

from create_db import connect_db


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        # ================= Background =================
        bg_color = "#021e2f"

        left_lbl = Label(self.root, bg="#08A3D2")
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        right_lbl = Label(self.root, bg=bg_color)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # ================= Register Frame =================
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=250, y=80, width=800, height=550)

        title = Label(
            frame1,
            text="REGISTER HERE",
            font=("times new roman", 30, "bold"),
            bg="white",
            fg="#08A3D2"
        )
        title.place(x=250, y=30)

        # ================= Variables =================
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_contact = StringVar()
        self.var_password = StringVar()
        self.var_confirm = StringVar()

        # ================= Name =================
        lbl_name = Label(
            frame1,
            text="Full Name",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_name.place(x=100, y=120)

        self.txt_name = Entry(
            frame1,
            textvariable=self.var_name,
            font=("times new roman", 15),
            bg="lightgray"
        )
        self.txt_name.place(x=100, y=155, width=250, height=35)

        # ================= Email =================
        lbl_email = Label(
            frame1,
            text="Email Address",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_email.place(x=430, y=120)

        self.txt_email = Entry(
            frame1,
            textvariable=self.var_email,
            font=("times new roman", 15),
            bg="lightgray"
        )
        self.txt_email.place(x=430, y=155, width=250, height=35)

        # ================= Contact =================
        lbl_contact = Label(
            frame1,
            text="Contact Number",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_contact.place(x=100, y=240)

        self.txt_contact = Entry(
            frame1,
            textvariable=self.var_contact,
            font=("times new roman", 15),
            bg="lightgray"
        )
        self.txt_contact.place(x=100, y=275, width=250, height=35)

        # ================= Password =================
        lbl_pass = Label(
            frame1,
            text="Password",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_pass.place(x=430, y=240)

        self.txt_pass = Entry(
            frame1,
            textvariable=self.var_password,
            font=("times new roman", 15),
            bg="lightgray",
            show="*"
        )
        self.txt_pass.place(x=430, y=275, width=250, height=35)

        # ================= Confirm Password =================
        lbl_confirm = Label(
            frame1,
            text="Confirm Password",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        lbl_confirm.place(x=100, y=360)

        self.txt_confirm = Entry(
            frame1,
            textvariable=self.var_confirm,
            font=("times new roman", 15),
            bg="lightgray",
            show="*"
        )
        self.txt_confirm.place(x=100, y=395, width=250, height=35)

        # ================= Terms =================
        self.var_check = IntVar()

        check = Checkbutton(
            frame1,
            text="I Agree To The Terms & Conditions",
            variable=self.var_check,
            onvalue=1,
            offvalue=0,
            bg="white",
            font=("times new roman", 12)
        )
        check.place(x=100, y=460)

        # ================= Register Button =================
        btn_register = Button(
            frame1,
            text="Register",
            command=self.register_data,
            font=("times new roman", 20, "bold"),
            fg="white",
            bg="#B00857",
            cursor="hand2"
        )
        btn_register.place(x=430, y=390, width=200, height=45)

        # ================= Login Button =================
        btn_login = Button(
            frame1,
            text="Already Have An Account? Login",
            command=self.login_window,
            font=("times new roman", 12),
            bg="white",
            fg="#B00857",
            bd=0,
            cursor="hand2"
        )
        btn_login.place(x=410, y=455)

    # ================= Register Function =================
    def register_data(self):

        if self.var_name.get() == "" or \
           self.var_email.get() == "" or \
           self.var_contact.get() == "" or \
           self.var_password.get() == "" or \
           self.var_confirm.get() == "":

            messagebox.showerror(
                "Error",
                "All Fields Are Required",
                parent=self.root
            )

        elif self.var_password.get() != self.var_confirm.get():

            messagebox.showerror(
                "Error",
                "Password & Confirm Password Should Be Same",
                parent=self.root
            )

        elif self.var_check.get() == 0:

            messagebox.showerror(
                "Error",
                "Please Agree Our Terms & Conditions",
                parent=self.root
            )

        else:
            try:
                con = connect_db()
                cur = con.cursor()

                # ================= Check Existing User =================
                # FIX: Table was 'employee' — changed to 'teacher' to match create_db and login
                cur.execute(
                    "SELECT * FROM teacher WHERE email=%s",
                    (self.var_email.get(),)
                )

                row = cur.fetchone()

                if row is not None:
                    messagebox.showerror(
                        "Error",
                        "User Already Exists, Try Another Email",
                        parent=self.root
                    )

                else:
                    # FIX: Table was 'employee' — changed to 'teacher'
                    cur.execute(
                        """
                        INSERT INTO teacher
                        (name, email, contact, password)
                        VALUES(%s,%s,%s,%s)
                        """,
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_contact.get(),
                            self.var_password.get()
                        )
                    )

                    con.commit()

                    messagebox.showinfo(
                        "Success",
                        "Registration Successful",
                        parent=self.root
                    )

                    self.clear()

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root
                )

            finally:
                if 'con' in locals():
                    con.close()

    # ================= Clear =================
    def clear(self):
        self.var_name.set("")
        self.var_email.set("")
        self.var_contact.set("")
        self.var_password.set("")
        self.var_confirm.set("")
        self.var_check.set(0)

    # ================= Login Window =================
    # FIX: Was destroying root then importing login with no Tk() — causes crash.
    #      Now destroys current window and opens a fresh Login Tk root.
    def login_window(self):
        self.root.destroy()
        from login import Login_Window
        new_root = Tk()
        Login_Window(new_root)
        new_root.mainloop()


# ================= Main =================
if __name__ == "__main__":
    root = Tk()
    obj = Register(root)
    root.mainloop()
