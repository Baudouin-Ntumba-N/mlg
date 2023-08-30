class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.loggedin = False

    @property
    def is_authenticated(self):
        if self.loggedin == True:
        	return True
        else:
            return False


user1 = User("Baudouin", 27)
