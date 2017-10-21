import os

from Rekha_Io.settings import JSX_FILES_DIR


class RIJSXCompiler(object):
    """
    This class will handle JSX file compilation and will save compiled js files into single file and will
    save them in specific location.
    """

    def __init__(self):
        self.x = os.walk(JSX_FILES_DIR)
        self.process()

    def process(self):
        one, two, three = zip(*self.x)
        print(one)
        print(two)
        print(three)
