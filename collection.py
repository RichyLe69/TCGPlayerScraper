import yaml


class Collection:

    def __init__(self, yaml_name):
        with open(yaml_name, 'r') as stream:
            try:
                yaml_data = yaml.safe_load(stream)
                card_list = list()
                for cards in yaml_data:
                    card_list.append(cards)
            except yaml.YAMLError as exc:
                print(exc)
        self.yaml_data = yaml_data
        self.card_list = card_list
        self.yaml_name = yaml_name.replace('decks/', '').replace('split_lists/', '').replace('.yaml', '').replace('old_lists', '')

    def get_card_list(self):
        return self.card_list

    def get_yaml_data(self):
        return self.yaml_data

    def get_yaml_name(self):
        return self.yaml_name
