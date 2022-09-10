
class Participant:
    def __init__(self, preferences, name, grade, medical_cond):
        self.preferences = preferences  # list of preferences as strings
        self.name = name
        self.grade = grade
        self.medical_cond = medical_cond

    def __str__(self):
        return '[' + self.name + ':::' + str(self.grade) + ']'

    def __repr__(self):
        return '[' + self.name + ':::' + str(self.grade) + ']'
