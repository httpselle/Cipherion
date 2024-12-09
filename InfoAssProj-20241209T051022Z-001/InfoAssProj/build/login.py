from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, Label, PhotoImage, messagebox
import subprocess
import pyodbc
import os

# Define paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Joshua Rei Nuñez\Downloads\InfoAssProj\build\assets(1)\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def open_signup():
    # Close the current window (login window)
    window.destroy()
    
    # Open the signup window (Ensure signup.py is in the same directory)
    import signup

# Function to encrypt/decrypt the password (same as during signup)
def encrypt_decrypt_password(password, shift_letters, shift_digits, encrypt=True):
    encrypted_password = []
    for char in password:
        if char.isalpha():  # For letters
            shift = shift_letters if encrypt else -shift_letters
            new_char = chr(((ord(char.lower()) - ord('a') + shift) % 26) + ord('a'))
            encrypted_password.append(new_char.upper() if char.isupper() else new_char)
        elif char.isdigit():  # For digits
            shift = shift_digits if encrypt else -shift_digits
            new_char = chr(((ord(char) - ord('0') + shift) % 10) + ord('0'))
            encrypted_password.append(new_char)
        else:
            encrypted_password.append(char)  # Non-alphabetic, non-digit characters remain the same
    return ''.join(encrypted_password)

def open_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    if os.path.exists(dashboard_path):
        try:
            subprocess.run(['python', dashboard_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {e}")
    else:
        messagebox.showerror("Error", "Dashboard file not found!")

def login_user():
    username = entry_1.get()
    password = entry_2.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required!")
        return

    # Encrypt the password using the same method used in signup
    shift_letters = 3
    shift_digits = 2
    encrypted_password = encrypt_decrypt_password(password, shift_letters, shift_digits, encrypt=True)

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MEDUSA\\SQLEXPRESS;"
        "DATABASE=UserAuthDB;"
        "Trusted_Connection=yes;"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM Signup WHERE username=?", (username,))
    result = cursor.fetchone()

    if result and result[0] == encrypted_password:
        cursor.execute("INSERT INTO Login (Username, Password) VALUES (?, ?)", (username, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Login successful!")

        # Close the current login window
        window.destroy()
        
        # Open the dashboard
        open_dashboard()

    else:
        messagebox.showerror("Error", "Invalid username or password!")

    cursor.close()
    conn.close()

# Setup window
window = Tk()
window.geometry("692x429")
window.configure(bg="#D8F3DC")

canvas = Canvas(
    window,
    bg="#D8F3DC",
    height=429,
    width=692,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(346.0, 214.0, image=image_image_1)

canvas.create_text(
    233.0,
    222.0,
    anchor="nw",
    text="USERNAME",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(344.0, 249.0, image=entry_image_1)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=245.0,
    y=237.0,
    width=198.0,
    height=22.0
)

canvas.create_text(
    233.0,
    276.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(344.0, 308.0, image=entry_image_2)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"  # This will hide the password initially
)
entry_2.place(
    x=245.0,
    y=296.0,
    width=198.0,
    height=22.0
)

# Load eye images
open_eye_image = PhotoImage(file=relative_to_assets("show.png"))
closed_eye_image = PhotoImage(file=relative_to_assets("hide.png"))

# Function to toggle the password visibility
def toggle_password():
    current_show = entry_2.cget("show")
    if current_show == "*":
        entry_2.config(show="")  # Show the password
        eye_label.config(image=closed_eye_image)  # Switch to closed eye image
    else:
        entry_2.config(show="*")  # Hide the password
        eye_label.config(image=open_eye_image)  # Switch to open eye image

# Create the eye label (using images for the eye) with white background
eye_label = Label(window, image=open_eye_image, bg="#FFFFFF", bd=0, relief="flat", cursor="hand2")
eye_label.place(x=430.0, y=296.0, width=22, height=22)

# Bind the toggle function to the eye image click event
eye_label.bind("<Button-1>", lambda e: toggle_password())

# Login Button (execute login_user function)
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=login_user,  # Link to the login function
    relief="flat",
    bg="#D8F3DC",  # Ensure the button background is the same as the window's background
    activebackground="#D8F3DC",  # Remove background color change when clicked
    highlightbackground="#D8F3DC",  # Remove any border highlighting
   
)
button_1.place(
    x=293.0,
    y=345.0,
    width=103.0,
    height=19.0
)

# Sign-up button (open signup window)
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_signup,  # Link the button to open signup window
    relief="flat",
    bg="#D8F3DC",  # Ensure the button background is the same as the window's background
    activebackground="#D8F3DC",  # Remove background color change when clicked
    highlightbackground="#D8F3DC"  # Remove any border highlighting
)
button_2.place(
    x=223.0,
    y=389.0,
    width=243.0,
    height=12.0
)

# Adding "Doesn't have an account?" text without a background
canvas.create_text(
    233.0,
    389.0,  # Adjust the y-position based on your design
    anchor="nw",
    text="Doesn't have an account?",  # Updated text
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

window.resizable(False, False)
window.mainloop()
