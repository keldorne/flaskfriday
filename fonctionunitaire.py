import cv2
from PIL import Image

def otoscopieimager(imageod, imageog, nompatient):

    #On concatene les images
    imageodg = cv2.vconcat([imageod, imageog])

    # Paramètres écriture
    # font
    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    orgnom = (10, 25)
    orgod = (10, 75)
    orgog = (10, 515)

    # fontScale
    fontscale = 1

    # Couleur
    colornom = (200, 200, 200)
    colorod = (0, 50, 255)
    colorog = (255, 50, 0)

    # Line thickness of 2 px
    thicknessnom = 1
    thicknessodg = 2

    imageodg = cv2.putText(imageodg, nompatient, orgnom, font,
                           fontscale, colornom, thicknessnom, cv2.LINE_AA)

    imageodg = cv2.putText(imageodg, 'Oreille Droite', orgod, font,
                       fontscale, colorod, thicknessodg, cv2.LINE_AA)

    imageodg = cv2.putText(imageodg, 'Oreille Gauche', orgog, font,
                       fontscale, colorog, thicknessodg, cv2.LINE_AA)


    dimensions = imageodg.shape
    print(dimensions)
    cv2.imwrite('oktest.jpg', imageodg)

    image_pdf = Image.open('oktest.jpg')
    image_pdf.save('oktest.pdf')

    cv2.imshow('ok', imageodg)
    cv2.waitKey(0)

imgod = cv2.imread('IMG20220402_082030_500.jpg')
imgog = cv2.imread('IMG20220402_082104_533.jpg')
nompatient = "M.Robert Hue"

otoscopieimager(imgod, imgog, nompatient)