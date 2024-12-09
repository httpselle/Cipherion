from pathlib import Path
from tkinter import Tk, Canvas, Entry, Label, Button, PhotoImage

# Encryption and Decryption logic (adjusted for general text)
def encrypt_decrypt_text(text, shift_letters, shift_digits, encrypt=True):
    encrypted_text = []
    for char in text:
        if char.isalpha():  # For letters
            shift = shift_letters if encrypt else -shift_letters
            new_char = chr(((ord(char.lower()) - ord('a') + shift) % 26) + ord('a'))
            encrypted_text.append(new_char.upper() if char.isupper() else new_char)
        elif char.isdigit():  # For digits
            shift = shift_digits if encrypt else -shift_digits
            new_char = chr(((ord(char) - ord('0') + shift) % 10) + ord('0'))
            encrypted_text.append(new_char)
        else:
            encrypted_text.append(char)  # Non-alphabetic, non-digit characters remain the same
    return ''.join(encrypted_text)

# Define paths for assets
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Joshua Rei Nuñez\Downloads\InfoAssProj\build\assets(3)\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("692x429")
window.configure(bg="#979797")

canvas = Canvas(
    window,
    bg="#979797",
    height=429,
    width=692,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(346.0, 214.0, image=image_image_1)

# Button for encryption
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: process_encryption(True),
    relief="flat"
)
button_1.place(
    x=196.0,
    y=183.0,
    width=119.0,
    height=24.0
)

# Button for decryption
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: process_encryption(False),
    relief="flat"
)
button_2.place(
    x=55.0,
    y=183.0,
    width=125.0,
    height=24.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=12.0,
    y=362.0,
    width=243.0,
    height=39.0
)

# Text box for input
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(180.5, 165.0, image=entry_image_1)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=88.0,
    y=152.0,
    width=185.0,
    height=24.0
)

canvas.create_text(
    84.0,
    140.0,
    anchor="nw",
    text="ENTER TEXT HERE",
    fill="#FFFFFF",
    font=("KantumruyPro Bold", 10 * -1)
)

# Label to display the results in the designed area (Results Label)
results_label = Label(window, text="", bd=0, bg="#043927", fg="#FFFFFF", font=("Arial", 20), anchor="w", justify="left")
results_label.place(x=320.0, y=285.0, width=300.0, height=120.0)

# Process encryption and decryption
def process_encryption(encrypt=True):
    input_text = entry_1.get()
    if not input_text:
        results_label.config(text="Please enter text!")  # Update label text
        return

    shift_letters = 3  # You can customize the shift
    shift_digits = 2   # You can customize the shift for digits

    # Encrypt or Decrypt based on the button pressed
    result = encrypt_decrypt_text(input_text, shift_letters, shift_digits, encrypt)

    # Display the result in the results label
    if encrypt:
        results_label.config(text=f"Encrypted: {result}")
    else:
        results_label.config(text=f"Decrypted: {result}")

window.resizable(False, False)
window.mainloop()
