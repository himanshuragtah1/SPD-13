__author__ = 'David Manouchehri (david@davidmanouchehri.com)'

# Everything used should be cross-platform (Linux and Windows if you're willing) and cross-architecture (ARM and x86).

# Comment the following line out and everything else with cv2 if you aren't going to use it
import cv2  # I'm using OpenCV 3 with Python 3 support compiled in, you will need to recompile it yourself most likely

# Using zbar might give a performance boost
import pyzxing  # This requires Java (I'm testing against OpenJDK-7)
# import timeit  # For development only, I use it to time different tasks
from multiprocessing import Process, Queue  # To avoid blocking

decoder = pyzxing.BarCodeReader("zxing")  # The ZXing binaries must be placed in zxing/ (local directory)
queuing = Queue()  # Needed for handling the outputs

print("Speedy started. Written by " + __author__ + ".")

# start_time = timeit.default_timer()

# TODO: Add PTP to fetch the live view
'''
//I would suggest using this module by Zachary Berkowitz (zac.berkowitz@gmail.com)
//https://code.google.com/p/pyptp2/

import pyptp2
import numpy as np

cam_address = pyptp2.util.list_ptp_cameras()[0]  #Only one device is attached.
camera = pyptp2.CHDKCamera(cam_address)
print camera.get_chdk_version()  #Just to make sure it is working.

a, live_data = camera.get_live_view_data(liveview=True, overlay=False, palette=False)  
#print live_data

#Get viewport height & width
vp_width = live_data.vp_desc.buffer_width
vp_height = live_data.vp_desc.visible_height

#Create empty array to hold intensity values
lv_image = np.empty((vp_height * vp_width,), dtype='uint16')

#Loop over raw values & discard color information from U,V values
indx = 0
for raw_indx, k in enumerate(live_data.vp_data):

    #For my camera the data was packed UYVYYY, so we want to discard
    #every 0'th and 2'nd indexed 2-byte short
    if raw_indx % 6 in [0, 2]:
        continue

    lv_image[indx] = k
    indx += 1

#Reshape the array into a rectangle
lv_image.reshape((vp_height, vp_width), order='C')


//Be sure to use the same style of threading as shown lower down to avoid blocking.
'''

# TODO: SD card photo downloading through PTP
'''
More or less the same thing as fetching the live view.
'''

# TODO: PTP/SD cardless photos with CHDK
'''
Using Zac's module, I think photos are going to have to be stored on a small SD card first, then transferred.
Ideally I'd like to run the the camera cardless, so maybe look into forking pyptp2 and adding that.
If not, it's not the end of the world. Still, keep this notice here until and it'll happen one day.

It's definitely possible, it's been there since CHDK 1.2.
http://chdk.wikia.com/wiki/PTP_Extension#Remote_shooting
'''

# TODO: Not a programming request for once! Can somebody please create some more realistic examples?
filename1 = 'sample.png'  # QR Code exists
filename2 = 'sample2.jpg'  # QR code exists
filename3 = 'sample3.jpg'  # QR code fails to be found
'''
Actually, this gives me an idea, why not use both zbar and XZing if possible? Run whichever is faster first,
then the other if there's still time. Not terribly important.
'''


def get_qr(image_file, queue_text):  # Try adding zbar as an option
    try:
        # You *MUST* provide a valid file name or otherwise pyzxing will flip out
        queue_text.put(decoder.decode(image_file, try_harder=True, qr_only=True).data)
        print("QR code found.")  # TODO: Change this to logging instead of print
    except AttributeError:  # If no QR codes can be found
        print("No QR code found.")
    return


if __name__ == '__main__':  # I can't see why someone would run this as a module, but hey, why not right?
    '''
    Right now this is mostly for testing, it gives you the general overview of why threading is useful.
    What I picture happening is after a QR code is found, kill all other processes still in search.
    It might prove useful to kill a thread if it takes too long to find a code, as I find that it takes >4 seconds
    for some pictures that contain no codes. Trial and error will help figure this one out.
    '''
    p = Process(target=get_qr, args=(filename1, queuing,))  # TODO: Turn these into an array?
    p.start()
    print('thread1 started')
    p = Process(target=get_qr, args=(filename2, queuing,))
    p.start()
    print('thread2 started')
    p = Process(target=get_qr, args=(filename3, queuing,))
    p.start()
    print('thread3 started')
    p.join()
    print('threads ended')
    print(queuing.get())  # TODO: Fix overwriting
    # elapsed = timeit.default_timer() - start_time
    # print(elapsed)

    '''
    These OpenCV commands don't really do anything at the moment, they're more for ensuring that OpenCV is properly
    set up as they will be used later most likely.
    '''
    img = cv2.imread(filename1)  # Load the file
    cv2.imshow('window title', img)  # Make it popup in GTK/Qt, make sure not to attempt this on a headless system
    # cv2.waitKey(0)  # Wait for user input before closing, otherwise it flashes open/close before you can see it
    # cv2.destroyAllWindows()

    # TODO: Objection detection (sounds easy right?)
    '''
    Check section 3 (page 11) for details
    http://www.unmannedsystems.ca/media.php?mid=4345

    In this, it's section 7.2 (pdf page 26, "real" page 24)
    http://www.auvsi-seafarer.org/documents/2015Documents/2015_AUVSI_SUAS_Rules_Rev_1.0_FINAL_14-1023-1.pdf
    '''

# TODO: Communication via State-Synchronization Protocol (Keith Winstein and Hari Balakrishnan)
'''
https://mosh.mit.edu/mosh-paper-draft.pdf
A large issue I personally see with most existing UAV communication systems is that they run under the assumption that
they take an "all or nothing" approach with relaying information to a ground station. With SSP, a smooth transition
between 802.11 2.4GHz, 3G and satellite could be possible. There's still some unanswered questions I have with this
part of the project, so this isn't a priority. Probably the script's output will be watched via SSH until this gets
done.
'''

# Suggestion: If the live view of the payload camera ends up working decently, maybe pipe the FPV camera through the
# on-board system.
