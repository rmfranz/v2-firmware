import logging

class TheCounter():

    def __init__(self):
        self.lines = []
        self.logger = logging.getLogger('gcode_logger')

    def add_line(self, line):
        self.lines.append(line)
        self.logger.debug(line)
    
    def count_lines(self):
        return len(self.lines)

    def remove_lines(self):
        self.lines.clear()