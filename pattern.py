from math import cos, pi, sin
import numpy as np
from PIL import Image
from typing import Tuple, List

# TODO: change this dynamically based on the config data
MAX_DATA_LEN = 5000


class Pattern:
    def __init__(self, dimensions: Tuple[int, int], center: Tuple[int, int], radius: int, angleIncrement: float, angleDecrement: float, layerGap: int):
        self.rows = dimensions[0]
        self.cols = dimensions[1]
        self.__centerX = center[0]
        self.__centerY = center[1]
        self.__radius = radius
        self.__angleIncrement = angleIncrement
        self.__angleDecrement = angleDecrement
        self.__layerGap = layerGap
        self.__img = np.zeros((self.rows, self.cols), dtype=np.uint8)
        self.__encImg = None

    def clear(self) -> None:
        self.__img = np.zeros((self.rows, self.cols), dtype=np.uint8)

    def show(self) -> None:
        # mode='L' is for grayscale images
        if (self.__encImg == None):
            return
        self.__encImg.show()

    def save(self, filename: str = None):
        outputFilename = "output"
        if (filename != None):
            outputFilename = filename
        if (self.__encImg == None):
            return
        self.__encImg.save(f"output/{outputFilename}.png")

    def encrypt(self, data: List[int]) -> None:
        # maximum safe length of output can be 1400
        centerX, centerY = self.__centerX, self.__centerY
        radius = self.__radius
        img = self.__img

        angleOffset = self.__angleIncrement
        indexOffset = 0
        dataSize = len(data)

        while (indexOffset < dataSize and angleOffset > 0):
            counter = 0
            # for each alphabet 26 layers are required
            for layer in range(0, 5):
                # angle goes from 0 -> 2pi
                angle = 0
                # indexOffset represent from which index in data do we need to start this new layer off
                counter = indexOffset
                # initilization of a new layer
                while (angle < 2*pi):
                    # using parametric coordinates to create one layer of dots
                    x, y = centerX + int(radius * cos(angle)
                                         ), centerY + int(radius * sin(angle))
                    if (counter >= dataSize):
                        # there is no more data to encrypt
                        break
                    if ((1 << layer) & data[counter]):
                        # if a character belongs to that layer
                        img[x][y] = 255
                    else:
                        img[x][y] = 128
                    # increase the angle with angleOffset
                    # increase the counter to point to the next index in data
                    angle += angleOffset
                    counter += 1
                # since one layer has ended, increase the radius so that the new layer does not collide
                # with the previous layer
                radius += self.__layerGap

            # decrease the angleOffset with angleDecrement so that a bigger circle can
            # accomodate more data
            angleOffset -= self.__angleDecrement
            indexOffset = counter
            # after 26 layers increase the radius with layer gap to denote a diff
            # batch of data start
            radius += self.__layerGap
        self.__encImg = Image.fromarray(self.__img, mode='L')

    @staticmethod
    def decrypt(center: Tuple[int, int], radius: int, angleIncrement: float, angleDecrement: float, layerGap: int, imgPath: str) -> List[int]:
        # same explanations as for the encrypt data function
        # returns an array of data with each value denoting a character, i.e., [1 -> a,... 26 -> z]
        img = Image.open(imgPath)
        img_arr = np.array(img).astype(np.uint8)
        centerX, centerY = center[0], center[1]
        data = MAX_DATA_LEN * [0]

        angleOffset = angleIncrement
        indexOffset = 0

        while (angleOffset > 0):
            counter = 0
            for layer in range(0, 5):
                angle = 0
                counter = indexOffset

                while (angle < 2*pi):
                    x, y = centerX + int(radius * cos(angle)
                                         ), centerY + int(radius * sin(angle))

                    if (counter >= MAX_DATA_LEN):
                        break
                    if (img_arr[x][y] == 255):
                        data[counter] = (1 << layer) | data[counter]

                    angle += angleOffset
                    counter += 1
                radius += layerGap

            angleOffset -= angleDecrement
            indexOffset = counter
            radius += layerGap

        return data
