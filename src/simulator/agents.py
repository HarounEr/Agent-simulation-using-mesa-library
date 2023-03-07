import random
import mesa
#from simulator.model import width
NUMBER_OF_CELLS = 25
UNDONE = 3
# drone states
DRONE_FREE = 5
DRONE_SEARCHING = 6
DRONE_WAITING = 7
# drone_return = 5
SEARCHING_LEFT = 8
SEARCHING_RIGHT = 9
DRONE_FINISHED = 10

#person states
PERSON_WAITING = 14
PERSON_FOUND = 15
PERSON_RESCUED = 16

# first aid sates
F_A_FREE = 17
F_A_WAITING = 18
F_A_BUSY = 19
F_A_HELPING = 20
F_A_DONE = 21


class Drone(mesa.Agent):
    """Represents a drone of the simulator."""
    def __init__(self, id, pos, model, init_state=DRONE_FREE):
        """
        Initialise state attributes, including:
          * current and next position of the robot
          * state (FREE/BUSY)
          * payload (id of any box the robot is carrying)
        """
        super().__init__(id, model)
        self.x, self.y = pos
        self.next_x, self.next_y = None, None
        self.state = init_state
        self.payload= []
        self.battery = random.randint(70,100)
        self.base_location = pos
  


    def step(self):
        """
        * Obtain action as a result of deliberation
        * trigger action
        """
        #
        str_action = self.make_decision()
        action = getattr(self,str_action)
        #print(self.battery)
        # drones lose 0.1 battery every step
        if self.state == SEARCHING_LEFT or self.state == SEARCHING_RIGHT or self.state == DRONE_WAITING:
            self.battery = self.battery-0.1
        action()

    # Robot decision model

    def make_decision(self):
        """
        
        Simple rule-based architecture, should determine the action to execute based on the robot state.

        """
        
        action = "wait"
        # checking if the drones are in free state, if so charge battery
        if self.state == DRONE_FREE:
            self.battery = self.battery +1
            # initiate drones to search left
            self.state = SEARCHING_LEFT
        
        elif self.state == SEARCHING_LEFT:
            next_position = (self.x, self.y)
            # checking if in the same cell an agent of type person is there and its state
            person_pos_state = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.pos == next_position and a.state == UNDONE]

            if not self.model.grid.is_cell_empty(next_position) and len(person_pos_state)>0:
                print('scanning health of the person: LOADING')
                print('health of person:',person_pos_state[0].health)
                print('Age of person found:',person_pos_state[0].age)
                ## calculating person urgency, by dividing person health by their age
                person_urgency = person_pos_state[0].health/person_pos_state[0].age
                print('Person urgency:', person_urgency)
                print('Sending broadcast with person health:',person_pos_state[0].health, 'and position:', self.pos, 'Person urgency:', person_urgency)
                person_pos_state[0].state = PERSON_FOUND
                self.state= DRONE_WAITING

                
            elif self.pos[0] ==0:
                action = 'move_up'
                self.state = SEARCHING_RIGHT
            else:
                action= 'move_left'

        elif self.state == SEARCHING_RIGHT:
            
            next_pos = (self.x, self.y)
            
            person_checking = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.pos == next_pos and a.state == UNDONE]# and  a.state== UNDONE]
            
            if not self.model.grid.is_cell_empty(next_pos) and len(person_checking)>0:
                print('scanning health of the person: LOADING')
                print('health of person found:',person_checking[0].health)
                print('Age of person found:',person_checking[0].age)
                ## calculating person urgency, by dividing person health by their age
                person_urgency = person_checking[0].health/person_checking[0].age
                print('Person urgency:', person_urgency)
                print('sending broadcast with person health:',person_checking[0].health, 'and position:', next_pos, 'Person urgency:', person_urgency)
                person_checking[0].state = PERSON_FOUND
                self.state= DRONE_WAITING

            # if no person left by the end of the cells then move up thenn change state 
            elif self.x == NUMBER_OF_CELLS-1:
                action = 'move_up'
                self.state = SEARCHING_LEFT
            else:
                action = 'move_right'

        #after drone finds person it waits for first aid robot to show up
        elif self.state == DRONE_WAITING:
            

            action='wait'

        # when first aid robots comes
        elif self.state == DRONE_FINISHED:
            action = 'wait'
            f_a_state = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.state == PERSON_RESCUED]
            if len(f_a_state)>0:
                action = 'move_to_base'




        print("ag_",self.unique_id," action:",action)
        return action
        

    
    # agent actions


    def move(self):
        """
        Move robot to the next position.
        """
        #
        self.model.grid.move_agent(self,(self.next_x,self.next_y))
    
    def move_to(self,destination):
        """
        Generic method to move robot to a given destination, considering the edges of the grid.
        """
        delta_y = 0
        delta_x = 0
        
        if self.pos[1] > destination[1] and self.pos[1] >= 2 : 
            delta_y = -1
        elif self.pos[1] < destination[1] and self.pos[1] <= NUMBER_OF_CELLS -1:
            delta_y = 1 

        if self.pos[0] > destination[0] and self.pos[0] >= 2: 
            delta_x = -1
        elif self.pos[0] < destination[0] and self.pos[0] < NUMBER_OF_CELLS -1:
            delta_x = 1 
        
        self.next_x = self.pos[0] + delta_x
        self.next_y = self.pos[1] + delta_y
        self.move()

    def move_to_base(self):

        self.move_to([self.base_location[0], self.base_location[1]]) 


    def wait(self):
        """
        Keep the same position as the current one.
        """
        #
        self.next_x = self.x
        self.next_y = self.y
    def move_right(self):
        """
        Move the robot towards the boxes from left to right.
        """
        #
        self.next_x = self.x+1
        self.next_y = self.y
        self.move()
    
    def move_left(self):
        """
        Move the robot and the payload towards the collection point (right to left).
        """
        #
        self.next_x = self.x-1
        self.next_y = self.y
        self.move()

    def move_up(self):
        """
        Move the robot towards the boxes from left to right.
        """
        #
        self.next_x = self.x
        self.next_y = self.y+1
        self.move()
    
    def move_down(self):
        """
        Move the robot and the payload towards the collection point (right to left).
        """
        #
        self.next_x = self.x
        self.next_y = self.y-1
        self.move()
       
    def advance(self):
       """
       Advances position of the robot.
       """
       self.x = self.next_x
       self.y = self.next_y
    
##################################################################### MOUNTAIN ################################################################################

class Mountain(mesa.Agent):
    """Represents the mountain in the simulation."""
    def __init__(self, id, pos, model):
        """
        Intialise state and position of the box
        """
        super().__init__(id, model)
        #

        self.x, self.y = pos
        self.height = 0
##################################################################### PERSON ################################################################################
        
class Person(mesa.Agent):
    """
    A Person that is located whiten the mountain levels
    """

    energy = None

    def __init__(self, id, pos, model, init_state=UNDONE):
        super().__init__(id, model)
        self.state = init_state
        self.x, self.y = pos
        self.health = random.randint(40,60)
        self.age = random.randint(6,80)

    def set_state(self,new_state):
        """
        Enables update of the state of the box by the robot.
        """
        self.state = new_state

    @property
    def isUndone(self):
        return self.state == UNDONE

    @property
    def isRescued(self):
        return self.state == PERSON_RESCUED

    @property
    def isFound(self):
        return self.state == PERSON_FOUND
##################################################################### FIRST AID ################################################################################
class First_aid_robot(mesa.Agent ):
    """Represents a first aid Robot of the simulation."""
    def __init__(self, id, pos,init_tokens ,model, init_state=F_A_FREE):
        """
        Initialise state attributes, including:
          * current and next position of the robot
          * state (FREE/BUSY)
          * payload (id of any box the robot is carrying)
        """
        super().__init__(id, model)

        self.x, self.y = pos
        self.next_x, self.next_y = None, None
        self.state = init_state
        self.payload= []
        self.battery = random.randint(70,90)
        self.base_location = pos


    def step(self):
        """
        * Obtain action as a result of deliberation
        * trigger action
        * battery conditions
        """

        str_action = self.make_decision()
        action = getattr(self,str_action)
        action()
        if self.state == F_A_BUSY or self.state ==F_A_HELPING or self.state ==F_A_DONE:
            self.battery = self.battery - 1


        
    def set_state(self,new_state):
        """
        Enables update of the state of the first aid robot by other agent.
        """
        self.state = new_state


    def make_decision(self):

        action = "wait"


        if self.state == F_A_FREE:
            #if in base, charge battery by 0.2 per step
            action = "wait"
            if self.pos == self.base_location:
                self.battery += 0.2


        elif self.state == F_A_BUSY:
            next_position = (self.x, self.y)
            drone_found_person = [a for a in self.model.schedule.agents if isinstance(a,Drone) and a.state == DRONE_WAITING]

            robot_found_person = [a for a in self.model.schedule.agents if isinstance(a,Person) and a.state == PERSON_WAITING]
            
            if  self.pos == drone_found_person[0].pos:
                self.state= F_A_HELPING
                # changing drone state as the first aid robot is here 
                drone_found_person[0].state = DRONE_FINISHED
                print('drone finished')
 
            else:
                action = 'move_to_person'


        elif self.state == F_A_HELPING:
            next_position = (self.x, self.y)
            print('drop first aid kit, Returning to base')
            
            person_pos_state = [ a for a in self.model.schedule.agents if isinstance(a,Person) and a.pos == self.pos and a.state == PERSON_WAITING ]# and  a.state== UNPERSON_WAITING]
            if  self.pos == person_pos_state[0].pos:
                person_pos_state[0].state = PERSON_RESCUED 
                # increase person health after rescueing 
                person_pos_state[0].health = person_pos_state[0].health + 15
                self.state = F_A_DONE


        elif self.state == F_A_DONE:
            
            action = 'move_to_base'
            if self.pos == self.base_location:
                self.state = F_A_FREE
                


        print("ag_",self.unique_id," action:",action)
        return action

    
    # agent actions

    def move_to_person(self):

        person_found = [a for a in self.model.schedule.agents if isinstance(a,Drone) and a.state == DRONE_WAITING]
            
        if len(person_found) >0:
            person_found_pos_x = person_found[0].x
            person_found_pos_y = person_found[0].y
            self.move_to([person_found_pos_x, person_found_pos_y]) 

    def move_to_base(self):
        self.move_to([self.base_location[0], self.base_location[1]]) 
    

    def move_to(self,destination):
        """
        Generic method to move robot to a given destination, considering the edges of the grid.
        """
        delta_y = 0
        delta_x = 0
        
        if self.pos[1] > destination[1] and self.pos[1] >= 2 : 
            delta_y = -1
        elif self.pos[1] < destination[1] and self.pos[1] <= NUMBER_OF_CELLS -1:
            delta_y = 1 

        if self.pos[0] > destination[0] and self.pos[0] >= 2: 
            delta_x = -1
        elif self.pos[0] < destination[0] and self.pos[0] < NUMBER_OF_CELLS -1:
            delta_x = 1 
        
        self.next_x = self.pos[0] + delta_x
        self.next_y = self.pos[1] + delta_y
        self.move()


    def move_right(self):
        """
        Move the robot towards the boxes from left to right.
        """
        #
        self.next_x = self.x+1
        self.next_y = self.y
        self.move()
    
    def move_left(self):
        """
        Move the robot and the payload towards the collection point (right to left).
        """
        #
        self.next_x = self.x-1
        self.next_y = self.y
        self.move()

    def move_up(self):
        """
        Move the robot towards the boxes from left to right.
        """
        #
        self.next_x = self.x
        self.next_y = self.y+1
        self.move()
    
    def move_down(self):
        """
        Move the robot and the payload towards the collection point (right to left).
        """
        #
        self.next_x = self.x
        self.next_y = self.y-1
        self.move()

    def move(self):
        """
        Move robot to the next position.
        """
        #
        self.model.grid.move_agent(self,(self.next_x,self.next_y))

    def wait(self):
        """
        Keep the same position as the current one.
        """
        #
        self.next_x = self.x
        self.next_y = self.y
 
    def advance(self):
       """
       Advances position of the robot.
       """
       self.x = self.next_x
       self.y = self.next_y
