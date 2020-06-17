import dill


class SelfPickling:
    """Base class to provide pickling functionality.

    Makes use of files with a `.<class-name>.p` extension.
    """

    def save(self, filename_wo_ext: str):
        """Saves the class.

        :param filename_wo_ext: filename without extension
        """
        with open(self._add_ext(filename_wo_ext), 'wb') as file:
            dill.dump(self, file)

    @classmethod
    def load(cls, filename_wo_ext: str):
        """Loads the class.

        :param filename_wo_ext: filename without extension
        :return: instance of class read from file
        """
        with open(cls._add_ext(filename_wo_ext), 'rb') as file:
            return dill.load(file)

    @classmethod
    def _add_ext(cls, filename_wo_ext):
        return filename_wo_ext + "." + cls.__name__ + ".p"
