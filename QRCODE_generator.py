import tkinter as tk
import qrcode
import cv2
import webbrowser
import os
from tkinter import messagebox, filedialog, colorchooser
from PIL import Image, ImageTk

# -------- GLOBAL VARIABLES -------- #
history = []
qr_color = "black"
bg_color = "white"

#  TWO FILES (IMPORTANT PART OF OPTION 2)
DISPLAY_QR = "colored_qr.png"
SAFE_QR = "qrcode.png"


# -------- GENERATE QR -------- #
def generate_qr():
    global history

    data = entry.get()

    if data == "":
        messagebox.showwarning("⚠️ Warning", "Enter text or URL")
        return

    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    #  Colored QR (for display only)
    colored_img = qr.make_image(
        fill_color=qr_color,
        back_color=bg_color
    ).convert("RGB")

    #  SAFE QR (for scanning)
    safe_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    # Save BOTH
    colored_img.save(DISPLAY_QR)
    safe_img.save(SAFE_QR)

    # Show colored QR in GUI
    show_qr(DISPLAY_QR)

    history.append(data)
    update_history()

    messagebox.showinfo("✅ Done", "QR Generated Successfully!")


# -------- SHOW QR -------- #
def show_qr(path):
    img = Image.open(path)
    img = img.resize((220, 220))
    img = ImageTk.PhotoImage(img)

    qr_label.config(image=img)
    qr_label.image = img


# -------- SCAN FROM IMAGE -------- #
def scan_from_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )

    if not file_path:
        return

    img = cv2.imread(file_path)

    if img is None:
        messagebox.showerror("Error", "Cannot load image")
        return

    #  ALWAYS USE SAFE SCAN METHOD
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(gray)

    if data:
        messagebox.showinfo("Result", data)

        if data.startswith("http"):
            webbrowser.open(data)
    else:
        messagebox.showinfo("Result", "No QR found")


# -------- COLORS -------- #
def pick_qr_color():
    global qr_color
    color = colorchooser.askcolor()[1]
    if color:
        qr_color = color


def pick_bg_color():
    global bg_color
    color = colorchooser.askcolor()[1]
    if color:
        bg_color = color


# -------- HISTORY -------- #
def update_history():
    history_box.delete(0, tk.END)
    for item in history[-10:]:
        history_box.insert(tk.END, item)


def use_selected():
    try:
        selected = history_box.get(history_box.curselection())
        entry.delete(0, tk.END)
        entry.insert(0, selected)
    except:
        pass


# -------- GUI -------- #
root = tk.Tk()
root.title(" Advanced QR Tool (Option 2)")
root.geometry("450x650")
root.config(bg="#121212")

FONT = ("Segoe UI", 11)

tk.Label(root, text="QR Generator + Scanner",
         font=("Segoe UI", 18, "bold"),
         bg="#121212", fg="#00ffd5").pack(pady=10)

entry = tk.Entry(root, width=35, font=FONT, justify="center")
entry.pack(pady=10)

# Buttons
tk.Button(root, text="Generate QR", command=generate_qr,
          bg="#4CAF50", fg="white", font=FONT).pack(pady=5)

tk.Button(root, text="Scan from Image", command=scan_from_image,
          bg="#FF9800", fg="white", font=FONT).pack(pady=5)

tk.Button(root, text="Pick QR Color", command=pick_qr_color,
          bg="#9C27B0", fg="white", font=FONT).pack(pady=5)

tk.Button(root, text="Pick Background Color", command=pick_bg_color,
          bg="#FF5722", fg="white", font=FONT).pack(pady=5)

# QR Display
qr_label = tk.Label(root, bg="#121212")
qr_label.pack(pady=15)

# History
tk.Label(root, text="History (last 10)",
         bg="#121212", fg="white", font=FONT).pack()

history_box = tk.Listbox(root, width=40, height=8)
history_box.pack(pady=10)

tk.Button(root, text="Use Selected",
          command=use_selected,
          bg="#607D8B", fg="white").pack(pady=5)

# Footer
tk.Label(root, text="Made with Python 🚀",
         bg="#121212", fg="#888").pack(side="bottom", pady=10)

root.mainloop()