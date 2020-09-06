from PIL import Image, ImageFilter, ImageOps

NEIGHBORHOOD_DIFFERENCE_THRES = 50

def distance(c1, c2=(0, 0, 0)):
    return sum((x - y) ** 2 for x, y in zip(c1, c2)) ** 0.5

class EllipseInfo:
    @StaticMethod
    def find_ellipses(borders, distance_thres):
        # using
        # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1.8792&rep=rep1&type=pdf
        pass
    def __init__(self, center, major_axis, orientation):
        self.center = center
        self.major_axis = major_axis
        self.orientation = orientation
        self.ready = False
    def update_third_pixel(self, pixel):
        other = 
    def __hash__(self):
        

def borders_to_polygons(borders, distance_thres):
    paths = []
    point = borders.pop()
    curr_path = [point]
    while len(borders) > 0:
        # tie-breaking favors upper left for literally no reason -- we just need
        # a way to talk about paths
        probably_next = min(borders, key=lambda nbr: (distance(nbr, point), nbr))
        borders.remove(probably_next)
        if distance(point, probably_next) > distance_thres:
            paths.append(curr_path)
            curr_path = [probably_next]
        else:
            curr_path.append(probably_next)
        point = probably_next
    return paths

def colorize_path(pixels, polygons, colors=None):
    if colors is None:
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]
    for idx, path in enumerate(polygons):
        for point in path:
            pixels[point] = colors[idx % len(colors)]

def main(in_file, out_file):
    im = Image.open(in_file)
    width, height = im.size
    edgy_im = ImageOps.invert(im.filter(ImageFilter.FIND_EDGES))
    edgy_pix = edgy_im.load()
    borders = {(x, y) for x in range(width) for y in range(height) if distance(edgy_pix[x, y]) < 20}
    polygons = borders_to_polygons(borders, 4)
    colorize_path(edgy_pix, polygons)
    edgy_im.save(out_file)

if __name__ == "__main__":
    from sys import argv
    main(*(argv[1:]))
