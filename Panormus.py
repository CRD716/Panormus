from cryptography.fernet import Fernet, InvalidToken
from time import sleep
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.simpledialog as sd
import base64
#End imports

key = b''

def getKey():
	global key
	key = Fernet.generate_key()
	key = sd.askstring(
				"Encryption Key",
				"Enter your encryption key. A key has been generated if you need it.",
				initialvalue = key
				)

def open_file():
	#Open a file for editing.
	filepath = askopenfilename(
		filetypes=[("Panormus Encrypted Document", "*.pan"), ("All Files", "*.*")]
	)
	if not filepath:
		return
	txt_edit.delete(1.0, tk.END)
	with open(filepath, "rb") as input_file:
		rawBytes = input_file.read()
		#Decrypt
		global key
		fernetKey = Fernet(key)
		try:
			text = fernetKey.decrypt(rawBytes).decode()
			txt_edit.insert(tk.END, text)
		except InvalidToken as e:
			print("Invalid Key - Unsuccessfully decrypted ")
			print(e)
	window.title(f"Panormus - {filepath}")

def save_file():
	#Save the current file as a new file.
	filepath = asksaveasfilename(
		defaultextension="pan",
		filetypes=[("Panormus Encrypted Document", "*.pan"), ("All Files", "*.*")],
	)
	if not filepath:
		return
	with open(filepath, "wb") as output_file:
		rawText = txt_edit.get(1.0, tk.END)
		#Encrypt
		global key
		fernetKey = Fernet(key)
		encBytes = fernetKey.encrypt(rawText.encode())
		output_file.write(encBytes)
	window.title(f"Panormus - {filepath}")

window = tk.Tk()
window.title("Panormus")
window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.after(250, getKey)
window.mainloop()