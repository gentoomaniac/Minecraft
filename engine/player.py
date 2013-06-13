import json

class Player(object):
    """ This class defines a player including the state, position etc. """
    
    def __init__(self):
        # player position in the gameworld
        self.position = (0, 0, 0)
        
        # player name
        self.name = "Player"
        
        # player life
        self.life = 100
        
        # player maximum life
        self.maxLife = 100
 
        # A list of blocks the player can place. Hit num keys to cycle.
        self.inventory = []
        
        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)
        
        # When flying gravity has no effect and speed is increased.
        self.flying = False
                
        # is player crouched or normal standing?
        self.isCrouch = False
        
        
    def toJson(self):
        out = {
            'name': self.name,
            'life': self.life,
            'maxlife': self.maxLife,
            'position': list(self.position),
            'inventory': self.inventory,
            'rotation': list(self.rotation),
            'flying': self.flying
        }
        
        return json.dumps(out)
    
    def fromJson(self, data):
        obj = json.loads(data)
        self.name = obj['name']
        self.life = obj['life']
        self.maxLife = obj['maxlife']
        self.position = tuple(obj['position'])
        self.inventory = list(obj['inventory'])
        self.rotation = tuple(obj['rotation'])
        self.flying = obj['flying']