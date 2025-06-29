import pyodbc
import re
from cryptography.fernet import Fernet
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, Label, PhotoImage, StringVar, messagebox


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Joshua Rei Nuñez\Downloads\InfoAssProj\build\assets(2)\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to open the login window and close the signup window
def open_login():
    window.destroy()  # Close the signup window
    import login  # Open the login window (make sure 'login.py' is in the same directory)

# Custom shift_char function for encryption/decryption
def shift_char(c, shift_letters, shift_digits, encrypt=True):
    if not encrypt:
        shift_letters = -shift_letters
        shift_digits = -shift_digits
    
    # Handle uppercase letters
    if 'A' <= c <= 'Z':
        new_position = (ord(c) - ord('A') + shift_letters) % 26
        return chr(new_position + ord('A'))
    
    # Handle lowercase letters
    elif 'a' <= c <= 'z':
        new_position = (ord(c) - ord('a') + shift_letters) % 26
        return chr(new_position + ord('a'))
    
    # Handle digits (0-9)
    elif '0' <= c <= '9':
        new_position = (ord(c) - ord('0') + shift_digits) % 10
        return chr(new_position + ord('0'))
    
    # Special characters remain unchanged
    else:
        return c

# Function to encrypt/decrypt the password using shift_char algorithm
def encrypt_decrypt_password(password, shift_letters, shift_digits, encrypt=True):
    return ''.join([shift_char(c, shift_letters, shift_digits, encrypt) for c in password])

# Modify the register_user function to use shift_char encryption
def register_user():
    # Get user input
    username = entry_1.get()
    email = entry_2.get()
    password = password_var.get()
    confirm_password = confirm_password_var.get()

    # Validate that none of the fields are empty
    if not username or not email or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Validate email format
    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format!")
        return
    
    # Check if the email already exists
    if check_email_exists(email):
        messagebox.showerror("Error", "Email is already used!")
        return

    # Validate that the passwords match
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Validate password strength
    if not validate_password_strength(password):
        messagebox.showerror("Error", "Password is not strong enough!")
        return

    # Check if the username already exists
    if check_username_exists(username):
        messagebox.showerror("Error", "Username already exists!")
        return

    # Encrypt the password before saving to the database
    shift_letters = 3  # Define how many positions to shift letters
    shift_digits = 2   # Define how many positions to shift digits
    encrypted_password = encrypt_decrypt_password(password, shift_letters, shift_digits, encrypt=True)

    # Establish database connection
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MEDUSA\\SQLEXPRESS;"  # Update with your server name
        "DATABASE=UserAuthDB;"        # Update with your database name
        "Trusted_Connection=yes;"     # Use authentication as applicable
    )
    
    
    cursor = conn.cursor()

    # SQL query to insert new user data
    try:
        cursor.execute(
            "INSERT INTO Signup (username, email, password) VALUES (?, ?, ?)",
            (username, email, encrypted_password)  # Insert encrypted password
        )
        conn.commit()  # Commit the transaction
        messagebox.showinfo("Success", "User registered successfully!")

        # Clear all fields after successful registration
        entry_1.delete(0, 'end')  # Clear username field
        entry_2.delete(0, 'end')  # Clear email field
        password_var.set('')  # Clear password field
        confirm_password_var.set('')  # Clear confirm password field
        
       

    except Exception as e:
        messagebox.showerror("Error", f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Use this for login or decryption of the password when needed
def decrypt_password(encrypted_password, shift_letters, shift_digits):
    return encrypt_decrypt_password(encrypted_password, shift_letters, shift_digits, encrypt=False)



def validate_email(email):
    # Simple email validation using regex
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email)

def validate_password_strength(password):
    # Validate password strength: At least 8 characters, at least one number, one uppercase letter, and no spaces
    if len(password) < 8 or len(password) > 20:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if " " in password:
        return False
    return True

def check_username_exists(username):
    # Check if the username already exists in the database
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MEDUSA\\SQLEXPRESS;"  # Update with your server name
        "DATABASE=UserAuthDB;"        # Update with your database name
        "Trusted_Connection=yes;"     # Use authentication as applicable
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Signup WHERE username=?", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] > 0

def check_email_exists(email):
    # Check if the email already exists in the database
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=MEDUSA\\SQLEXPRESS;"  # Update with your server name
        "DATABASE=UserAuthDB;"        # Update with your database name
        "Trusted_Connection=yes;"     # Use authentication as applicable
    )
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Signup WHERE email=?", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] > 0

# Function to encrypt the password using Fernet
def encrypt_password(password):
    # Generate a key for encryption (it should be securely stored and reused for decryption)
    encryption_key = b'YOUR_SECRET_KEY_HERE'  # Replace with a securely stored key
    cipher = Fernet(encryption_key)
    encrypted_password = cipher.encrypt(password.encode('utf-8'))
    return encrypted_password

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

# Background image
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(346.0, 214.0, image=image_image_1)

# Variables for password fields
password_var = StringVar()
confirm_password_var = StringVar()

# Username field
canvas.create_text(
    235.0,
    118.0,
    anchor="nw",
    text="USERNAME",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(343.0, 142.0, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_1.place(x=244.0, y=130.0, width=198.0, height=22.0)

# Email field
canvas.create_text(
    235.0,
    159.0,
    anchor="nw",
    text="EMAIL",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(343.0, 183.0, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
entry_2.place(x=244.0, y=171.0, width=198.0, height=22.0)

# Password field
canvas.create_text(
    235.0,
    200.0,
    anchor="nw",
    text="PASSWORD",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(343.0, 226.0, image=entry_image_3)
entry_3 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, textvariable=password_var, show="*")
entry_3.place(x=244.0, y=214.0, width=198.0, height=22.0)

# Confirm password field
canvas.create_text(
    235.0,
    304.0,
    anchor="nw",
    text="CONFIRM PASSWORD",
    fill="#000000",
    font=("KantumruyPro Regular", 10 * -1)
)

entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(343.0, 330.0, image=entry_image_4)
entry_4 = Entry(bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0, textvariable=confirm_password_var, show="*")
entry_4.place(x=244.0, y=318.0, width=198.0, height=22.0)

# Password requirements labels
req_labels = {
    "length": Label(window, text="❌ 8-20 Characters", font=("KantumruyPro Regular", 6), bg="#D8F3DC", fg="#CC0B0B"),
    "uppercase": Label(window, text="❌ At least one capital letter", font=("KantumruyPro Regular", 6), bg="#D8F3DC", fg="#CC0B0B"),
    "number": Label(window, text="❌ At least one number", font=("KantumruyPro Regular", 6), bg="#D8F3DC", fg="#CC0B0B"),
    "no_spaces": Label(window, text="❌ No spaces", font=("KantumruyPro Regular", 6), bg="#D8F3DC", fg="#CC0B0B"),
    "match": Label(window, text="❌ Password Match", font=("KantumruyPro Regular", 6), bg="#D8F3DC", fg="#CC0B0B"),
}

# Place requirements labels
req_labels["length"].place(x=253.0, y=240.0)
req_labels["uppercase"].place(x=253.0, y=252.0)
req_labels["number"].place(x=253.0, y=264.0)
req_labels["no_spaces"].place(x=253.0, y=276.0)
req_labels["match"].place(x=253.0, y=288.0)

# Validate password in real-time
def validate_password(*args):
    password = password_var.get()
    confirm_password = confirm_password_var.get()

    # Length check
    if 8 <= len(password) <= 20:
        req_labels["length"].config(text="✔️ 8-20 Characters", fg="#00A300")
    else:
        req_labels["length"].config(text="❌ 8-20 Characters", fg="#CC0B0B")

    # Uppercase check
    if any(char.isupper() for char in password):
        req_labels["uppercase"].config(text="✔️ At least one capital letter", fg="#00A300")
    else:
        req_labels["uppercase"].config(text="❌ At least one capital letter", fg="#CC0B0B")

    # Number check
    if any(char.isdigit() for char in password):
        req_labels["number"].config(text="✔️ At least one number", fg="#00A300")
    else:
        req_labels["number"].config(text="❌ At least one number", fg="#CC0B0B")

    # Space check
    if " " not in password:
        req_labels["no_spaces"].config(text="✔️ No spaces", fg="#00A300")
    else:
        req_labels["no_spaces"].config(text="❌ No spaces", fg="#CC0B0B")

    # Match check
    if password == confirm_password and password != "":
        req_labels["match"].config(text="✔️ Password Match", fg="#00A300")
    else:
        req_labels["match"].config(text="❌ Password Match", fg="#CC0B0B")

# Trace password field updates
password_var.trace("w", validate_password)
confirm_password_var.trace("w", validate_password)

# Toggle visibility for Password
def toggle_password():
    current_show = entry_3.cget("show")
    if current_show == "*":
        entry_3.config(show="")  # Show password
        eye_label_1.config(image=closed_eye_image)
    else:
        entry_3.config(show="*")  # Hide password
        eye_label_1.config(image=open_eye_image)

# Toggle visibility for Confirm Password
def toggle_confirm_password():
    current_show = entry_4.cget("show")
    if current_show == "*":
        entry_4.config(show="")  # Show password
        eye_label_2.config(image=closed_eye_image)
    else:
        entry_4.config(show="*")  # Hide password
        eye_label_2.config(image=open_eye_image)

# Load eye images
open_eye_image = PhotoImage(file=relative_to_assets("show.png"))
closed_eye_image = PhotoImage(file=relative_to_assets("hide.png"))

# Eye button for Password
eye_label_1 = Label(window, image=open_eye_image, bg="#FFFFFF", bd=0, cursor="hand2")
eye_label_1.place(x=430.0, y=214.0, width=22, height=22)
eye_label_1.bind("<Button-1>", lambda e: toggle_password())

# Eye button for Confirm Password
eye_label_2 = Label(window, image=open_eye_image, bg="#FFFFFF", bd=0, cursor="hand2")
eye_label_2.place(x=430.0, y=318.0, width=22, height=22)
eye_label_2.bind("<Button-1>", lambda e: toggle_confirm_password())

# Signup button
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=register_user,
    relief="flat"
)
button_1.place(x=294.0, y=356.0, width=103.0, height=19.0)

# "Already have an account?" button
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=open_login,  # Open login page
    relief="flat",
    bg="#D8F3DC",
    activebackground="#D8F3DC",
    highlightbackground="#D8F3DC"
)
button_2.place(x=225.0, y=389.0, width=243.0, height=12.0)

window.resizable(False, False)
window.mainloop()
