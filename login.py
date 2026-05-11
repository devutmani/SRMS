from tkinter import *
from PIL import Image, ImageTk, ImageDraw   # pip install Pillow
from datetime import datetime
from math import *
from tkinter import messagebox

from create_db import connect_db


class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")

        # ================= Background =================
        left_lbl = Label(self.root, bg="#08A3D2", bd=0)
        left_lbl.place(x=0, y=0, relheight=1, width=600)

        right_lbl = Label(self.root, bg="#031F3C", bd=0)
        right_lbl.place(x=600, y=0, relheight=1, relwidth=1)

        # ================= Login Frame =================
        login_frame = Frame(self.root, bg="white")
        login_frame.place(x=250, y=100, width=800, height=500)

        title = Label(
            login_frame,
            text="LOGIN HERE",
            font=("times new roman", 30, "bold"),
            bg="white",
            fg="#08A3D2"
        )
        title.place(x=250, y=50)

        # ================= Email =================
        email = Label(
            login_frame,
            text="EMAIL ADDRESS",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        email.place(x=250, y=150)

        self.txt_email = Entry(
            login_frame,
            font=("times new roman", 15),
            bg="lightgray"
        )
        self.txt_email.place(x=250, y=180, width=350, height=35)

        # ================= Password =================
        pass_ = Label(
            login_frame,
            text="PASSWORD",
            font=("times new roman", 18, "bold"),
            bg="white",
            fg="gray"
        )
        pass_.place(x=250, y=250)

        self.txt_pass_ = Entry(
            login_frame,
            font=("times new roman", 15),
            bg="lightgray",
            show="*"
        )
        self.txt_pass_.place(x=250, y=280, width=350, height=35)

        # ================= Register Button =================
        btn_reg = Button(
            login_frame,
            text="Register New Account?",
            command=self.register_window,
            font=("times new roman", 14),
            bg="white",
            bd=0,
            fg="#B00857",
            cursor="hand2"
        )
        btn_reg.place(x=250, y=320)

        # ================= Forget Password =================
        btn_forget = Button(
            login_frame,
            text="Forget Password?",
            command=self.forget_password,
            font=("times new roman", 14),
            bg="white",
            bd=0,
            fg="#B00857",
            cursor="hand2"
        )
        btn_forget.place(x=450, y=320)

        # ================= Login Button =================
        btn_login = Button(
            login_frame,
            text="Login",
            command=self.login,
            font=("times new roman", 20, "bold"),
            fg="white",
            bg="#B00857",
            cursor="hand2"
        )
        btn_login.place(x=250, y=380, width=180, height=40)

        # ================= Clock Label =================
        self.lbl = Label(
            self.root,
            text="\nDev Kumar",
            font=("Book Antiqua", 25, "bold"),
            fg="white",
            compound=BOTTOM,
            bg="#081923",
            bd=0
        )
        self.lbl.place(x=90, y=120, height=450, width=350)

        self.working()

    # ================= Register Window =================
    def register_window(self):
        self.root.destroy()
        import register

    # ================= Forget Password =================
    def forget_password(self):

        if self.txt_email.get() == "":
            messagebox.showerror(
                "Error",
                "Please Enter Email Address First",
                parent=self.root
            )
            return

        try:
            con = connect_db()
            cur = con.cursor()

            cur.execute(
                "SELECT * FROM teacher WHERE email=%s",
                (self.txt_email.get(),)
            )

            row = cur.fetchone()

            if row is None:
                messagebox.showerror(
                    "Error",
                    "Invalid Email Address",
                    parent=self.root
                )

            else:
                self.root2 = Toplevel()
                self.root2.title("Reset Password")
                self.root2.geometry("400x350+500+200")
                self.root2.config(bg="white")
                self.root2.focus_force()
                self.root2.grab_set()

                # ================= Title =================
                title = Label(
                    self.root2,
                    text="Reset Password",
                    font=("times new roman", 20, "bold"),
                    bg="white",
                    fg="#3f51b5"
                )
                title.pack(pady=20)

                # ================= New Password =================
                lbl_new = Label(
                    self.root2,
                    text="New Password",
                    font=("times new roman", 15, "bold"),
                    bg="white"
                )
                lbl_new.place(x=50, y=100)

                self.txt_new_pass = Entry(
                    self.root2,
                    font=("times new roman", 15),
                    bg="lightyellow",
                    show="*"
                )
                self.txt_new_pass.place(x=50, y=140, width=300)

                # ================= Confirm Password =================
                lbl_confirm = Label(
                    self.root2,
                    text="Confirm Password",
                    font=("times new roman", 15, "bold"),
                    bg="white"
                )
                lbl_confirm.place(x=50, y=190)

                self.txt_confirm_pass = Entry(
                    self.root2,
                    font=("times new roman", 15),
                    bg="lightyellow",
                    show="*"
                )
                self.txt_confirm_pass.place(x=50, y=230, width=300)

                # ================= Reset Button =================
                btn_reset = Button(
                    self.root2,
                    text="Reset Password",
                    command=self.reset_password,
                    font=("times new roman", 15, "bold"),
                    bg="#3f51b5",
                    fg="white",
                    cursor="hand2"
                )
                btn_reset.place(x=110, y=290, width=180, height=40)

        except Exception as es:
            messagebox.showerror(
                "Error",
                f"Error Due To : {str(es)}",
                parent=self.root
            )

        finally:
            if 'con' in locals():
                con.close()

    # ================= Reset Password =================
    def reset_password(self):

        if self.txt_new_pass.get() == "" or self.txt_confirm_pass.get() == "":
            messagebox.showerror(
                "Error",
                "All Fields Are Required",
                parent=self.root2
            )

        elif self.txt_new_pass.get() != self.txt_confirm_pass.get():
            messagebox.showerror(
                "Error",
                "Passwords Do Not Match",
                parent=self.root2
            )

        else:
            try:
                con = connect_db()
                cur = con.cursor()

                cur.execute(
                    "UPDATE teacher SET password=%s WHERE email=%s",
                    (
                        self.txt_new_pass.get(),
                        self.txt_email.get()
                    )
                )

                con.commit()

                messagebox.showinfo(
                    "Success",
                    "Password Changed Successfully",
                    parent=self.root2
                )

                self.root2.destroy()

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root2
                )

            finally:
                if 'con' in locals():
                    con.close()

    # ================= Login =================
    def login(self):

        if self.txt_email.get() == "" or self.txt_pass_.get() == "":
            messagebox.showerror(
                "Error",
                "All Fields Are Required",
                parent=self.root
            )

        else:
            try:
                con = connect_db()
                cur = con.cursor()

                cur.execute(
                    "SELECT * FROM teacher WHERE email=%s AND password=%s",
                    (
                        self.txt_email.get(),
                        self.txt_pass_.get()
                    )
                )

                row = cur.fetchone()

                if row is None:
                    messagebox.showerror(
                        "Error",
                        "Invalid Email or Password",
                        parent=self.root
                    )

                else:
                    messagebox.showinfo(
                        "Success",
                        f"Welcome {row[1]}",
                        parent=self.root
                    )

                    self.root.destroy()

                    import dashboard

                con.close()

            except Exception as es:
                messagebox.showerror(
                    "Error",
                    f"Error Due To : {str(es)}",
                    parent=self.root
                )

    # ================= Clock Image =================
    def clock_image(self, hr, min_, sec_):

        clock = Image.new("RGB", (400, 400), (8, 25, 35))
        draw = ImageDraw.Draw(clock)

        try:
            bg = Image.open("images/c.png")
            bg = bg.resize((300, 300), Image.Resampling.LANCZOS)
            clock.paste(bg, (50, 50))
        except:
            pass

        origin = 200, 200

        # ================= Hour Hand =================
        draw.line(
            (
                origin,
                200 + 50 * sin(radians(hr)),
                200 - 50 * cos(radians(hr))
            ),
            fill="#DF005E",
            width=4
        )

        # ================= Minute Hand =================
        draw.line(
            (
                origin,
                200 + 80 * sin(radians(min_)),
                200 - 80 * cos(radians(min_))
            ),
            fill="white",
            width=3
        )

        # ================= Second Hand =================
        draw.line(
            (
                origin,
                200 + 100 * sin(radians(sec_)),
                200 - 100 * cos(radians(sec_))
            ),
            fill="yellow",
            width=2
        )

        draw.ellipse((195, 195, 210, 210), fill="#1AD5D5")

        return clock

    # ================= Clock Working =================
    def working(self):

        h = datetime.now().hour
        m = datetime.now().minute
        s = datetime.now().second

        hr = (h / 12) * 360
        min_ = (m / 60) * 360
        sec_ = (s / 60) * 360

        clock_img = self.clock_image(hr, min_, sec_)

        self.img = ImageTk.PhotoImage(clock_img)

        self.lbl.config(image=self.img)

        self.lbl.after(200, self.working)


# ================= Main =================
if __name__ == "__main__":

    root = Tk()
    obj = Login_Window(root)
    root.mainloop()