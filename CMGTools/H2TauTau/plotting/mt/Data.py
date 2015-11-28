class CompatibilityData:
    def __init__(self):
        self.weight_name= ""
        self.variable = ""
        self.binning = {'nbinsx':0, 'xmin':0., 'xmax': 0.}
        self.backgrounds = []
        self.chi2 = []

    def __str__(self):
        string = ""
        string += self.weight_name + " "
        string += self.variable + " "
        string += str(self.binning) + " "
        string += str(self.backgrounds) + " "
        string += str(self.chi2)
        return string

    def __hash__(self):
        return hash(str(self))

    def toDict(self):
        dictionnary = {}
        dictionnary["Weight_name"] = self.weight_name
        dictionnary["Variable"] = self.variable
        dictionnary["Binning"] = self.binning
        dictionnary["Backgrounds"] = self.backgrounds
        dictionnary["Chi2"] = self.chi2
        return dictionnary

    def fillFromDict(self, dictionnary):
        self.weight_name = dictionnary["Weight_name"]
        self.variable = dictionnary["Variable"]
        self.binning = dictionnary["Binning"]
        self.backgrounds = dictionnary["Backgrounds"]
        self.chi2 = dictionnary["Chi2"]
        return dictionnary
