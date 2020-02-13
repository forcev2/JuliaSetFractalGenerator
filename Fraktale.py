# Python code for Julia Fractal
from PIL import Image

def generateFract(w,h,zoom,moveX,moveY,maxIter):
    bitmap = Image.new("RGB", (w, h), "white")
    pix = bitmap.load()
    cX, cY = -0.7, 0.27015

    for x in range(w):
        for y in range(h):
            zx = 1.5 * (x - w / 2) / (0.5 * zoom * w) + moveX
            zy = 1.0 * (y - h / 2) / (0.5 * zoom * h) + moveY
            i = maxIter
            while zx * zx + zy * zy < 4:
                tmp = zx * zx - zy * zy + cX
                zy = 2.0 * zx * zy + cY
                zx = tmp
                i -= 1
                if i < 1:
                    break

            pix[x, y] = (i << 21) + (i << 10) + i * 8

    return bitmap

#geeksforgeeks.org/julia-fractal-python/
