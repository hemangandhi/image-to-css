from PIL import Image

NEIGHBORHOOD_DIFFERENCE_THRES = 128 * (3 ** 0.5)

def distance(c1, c2=(0, 0, 0)):
    return sum((x - y) ** 2 for x, y in zip(c1, c2)) ** 0.5

def points_within_distance(x, y, width, height, neighborhood, values):
    x_idxs = range(max(0, x - neighborhood), min(x + neighborhood + 1, width))
    y_idxs = range(max(0, y - neighborhood), min(y + neighborhood + 1, height))
    ok_idxs = ((x_in, y_in) for x_in in x_idxs for y_in in y_idxs if distance((x_in, y_in), (x, y)))
    return [values(ok_idx[0], ok_idx[1]) for ok_idx in ok_idxs]

def get_border_pixels(width, height, grayscale, neighborhood):
    border_pix = []
    for x in range(width):
        for y in range(height):
            pts = points_within_distance(x, y, width, height,
                                         neighborhood, lambda i, j: grayscale[i][j])
            if sum(pts) >= NEIGHBORHOOD_DIFFERENCE_THRES * len(pts) / 2:
                border_pix.append((x, y))
    return border_pix

def main(in_file, out_file, neighborhood):
    im = Image.open(in_file)
    pix = im.load()
    width, height = im.size
    grayscale = [[sum(distance(pix[x, y], nbr)
                      for nbr in points_within_distance(x, y, width, height,
                                                        neighborhood, lambda i, j: pix[i, j]))
                  for y in range(height)]
                 for x in range(width)]
    borders = get_border_pixels(width, height, grayscale, neighborhood)
    with open(out_file, 'w') as output:
        for b in borders:
            output.write(str(b))

if __name__ == "__main__":
    from sys import argv
    main(*(argv[1:]))
