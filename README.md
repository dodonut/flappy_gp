![screen-gif](./screen_rec.gif)

# flappy_gp

## Description
Flappy bird game using genetic programming. The population are randomly initialized, and the bird who gone the fardest is the one to populate the next gen. A little probabilistic mutation is added and all the config can be seen in config.txt file. The objective is to learn how to play the game by itself. 


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