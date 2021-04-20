import numpy as np
from math import sin, cos, floor

def create_circle(canvas, x, y, r, color):
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=color)

def rgbtohex(rgb):
    r, g, b = rgb
    return f'#{floor(r):02x}{floor(g):02x}{floor(b):02x}'

def rotVecteur(vect, angle):
    rot = np.array([[cos(angle), -sin(angle)], [sin(angle), cos(angle)]])
    return np.dot(rot, vect)

def theta(v, w):
    return np.arccos(v.dot(w)/(np.linalg.norm(v)*np.linalg.norm(w)))
