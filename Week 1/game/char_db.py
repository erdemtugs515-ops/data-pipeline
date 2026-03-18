class Character():
    def attack(self):
        print(self._attack)
    
    def defend(self):
        print(self.defend)

class Warrior(Character):
    def __init__(self) -> None:
        super().__init__("TAKE THIS","ENGARDE")
        return None
    
class Wizard(Character):
    def __init__(self)-> None:
        super().__init__("ABRACADABRA","RANDOM BULLSHIT, GO")
        return None
    
class Archer(Character):
    def __init__(self) -> None:
        super().__init__("*bow noises*")
        return None