class TheCounter():

    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)
    
    def count_lines(self):
        return len(self.lines)

    def remove_lines(self):
        self.lines.clear()