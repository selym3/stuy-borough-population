def read_lines(f):
    line = f.readline()
    while line != '':
        yield line
        line = f.readline()

def validate_br(br):
    return br.strip().lower()

def formal_capitalize(s):
    c = ' '
    out = ''
    for char in s:
        if c == ' ':
            char = char.upper()
        else:
            char = char.lower()
        
        out += char
        c = char

    return out

def format_list(L):
    if len(L) <= 2:
        return ' and '.join(L)
    else:
        comma_separated = ', '.join(L[:-1])
        return comma_separated + f', and {L[-1]}'

def parse(filename):
    
    def get_parts(l):
        return l.strip().split(',')

    with open(filename) as f:
        header = get_parts(f.readline())
        boroughs = [ validate_br(br) for br in header[1:] ]

        city_population = {}

        for line in read_lines(f):
            data = [ int(part) for part in get_parts(line) ]

            year, populations = data[0], data[1:]

            city_population[year] = {
                borough: population
                for borough, population
                in zip(boroughs, populations)
            }

        return boroughs, city_population

import matplotlib.pyplot as plt

class CityManager:

    def __init__(self, from_csv):
        self.boroughs, self.populations = parse(from_csv)
        self.years = list(self.populations.keys())

    def get_borough_data(self, borough):
        borough = validate_br(borough)
        y = []
        for populations in self.populations.values():
            y += [ populations[borough] ]
        return self.years, y

    def setup_borough(self, borough):
        borough = validate_br(borough)

        years, populations = self.get_borough_data(borough)
        plt.plot(
            years, 
            populations, 
            label=f'{borough}'
        )

    def graph_boroughs(self, boroughs=None, savefile=None, show=True):
        boroughs = self.boroughs if boroughs is None else boroughs

        for borough in boroughs:
            self.setup_borough(borough)

        plt.xlabel('Year')
        plt.ylabel('Population (millions)')

        plt.legend()

        boroughs = [ formal_capitalize(b) for b in boroughs ]
        plt.title(f'{format_list(boroughs)} Populations')
        
        if savefile is not None:
            plt.savefig(savefile, dpi=300, bbox_inches='tight')

        if show:
            plt.show()

if __name__ == "__main__":

    # Save the .GIF programatically
    SAVE_TYPE = '.png' #<-- GIF is not available
    
    MY_BOROUGH = 'images/my_borough' + SAVE_TYPE
    ALL_BOROUGHS = 'images/all_boroughs' + SAVE_TYPE
    
    SHOW_PLOT = True

    # Parse the CSV file
    CSV_PATH = "resources/nyc-population.csv"
    
    manager = CityManager(from_csv=CSV_PATH)

    '''
    Question 1:
    '''

    my_borough = 'BROOKLYN'

    manager.graph_boroughs(
        boroughs=[my_borough],
        savefile=MY_BOROUGH,
        show=SHOW_PLOT
    )

    '''
    Question 2:
    '''

    # passing in none handles all boroughs

    manager.graph_boroughs(
        savefile=ALL_BOROUGHS,
        show=SHOW_PLOT
    )
