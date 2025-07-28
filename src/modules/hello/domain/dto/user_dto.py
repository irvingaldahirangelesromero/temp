class UserDTO:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name
        }