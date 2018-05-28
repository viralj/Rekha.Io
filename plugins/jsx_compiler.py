import os

from react import jsx

from Rekha_Io.settings import JSX_FILES_DIR, JSX_FILES_COMPILED_DIR, JSX_COMPILE_FILES


class RIJSXCompiler(object):
    """
    This class will handle JSX file compilation and will save compiled js files into single file and will
    save them in specific location.
    """

    def __init__(self):
        self.x = os.walk(JSX_FILES_DIR)
        if JSX_COMPILE_FILES:
            self.process()

    def process(self):
        one, two, three = zip(*self.x)

        for z in two[0]:
            current_dir = "{}/{}".format(JSX_FILES_DIR, z)

            """
            Creating directory for compiled js
            """
            self.create_dir_and_file(z)

            """
            Walking through current directory and grabbing all JSX files to compile
            """
            self.x = os.walk(current_dir)
            one, two, three = zip(*self.x)

            for t in three[0]:
                jsx.transform(jsx_path="{}/{}".format(current_dir, t),
                              js_path="{}/{}/{}".format(JSX_FILES_COMPILED_DIR, z, str(t).replace("jsx", "js")))

    def create_dir_and_file(self, dir_name):
        """
        To create directory and compiled file in js compiled files directory.
        :param dir_name:
        :return:
        """
        if not os.path.exists("{}/{}".format(JSX_FILES_COMPILED_DIR, dir_name)):
            os.makedirs("{}/{}".format(JSX_FILES_COMPILED_DIR, dir_name))
