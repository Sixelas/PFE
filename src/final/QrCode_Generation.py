import pyqrcode
from PIL import Image
import enum

# Code repris de mon Projet de Programmation de Master 1 : https://services.emi.u-bordeaux.fr/projet/git/qr-pdp-2021

class ErrorCorrection(enum.Enum):
    low = 'L'
    medium = 'M'
    quality = 'Q'
    high = 'H'


'''
    'size' is an integer, acceptable values are between 1 and 40

    Default size is the smallest possible
    (depending on the amount of content and errorCorrection level)

    If the given size is too small, it will use the default size instead.

'''


class QRCode:

    def __init__(self,
                 content: str,
                 errorCorrection: ErrorCorrection = ErrorCorrection.medium,
                 size: int = None):

        if not isinstance(errorCorrection, ErrorCorrection):
            error = 'The parameter errorCorrection should be of type <enum \
                    \'ErrorCorrection\'> (i.e use "ErrorCorrection.low").'
            raise TypeError(error)

        self.__content = content
        self.__errorCorrection = errorCorrection.value

        if size is not None and (size < 1 or size > 40):
            error = 'The given size of ' + str(size)
            error += 'is not valid. Acceptable values are between 1 and 40'
            raise ValueError(error)

        self.__size = size

    def getSize(self):
        return self.__size

    # __ is used to declare a "private" method
    # see more at:
    # https://docs.python.org/3/tutorial/classes.html#private-variables
    def __generate(self):
        try:
            qrcode = pyqrcode.create(self.__content,
                                     self.__errorCorrection,
                                     self.__size)

        # If there is a Unicode character, convert to utf-8
        except UnicodeEncodeError as error:
            qrcode = pyqrcode.create(self.__content,
                                     self.__errorCorrection,
                                     self.__size,
                                     encoding='utf-8')

        # If the given size is too small, it will use the default size instead.
        except ValueError as error:
            qrcode = pyqrcode.create(self.__content, self.__errorCorrection)

        # Raises any other errors
        except Exception as error:
            raise error

        return qrcode

    def toPNG(self, path: str):
        self.__generate().png(path,
                              scale=15,
                              module_color='#000000',
                              background='#FFFFFF')
