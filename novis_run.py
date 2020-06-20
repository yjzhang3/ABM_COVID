from model_SIR import PopulationModel
from mesa.visualization.ModularVisualization import ModularServer
from SimpleContinuousModule import SimpleCanvas
import matplotlib.pyplot as plt

model = PopulationModel(10, 6, 0.2, 12,12)
""" customize parameters here: (number of total agents, required social distance,
infection probability, width of the 2D space, height of the 2D space)
"""

for i in range(5): 
    model.step()
    """ how many steps you would like the model to run """


##def person_draw(agent):
##    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}
##
##
##persons_canvas = SimpleCanvas(person_draw, 500, 500)
##model_params = {
##    "N": 5,
##    "r":6,
##    "p": 0.2,
##    "width": 100,
##    "height": 100,
##}
##
##server = ModularServer(PopulationModel, [persons_canvas], "Person", model_params)
