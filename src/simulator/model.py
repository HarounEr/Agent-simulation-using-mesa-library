import mesa
import random
import numpy as np
from random import randint
from pydoc import doc
from simulator.agents import Drone
from simulator.agents import Mountain,Person,First_aid_robot
from .agents import UNDONE, PERSON_RESCUED,PERSON_FOUND, PERSON_WAITING, F_A_FREE, F_A_BUSY, F_A_HELPING, F_A_DONE

# pending person checking
def pending_people(model):
    return len([a for a in model.schedule.agents if isinstance(a,Person) and a.state != PERSON_RESCUED ])


# the simulation class includes the number of agents and intialise them
class Simulator(mesa.Model):
    """ Model representing an automated search for people"""
    def __init__(self, n_robots = 3, n_person = 3, n_first_aid = 3,n_boxes=25, width=50, height=50):
        """
            * Set schedule defining model activation
            * Sets the number of robots as per user input
            * Sets the grid space of the model
            * Create n Robots as required and place them randomly on the edge of the left side of the 2D space.
            * Create m Boxes as required and place them randomly within the model (Hint: To simplify you can place them in the same horizontal position as the Robots). Make sure robots or boxes do not overlap with each other.
        """
        # TODO implement
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.n_robots = n_robots
        self.n_boxes = n_boxes
        self.n_person = n_person 
        self.n_first_aid = n_first_aid
        #using a multi grid so agent to collide
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        
        # Drones 
        y=1
        x = width -5
        for n in range(self.n_robots):
            #x = width -5
            pr = Drone(n,(x,y), self)
            self.schedule.add(pr)
            self.grid.place_agent(pr,(x,y))
            x=x-3


        # Mountain parameters
        list_2 = [
                        (4,15),(5,15),(6,15),
                        (4,16),(6,16),
                        (4,17),(5,17),(6,17)
                     ]

        list_1 = [(3,14),(4,14),(5,14),(6,14),(7,14),
                        (3,15),(7,15),
                        (3,16),(7,16),
                        (3,17),(7,17),
                        (3,18),(4,18),(5,18),(6,18),(7,18)]

        list_3 = (5,16)

        # Mountain
        for n in range(self.n_boxes):

            if n in range(0,16):    
                b = Mountain(n+self.n_robots, list_1[n], self)
                #if b.pos == list_1[n] :
                b.height = 1#k
                self.schedule.add(b)
                self.grid.place_agent(b,list_1[n])
                

            elif n in range(16,24):
                f = Mountain(n+self.n_robots+250, list_2[n-16], self)
                f.height = 2#k
                self.schedule.add(f)
                self.grid.place_agent(f,list_2[n-16])

            elif n == 24:
                e = Mountain(n+self.n_robots+500, list_3, self)
                e.height = 3#k
                self.schedule.add(e)
                self.grid.place_agent(e,list_3)
        # Person
        for n in range(self.n_person):
            if n_person == 3 and n==2:
                person = Person(n+self.n_robots+n_boxes, random.choice(list_1), self)
                self.grid.place_agent(person,random.choice(list_1))
                self.schedule.add(person)

            elif n_person == 3 and n ==1:
                person = Person(n+self.n_robots+n_boxes, random.choice(list_2), self)
                self.grid.place_agent(person,random.choice(list_2))
                self.schedule.add(person)

            elif n_person == 3 and n==0:
                person = Person(n+self.n_robots+n_boxes, list_3, self)
                self.grid.place_agent(person, list_3)
                self.schedule.add(person)

        # Terrain robots
        y = 12
        for n in range(self.n_first_aid):
            x = width -1

            first_a = First_aid_robot(n+1000,(x,y),0, self)
            self.schedule.add(first_a)
            self.grid.place_agent(first_a,(x,y))
            y = y+2


        self.running = True


        # Data collection to use for Jupyter notebook
        self.datacollector = mesa.DataCollector(
            model_reporters={
                            "pending_people": pending_people,
                            "person_rescued": lambda m: len([a for a in m.schedule.agents if isinstance(a,Person) and a.state == PERSON_RESCUED ]),
                            "robot_arrive_to_person_step": lambda m: len([a for a in m.schedule.agents if isinstance(a,First_aid_robot) and a.state == F_A_HELPING]),
                            "First_aid_free": lambda m: len([a for a in m.schedule.agents if isinstance(a,First_aid_robot) and a.state == F_A_FREE]),
                            "First_aid_finished": lambda m: len([a for a in m.schedule.agents if isinstance(a,First_aid_robot) and a.state == F_A_DONE]),
                            "First_aid_busy": lambda m: len([a for a in m.schedule.agents if isinstance(a,First_aid_robot) and a.state == F_A_BUSY])
            
            }, agent_reporters={"state": "state","type":lambda a:str(a.__class__.__name__)})
        

    def step(self):
        """
        * Run while there are person to be rescued, Drones and first aid robot out of base, otherwise stop running model.
        """
        pending_first_aid = [a for a in self.schedule.agents if isinstance(a,Drone) and a.pos != a.base_location]
        pending_FirstAid_R =  [a for a in self.schedule.agents if isinstance(a,First_aid_robot) and a.pos != a.base_location]

        if pending_people(self)>0 or len(pending_first_aid)>0 or len(pending_FirstAid_R)>0:
            k = [a for a in self.schedule.agents if isinstance(a,First_aid_robot) and a.state == F_A_FREE]
            p = [a for a in self.schedule.agents if isinstance(a,Person) and a.state == PERSON_FOUND ]
            if len(k)>0 and len(p)>0:
                print('IMHERE')
                self.run_auction()
                p[0].state = PERSON_WAITING
            self.schedule.step()
        else :
            self.running = False
        self.datacollector.collect(self)

    
    ## auction using highest battery
    def run_auction(self):

        winning_battery = 0
        #ag_id = 0
        for i in range (len(self.schedule.agents)):
            if  isinstance(self.schedule.agents[i], First_aid_robot) and self.schedule.agents[i].state == F_A_FREE :
                if self.schedule.agents[i].battery > winning_battery  :
                    winning_battery = self.schedule.agents[i].battery
                    ag_id = i
        self.schedule.agents[ag_id].set_state(F_A_BUSY)





    