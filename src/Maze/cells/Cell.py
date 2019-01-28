class Cell():
    """
    Definition of the mother class Cell that describes a room in the maze
    """

    def __init__(self, x, y, type, id, symbole):
        """ Constructor """
        self.type = type            # the type of the cell
        self.x = x                  # the x coordinate
        self.y = y                  # the y coordinate
        self.id = id                # the id of the cell
        self.symbole = symbole      # the symbole of the cell to print

    def __str__(self):
        """
        Method to convert the object into string
        """
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        return str(self.type)+" cell "+str(self.id)+" at ("+str(alphabet[self.x])+", "+str(alphabet[self.y])+")"
