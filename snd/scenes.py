import pygame
from sprites import *
from settings import *
from random import randint

scene = {"background":
    [[0,0, WIDTH, 400, WHITE]],
    "plat":
    [[0, 400, WIDTH, 300, RED],
    [WIDTH, 400, WIDTH, 300, BLUE]],
    "grass":
    [[0,0]],
    "minions":
    [[WIDTH+randint(50,150), 400+randint(10,290), 20, 20, YELLOW],
    [WIDTH+randint(250,350), 400+randint(10,290), 20, 20, YELLOW],
    [WIDTH+randint(450,550), 400+randint(10,290), 20, 20, YELLOW],
    [WIDTH+randint(650,750), 400+randint(10,290), 20, 20, YELLOW],
    [WIDTH+randint(850,950), 400+randint(10,290), 20, 20, YELLOW],
    [WIDTH+randint(1050,1150), 400+randint(10,290), 20, 20, YELLOW]]
    }