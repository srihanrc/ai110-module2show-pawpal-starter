class PetOwner:
    """Stores the owner of pets information and time constraints."""
    
    def __init__(self, name, daily_hours, years_experience):
        self.name = name
        self.daily_hours = daily_hours
        self.years_experience = years_experience
    
    def getName(self):
        pass
    
    def get_available_time(self):
        pass
    
    def check_experience(self):
        pass


class Pet:
    """Stores all pet information and special needs."""
    
    def __init__(self, name, speciesType, foodType, list_special_needs):
        self.name = name
        self.speciesType = speciesType
        self.foodType = foodType
        self.list_special_needs = list_special_needs
    
    def getName(self):
        pass
    
    def getType(self):
        pass
    
    def getFoodType(self):
        pass
    
    def special_needs(self):
        pass


class Task:
    """Stores all task details for pet care activities."""
    
    def __init__(self, time, priorTasks):
        self.time = time
        self.priorTasks = priorTasks
    
    def time_duration(self):
        pass
    
    def pet_priority(self):
        pass


class Scheduler:
    """Generates the daily plan for pets by prioritizing tasks within time constraints."""
    
    def __init__(self, owner, pet, prior_tasks, time_avail):
        self.owner = owner
        self.pet = pet
        self.prior_tasks = prior_tasks
        self.time_avail = time_avail
    
    def priority_tasks(self):
        pass
    
    def schedule_tasks(self):
        pass
    
    def generate_plan(self):
        pass
