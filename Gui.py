import tkinter as tk
from PIL import Image, ImageTk
from Fraktale import *
import _thread as thrd


semaphore = True
beenCreated = False

width = 700
height = 400

root = tk.Tk()
root.geometry("850x400")
root.resizable(0,0)
root.title("Fractal Generator")
canvas = tk.Canvas(root, width=width, height=height)
moveX = tk.Entry(root)

label1 = tk.Label( root, text="Zoom")
E1 = tk.Entry(root, bd =5)
E1.insert(tk.END, '1')

label2 = tk.Label( root, text="Max Iterations")
E2 = tk.Entry(root, bd =5)
E2.insert(tk.END, '255')

label3 = tk.Label( root, text="Pos x")
E3 = tk.Entry(root, bd =5)
E3.insert(tk.END, '0')

label4 = tk.Label( root, text="Pos y")
E4 = tk.Entry(root, bd =5)
E4.insert(tk.END, '0')

status = tk.Label( root, text="Status:", font='Helvetica 10 bold')
progress = tk.Label( root, text="")


def showImage(zoom=None, posX=None, posY=None):
    global semaphore
    global beenCreated
    semaphore = False


    good = True

    try:
        maxIter = int(E2.get())
        if maxIter < 0 or zoom == 0:
            raise ValueError
        if zoom is None:
            zoom = float(E1.get())
        if posX is None:
            posX = float(E3.get())
        if posY is None:
            posY = float(E4.get())
    except ValueError:
        statusChange("ERR: Wrong args")
        good = False



    print(zoom, maxIter)
    if good:
        statusChange("Generating....")
        image = generateFract(width,height,zoom,posX,posY,maxIter)
        ph = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=ph)
        label.image = ph
        canvas.create_image(width/2 ,height/2, image=label.image)
        canvas.pack(fill=tk.BOTH, expand=tk.TRUE)
        beenCreated = True
        statusChange("Generated.")

    semaphore = True


def getOrigin(eventorigin):
    global x, y
    x = eventorigin.x * -1
    y = eventorigin.y
    if x > -width and y < height and beenCreated and semaphore:

        x += width/2
        y -= height/2

        zoom = float(E1.get())

        nY = float(E4.get())
        nY += y/(height/2 * zoom)

        nX = float(E3.get())
        nX -= x/(width * 0.333 * zoom)


        print(nX, nY)
        print(x, y, -width, height)

        zoom *= 2

        set_inputText(zoom,nX,nY)

        showImageThreadStart(zoom=zoom, posY=nY, posX=nX)


def set_inputText(zoom,posX, posY):
    E1.delete(0,tk.END)
    E1.insert(0,zoom)
    E3.delete(0,tk.END)
    E3.insert(0,posX)
    E4.delete(0,tk.END)
    E4.insert(0,posY)
    return


def statusChange(progres):
    global progress
    progress.config(text=progres)


def showImageThreadStart(zoom=None, posX=None, posY=None):
    if semaphore:
        try:
            thrd.start_new_thread(showImage, (zoom, posX, posY))
        except:
            print("Error: unable to start thread")
    else:
        print("Wait for the image to be generated")



submit = tk.Button(root, text ="Generate", command = showImageThreadStart, width=16)

label1.place(x=width+10, y=0)
E1.place(x=width+10, y=20)
label2.place(x=width+10, y=50)
E2.place(x=width+10, y=70)
label3.place(x=width+10, y=100)
E3.place(x=width+10, y=120)
label4.place(x=width+10, y=150)
E4.place(x=width+10, y=170)
submit.place(x=width+10, y=210)
status.place(x=width+10, y=250)
progress.place(x=width+55, y=251)
canvas.bind("<Button 1>", getOrigin)
tk.mainloop()