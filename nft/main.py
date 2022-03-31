from pathlib import Path
from tkinter import W
from typing import List, Tuple
import random
import json
from PIL import Image

POPULATION_COUNT = 1000
incompatibilities = []
file = open("incompatibilities.txt")
# file=open(str(Path().cwd().parent.joinpath("incompatibilities.txt")))

for line in file:
    incompatibilities.append(line)


root: Path = Path().cwd() / "assets"


class NFTObject:
    # title: str
    # weight: int

    def __init__(self, title: str, weight: int):
        self.title = title
        self.weight = int(weight)

    def __repr__(self) -> str:
        return (
            f"({self.__class__.__name__}) [Title: {self.title}, Weigth: {self.weight}]"
        )


class Asset(NFTObject):
    # path: str

    def __init__(self, title: str, weight: int, path: str, layer):
        super().__init__(title, weight)
        self.path = path
        self.layer = layer

    def __repr__(self) -> str:
        return f"(Asset) [Title: {self.title}, Weigth: {self.weight}, Layer: {self.layer.title}]"


class Layer:
    # title: str
    # assets: List[Asset] = []

    def __init__(self, title: str) -> None:
        self.title = title
        self.assets: List[Asset] = []

    def choice(self) -> Asset:
        if len(self.assets) == 0:
            return 0
        return random.choices(
            self.assets, map(lambda asset: asset.weight, self.assets), k=1
        )[0]

    def append_asset(self, asset: Asset):
        self.assets.append(asset)

    def __repr__(self) -> str:
        return self.title


class Person:
    def __init__(self, assets: List[Asset]) -> None:
        self.assets = assets
        self.id = "-".join(
            map(lambda asset: f"{asset.layer.title}:{asset.title}", assets)
        )

    def is_compatible(self, incompatibilities: List[str]) -> bool:
        for incompatibility in incompatibilities:
            if all(map(lambda word: word in self.id, incompatibility.split("-"))):
                return False
        return True

    def get_metadata(self, index: int):
        return {
            "description": "Fake Non-Fungible characters in the testnet",
            "external_url": "https://openseacreatures.io/3",
            "image": "",
            "name": f"Non-Fungible Character #{index}",
            "attributes": {asset.layer.title: f"Type: #{asset.title}" for asset in self.assets},
        }        
    def save_metadado(self, path: Path, index: int):
        with open(str(path), "w") as file:
            
            json.dump(self.get_metadata(index), file)


    def render(self) -> Image:
        result = None
        for asset in self.assets:
            currentImage = Image.open(asset.path)
            if result:
                result.paste(currentImage, (0, 0), currentImage)
            else:
                result = currentImage

        return result.resize((360, 360), Image.BOX)


class Ethnicity(NFTObject):
    def __init__(self, title: str, weight: int):
        super().__init__(title, weight)
        self.layers: List[Tuple[int, Layer]] = []

    def append(self, *, layer: Layer, priority: int):
        self.layers.append((priority, layer))

    def generate(self) -> Person:
        # TODO:
        sortedLayers = map(
            lambda data: data[1], sorted(self.layers, key=lambda layer: layer[0])
        )
        return Person(assets=[layer.choice() for layer in sortedLayers])


class EthinicitySelector:
    def __init__(self, ethnicities: List[Ethnicity]) -> None:
        self.ethnicities = ethnicities

    def choice(self) -> Ethnicity:
        return random.choices(
            self.ethnicities, map(lambda e: e.weight, self.ethnicities), k=1
        )[0]


class Population:
    def __init__(
        self, ethnicities: List[Ethnicity], count: int, incompatibilities
    ) -> None:
        self.ethnicities = ethnicities
        self.count = count
        self.incompatibilites = incompatibilities

    def getPeople(self) -> List[Person]:
        history_ids = []
        people = []
        while len(people) < self.count:
            ethnicity = EthinicitySelector(self.ethnicities).choice()
            person = ethnicity.generate()
            if person.id not in history_ids and person.is_compatible(
                self.incompatibilites
            ):
                people.append(person)
                history_ids.append(person.id)

        return people


ethnicities = []
for dir in root.iterdir():
    title, weigth = dir.name.split("_")
    ethnicity = Ethnicity(title=title, weight=int(weigth))
    for layerDir in dir.iterdir():
        priority, title = layerDir.name.split("_")
        layer = Layer(title=title)
        for assetPath in layerDir.iterdir():
            id, weight = assetPath.name.split(".")[0].split("_")
            asset = Asset(
                title=id, weight=int(weigth), path=str(assetPath), layer=layer
            )
            layer.append_asset(asset)
        ethnicity.append(layer=layer, priority=int(priority))

    ethnicities.append(ethnicity)

population = Population(
    ethnicities=ethnicities, count=POPULATION_COUNT, incompatibilities=incompatibilities
)

for index, person in enumerate(population.getPeople()):
    person.render().save(f"collection/Non-Fungible Character-#{index}.png")
    person.save_metadado(Path(f"collectionjson/Non-Fungible Character-#{index}.json"), index)
    
