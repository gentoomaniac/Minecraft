class Config():
    _instance = None
    
    # app information
    APP_NAME = u'PyCraft'
    APP_VERSION = u'0.1'
    
    def __init__(self):
        if Config._instance is not None:
            return _instance
        self.configSettings = {}
        self.configSettings['screenHight'] = 800
        self.configSettings['screenWidth'] = 600
        self.configSettings['resizeable'] = True
        self.configSettings['walkingSpeed'] = 5
        self.configSettings['flyingSpeed'] = 10
        self.configSettings['gravity'] = 5
        self.configSettings['playerHight'] = 2

    def getConfValue(self, key):
        if key in self.configSettings.keys():
             return self.configSettings[key]
        else:
             raise Exception("Setting not found!")