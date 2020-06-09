from mesa.visualization.ModularVisualization import VisualizationElement


class SimpleCanvas(VisualizationElement):
    local_includes = ["/home/cyn/COVID-Net2.0/ABM_COVID/SimpleContinuousConvas.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        space_state = []
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            x, y = obj.pos
            x = (x - model.district.x_min) / (model.district.x_max - model.district.x_min)
            y = (y - model.district.y_min) / (model.district.y_max - model.district.y_min)
            portrayal["x"] = x
            portrayal["y"] = y
            space_state.append(portrayal)
        return space_state
