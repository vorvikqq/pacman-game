from constants import *

class DefaultMode():
    def __init__(self, start_mode = WAIT):  
        self.timer = 0
        self.mode = None
        self.set_mode(start_mode)

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.time:
            if self.mode == WAIT:
                self.scatter()
            elif self.mode == SCATTER:
                self.chase()
            elif self.mode == CHASE:
                self.scatter()

            elif self.mode == RANDOM:
                self.scatter()
                
            elif self.mode == FREIGHT:
                self.scatter()

            elif self.mode == SPAWN:
                self.wait()
    
    def reset_mode(self):
        """Повертає привида в стандартний режим (CHASE або SCATTER)"""
        # Якщо привид зараз в режимі FREIGHT або іншому режимі, повертаємо до SCATTER або CHASE
        if self.mode.current_mode == FREIGHT:
            # Можна обрати між SCATTER та CHASE, залежно від поточної ситуації
            self.mode.set_mode(SCATTER)  # або CHASE, якщо треба
        elif self.mode.current_mode == WAIT:
            self.mode.set_mode(SCATTER)  # можна за умовами гри встановити інший початковий режим

    def normal_mode(self):
        """Відновлює нормальну швидкість та режим для привида"""
        # Встановлюємо стандартну швидкість привида, наприклад, 100
        self.speed = self.set_speed(100)

        # Визначаємо метод руху залежно від поточного режиму
        self.update_move_method()

    def set_mode(self, mode):  
        if mode == SCATTER:
            self.scatter()
        elif mode == CHASE:
            self.chase()
        elif mode == WAIT:
            self.wait()
        elif mode == RANDOM:
            self.random()
        elif mode == FREIGHT:
            self.freight()
        elif mode == SPAWN:
            self.spawn()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

    def wait(self):
        self.mode = WAIT
        self.time = 3
        self.timer = 0

    def random(self):
        self.mode = RANDOM
        self.time = 10
        self.timer = 0
    
    def freight(self):
        self.mode = FREIGHT
        self.time = 7
        self.timer = 0

    def spawn(self):
        self.mode = SPAWN
        self.time = 5  
        self.timer = 0

    

class ModeController():
    def __init__(self, ghost, start_mode = WAIT):
        self.time = 0
        self.timer = 0
        self.main_mode = DefaultMode(start_mode)
        self.current_mode = self.main_mode.mode
        self.ghost = ghost

    def update(self, dt):
        self.main_mode.update(dt)
        self.current_mode = self.main_mode.mode  
        self.ghost.update_move_method()

        if self.current_mode == SPAWN and self.ghost.node.position == self.ghost.home_goal:
            self.main_mode.set_mode(WAIT)

        if self.current_mode is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.ghost.normal_mode()
                self.current_mode = self.main_mode.mode
        else:
            self.current_mode =  self.main_mode.mode
            

    def set_mode(self, mode):
        """Динамічно змінює режим привида"""
        self.main_mode.set_mode(mode)
        self.current_mode = self.main_mode.mode  # Оновлюємо поточний режим
        self.ghost.update_move_method()  # Оновлюємо метод руху відповідно до нового режиму

    def set_freight_mode(self):
        """Вмикає режим страху (FREIGHT), якщо привид у SCATTER або CHASE"""
        if self.current_mode in [SCATTER, CHASE]:  
            self.timer = 0
            self.time = 7
            self.set_mode(FREIGHT)
        elif self.current_mode is FREIGHT:
            self.timer = 0