from abc import ABC, abstractmethod


class User(ABC):
    """Base class for Admin, Seller and Customer."""

    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email
        self.logged_in = False

    def login(self):
        self.logged_in = True
        print(f"{self.name} logged in")

    def logout(self):
        self.logged_in = False
        print(f"{self.name} logged out")

    @abstractmethod
    def get_role(self):
        pass


class Admin(User):
    """Manages users and categories."""

    def get_role(self):
        return "admin"


class Seller(User):
    """Adds products."""

    def __init__(self, user_id, name, email, store_name):
        super().__init__(user_id, name, email)
        self.store_name = store_name

    def get_role(self):
        return "seller"


class Customer(User):
    """Places orders."""

    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.addresses = []

    def add_address(self, address):
        self.addresses.append(address)

    def get_role(self):
        return "customer"