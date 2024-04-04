class Person:
    def __init__(self, isStrong, isRational, isRelaxed, location):
        self.isStrong = isStrong
        self.isRational = isRational
        self.location = location # Location will be a cell object?
        self.isRelaxed = isRelaxed
        # Based on Table 3 in the paper
        self.vulnerable = not isStrong and not isRelaxed

        self.isFallen = False
        self.isDead = False

        # We may need additional attibutes like momentum and strategy

    # Feel free to change these attributes or add functions to this class as we go




