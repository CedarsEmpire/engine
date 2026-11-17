# engine/targets.py
class Targets:
    AI_DAILY_TARGET = 2500  # €2500 for AI workers every 24h
    HUMAN_VERIFICATION_REWARD = 15  # €15 per human task

    def __init__(self, region):
        self.region = region
        self.enabled = False  # enable/disable switch per region

    def enable_region(self):
        self.enabled = True

    def disable_region(self):
        self.enabled = False
