__author__ = 'David Manouchehri'
__name__ = 'SPD-13'

# Everything used is cross-platform with ARM and x86, and it will stay this way.
import cv2  # I'm using OpenCV 3 with Python 3 support compiled in
import pyzxing  # This requires Java (I'm testing against OpenJDK-7)

qrreader = pyzxing.BarCodeReader("zxing") # The ZXing binaries must be placed in zxing/ (local directory)

print("Weclome to " + __name__ + ", also called Speedy for short. Written by " + __author__ + ".")

filename = "sample.png"

print("The sample QR code reads as: " + qrreader.decode(filename, qr_only=True).raw)

img = cv2.imread(filename)  # Load the file

cv2.imshow('window title', img) # Make it popup in GTK/Qt, make sure not to attempt this on a headless system
# cv2.waitKey(0)
# cv2.destroyAllWindows()