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
    '''
    this function parses the file in a way that's ideal for 
    using matplotlib 

    it returns (list of years), (list of boroughs), (map of borough -> list of populations)

    a better/cooler representation of the data might be (map of year -> (map of borough -> population))
    but this makes it harder to use matplot lib
    '''

    def get_parts(l):
        return l.strip().split(',')

    with open(filename) as f:

        header = get_parts(f.readline())
        boroughs = [ validate_br(br) for br in header[1:] ]
        
        years = []

        city_population = {
            borough: []
            for borough
            in boroughs
        }

        for line in read_lines(f):
            data = [ int(part) for part in get_parts(line) ]

            year, populations = data[0], data[1:]

            years += [ year ]

            for borough, population in zip(city_population, populations):
                city_population[borough] += [ int(population) ]
                

        return years, boroughs, city_population

import matplotlib.pyplot as plt

class CityManager:

    def __init__(self, from_csv):
        '''
        class to encapsulate city population data

        parameters-
            from_csv - data file to read from

        fields-
            years - list of years (x-values)
            boroughs - list of boroughs (in population map), help choose a y data set
            populations - map of lists of populations (all possible y values)
        '''

        parsed = parse(from_csv)
        self.years, self.boroughs, self.populations = parsed

    def get_borough_data(self, borough):
        return self.years, self.populations[borough]

    def setup_borough(self, borough):
        borough = validate_br(borough)

        years, populations = self.get_borough_data(borough)
        plt.plot(
            years, 
            populations, 
            label=formal_capitalize(borough)
        )

    def graph_boroughs(self, boroughs=None, savefile=None, show=True):
        plt.close()
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

    # Choose what the program should do
    SAVE_IMAGE = True
    SHOW_PLOT = False

    # If going to save the images, select where
    SAVE_TYPE = '.png' #<-- GIF is not available
    
    MY_BOROUGH = 'images/my_borough' + SAVE_TYPE
    ALL_BOROUGHS = 'images/all_boroughs' + SAVE_TYPE

    if not SAVE_IMAGE:
        MY_BOROUGH, ALL_BOROUGHS = None, None

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
