# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""
from utils import *

def fuzzify(x, left, middle, right):
    if left is not None and left <= x < middle:
        return (x - left) / (middle - left)
    elif right is not None and middle <= x < right:
        return (right - x) / (right - middle)
    elif left is None and x <= middle:
        return 1
    elif right is None and x >= middle:
        return 1
    else:
        return 0


def compute_values(value, value_ranges):
    result = dict()

    for key in value_ranges:
        result[key] = fuzzify(value, *value_ranges[key])

    return result


def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
    
    None :if we have a division by zero

    """

    theta = compute_values(t, THETA)
    omega = compute_values(w, OMEGA)
    middle_values = {key: value[1] for key, value in FORCE.items()}
    forces = dict()

    for theta_key in FUZZY_TABLE:
        for omega_key, force_value in FUZZY_TABLE[theta_key].items():
            value = min(theta[theta_key], omega[omega_key])

            if force_value not in forces:
                forces[force_value] = value
            else:
                forces[force_value] = max(value, forces[force_value])

    s = sum(forces.values())
    if s == 0:
        return None

    return sum(forces[x] * middle_values[x] for x in forces.keys())

