from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from io import BytesIO
import os

class Stegno:
    def main(self, root):
        root.title('Image Steganography')
        root.geometry('500x600')
        root.resizable(True, True)
        
        main_frame = Frame(root, padx=20, pady=20)
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        title = Label(main_frame, text='Image Steganography', font=('Courier', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=10)

        b_encode = Button(main_frame, text="Encode", command=lambda: self.frame1_encode(main_frame), font=('Courier', 14), width=10)
        b_encode.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        b_decode = Button(main_frame, text="Decode", command=lambda: self.frame1_decode(main_frame), font=('Courier', 14), width=10)
        b_decode.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            main_frame.grid_columnconfigure(i, weight=1)

    def home(self, frame):
        frame.destroy()
        self.main(root)

    def frame1_decode(self, main_frame):
        main_frame.destroy()
        decode_frame = Frame(root, padx=20, pady=20)
        decode_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        l1 = Label(decode_frame, text='Select Image with Hidden Text:', font=('Courier', 18))
        l1.grid(row=0, column=0, columnspan=2, pady=10)

        bws_button = Button(decode_frame, text='Select', command=lambda: self.frame2_decode(decode_frame), font=('Courier', 18))
        bws_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        back_button = Button(decode_frame, text='Cancel', command=lambda: self.home(decode_frame), font=('Courier', 18))
        back_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            decode_frame.grid_columnconfigure(i, weight=1)

    def frame2_decode(self, decode_frame):
        myfile = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpeg;*.jpg')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
            return
        
        decode_frame.destroy()
        password_frame = Frame(root, padx=20, pady=20)
        password_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        l1 = Label(password_frame, text='Enter Password:', font=('Courier', 18))
        l1.grid(row=0, column=0, columnspan=2, pady=10)
        password_entry = Entry(password_frame, show='*', font=('Courier', 18))
        password_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        submit_button = Button(password_frame, text='Submit', command=lambda: self.decode_image(myfile, password_entry.get(), password_frame), font=('Courier', 18))
        submit_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        back_button = Button(password_frame, text='Cancel', command=lambda: self.home(password_frame), font=('Courier', 18))
        back_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            password_frame.grid_columnconfigure(i, weight=1)

    def decode_image(self, filepath, password, frame):
        frame.destroy()
        result_frame = Frame(root, padx=20, pady=20)
        result_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        myimg = Image.open(filepath, 'r')
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)
        
        l4 = Label(result_frame, text='Selected Image:', font=('Courier', 18))
        l4.grid(row=0, column=0, columnspan=2, pady=10)
        panel = Label(result_frame, image=img)
        panel.image = img
        panel.grid(row=1, column=0, columnspan=2)

        hidden_data = self.decode(myimg, password)
        l2 = Label(result_frame, text='Hidden data is:', font=('Courier', 18))
        l2.grid(row=2, column=0, columnspan=2, pady=10)
        text_area = Text(result_frame, width=50, height=10)
        text_area.insert(INSERT, hidden_data)
        text_area.configure(state='disabled')
        text_area.grid(row=3, column=0, columnspan=2)

        back_button = Button(result_frame, text='Back', command=lambda: self.home(result_frame), font=('Courier', 14))
        back_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        show_info = Button(result_frame, text='More Info', command=self.info, font=('Courier', 14))
        show_info.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            result_frame.grid_columnconfigure(i, weight=1)

    def decode(self, image, password):
        data = ''
        imgdata = iter(image.getdata())

        while True:
            pixels = [value for value in imgdata.__next__()[:3] +
                      imgdata.__next__()[:3] +
                      imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binstr += '0'
                else:
                    binstr += '1'

            char = chr(int(binstr, 2))
            data += char
            if pixels[-1] % 2 != 0:
                break

        return self.xor_encrypt(data, password)

    def frame1_encode(self, main_frame):
        main_frame.destroy()
        encode_frame = Frame(root, padx=20, pady=20)
        encode_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        l1 = Label(encode_frame, text='Select the Image to Hide Text:', font=('Courier', 18))
        l1.grid(row=0, column=0, columnspan=2, pady=10)

        bws_button = Button(encode_frame, text='Select', command=lambda: self.frame2_encode(encode_frame), font=('Courier', 18))
        bws_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        back_button = Button(encode_frame, text='Cancel', command=lambda: self.home(encode_frame), font=('Courier', 18))
        back_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            encode_frame.grid_columnconfigure(i, weight=1)

    def frame2_encode(self, encode_frame):
        myfile = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpeg;*.jpg')])
        if not myfile:
            messagebox.showerror("Error", "You have selected nothing!")
            return
        
        encode_frame.destroy()
        text_frame = Frame(root, padx=20, pady=20)
        text_frame.grid(row=0, column=0, sticky="nsew")
        
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        myimg = Image.open(myfile)
        myimage = myimg.resize((300, 200))
        img = ImageTk.PhotoImage(myimage)
        
        l3 = Label(text_frame, text='Selected Image:', font=('Courier', 18))
        l3.grid(row=0, column=0, columnspan=2, pady=10)
        panel = Label(text_frame, image=img)
        panel.image = img
        panel.grid(row=1, column=0, columnspan=2)
        
        self.output_image_size = os.stat(myfile)
        self.o_image_w, self.o_image_h = myimg.size

        l2 = Label(text_frame, text='Enter the Message:', font=('Courier', 18))
        l2.grid(row=2, column=0, columnspan=2, pady=10)
        text_area = Text(text_frame, width=50, height=10)
        text_area.grid(row=3, column=0, columnspan=2)

        l4 = Label(text_frame, text='Enter Password:', font=('Courier', 18))
        l4.grid(row=4, column=0, columnspan=2, pady=10)
        password_entry = Entry(text_frame, show='*', font=('Courier', 18))
        password_entry.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        encode_button = Button(text_frame, text='Encode', command=lambda: [self.enc_fun(text_area, myimg, password_entry.get()), self.home(text_frame)], font=('Courier', 14))
        encode_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        back_button = Button(text_frame, text='Cancel', command=lambda: self.home(text_frame), font=('Courier', 14))
        back_button.grid(row=6, column=1, padx=10, pady=10, sticky="ew")

        for i in range(2):
            text_frame.grid_columnconfigure(i, weight=1)

    def enc_fun(self, text_area, myimg, password):
        data = text_area.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Please enter text in the TextBox")
        else:
            newimg = myimg.copy()
            encrypted_data = self.xor_encrypt(data, password)
            self.encode_enc(newimg, encrypted_data)
            temp = os.path.splitext(os.path.basename(myimg.filename))[0]
            saved_path = filedialog.asksaveasfilename(initialfile=temp, filetypes=[('PNG', '*.png')], defaultextension=".png")
            newimg.save(saved_path)
            self.d_image_size = os.stat(saved_path).st_size
            self.d_image_w, self.d_image_h = newimg.size
            messagebox.showinfo("Success", f"Encoding Successful\nFile is saved as {os.path.basename(saved_path)}")

    def info(self):
        try:
            info_str = (f"Original Image:\n"
                        f"Size: {self.output_image_size.st_size / 1000000:.2f} MB\n"
                        f"Width: {self.o_image_w}\n"
                        f"Height: {self.o_image_h}\n\n"
                        f"Encoded Image:\n"
                        f"Size: {self.d_image_size / 1000000:.2f} MB\n"
                        f"Width: {self.d_image_w}\n"
                        f"Height: {self.d_image_h}")
            messagebox.showinfo("Image Info", info_str)
        except Exception as e:
            messagebox.showinfo("Info", f"Unable to get the information: {e}")

    def genData(self, data):
        newd = [format(ord(i), '08b') for i in data]
        return newd

    def modPix(self, pix, data):
        datalist = self.genData(data)
        lendata = len(datalist)
        imdata = iter(pix)

        for i in range(lendata):
            pixels = [value for value in imdata.__next__()[:3] +
                      imdata.__next__()[:3] +
                      imdata.__next__()[:3]]

            for j in range(0, 8):
                if datalist[i][j] == '0' and pixels[j] % 2 != 0:
                    pixels[j] -= 1
                elif datalist[i][j] == '1' and pixels[j] % 2 == 0:
                    pixels[j] += 1

            if i == lendata - 1:
                if pixels[-1] % 2 == 0:
                    pixels[-1] -= 1
            else:
                if pixels[-1] % 2 != 0:
                    pixels[-1] -= 1

            yield tuple(pixels[:3])
            yield tuple(pixels[3:6])
            yield tuple(pixels[6:9])

    def encode_enc(self, newimg, data):
        w = newimg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modPix(newimg.getdata(), data):
            newimg.putpixel((x, y), pixel)
            if x == w - 1:
                x = 0
                y += 1
            else:
                x += 1

    def xor_encrypt(self, data, key):
        key = key or 'default_password'
        return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(data, key * (len(data) // len(key) + 1)))

root = Tk()
app = Stegno()
app.main(root)
root.mainloop()
