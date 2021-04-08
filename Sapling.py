class Sapling:

    def __init__(self, height, tag):
        self.growth_over_time = []
        self.height = height
        self.tag = tag
        self.add_growth(height)

    """ 
    * Name: add_growth
    * Inputs: self, float 
    * Return: None
    * Purpose: add new growth to list
    """
    def add_growth(self, height):
        self.growth_over_time.append(height)

    """ 
    * Name: get_growth
    * Inputs: self
    * Return: list
    * Purpose: return list
    """
    def get_growth(self):
        return self.growth_over_time

    """ 
    * Name: remove_grwoth
    * Inputs: self, height
    * Return: None
    * Purpose: remove height from grow_over_time
    """
    def remove_growth(self, height):
        self.growth_over_time.remove(height)

    """ 
    * Name: add_tag
    * Inputs: self, int 
    * Return: None
    * Purpose: add new tag to sapling
    """
    def add_tag(self, tag):
        self.tag = tag

    """ 
    * Name: get_tag
    * Inputs: self 
    * Return: tag
    * Purpose: return tag value
    """
    def get_tag(self):
        return self.tag

    """ 
    * Name: add_height
    * Inputs: self, height
    * Return: None
    * Purpose: Set height value
    """
    def add_height(self, height):
        self.height = height

    """ 
    * Name: get_height
    * Inputs: self
    * Return: height value
    * Purpose: get the height of specific sapling
    """
    def get_latest_height(self):
        return float(self.growth_over_time[-1])
