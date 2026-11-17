# engine/real_engine.py
import targets
import task_engine
import payout_logic
import central_hub

class EngineFive:
    def __init__(self):
        self.regions = [1,2,3,4,5]
        self.ai_target = targets.Targets.AI_DAILY_TARGET  # €2500
        self.human_reward = targets.Targets.HUMAN_VERIFICATION_REWARD  # €15
        self.region_status = {r: False for r in self.regions}

    def enable_region(self, region):
        if region in self.regions:
            self.region_status[region] = True
            central_hub.update_region(region, True)

    def disable_region(self, region):
        if region in self.regions:
            self.region_status[region] = False
            central_hub.update_region(region, False)

    def process_task(self, task_type, client):
        # AI + human flow in task_engine.py
        task_engine.process(task_type, client)

    def payout(self, worker):
        # Crypto payout in payout_logic.py
        return payout_logic.payout_crypto(worker)

    def get_region_status(self):
        return self.region_status
