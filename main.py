__author__ = 'David Manouchehri'

# Everything used is cross-platform with ARM and x86, and it will stay this way.
import cv2  # I'm using OpenCV 3 with Python 3 support compiled in
import pyzxing  # This requires Java (I'm testing against OpenJDK-7)
# import timeit  # For development only
from multiprocessing import Process, Queue  # To avoid blocking

decoder = pyzxing.BarCodeReader("zxing")  # The ZXing binaries must be placed in zxing/ (local directory)
queuing = Queue()

print("Speedy started. Written by " + __author__ + ".")

# start_time = timeit.default_timer()

filename1 = 'sample.png'  # QR Code exists
filename2 = 'sample2.jpg'  # QR code exists
filename3 = 'sample3.jpg'  # QR code fails to be found


def get_qr(image_file, queue_text):
    try:
        queue_text.put(decoder.decode(image_file, try_harder=True, qr_only=True).data)
        print("QR code found.")
    except AttributeError:  # If no QR codes can be found
        print("No QR code found.")
    return


p = Process(target=get_qr, args=(filename1, queuing,))
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
print(queuing.get())  # At the moment all the threads write each other over

# elapsed = timeit.default_timer() - start_time
# print(elapsed)

img = cv2.imread(filename1)  # Load the file

cv2.imshow('window title', img)  # Make it popup in GTK/Qt, make sure not to attempt this on a headless system
# cv2.waitKey(0)
# cv2.destroyAllWindows()