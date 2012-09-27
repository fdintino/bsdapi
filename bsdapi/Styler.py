class Colorizer(object):

    colors = {
        'purple': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',}

    endc = '\033[0m'

    def __init__(self, ansi_colors=False):
        self.ansi_colors = ansi_colors

    def color(self, string, color):
        if self.ansi_colors:
            return "%s%s%s" % (self.colors[color], string, self.endc)
        else:
            return string
