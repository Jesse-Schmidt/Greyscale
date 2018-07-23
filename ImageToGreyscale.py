from PIL import Image, ImageDraw
done = "yes"
count = 0

def Transform(r,g,b, method, predefined):
    if method == 1:
        R, G, B, predefined = Averaging(r, g, b)

    elif method == 2:
        R, G, B, predefined = LumaCorrecting(r, g, b)

    elif method == 3:
        R, G, B, predefined = Desaturation(r, g, b)

    elif method == 4:
        if predefined != 0:
            R, G, B, predefined = Decomposition(r, g, b, predefined)
        else:
            intensity = input("Would you like maximum or minimum intensity? (max/min)\n")
            R, G, B, predefined = Decomposition(r, g, b, intensity.lower())

    elif method == 5:
        if predefined != 0:
            R, G, B, predefined = SingleChannel(r, g, b, predefined)
        else:
            color = input("What color channel do you want to use? (red/green/blue)\n")
            R, G, B, predefined = SingleChannel(r, g, b, color.lower())

    elif method == 6:
        if predefined != 0:
            R, G, B,  predefined = CustomNumber(r, g, b, predefined)
        else:
            number = input("How many shades of grey would you like? (2-256)\n")
            R, G, B,  predefined = CustomNumber(r, g, b, number)
    return R, G, B, predefined

def Averaging(r,g,b):
    grey = (r+b+g)/3
    return grey, grey, grey, 0

def LumaCorrecting(r,g,b):
    grey = (r * 0.2126 + g * 0.7152 + b * 0.0722)
    return grey, grey, grey, 0

def Desaturation(r,g,b):
    grey = (max(r, g, b) + min(r, g, b)) / 2
    return grey, grey, grey, 0

def Decomposition(r, g, b, intensity):
    if intensity == "max":
        grey = max(r, g, b)
    else:
        grey = min(r, g, b)
    return grey, grey, grey, intensity

def SingleChannel(r, g, b, color):
    if color == "red":
        grey = r
    elif color == "blue":
        grey = b
    else:
        grey = g
    return grey, grey, grey, color

def CustomNumber(r, g, b, numberOfGreys):
    ConversionFactor = 255 / (int(numberOfGreys) - 1)
    AverageValue = (r + g + b) / 3
    grey = int((AverageValue / ConversionFactor) + 0.5) * ConversionFactor
    return grey, grey, grey, int(numberOfGreys)


while done != "no":
    count += 1
    name = input("What is the file path of the image you would like to convert?\n")
    getName = name.split('\\')
    current = Image.open(name)
    RGB = current.convert('RGB')
    (w,h) = current.size
    transformed = Image.new("RGB", (w,h))
    convertType = int(input("How would you like to convert the image? \n1)Averaging\n"
                            "2)luminance Correcting\n3)Desaturation\n4)Decomposition\n"
                            "5)Single Channel\n6)Custom number of Greys\n7)All of them\n"))
    if convertType == 7:
        for number in range(1,7):
            predefined = 0
            convertType = number
            for i in range(w):
                for j in range(h):
                    r, g, b = RGB.getpixel((i, j))
                    r, g, b, predefined = Transform(r, g, b, convertType, predefined)
                    transformed.putpixel((i, j), (round(r), round(g), round(b)))
            transformed.save("Transformed\\" + str(number) + getName[len(getName)-1])
    else:
        predefined = 0
        for i in range(w):
            for j in range(h):
                r, g, b = RGB.getpixel((i,j))
                r, g, b, predefined = Transform(r, g, b, convertType, predefined)
                transformed.putpixel((i,j), (round(r),round(g),round(b)))
        transformed.save("Transformed\Transformed image " + str(count) + ".jpg")
    done = input("Would you like to convert another image? (yes/no)\n")

