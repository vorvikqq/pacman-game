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

