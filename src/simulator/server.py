
import mesa
from mesa.visualization.UserParam import UserSettableParameter
from simulator.model import Simulator
from .portrayal import simulator_portrayal
from .agents import NUMBER_OF_CELLS

SIZE_OF_CANVAS_IN_PIXELS_X = 600
SIZE_OF_CANVAS_IN_PIXELS_Y = 600



simulation_params = {
    "height": NUMBER_OF_CELLS, 
    "width": NUMBER_OF_CELLS,
    }
grid = mesa.visualization.CanvasGrid(simulator_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_IN_PIXELS_X, SIZE_OF_CANVAS_IN_PIXELS_Y)


server = mesa.visualization.ModularServer(
    Simulator, [grid], "Drone and First Aid Terrain Robots Simulator", simulation_params
)
