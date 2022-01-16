from time import sleep
from PIL import Image
import os
import json

def get_pixel(x,y,pixel_values,width):
    '''get pixel given list of im.getdata'''
    return pixel_values[width*y+x]

def array_pixels(pixel_values,width,height):
    '''returns an array, in the ROW COLLUMN format'''
    return_array = []

    for y in range(width):
        col_array = []
        for x in range(height):
            pixel = get_pixel(x,y,pixel_values,width)
            col_array.append(pixel)
        return_array.append(col_array)
    
    return return_array

def black_scale(pixel_array):
    '''converts array of pixels to array of 1's and 0's'''
    return_array = []

    for r in range(len(pixel_array)):
        col_array = []
        for c in range(len(pixel_array[0])):
            pixel = pixel_array[r][c]
            sum_RGB = pixel[0] + pixel[1] + pixel[2]
            if sum_RGB > 200:
                col_array.append(0)
            else:
                col_array.append(1)
            
        return_array.append(col_array)
    
    return return_array

def bw_2_binary(bw):
    binary = ""
    for r in range(len(bw)):
        for c in range(len(bw[0])):
            binary += str(bw[r][c])
    return binary

def frames_2_binary(frames):
    binary = ""
    for frame in frames:
        binary += bw_2_binary(frame)

    return binary

def print_matrix_bw(array):
    '''prints a given 2D array'''
    for r in range(len(array)):
        for c in range(len(array[0])):
            if array[r][c] == 0:
                print("#",end="")
            else:
                print("@",end="")
            print("",end="")

        print("")
        

def preview(bw):
    print(len(bw))
    print(len(bw[0]))
    img = Image.new(
        mode="1", 
        size=(len(bw), len(bw[0])), 
        color=0)

    pixels = img.load()
    for c in range(img.size[0]):
        for r in range(img.size[1]):
            pixels[c,r] = bw[r][c]
    img.show()

def test():
    im = Image.open('bad_apple_files/images/00101.png', 'r')

    width, height = im.size
    pixel_values = list(im.getdata())
    bw = black_scale(array_pixels(pixel_values, width, height))
    print_matrix_bw(bw)

    preview(bw)

def img_2_BW_arr(image):
    img = Image.open(image,'r')

    width, height = img.size

    pixel_values = list(img.getdata())

    bw = black_scale(array_pixels(pixel_values, width, height))

    return bw

def count_frames(dir):

    initial_count = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            initial_count += 1
    return initial_count

def number_to_string(places,number):
    number_length = len(str(number))
    number = str(number)
    for i in range(places - number_length):
        number = "0" + number
    return number

def apples(image_directory,img_format):
    '''gets all the frames from a directory'''
    frames_count = count_frames(image_directory)
    places = len(str(frames_count)) + 1
    frames_arrays = []


    for i in range(frames_count):
        file_number = number_to_string(places,i+1)
        filename = f"{image_directory}/{file_number}.{img_format}"
        frames_arrays.append(img_2_BW_arr(filename))
    return frames_arrays


def bad_apple_json():
    '''gets bad apple in json'''
    applez = apples("bad_apple_files/images", "png")

    applez_json = json.dumps(applez)
    print(applez_json)

    file = open("bad_apple.json", 'a')
    file.write(applez_json)
    file.close()

def apples_2_vhex(applez):
    '''takes in a set of video frames and converts it to vhex'''
    binary = frames_2_binary(applez)
    byte_count = 16
    eight_bit_bytes = [binary[i:i + byte_count]
                       for i in range(0, len(binary), byte_count)]
    
    four_bit_bytes_paired = []
    for byte in eight_bit_bytes:
        byte_count = 8
        four_bit_bytes_duo = [int(byte[i:i + byte_count],2)
                              for i in range(0, len(byte), byte_count)]
        four_bit_bytes_paired.append(four_bit_bytes_duo)

    for byte in four_bit_bytes_paired:
        print(byte)
    start = "v2.0 raw"
    end = str(hex(15))
    byte_prefix = hex(5)
    return_string = start + "\n"

    for byte_duo in four_bit_bytes_paired:
        return_string += f"{byte_prefix}\n{hex(int(byte_duo[0]))}\n{hex(int(byte_duo[1]))}\n"
    
    return_string += end
    print (return_string)
    return return_string

def create_vhex(applez,name,start,end):
    '''creates vhex file for set of frames, applez'''
    output = apples_2_vhex(applez)
    if not end:
        output.replace(str(hex(15)),"")

    file = open(name, 'w')
    file.write(output)
    file.close()

def printAnimation(applez,fps):
    frequency = 1.0/60
    for apple in applez:
        sleep(frequency)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n")
        print_matrix_bw(apple)


if __name__ == "__main__":
    applez = apples("bad_apple_files/images", "png")
    basket = int(65536/48)
    applez_baskets = [applez[i:i + basket]
                      for i in range(0, len(applez), basket)]

    for i in range(len(applez_baskets)):
        create_vhex(applez_baskets[i],
        f"baddapplehex{i}.hex",
        end=i==len(applez_baskets)-1)

    # print(applez)
    # print(len(applez)[0])

    # fps = 60
    # frequency = 1.0/60
    # for apple in applez:
    #     sleep(frequency)
    #     os.system('cls' if os.name == 'nt' else 'clear')
    #     print("\n")
    #     print_matrix_bw(apple)
    


    # im = Image.open('bad_apple_files/images/00101.png', 'r')

    # width, height = im.size
    # pixel_values = list(im.getdata())


    # bw = black_scale(array_pixels(pixel_values, width, height))
    # print_matrix(bw)

    # preview(bw)

    # test()
