import tkinter.filedialog
import tkinter.ttk as ttk
import tkinter.filedialog
from tkinter import simpledialog
from tkinter import messagebox
from tkinter.filedialog import *
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from PIL import ImageGrab
import csv
from copy import deepcopy
import copy
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

nccLevialdi = 0
iterationLevialdi = 0
iterationTSF = 0
pixelMapAsString=""
openedImage=None
binaryImage=None
framedImage=None

root = Tk()

def main():

    global root

    root.geometry("1622x962+247+16")
    root.title("Object Counter")

    root.Button1 = tk.Button(root)
    root.Button1.place(relx=0.031, rely=0.01, height=24, width=59)
    root.Button1.configure(background="#d9d9d9",text="File",width=59, command=openImage)

    root.Button2 = tk.Button(root)
    root.Button2.place(relx=0.08, rely=0.01, height=24, width=65)
    root.Button2.configure(background="#d9d9d9",text="Create",width=65,command= createImage)

    root.Button3 = tk.Button(root)
    root.Button3.place(relx=0.943, rely=0.01, height=24, width=67)
    root.Button3.configure(background="#d9d9d9",text="Save",width=67, command = saveReport)

    root.menubar = tk.Menu(root, font="TkMenuFont")
    root.configure(menu=root.menubar)

    root.Button4 = tk.Button(root)
    root.Button4.place(relx=0.937, rely=0.500, height=54, width=87)
    root.Button4.configure(background="#d9d9d9",text="TSF",width=87,command=lambda: TSF(framedImage))

    root.Button5 = tk.Button(root)
    root.Button5.place(relx=0.937, rely=0.052, height=54, width=87)
    root.Button5.configure(background="#d9d9d9",text="LEV",width=87,command= lambda:levialdi(framedImage))

    root.Button6 = tk.Button(root)
    root.Button6.place(relx=0.520, rely=0.013, height=25, width=90)
    root.Button6.configure(background="#d9d9d9",text="Send report to: ",width=70, command =lambda: sendReportToMail(getMailAddress))

    root.Label1 = tk.Label(root)
    root.Label1.place(relx=0.930, rely=0.135, height=21, width=37)
    root.Label1.configure(background="#d9d9d9",text="NCC: ")

    root.Label2 = tk.Label(root)
    root.Label2.place(relx=0.930, rely=0.180, height=21, width=35)
    root.Label2.configure(background="#d9d9d9",text="ITER: ")

    root.Label3 = tk.Label(root)
    root.Label3.place(relx=0.930, rely=0.580, height=21, width=37)
    root.Label3.configure(background="#d9d9d9",text="NCC: ")

    root.Label4 = tk.Label(root)
    root.Label4.place(relx=0.930, rely=0.620, height=21, width=35)
    root.Label4.configure(background="#d9d9d9",text="ITER: ")

    root.TSeparator1 = ttk.Separator(root)
    root.TSeparator1.place(relx=0.480, rely=0.01, relheight=0.988)
    root.TSeparator1.configure(orient="vertical")

    root.TSeparator2 = ttk.Separator(root)
    root.TSeparator2.place(relx=0.925, rely=0.0, relheight=0.988)
    root.TSeparator2.configure(orient="vertical")

    root.TSeparator3 = ttk.Separator(root)
    root.TSeparator3.place(relx=0.0, rely=0.042, relwidth=0.993)

    root.TSeparator4 = ttk.Separator(root)
    root.TSeparator4.place(relx=0.0, rely=0.480, relwidth=0.994)

    root.Canvas1 = Canvas(root, width=800, height=650, bg = '#afeeee')
    root.Canvas1.place(relx=0.480, rely=0.043, relheight=0.437, relwidth=0.445)
    root.Canvas1.configure(background="#d9d9d9",width=263)

    root.Canvas2 = tk.Canvas(root)
    root.Canvas2.place(relx=0.480, rely=0.480, relheight=0.637, relwidth=0.445)
    root.Canvas2.configure(background="#d9d9d9",width=263)

    root.mainloop()

def openImage():
    global filePath
    filePath = tkinter.filedialog.askopenfilename()
    fp = open(filePath,'rb')
    global img
    img = Image.open(fp).convert("1",dither=Image.NONE)
    printImageToScreen(img)
    imageProcess()

    root.Text1 = tk.Text(root)
    root.Text1.place(relx=0.0, rely=0.480, relheight=0.540, relwidth=0.480)
    root.Text1.configure(width=40,height=6,font=("Arial",4))
    root.Text1.insert(tk.INSERT,pixelMapAsString)

def imageProcess():
    global img, nCol, nRow
    nCol, nRow = img.size

    colorMap = img.load()

    global framedImage
    framedImage = Image.new('RGB', ((nCol+2), (nRow+2)), color='black').convert('1', dither=Image.NONE)

    for r in range(1,nRow+1):
        for c in range(1,nCol+1):
            framedImage.putpixel((c,r), colorMap[c-1,r-1])

    global binaryImage
    binaryImage = [[0 for x in range(nCol)] for y in range(nRow)]

    global pixelMapAsString

    for r in range(nRow):
        for c in range(nCol):
            if colorMap[c,r] > 200:
                binaryImage[r][c] = 1
            else:
                binaryImage[r][c] = 0
            pixelMapAsString +=  str(binaryImage[r][c])
        pixelMapAsString += "\n"

def printImageToScreen(img):
    render = ImageTk.PhotoImage(img)
    img = Label(root, image=render)
    img.image = render
    img.place(x=7, y=40)

def levialdi(framedImage):

    global Canvas1

    root.Label1 = tk.Label(root)
    root.Label1.place(relx=0.960, rely=0.135, height=21, width=37)

    root.Label2 = tk.Label(root)
    root.Label2.place(relx=0.960, rely=0.180, height=21, width=37)

    imgarray = np.array(framedImage.convert("1"))

    global nccLevialdi
    global iterationLevialdi
    nccLevialdi = 0
    iterationLevialdi = 0
    tempArray = deepcopy(imgarray)
    imgarray2 = deepcopy(imgarray)

    control = True
    while control:
        control = False

        for i in range(imgarray2.shape[0]):
            for j in range(imgarray2.shape[1]):
                if imgarray2[i][j] == 1:
                    if imgarray2[i - 1][j - 1] == 0 and imgarray2[i - 1][j] == 0 and imgarray2[i - 1][j + 1] == 0 and \
                            imgarray2[i][j + 1] == 0 and imgarray2[i + 1][j + 1] == 0 and imgarray2[i + 1][j] == 0 and \
                            imgarray2[i + 1][j - 1] == 0 and imgarray2[i][j - 1] == 0:
                        tempArray[i][j] = 0
                        nccLevialdi +=1
                        control = True
                    if imgarray2[i][j - 1] == 0 and imgarray2[i + 1][j - 1] == 0 and imgarray2[i + 1][j] == 0:
                        tempArray[i][j] = 0
                        control = True
                if imgarray2[i][j] == 0:
                    if imgarray2[i][j - 1] == 1 and imgarray2[i + 1][j] == 1:
                        tempArray[i][j] = 1
                        control = True

        imgarray2 = deepcopy(tempArray)
        imgarray2 = imgarray2*1
        iterations= ""
        for k in range(imgarray2.shape[0]):
            for l in range(imgarray2.shape[1]):
                iterations += str(imgarray2[k][l])
            iterations += "\n"

        root.Label1.configure(background="#d9d9d9", text=nccLevialdi)
        root.Label2.configure(background="#d9d9d9", text=iterationLevialdi)
        root.Canvas1.delete("levid")
        root.Canvas1.create_text(360,250,font=("Arial", 3),text=iterations, tag="levid")
        root.Canvas1.update()
        if control:
            iterationLevialdi+=1

def TSF(framedImage):

    root.Label4 = tk.Label(root)
    root.Label4.place(relx=0.960, rely=0.620, height=21, width=35)

    root.Label5 = tk.Label(root)
    root.Label5.place(relx=0.960, rely=0.580, height=21, width=35)
    imgarray = np.array(framedImage.convert("1"))
    nccTSF = 0
    global nrows, ncols, counter, i, j
    global iterationTSF
    nrows = len(imgarray)
    ncols = len(imgarray[1])
    tempArray = copy.deepcopy(imgarray)
    imgarray2 = copy.deepcopy(tempArray)
    control = True
    iterationTSF = 0
    while control == True:
        iterationTSF += 1

        control = False
        for i in range(1, nrows - 1, 2):
            for j in range(1, ncols - 1, 2):
                bp = findbp(i, j, tempArray)
                cp = findcp(i, j, tempArray)
                zero = connectedZeros(i, j, tempArray)
                if tempArray[i][j] == 1:
                    if bp == 0:
                        imgarray2[i][j] = 0
                        nccTSF += 1
                        control = True
                    bcase = False
                    if bp != 1:
                        bcase = True
                    else:
                        if tempArray[i - 1][j - 1] == 0 and tempArray[i - 1][j + 1] == 0:
                            bcase = True
                    if bcase == True:
                        if cp == 1 and zero:
                            imgarray2[i][j] = 0
                            control = True
                else:
                    if cp == 1 and (
                            (tempArray[i][j - 1] == 1 and tempArray[i - 1][j] == 1) or (
                            tempArray[i][j - 1] == 1 and tempArray[i + 1][j] == 1)):
                        imgarray2[i][j] = 1
                        control = True

        for i in range(2, nrows - 1, 2):
            for j in range(2, ncols - 1, 2):
                bp = findbp(i, j, tempArray)
                cp = findcp(i, j, tempArray)
                zero = connectedZeros(i, j, tempArray)
                if tempArray[i][j] == 1:
                    if bp == 0:
                        imgarray2[i][j] = 0
                        nccTSF += 1
                        control = True
                    bcase = False
                    if bp != 1:
                        bcase = True
                    else:
                        if tempArray[i - 1][j - 1] == 0 and tempArray[i - 1][j + 1] == 0:
                            bcase = True
                    if bcase == True:
                        if cp == 1 and zero:
                            imgarray2[i][j] = 0
                            control = True
                else:
                    if cp == 1 and (
                            (tempArray[i][j - 1] == 1 and tempArray[i - 1][j] == 1) or (
                            tempArray[i][j - 1] == 1 and tempArray[i + 1][j] == 1)):
                        imgarray2[i][j] = 1
                        control = True

        tempArray = copy.deepcopy(imgarray2)

        for i in range(1, nrows - 1, 2):
            for j in range(2, ncols - 1, 2):

                bp = findbp(i, j, tempArray)
                cp = findcp(i, j, tempArray)
                zero = connectedZeros(i, j, tempArray)
                if tempArray[i][j] == 1:
                    if bp == 0:
                        imgarray2[i][j] = 0
                        nccTSF += 1
                        control = True
                    bcase = False
                    if bp != 1:
                        bcase = True
                    else:
                        if tempArray[i - 1][j - 1] == 0 and tempArray[i - 1][j + 1] == 0:
                            bcase = True
                    if bcase == True:
                        if cp == 1 and zero:
                            imgarray2[i][j] = 0
                            control = True
                else:
                    if cp == 1 and (
                            (tempArray[i][j - 1] == 1 and tempArray[i - 1][j] == 1) or (
                            tempArray[i][j - 1] == 1 and tempArray[i + 1][j] == 1)):
                        imgarray2[i][j] = 1
                        control = True

        for i in range(2, nrows - 1, 2):
            for j in range(1, ncols - 1, 2):
                bp = findbp(i, j, tempArray)
                cp = findcp(i, j, tempArray)
                zero = connectedZeros(i, j, tempArray)
                if tempArray[i][j] == 1:
                    if bp == 0:
                        imgarray2[i][j] = 0
                        nccTSF += 1
                        control = True
                    bcase = False
                    if bp != 1:
                        bcase = True
                    else:
                        if tempArray[i - 1][j - 1] == 0 and tempArray[i - 1][j + 1] == 0:
                            bcase = True
                    if bcase == True:
                        if cp == 1 and zero:
                            imgarray2[i][j] = 0
                            control = True
                else:
                    if cp == 1 and (
                            (tempArray[i][j - 1] == 1 and tempArray[i - 1][j] == 1) or (
                            tempArray[i][j - 1] == 1 and tempArray[i + 1][j] == 1)):
                        imgarray2[i][j] = 1
                        control = True

        tempArray = deepcopy(imgarray2)

        tempArray = tempArray*1
        iterations=""
        for k in range(tempArray.shape[0]):
            for l in range(tempArray.shape[1]):
                iterations += str(tempArray[k][l])
            iterations += "\n"
        root.Canvas2.delete("TSF")
        root.Canvas2.create_text(360,250,font=("Arial", 3),text=iterations, tag="TSF")
        root.Canvas2.update()
        root.Label4.configure(background="#d9d9d9", text=iterationTSF)
        root.Label5.configure(background="#d9d9d9", text=nccTSF)

def connectedZeros(i, j, arr):
    flag = False
    p1 = arr[i - 1][j - 1]
    p2 = arr[i - 1][j]
    p3 = arr[i - 1][j + 1]
    p4 = arr[i][j + 1]
    p5 = arr[i + 1][j + 1]
    p6 = arr[i + 1][j]
    p7 = arr[i + 1][j - 1]
    p8 = arr[i][j - 1]
    neighbour = [p1, p2, p3, p4, p5, p6, p7, p8]
    for i in range(1, 7):
        if (neighbour[i] == 0 and neighbour[i + 1] == 0 and neighbour[i - 1] == 0):
            flag = True
    if (neighbour[7] == 0 and neighbour[6] == 0 and neighbour[0] == 0):
        flag = True
    if (neighbour[0] == 0 and neighbour[1] == 0 and neighbour[7] == 0):
        flag = True
    return flag

def findbp(i,j,arr):
    count = 0
    p1 = arr[i - 1][j - 1]
    p2 = arr[i - 1][j]
    p3 = arr[i - 1][j + 1]
    p4 = arr[i][j + 1]
    p5 = arr[i + 1][j + 1]
    p6 = arr[i + 1][j]
    p7 = arr[i + 1][j - 1]
    p8 = arr[i][j - 1]
    neighbour = [p1, p2, p3, p4, p5, p6, p7, p8]
    for i in range(0,8):
        if(neighbour[i]==1):
            count += 1
    return count

def findcp(i,j,arr):
    tp = 0
    p1 = arr[i - 1][j - 1]
    p2 = arr[i - 1][j]
    p3 = arr[i - 1][j + 1]
    p4 = arr[i][j + 1]
    p5 = arr[i + 1][j + 1]
    p6 = arr[i + 1][j]
    p7 = arr[i + 1][j - 1]
    p8 = arr[i][j - 1]
    neighbour = [p1, p2, p3, p4, p5, p6, p7, p8]
    if (p2==1 and p4==1):
        p3 = 1
        neighbour[2] = 1
    if (p4==1 and p6==1):
        p5 = 1
        neighbour[4] = 1
    if (p6==1 and p8==1):
        p7 = 1
        neighbour[6] = 1
    if (p2==1 and p8==1):
        p1 = 1
        neighbour[0] = 1
    if(p1+p2+p3+p4+p5+p6+p7+p8==8):
        tp +=1
    for i in range(0,7):
        if (neighbour[i]==0 and neighbour[i+1]==1):
            tp +=1
    if(neighbour[7] == 0 and neighbour[0] == 1):
        tp += 1
    return tp

def createImage():

    root = tk.Tk()
    def click(event):
        if object_id is not None:
            coord = can.coords(object_id)
            width = coord[2] - coord[0]
            height = coord[3] - coord[1]
            can.coords(object_id, event.x, event.y, event.x + width, event.y + height)

    root.title("Builder")

    def clear():
        can.delete(tk.ALL)

    def create_rectangle():
        global object_id
        object_id = can.create_rectangle(10, 10, 30, 30, fill='white', outline='white', width=3)

    def create_circle():
        global object_id
        object_id = can.create_oval(10, 10, 30, 30, fill='white', outline='white', width=3)

    def create_arc():
        global object_id

        object_id = can.create_arc(8, 60, 22, 25, start=0,
            extent=210, outline="white", fill="white", width=3)

    def save():
        x = root.winfo_rootx() + can.winfo_x()+5
        y = root.winfo_rooty() + can.winfo_y()+5
        x1 = x + can.winfo_width()-7
        y1 = y + can.winfo_height()-7
        ImageGrab.grab().crop((x, y, x1, y1)).save("C:/Users/baris/Desktop/studio/sample_images/croppedImage.png")
        tkinter.messagebox.showinfo("Info", "Image saved...")

    can = tk.Canvas(root, bg='black', height=100, width=100)
    can.pack(side=tk.RIGHT)
    can.bind("<Button-1>", click)

    btn_rectangle = tk.Button(root, text='Rectangle', width=30, command=create_rectangle)
    btn_rectangle.pack()

    btn_circle = tk.Button(root, text='Circle', width=30, command=create_circle)
    btn_circle.pack()

    btn_arc = tk.Button(root, text='Arc', width=30, command=create_arc)
    btn_arc.pack()

    btn_delete = tk.Button(root, text='Clear', width=30, command=clear)
    btn_delete.pack()

    btn_save= tk.Button(root, text='Save', width=30, command=save)
    btn_save.pack()

def saveReport():
    with open('report.csv', 'w') as f:
        writer = csv.writer(f)

        writer.writerow(['File Name ',filePath])
        writer.writerow(['File Size: ',str(nCol-2),'x',str(nRow-2)])
        writer.writerow(['NCC: ',str(nccLevialdi)])
        writer.writerow(['Iteration LEV',str(iterationLevialdi)])
        writer.writerow(['Iteration TSF',str(iterationTSF)])

    tkinter.messagebox.showinfo("Report Prepared!",".csv file is ready for check...")

def getMailAddress():
    mailAddress = simpledialog.askstring("Report","Enter your mail address")
    return mailAddress

def sendReportToMail(getMailAddress):

    email_user = 'erayreporter@gmail.com'
    email_password = 'alemdefener1899'
    email_send = getMailAddress()

    subject = 'Shrinking Algorithms Report'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    filename = 'report.csv'
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()

    tkinter.messagebox.showinfo("Done!","Report successfully sent")

if __name__ == '__main__':
    main()