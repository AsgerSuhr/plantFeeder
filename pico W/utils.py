import re

def read_html(filename):
    with open(filename, 'r') as f:
        html = ''
        for line in f.readlines():
            line = line.strip()
            html+=line
    return html

    
def find_ml(txt:str):
    ml_matcher = re.compile(r'ml=\d+')
    mtch = ml_matcher.search(txt)
    ml = mtch.group(0)
    return int(ml.split('=')[-1])

def tube_volume(length, diameter):
    #volume = r^2 * pi
    radius = diameter/2
    length = length*10 # from cm to mm
    return ((radius**2 * math.pi)*length)/1000

def flow(V, G=50):
    # time motor is on = volume[ml] * flowfactor [ms/ml] + tube [ms]
    # for some reason when i tested the tubes they all delivered 100 ml per 5 second
    # regardless of the tubes length. very confused
    # so for now the flow is as follows t[sec] = (V[ml] * flowfactor[ms/ml])/1000
    return (V * G)/1000
