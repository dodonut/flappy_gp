![screen-gif](./screen_rec.gif)

# flappy_gp

## Description
Flappy bird game using genetic programming. The population are randomly initialized, and the bird who gone the fardest is the one to populate the next gen. 

A little probabilistic mutation is added and all the config can be seen in config.txt file. The objective is to learn how to play the game by itself. 

When the population extincts, a new generation is formed based on the best fit bird. When she learn how to play, she'll never make a mistake! (I guess)

## How it works
The initial population are randomly initialized, and the bird who gone the fardest is the one to populate the next gen. One of the tubes height is randomly generated and the counterpart is X pixels of distance from the first one. The current value of X, is the lowest that I put and the bird learned how to pass through. A value lower than this, with the jump phisics, is not possible to traverse it. A little probabilistic mutation is added and all the config can be seen in config.txt file. 

## Tested with python 3.x and pip 21.x
### Dependencies:
- pygame: 
```
pip install pygame
```
- neat: 
```
pip install neat-python
```


## To run
    ```
    python main.py
    ```


### TODO
- add other types of obstacles and actions for the bird to decide when and where to use them. 
