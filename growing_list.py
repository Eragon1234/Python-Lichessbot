class GrowingList(list):
    """A list that grows as needed."""

    def __init__(self, default):
        self.default = default
        super().__init__()

    def __getitem__(self, index):
        if abs(index) >= len(self):
            return self.default
        return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None] * (index + 1 - len(self)))
        list.__setitem__(self, index, value)
