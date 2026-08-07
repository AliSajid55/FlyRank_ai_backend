class InMemoryRepository:
    def __init__(self):
        self.items = []

    def add(self, item_dict):
        self.items.append(item_dict)
        return item_dict

    def get_all(self):
        return self.items
