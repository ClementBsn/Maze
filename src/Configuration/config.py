""" Description of the configuration of all cell of the maze """

CONFIG = {
    "enemy" : {"p_enemy" : 0.7}, # probability for the player to win, if not he dies
    "trap" : {"p_die" : 0.1, "p_restart" : 0.3}, # probability for the player to die, or restart, if not player continues
}
