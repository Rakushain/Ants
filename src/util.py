import numpy as np
from math import sin, cos, floor
"""
    Fichier regroupant des fonctions utilisees dans differentes classes
    """


def create_circle(canvas, x, y, r, color, **kwargs):
    """
    Fonction qui permet de creer un cercle sur le canvas
    """
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvas.create_oval(x0, y0, x1, y1, fill=color, **kwargs)


def rgb_to_hex(rgb):
    """
    Fonction qui convertir une couleur rgb en hexadecimal, car tkinter ne reconnait pas le modele rgb
    """
    r, g, b = rgb
    return f'#{floor(r):02x}{floor(g):02x}{floor(b):02x}'


def distance(v, w):
    """
    Fonction qui retourne une distance entre deux points
    """
    return np.linalg.norm(w - v)


def angle(v, w):
    """
    Fonction qui retourne l angle entre deux vecteurs
    """
    return np.arccos(v.dot(w) / (np.linalg.norm(v) * np.linalg.norm(w)))


def rotate(v, angle):
    """
    Fonction qui permet d'effectuer une rotation d un vecteur
    """
    r = np.array(([np.cos(angle), -np.sin(angle)],
                 [np.sin(angle), np.cos(angle)]))
    return r.dot(v)


def random_inside_circle():
    """
    Fonction qui retourne un point aleatoire dans un cercle de rayon 1
    """
    length = np.sqrt(np.random.uniform(0, 1))
    angle = np.pi * np.random.uniform(0, 2)

    return np.array([length * np.cos(angle), length * np.sin(angle)])
