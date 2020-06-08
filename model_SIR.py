### https://mesa.readthedocs.io/en/master/tutorials/adv_tutorial.html
### https://github.com/projectmesa/mesa/tree/master/mesa

from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa.space import ContinuousSpace
from numpy.random import choice
from random import choices

class PersonAgent(Agent):

    
    """ an agent """
    def __init__(self, unique_id, radius, prob, model):
        super().__init__(unique_id,model)
        self.infect_state = random.randint(-1,1) # make it public so that if this agent is dead,
        # I can access this field when running the model

        """ -1 = removed, 0 = susceptible, 1 = infected """
        
        self.infect_dist = radius

        self.infect_prob = prob
        
        if self.infected == 1:
            self.model.num_infected += 1
            self.model.num_uninfected =self.model.num_agents-self.model.num_infected
        """ calculate infected and uninfected in the whole system """

        print('initialized as ' + 'id: '+ str(self.unique_id) + ' infected? '+ str(self.infected)+'\n')
        print('total infected: ' + str(self.model.num_infected)+'\n')

    def set_infect_state(self,st):
        """ setter of individual agent, set to S I or R """
        self.infect_state = st

    def set_infect_rad(self,r):
        """ setter of infection radius """
        self.infect_dist = r        

    def step(self):
        """ what happens at each step """
        
        self.move() 
        
        other_agent = self.random.choice(self.model.schedule.agents)
        """ the list of all agents are actually in model.schedule """

        all_neighbors = self.model.district.get_neighbors( # find all the neighbors in the radius of social distancing
            self.pos, # self.pos is a built-in field 
            self.infect_dist,
            include_center = False)
        """ get all the possible neighbors within a certain radius """

        print('there are ' + str(len(all_neighbors)) + ' neighbors')
        print('agent id ' + self.unique_id + 'has the following neighbors: ' + '\n')
        for neighbor in all_neighbors:
            print(str(neighbor.unique_id))



        """ infection with probability """
        if all_neighbors != [] and if self.infect_state == 1: # if any other agent is in my infection radius and I'm infected
            neighbor_infect_state = []
            for other_agent in all_neighbors: # record a list of what the infection state is of my neighbors
                neighbor_infect_state.append(other_agent)
            weights = [prob,1-prob] # probability of infecting others, not infecting others
            new_neighbor_infect_state = choices(neighbor_infect_state,weights = weights, k = len(all_neighbors))
            """ generate a random list of infected/uninfected """

            for i, other_agent in enumerate(all_neighbors): # now update their infection state
                other_agent.set_infect_state(new_neighbor_infect_state[i])
                if new_neighbor_infect_state[i] == 1: 
                    print('agent id ' + self.unique_id + 'infected this neighbor id' + other_agent.unique_id)


    def move(self):
        """ will need to get how people move from real-life data """
        """ maybe we can use random walk for now?? """

        if self.infect_state == -1: # if removed, no need to update
            self.model.district.remove_agent(self) # if dead, remove the agent from simulation
            return

        possible_steps = []
        x,y = self.pos
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                possible_steps.append([(x+dx),(y+dy)])
        """ for now, move as if we are in a grid, will figure out random walk later """
        
        
        new_position = self.random.choice(possible_steps)
        self.model.district.move_agent(self,new_position)
        


class PopulationModel(Model):
    """ a model with population in a district """
    num_S = 0
    num_I = 0
    num_R = 0
    num_agents = 0
    
    def __init__(self,N,r,width,height):
        self.num_agents = N   
        self.num_S = N
        # self.required_social_dist = r
        
        """ scheduler controls the order at which agents are activated """
        """ RandomActivation activates all the agents once per step """
        self.schedule = RandomActivation(self)

        """ create a continuous space """
        self.district = ContinuousSpace(width,height, True)

        # create agents 
        for i in range(self.num_agents):
            a = PersonAgent(i,self.required_social_dist,self)
            # i is the id number
            self.schedule.add(a)
            """ add an agent to the schedule using add method """

            # place the agent in the continuous space 
            x = self.random.randrange(self.district.width)
            y = self.random.randrange(self.district.height)
            self.district.place_agent(a,(x,y))
            print("id " + str(i) + " is at " + str(x) + "," + str(y))
            

    def step(self):
        """ advance the model by one step """
        self.schedule.step()
