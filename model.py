### https://mesa.readthedocs.io/en/master/tutorials/adv_tutorial.html
### https://github.com/projectmesa/mesa/tree/master/mesa

from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa.space import ContinuousSpace

class PersonAgent(Agent):

    
    """ an agent """
    def __init__(self, unique_id, radius, model):
        super().__init__(unique_id,model)
        self.infected = random.randint(0,1) # make it public so that if this agent is dead,
        # I can access this field when running the model
        self.hospitalized = 0 # how do I change this from the model level? maybe make it public 
        """ randomly assign who is infected but no one is hospitalized to start with """

        self.social_dist = radius
        
        if self.infected == 1:
            self.model.num_infected += 1
            self.model.num_uninfected =self.model.num_agents-self.model.num_infected
        """ calculate infected and uninfected in the whole system """


        print('initialized as ' + 'id: '+ str(self.unique_id) + ' infected? '+ str(self.infected)+'\n')
        print('total infected: ' + str(self.model.num_infected)+'\n')

    def step(self):

        self.move()

        if self.infected == -1: # dead
            self.model.district.remove_agent(self) # if dead, remove the agent from simulation
            return 
        
        other_agent = self.random.choice(self.model.schedule.agents)
        """ the list of all agents are actually in model.schedule """

        all_neighbors = self.model.district.get_neighbors( # find all the neighbors in the radius of social distancing
            self.pos, # self.pos is a built-in field 
            self.social_dist,
            include_center = False)
        """ get all the possible neighbors within a certain radius """

        print('there are ' + str(len(all_neighbors)) + ' neighbors')
        print('agent id ' + 'has the following neighbors: ' + '\n')
        for neighbor in all_neighbors:
            print(str(neighbor.unique_id))

        if all_neighbors != []: # if the distance between me and anyone is fewer than 6 ft, I get infected
            for other_agent in all_neighbors: 
                if other_agent.infected == 1: # being infected by its neighbor
                    if self.infected == 0:
                        self.infected = 1
                        self.model.num_infected += 1
                        self.model.num_uninfected -= 1

        print('after id ' + str(self.unique_id) + ' contacting with id: ' + str(other_agent.unique_id)+'\n')
        print('now' + ' id: '+ str(self.unique_id) + ' infected? '+ str(self.infected)+'\n')

    def move(self):
        """ will need to get how people move from real-life data """
        """ maybe we can use random walk for now?? """

        if self.hospitalized == 1: # if already in hospital, won't move
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
    num_dead = 0
    num_infected = 0
    num_uninfected = 0
    num_agents = 0
    
    def __init__(self,N,r,width,height):
        self.num_agents = N   
        self.num_uninfected = N
        self.required_social_dist = r
        
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
