import os,sys   # std lib
import Image # for image operations
from optparse import OptionParser # argument parsing


def calc_imgStartStopNeedles():
    global ImgStartNeedle
    global ImgStopNeedle
    global ImgPosition    

    if ImgPosition == 'center':
        _needleWidth = StopNeedle - StartNeedle
        ImgStartNeedle = (StartNeedle + _needleWidth/2) - knit_img_width/2
        ImgStopNeedle  = ImgStartNeedle + knit_img_width      

    elif ImgPosition == 'alignLeft':
        ImgStartNeedle = StartNeedle
        ImgStopNeedle  = ImgStartNeedle + knit_img_width

    elif ImgPosition == 'alignRight':
        ImgStopNeedle = StopNeedle
        ImgStartNeedle = ImgStopNeedle - knit_img_width

    elif int(ImgPosition) > 0 and int(ImgPosition) < 200:
        ImgStartNeedle = int(ImgPosition)
        ImgStopNeedle  = ImgStartNeedle + knit_img_width

    else:
        print "unknown alignment"
        return False
    return True


def checkSerial( curState ):
    time.sleep(1) #TODO optimize delay
    out = ''
    while ser.inWaiting() > 0:
        line = ser.readline()        

        msgId = ord(line[0])            
        if msgId == 0xC1:    # cnfStart
            msg = "> cnfStart: "
            if(ord(line[1])):
                msg += "success"
            else:
                msg += "failed"
            print msg

            # reqInfo showed the right version, proceed to next state
            if curState == 's_start' and ord(line[1]) == 1:
                curState = 's_operate'
            else:
                curState = 's_abort'

        elif msgId == 0xC3: # cnfInfo
            msg = "> cnfInfo: Version="
            msg += str(ord(line[1]))
            print msg

            # reqStart was successful, proceed to next state
            if curState == 's_init' and ord(line[1]) == 1:
                curState = 's_start'
            else:
                curState = 's_abort'

        elif msgId == 0x82: #reqLine            
            msg = "> reqLine: "
            msg += str(ord(line[1]))
            print msg
            
            if curState == 's_operate':
                cnfLine(ord(line[1]))
        else:
            print "unknown message: "
            print line[:-2] #drop crlf
    return


def serial_reqInfo():
    print "< reqInfo"
    ser.write(chr(0x03) + '\n\r')

def serial_reqStart():
    startNeedle = raw_input("Start Needle: ")
    stopNeedle  = raw_input("Stop Needle : ")

    msg = chr(0x01)                     #msg id
    msg += chr(int(startNeedle))
    msg += chr(int(stopNeedle))
    print "< reqStart"
    ser.write(msg + '\n\r')

def serial_cnfLine(lineNumber, lineData, flags, crc8):
    msg  = chr(0x42)                    # msg id
    msg += chr(lineNumber)              # line number
    msg += lineData                     # line data
    msg += chr(flags)                   # flags
    msg += chr(crc8)                    # crc8
    print "< cnfLine"
    ser.write(msg + '\n\r')


def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)

def setPixel(bytearray,pixel):
    _numByte = int(pixel/8)
    bytearray[_numByte] = setBit(int(bytearray[_numByte]),pixel-(8*_numByte))
    return

def cnfLine(lineNumber):
    # TODO take care of pictures with > 255 lines height
    bytes = bytearray(25)
    if lineNumber < imageH:
        msg = ''
        for x in range(0, imageW):
            pxl = image.getpixel((x, lineNumber))            
            if pxl == 255:
                msg += "#"
                setPixel(bytes,x)
            else:
                msg += '-'
        print msg + str(lineNumber)

        if lineNumber == imageH-1:
            lastLine = 0x01
        else:
            lastLine = 0x00

        # TODO implement CRC8
        crc8 = 0x00

        cnfLine(lineNumber, bytes, lastLine, crc8)


#
# MENU FUNCTIONS
#

def a_showImage():
    """show the image in ASCII"""
    for y in range(0, knit_img_height):
        msg = ''
        for x in range(0, knit_img_width):
            pxl = knit_img.getpixel((x, y))
            if pxl == 255:
                msg += "#"
            else:
                msg += '-'
        print msg
    raw_input("press Enter")


def a_invertImage():
    """invert the pixels of the image"""
    global knit_img

    for y in range(0, knit_img_height):
      msg = ''
      for x in range(0, knit_img_width):
        pxl = knit_img.getpixel((x, y))
        if pxl == 255:
          knit_img.putpixel((x,y),0)
        else:
          knit_img.putpixel((x,y),255)


def a_rotateImage():
    """rotate the image 90 degrees clockwise"""
    global knit_img

    print "rotating image 90 degrees..."
    knit_img = knit_img.rotate(-90)


def a_resizeImage():
    """resize the image to a given width, keeping the aspect ratio"""
    global knit_img
    global knit_img_width
    global knit_img_height

    newWidth = int(raw_input("New Width (pixel): "))
    wpercent = (newWidth/float(knit_img_width))
    hsize = int((float(knit_img_height)*float(wpercent)))
    knit_img = knit_img.resize((newWidth,hsize), Image.ANTIALIAS)
    
    knit_img_width  = knit_img.size[0]
    knit_img_height = knit_img.size[1]


def a_setNeedles():
    """set the start and stop needle"""
    global StartNeedle
    global StopNeedle
    
    StartNeedle = int(raw_input("Start Needle (0 <= x <  199): "))
    StopNeedle  = int(raw_input("Stop Needle  (1 <  x <= 199): "))


def a_setImagePosition():
    global ImgPosition

    print "Allowed options:"
    print ""
    print "center"
    print "alignLeft"
    print "alignRight"
    print "<position from left>"
    print ""
    ImgPosition = raw_input("Image Position: ")
    return

def a_showImagePosition():
    """show the current positioning of the image"""

    calc_imgStartStopNeedles()
    
    print "Image Start: ", ImgStartNeedle
    print "Image Stop : ", ImgStopNeedle  
    print ""

    # print markers for active area and knitted image
    msg = '|'
    for i in range(0,200):
        if i >= StartNeedle and i <= StopNeedle:
            if i >= ImgStartNeedle and i <= ImgStopNeedle:
                msg += '$'
            else:          
                msg += 'x'
        else:
            msg += '-'
    msg += '|'
    print msg

    # print markers at multiples of 10
    msg = '|'
    for i in range(0,200):
        if i == 100:
            msg += '|'
        else:
            if (i % 10) == 0:
                msg += '^'
            else:
                msg += ' '
    msg += '|'
    print msg

    raw_input("press Enter")
 

def a_knitImage():
    _curState = 's_init'
    _oldState = _curState
    _reqSent  = 0

    while True:
        checkSerial(_curState)

        if _oldState != _curState:
            _reqSent = 0
        elif _curState == 's_abort':
            return

        if _curState == 's_init':
            print "s_init"
            if _reqSent == 0:
                serial_reqInfo()
                _reqSent = 1

        elif _curState == 's_start':
            print "s_start"
            if _reqSent == 0:
                serial_reqStart()
                _reqSent = 1     

        elif _curState == 's_operate':
            print "s_operate"

        elif _curState == 's_finished':
            print "s_finished"
            raw_input("press Enter")
            return

        _oldState = _curState
    
    return     

def print_main_menu():
    """Print the main menu"""
    print "======================"
    print "=   AYAB CONTROL v1  ="
    print "======================"
    print ""
    print "IMAGE TOOLS"
    print " 1 - show"
    print " 2 - invert"
    print " 3 - resize"
    print " 4 - rotate"
    print ""
    print "KNITTING"
    print " 5 - set start and stop needle"
    print " 6 - set image position"
    print " 7 - show image position"
    print ""
    print " 9 - knit image with current settings"
    print ""
    print " 0 - Exit"
    print ""
    print "INFORMATION"
    print "Filename      : ", filename
    print "Original Image: ", orig_img.size, orig_img.mode
    print "Knitting Image: ", knit_img.size, "black/white" #knit_img.mode
    print ""
    print "Start Needle  : ", StartNeedle
    print "Stop Needle   : ", StopNeedle
    print "Image position: ", ImgPosition


def no_such_action():
    print "Please make a valid selection"


def mainFunction():
    """main"""


    actions = {"1": a_showImage, 
                "2": a_invertImage,
                "3": a_resizeImage, 
                "4": a_rotateImage, 
                "5": a_setNeedles, 
                "6": a_setImagePosition, 
                "7": a_showImagePosition,
                "9": a_knitImage}    
    while True:
        os.system('cls' if os.name=='nt' else 'clear')
        
        print_main_menu()
        print ""    
        selection = raw_input("Your selection: ")
        print ""
        if "0" == selection:
            #ser.close()
            exit()
            return
        toDo = actions.get(selection, no_such_action)
        toDo()

        #checkSerial( False )

    return


if __name__ == "__main__":
    if (len(sys.argv) < 2):
      print "Usage: ayab_control.py <FILE>"
      os.system("exit")
    else:
      filename = sys.argv[1]
      if filename != '':
          orig_img = Image.open(filename)
          knit_img = orig_img.convert('1')
          knit_img_width  = knit_img.size[0]
          knit_img_height = knit_img.size[1]

          StartNeedle = 79
          StopNeedle  = 119
          ImgPosition = 'center'
          ImgStartNeedle = 0
          ImgStopNeedle  = 0

          ser = serial.Serial('/dev/ttyACM0', 115200)

          mainFunction()
      else:
         print "Please check the filename"