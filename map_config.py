import json


class MapConfig:
    def __init__(self, map_name):
        file = open("jsons\\maps.json")
        self.data = json.load(file)[map_name[-5:]]
        file.close()

    def get_render_points(self):
        return self.data["resp_points"]
