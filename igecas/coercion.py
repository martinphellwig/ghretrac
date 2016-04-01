"""
Coercion is a module to help with the values stored in the database.
As these values are stored as strings and can be of different type.
As such we are emulating an EAV type data storage. It is likely that in the
future the values will actually be stored in a key/value like store.
"""

class FormatString(object):
    "As everything is stored as a string, this just returns whatever is put in."
    multi_item = False
    def __init__(self, value):
        self.value = value
        self.value_original = value
        self.reformat()

    def reformat(self):
        "reformat the string."
        pass

    def from_string(self):
        "Return the formation from the string in the database"
        return self.value

    def into_string(self):
        "Make it a string to be stored in the database"
        return str(self.value)


class FormatDualAllele(FormatString):
    "In the format of AA, CT, AG, etc."
    multi_item = True
    def reformat(self):
        tmp = self.value.replace(':', '').upper()
        tmp = list(tmp)
        tmp.sort()
        self.value = ''.join(tmp)

    def into_string(self):
        if len(self.value) != 2:
            text = "Value '%s' length must be exactly 2." % self.value_original
            raise ValueError(text)
        return self.value


class FormatBoolean(FormatString):
    "Must be either True or False"
    multi_item = False
    def reformat(self):
        self.value = self.value.strip().capitalize()

    def into_string(self):
        valid = ['True', 'False']
        if self.value not in valid:
            text = "Value '%s' must be either %s" % (self.value_original, valid)
            raise ValueError(text)
        return self.value

    def from_string(self):
        if self.value == 'True':
            return True
        elif self.value == 'False':
            return False
        else:
            text = "Database contains unexpected value '%s'"  % self.value
            raise ValueError(text)
        return FormatString.from_string(self)