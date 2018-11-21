import random
from PIL import Image

def main():
  filename = input("filename: ")
  input_image = Image.open(filename)
  k_input = input("k-value: ")
  k = int(k_input)
  input_image = Image.open(filename)
  default_colors = get_random_colors(input_image, k)
  default_cluster = create_cluster_dict(default_colors)
  clusters = populate_clusters(input_image, default_cluster, default_colors)
  final_clusters = change_clusters_if_needed(clusters, input_image)
  new_image = input_image.copy()
  populate_image_from_clusters(new_image, final_clusters)
  new_image.save("output_kmeans.png")

def change_clusters_if_needed(clusters, image):
  '''
  :param clusters: cluster dicts in the form {center: [colors]}
  :return: the clusters after convergence is reached
  '''
  new_centers = []
  something_changed = False
  for center in clusters:
    colors = clusters[center]
    average = get_average_color(colors)
    if average != center:
      something_changed = True
    new_centers.append(average)
  if something_changed:
    new_empty_clusters = create_cluster_dict(new_centers)
    new_populated_clusters = populate_clusters(image, new_empty_clusters, new_centers)
    return change_clusters_if_needed(new_populated_clusters, image)
  else:
    return clusters

def get_average_color(colors):
  '''
  :param colors: a list of colors in the form [(R, G, B)]
  :return: a color in the form (R, G, B)
  '''
  num_colors = len(colors)
  if num_colors == 0:
    return (0, 0, 0)
  r = 0
  g = 0
  b = 0
  for color in colors:
    r += color[0]
    g += color[1]
    b += color[2]
  return(int(r/num_colors), int(g/num_colors), int(b/num_colors))


def populate_clusters(image, clusters, centers):
  '''
  :param image: the image for which we are creating the clusters
  :param clusters: default cluster dict where the key is the center and the value is the list of colors in the cluster
  :param centers: a list of the colors that we are using to cluster
  :return: the cluster dict after populating with colors in the image
  '''
  for y in range(image.height):
    for x in range(image.width):
      color = image.getpixel((x, y))
      center = get_nearest_center(color, centers)
      clusters[center].append(color)
  return clusters

def get_nearest_center(color, centers):
  '''
  :param color: a color in the form (R, G, B)
  :param centers: a list of colors
  :return: the center that is closet to color according to distance_between_colors
  '''
  nearest_center = centers[0]
  shortest_distance = distance_between_colors(color, centers[0])
  for c in centers[1:]:
    distance = distance_between_colors(color, c)
    if distance < shortest_distance:
      shortest_distance = distance
      nearest_center = c
  return nearest_center

def get_random_colors(image, n):
  '''
  :param image: the image in which we are getting n random pixels
  :param n: the number of random pixels
  :return: a list of n pairs, each of which contains an (x, y) coordinate
  '''
  initial_colors = []
  while(len(initial_colors) < n):
    x = random.randint(0, image.width)
    y = random.randint(0, image.height)
    color = image.getpixel((x, y))
    initial_colors.append(color)
  return initial_colors

def distance_between_colors(color1, color2):
  '''
  :param color1: a color in the format (R, G, B)
  :param color2: a color in the format (R, G, B)
  :return: a floating point number representing the color space distance between color1 and color2
  '''
  sum = 0
  for index in range(3):
    sum += (color1[index] - color2[index])**2
  return sum ** (1/2)

def populate_image_from_clusters(image, clusters):
  '''
  :param image: a blank image whose pixels' colors will be set
  :param clusters: the groups of similar pixels in a dict object
  :return: nothing, this function edits 'image'
  '''
  centers = list(clusters.keys())
  for y in range(image.height):
    for x in range(image.width):
      old_color = image.getpixel((x, y))
      closest_center = get_nearest_center(old_color, centers)
      image.putpixel((x, y), closest_center)

def create_cluster_dict(centers):
  d = {}
  for c in centers:
    d[c] = []
  return d

main()
