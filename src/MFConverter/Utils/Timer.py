import time

def sec2timerstr(sec)->str:
    h = sec//3600 
    m = (sec-h)//60
    s = (sec-h-m)
    return 'h='+str(h)+', m='+str(m)+', s='+str(s)

class timerClass():
    start_time : float  
    
    def start(self):
        self.start_time = time.time()
        self.lap_time = 0   
        
    def lap(self) -> float:      
        return time.time() - self.start_time
    
    def stop(self) -> float:
        result = self.lap()
        self.start_time =0
        self.lap_time = 0
        return result
    