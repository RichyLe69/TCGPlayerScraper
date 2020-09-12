import yaml


class Collection:

    def __init__(self):
        with open('decks/card_list.yaml', 'r') as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                card_list = list()
                for cards in yaml_data:
                    card_list.append(cards)
            except yaml.YAMLError as exc:
                print(exc)
        self.yaml_data = yaml_data
        self.card_list = card_list

    def get_card_list(self):
        return self.card_list

    def get_yaml_data(self):
        return self.yaml_data
