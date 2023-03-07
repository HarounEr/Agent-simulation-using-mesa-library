
from simulator.agents import Drone
from simulator.agents import Mountain ,Person, First_aid_robot
from simulator.model import Simulator


def simulator_portrayal(agent):
    """
    Determine which portrayal to use according to the type of agent.
    """

    if isinstance(agent,Drone):
        return robot_portrayal(agent)
    elif isinstance(agent,Person):
        return person_portrayal(agent)
    elif isinstance(agent,First_aid_robot):
        return first_aid_portrayal(agent)

    elif isinstance(agent,Mountain) and agent.height == 1:
        return mountain_portrayal_level_1(agent)

    elif isinstance(agent,Mountain) and agent.height == 2:
        return mountain_portrayal_level_2(agent)
    
    elif isinstance(agent,Mountain) and agent.height == 3 :
        return mountain_portrayal_level_3(agent)

    


def robot_portrayal(robot):
 
    if robot is None:
        raise AssertionError
    return {
        "Shape": "simulator/resources/droness.png", 
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": robot.x,
        "y": robot.y,
        "scale": 2,
        
    }

def mountain_portrayal(box):
 
    if box is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": box.x,
        "y": box.y,
        "scale": 1,
        "Color": "green", 
    }

def mountain_portrayal_level_1(cox):
 
    if cox is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": cox.x,
        "y": cox.y,
        "scale": 1,
        "Color": "green",
    }

def mountain_portrayal_level_2(fox):
 
    if fox is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": fox.x,
        "y": fox.y,
        "scale": 1,
        "Color": "#818B99",
    }


def mountain_portrayal_level_3(box):
 
    if box is None:
        raise AssertionError
    return {
        "Shape": "rect",
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": box.x,
        "y": box.y,
        "scale": 1,
        "Color": "#E8F6FB",
    }

def person_portrayal(person):
 
    if person is None:
        raise AssertionError
    return {
        "Shape": "simulator/resources/emergency.png" if person.isRescued  else "simulator/resources/person.png", # https://icons8.com/icons/set/person-arms-up , https://www.flaticon.com/free-icon/emergency_497081?related_id=496979&origin=search
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": person.x,
        "y": person.y,
        "scale": 1,
        "Color": "blue",
    }

def first_aid_portrayal(f_aid):
 
    if f_aid is None:
        raise AssertionError
    return {
        "Shape": "simulator/resources/firstAidRobot.png", # https://icons8.com/icons/set/robot
        "w": 1,
        "h": 1,
        "Filled": "true",
        "Layer": 0,
        "x": f_aid.x,
        "y": f_aid.y,
        "scale": 1,
        "Color": "blue",
    }