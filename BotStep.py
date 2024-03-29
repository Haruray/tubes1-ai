class BotStep():
    #botstep gunanya untuk merekam value dan steps yg telah diambil
    def __init__(self, value) -> None:
        self.value = value
        self.steps_recorded = []
        #steps_recorded adalah array yang menyimpan ["row/col",x,y] yang merupakan posisi garis yang ditandai dalam setiap stepnya
    def get_first_step(self):
        return self.steps_recorded[0]
    def get_first_step_type(self):
        #return "row" atau "col"
        return self.steps_recorded[0][0]
    def get_first_step_x(self):
        #return "row" atau "col"
        return self.steps_recorded[0][1]
    def get_first_step_y(self):
        #return "row" atau "col"
        return self.steps_recorded[0][2]
    def get_steps(self):
        return self.steps_recorded
    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
    def set_steps(self, steps):
        self.steps_recorded = steps
    def add_step(self, new_step:list):
        self.steps_recorded.append(new_step)

    def clear_steps(self):
        self.steps_recorded.clear()
    
    #operator overloading
    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, BotStep):
            return NotImplemented
        return self.value == __o.value

    def __gt__(self, __o):
        if not isinstance(__o, BotStep):
            return NotImplemented
        return self.value > __o.value

    def __ge__(self, __o):
        if not isinstance(__o, BotStep):
            return NotImplemented
        return self.value >= __o.value

    def __lt__(self, __o):
        if not isinstance(__o, BotStep):
            return NotImplemented
        return self.value < __o.value

    def __le__(self, __o):
        if not isinstance(__o, BotStep):
            return NotImplemented
        return self.value <= __o.value


