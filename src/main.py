import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip

FILTER = 3
img = None
SIZE = 300
OUTPUT = 1

#Create GUI later...
root = tk.Tk()
root.title("Image to ASCII converter")

def open_file() -> None:
	global file_path, img
	file_path = filedialog.askopenfilename()
	img = file_path
def process() -> None:
	global SIZE, size, FILTER, filter, OUTPUT
	SIZE = int(size.get())
	FILTER = filter.get()
	OUTPUT = outputVar.get()
	root.destroy()
def hlp() -> None:
	messagebox.showinfo("Help", "Filters: ascii 1, ascii 2, and sharp are the prebuilt ones, to have a custom, just input the characters you want in decending order e.g \"@#%+=- \"")
	messagebox.showinfo("Help", "Process button: Remember to press this when you are done applying your settings! If you want to reapply your settings after already pressing process, just hit it again and exit out of the program when you are done, it will copy it to clipboard")
label = tk.Label(root, text="Image to ASCII converter\n\nChoose File")
size_lbl = tk.Label(root, text="Size of output in pixels (Recommended: 100 for simple and 300 for complex images):")
btn = tk.Button(root, text="choose file", command= open_file)
size = tk.Entry()
filter_lbl = tk.Label(root, text="ASCII filter: ")
filter = tk.Entry()
proc_btn = tk.Button(root, text="Process", command= process)
hlp_btn = tk.Button(root, text="?", command=hlp)
outputVar = tk.IntVar()
output = tk.Checkbutton(root, text="Output.txt", variable = outputVar)

hlp_btn.pack()
label.pack()
btn.pack()
size_lbl.pack()
size.pack()
filter_lbl.pack()
filter.pack()
output.pack()
proc_btn.pack()
#if size.get():

root.mainloop()
# I think this is how you read opencv pictures
processed_img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE) # Read as grayscale

# To resize...
h, w = processed_img.shape
a_ratio = h / float(w)
new_width = SIZE
new_height = int(a_ratio * new_width * 0.55)
resized_img = cv2.resize(processed_img, (new_width, new_height))

# ASCII chars from most to least
if FILTER == 'ascii 1':
	ascii_chars = '@%#*+=-:. '
elif FILTER == 'ascii 2':
	ascii_chars = '#@&+=*-. '
elif FILTER == 'sharp':
	ascii_chars = '# '
else:
	ascii_chars = FILTER 
#ascii_chars = '@%#*+=-:. ' if FILTER == 1 else '#@&+=*-. ' if FILTER == 2 else '#  '

# Create a range that acts as a key
def pixel_convert(pixel) -> int:
	# get teh remander of the  pixel value
	# multiplied by how many characters there are -1 
	# because there is zero included in indexes
	index_of = pixel * (len(ascii_chars) -1) // 255 
	return ascii_chars[index_of]

# Now time to use our pixel to ascii converter
ascii_img = []
ascii_img_text = ''
for row in resized_img:
	ascii_row = ''.join([pixel_convert(pixel) for pixel in row])
	ascii_img.append(ascii_row)

for row in ascii_img:
	#print(row)
	ascii_img_text += f'{row}\n'
print(ascii_img_text)
pyperclip.copy(ascii_img_text)
if OUTPUT == 1:
	with open("output.txt", "w") as f:
		f.write(ascii_img_text)