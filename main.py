from PIL import Image, ImageFilter, ImageOps

NEIGHBORHOOD_DIFFERENCE_THRES = 50

def distance(c1, c2=(0, 0, 0)):
    return sum((x - y) ** 2 for x, y in zip(c1, c2)) ** 0.5

def borders_to_polygons(borders, distance_thres):
    paths = []
    point = borders.pop()
    curr_path = [point]
    while len(borders) > 0:
        probably_next = min(borders, key=lambda nbr: distance(nbr, point))
        borders.remove(probably_next)
        if distance(point, probably_next) > distance_thres:
            paths.append(curr_path)
            curr_path = [probably_next]
        else:
            curr_path.append(probably_next)
        point = probably_next
    return paths

def main(in_file, out_file):
    im = Image.open(in_file)
    width, height = im.size
    edgy_im = ImageOps.invert(im.filter(ImageFilter.FIND_EDGES))
    edgy_pix = edgy_im.load()
    borders = {(x, y) for x in range(width) for y in range(height) if distance(edgy_pix[x, y]) < 20}
    polygons = borders_to_polygons(borders, 4)


if __name__ == "__main__":
    from sys import argv
    main(*(argv[1:]))
