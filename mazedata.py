from constants import * 

class MazeBase:
  def __init__(self) -> None:
    self.portal_pairs = {}
    self.home_offset = (0,0)
    self.ghost_node_deny = {UP:(), DOWN:(), LEFT:(), RIGHT:()}
  
  def set_portal_pairs(self, nodes):
    for pair in list(self.portal_pairs.values()):
      nodes.setPortalPair(*pair)

  def connect_home_nodes(self, nodes):
    key = nodes.createHomeNodes(*self.home_offset)
    nodes.connectHomeNodes(key, self.home_node_connect_left, LEFT)
    nodes.connectHomeNodes(key, self.home_node_connect_right, RIGHT)

  def add_offset(self, x,y):
    return x + self.home_offset[0], y + self.home_offset[1]
  
  def deny_ghosts_access(self, ghosts, nodes):
    nodes.denyAccessList(*(self.add_offset(2,3) + (LEFT,ghosts)))
    nodes.denyAccessList(*(self.add_offset(2,3) + (RIGHT,ghosts)))

    for direction in list(self.ghost_node_deny.keys()):
      for values in self.ghost_node_deny[direction]:
        nodes.denyAccessList(*(values + (direction, ghosts)))


class Maze1(MazeBase):
  def __init__(self) -> None:
    super().__init__(self)
    self.name = "maze1"
    self.portal_pairs =  {0:((0, 17), (27, 17))}
    self.home_offset = (11.5, 14)
    self.home_node_connect_left = (12, 14)
    self.home_node_connect_right = (15, 14)
    self.pacman_start = (15, 26)
    self.fruit_start = (9, 20)
    self.ghost_node_deny =  {UP:((12, 14), (15, 14), (12, 26), (15, 26)), LEFT:(self.add_offset(2, 3),),
                              RIGHT:(self.add_offset(2, 3),)}
    
class Maze2(MazeBase):
    def __init__(self):
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portal_pairs = {0:((0, 4), (27, 4)), 1:((0, 26), (27, 26))}
        self.home_offset = (11.5, 14)
        self.home_node_connect_left = (9, 14)
        self.home_node_connect_right = (18, 14)
        self.pacman_start = (16, 26)
        self.fruit_start = (11, 20)
        self.ghost_node_deny = {UP:((9, 14), (18, 14), (11, 23), (16, 23)), LEFT:(self.add_offset(2, 3),),
                              RIGHT:(self.add_offset(2, 3),)}
        