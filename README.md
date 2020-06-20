# ABM_COVID
An agent-based model for COVID 19 transmission to test the optimal social distancing requirements
(note: this is developed by a novice who has no previous experiences with ABM. Please stay tuned for error checking and more updates)

Developed using Mesa https://mesa.readthedocs.io/en/master/
Minimum requirement is Python 3+.

Originally intended to be visualized as a webpage. However, visualization interface with ContinuousSpace in Mesa throws errors.

For now, initiate the model without any visual elements, in command line:

python3 novis_run.py 

or run novis_run.py using Python3 IDLE.

Print statements within the model will help understand each step as model is initiated. These include:
  a. how is each agent initialized, infected(1), susceptible(0), or removed/dead(1); 
  b. number of infected, susceptible, and removed agents in total;
  c. how many agents are in neighborhood and if they are within my safe social distance;
  d. if I will infect my neighbors;
  e. who infected who (identified by id)

To customize model parameters, go to novis_run.py. The user can specify:
model = PopulationModel(total number of agents, required social distance, individual infection probability, width of map, height of map)

For now, all agents are initialized with the social distancing requirements and infection probability specified from a model level.
If you want to customize these variables for individual agents, go to model_SIR.py and modify these parameters of PersonAgent():

self.infect_dist = what you want

self.infect_prob = what you want

Note, however, all agents will still be initialized with the same values. 

To be continued...