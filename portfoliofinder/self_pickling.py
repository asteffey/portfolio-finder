import dill


class SelfPickling:
    def save(self, filename_wo_ext):
        with open(self._add_ext(filename_wo_ext), 'wb') as file:
            dill.dump(self, file)

    @classmethod
    def load(cls, filename_wo_ext):
        with open(cls._add_ext(filename_wo_ext), 'rb') as file:
            return dill.load(file)

    @classmethod
    def _add_ext(cls, filename_wo_ext):
        return filename_wo_ext + "." + cls.__name__ + ".p"
