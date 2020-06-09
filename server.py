from model_SIR import PopulationModel
from mesa.visualization.ModularVisualization import ModularServer
from SimpleContinuousModule import SimpleCanvas
import matplotlib.pyplot as plt

model = PopulationModel(10, 6, 0.2, 12,12)

for i in range(5):
    model.step()


def person_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}


persons_canvas = SimpleCanvas(person_draw, 500, 500)
model_params = {
    "N": 5,
    "r":6,
    "p": 0.2,
    "width": 100,
    "height": 100,
}

server = ModularServer(PopulationModel, [persons_canvas], "Person", model_params)
