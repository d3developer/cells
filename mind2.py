import random,cells

class AgentMind:
  def __init__(self):
    self.my_plant = None
    self.mode = 1
    self.target_range = random.randrange(50,200)
    pass

  def act(self,view,msg):
    x_sum = 0
    y_sum = 0
    dir = 1
    n = len(view.get_plants())
    mp = (mx,my)=view.get_me().get_pos()
    me = view.get_me()
    for a in view.get_agents():
      if (a.get_team()!=me.get_team()):
        return cells.Action(cells.ActionType.ATTACK,a.get_pos())

    for m in msg.get_messages():
      if (random.random()>0.6) and self.my_plant:
        self.mode = 5
        (tx,ty) = m
        self.target = (tx+random.randrange(-3,4),ty+random.randrange(-3,4))

    if(n>0):
      if (not self.my_plant):
        self.my_plant = view.get_plants()[0]
      elif self.my_plant.get_eff()<view.get_plants()[0].get_eff():
        self.my_plant = view.get_plants()[0]

    if self.mode == 5:
      dist = max(abs(mx-self.target[0]),abs(my-self.target[1]))
      self.target_range = max(dist,self.target_range)
      if view.get_me().get_energy() > dist*1.5:
        self.mode = 6 

    if self.mode == 6:
      dist = max(abs(mx-self.target[0]),abs(my-self.target[1]))
      if dist > 4:
        return cells.Action(cells.ActionType.MOVE,self.target)
      else:
        self.my_plant = None
        self.mode = 0

    if (view.get_me().get_energy() < self.target_range) and (view.get_energy().get(mp) > 0):
      return cells.Action(cells.ActionType.EAT)

    if self.my_plant:
      dist = max(abs(mx-self.my_plant.get_pos()[0]),abs(my-self.my_plant.get_pos()[1])) 
      if view.get_me().get_energy() < dist*1.5:
        (mx,my) = self.my_plant.get_pos()
        return cells.Action(cells.ActionType.MOVE,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
      if (random.random()>0.9999):
        (mx,my) = self.my_plant.get_pos()
        msg.send_message((my,mx)) 

    if (random.random()>0.9):
      return cells.Action(cells.ActionType.SPAWN,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
    else:
      return cells.Action(cells.ActionType.MOVE,(mx+random.randrange(-1,2),my+random.randrange(-1,2)))
