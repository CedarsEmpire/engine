# CEDARS EMPIRE - BIG ENGINE
# 1 Big Engine = 5 Sub-Engines
# 100 AI Workers = 20 per Sub-Engine
# Features: Register, Deposit ON/OFF, Task, Withdraw, Referral

import time, random, uuid
from dataclasses import dataclass, field
from datetime import datetime

# ============ AI WORKER ============
@dataclass
class AIWorker:
    id: str
    region: str
    engine_id: int
    status: str = "Idle"
    tasks_done: int = 0
    earned: float = 0.0
    confidence: int = 0

    def do_task(self):
        """One worker does one task live"""
        task_types = ["Image Label", "Audio Transcription", "AI Rating", "Data Capture", "Text Review"]
        task = random.choice(task_types)
        self.status = f"Working: {task}"
        self.confidence = random.randint(95, 99)
        time.sleep(0.05)  # Simulate work
        reward = round(random.uniform(0.30, 0.75), 2)
        self.tasks_done += 1
        self.earned += reward
        self.status = "Done"
        return {
            "worker_id": self.id,
            "region": self.region,
            "task": task,
            "confidence": self.confidence,
            "reward": reward,
            "time": datetime.now().strftime("%H:%M:%S")
        }

# ============ SUB-ENGINE ============
@dataclass
class SubEngine:
    id: int
    name: str  # Africa, Asia, America, Europe, Oceania
    is_on: bool = True
    workers: list = field(default_factory=list)

    def __post_init__(self):
        # Create exactly 20 workers per sub-engine
        for i in range(1, 21):
            wid = f"W-{self.id:02d}-{i:03d}"
            self.workers.append(AIWorker(id=wid, region=self.name, engine_id=self.id))

    def toggle(self, on: bool):
        self.is_on = on
        status = "ON - UNLOCKED" if on else "OFF - LOCKED"
        print(f"[{self.name} Engine] -> {status}")
        return self.is_on

    def run_cycle(self):
        """Run all 20 workers if engine is ON"""
        if not self.is_on:
            return []
        results = []
        for w in self.workers:
            # Only some workers work per cycle to look live
            if random.random() < 0.3:
                results.append(w.do_task())
        return results

    def stats(self):
        return {
            "engine": self.name,
            "is_on": self.is_on,
            "workers": len(self.workers),
            "tasks_done": sum(w.tasks_done for w in self.workers),
            "earned": round(sum(w.earned for w in self.workers), 2)
        }

# ============ BIG ENGINE ============
class CedarsBigEngine:
    def __init__(self):
        self.name = "CEDARS BIG ENGINE - MASTER ENGINE"
        self.is_running = True
        self.ai_target = 2500.0
        self.total_earned = 0.0
        self.users = {}  # email -> user dict
        self.deposit_enabled = True  # Deposit ON/OFF - Admin controls

        # 5 Sub-Engines as planned
        self.sub_engines = [
            SubEngine(id=1, name="Africa", is_on=True),
            SubEngine(id=2, name="Asia", is_on=True),
            SubEngine(id=3, name="America", is_on=False),
            SubEngine(id=4, name="Europe", is_on=True),
            SubEngine(id=5, name="Oceania", is_on=False),
        ]
        print(f"✅ {self.name} STARTED")
        print(f"✅ Total Workers: {self.total_workers()} (20 x 5)")

    def total_workers(self):
        return sum(len(e.workers) for e in self.sub_engines)

    # ---- REGISTER ----
    def register(self, email, password, referrer_code=None):
        if email in self.users:
            return {"error": "User already exists"}
        ref_code = str(uuid.uuid4())[:8].upper()
        user = {
            "email": email,
            "password": password,
            "deposit_balance": 0.0,
            "earned": 0.0,
            "referral_code": ref_code,
            "referral_earnings": 0.0,
            "referred_by": referrer_code,
            "created": datetime.now().isoformat()
        }
        self.users[email] = user
        # Pay referrer 10% bonus logic
        if referrer_code:
            for u in self.users.values():
                if u["referral_code"] == referrer_code:
                    u["referral_earnings"] += 5.0
                    print(f"🎁 Referral: {u['email']} earned €5 from {email}")
        print(f"✅ Registered: {email} | Referral Code: {ref_code}")
        return user

    # ---- DEPOSIT ----
    def set_deposit(self, on: bool):
        self.deposit_enabled = on
        print(f"Deposit is now {'ON' if on else 'OFF'}")
        return self.deposit_enabled

    def deposit(self, email, amount):
        if not self.deposit_enabled:
            return {"error": "Deposit is OFF"}
        if email not in self.users:
            return {"error": "User not found"}
        self.users[email]["deposit_balance"] += amount
        print(f"💰 Deposit: {email} +€{amount} | Balance: €{self.users[email]['deposit_balance']}")
        return self.users[email]

    # ---- TASK ----
    def run_tasks(self, cycles=1):
        """Run live tasks across all ON engines"""
        all_results = []
        for _ in range(cycles):
            for engine in self.sub_engines:
                results = engine.run_cycle()
                all_results.extend(results)
                for r in results:
                    self.total_earned += r["reward"]
        return all_results

    # ---- WITHDRAW ----
    def withdraw(self, email, amount):
        if email not in self.users:
            return {"error": "User not found"}
        user = self.users[email]
        available = user["deposit_balance"] + user["earned"] + user["referral_earnings"]
        if amount > available:
            return {"error": f"Insufficient. Available: €{available}"}
        user["deposit_balance"] -= amount
        print(f"💸 Withdraw: {email} -€{amount} | Crypto Payout Sent")
        return {"success": True, "withdrawn": amount, "remaining": user["deposit_balance"]}

    # ---- REFERRAL ----
    def referral_info(self, email):
        user = self.users.get(email)
        if not user:
            return {"error": "User not found"}
        return {
            "your_code": user["referral_code"],
            "link": f"https://cedarsempire.com/register?ref={user['referral_code']}",
            "referral_earnings": user["referral_earnings"]
        }

    def dashboard(self):
        print("\n========== CEDARS EMPIRE DASHBOARD ==========")
        print(f"Big Engine: {'RUNNING' if self.is_running else 'STOPPED'}")
        print(f"AI Workers Online: {self.total_workers()}")
        print(f"Earned Today: €{self.total_earned:.2f} / €{self.ai_target} ({self.total_earned/self.ai_target*100:.1f}%)")
        print(f"Deposit: {'ON' if self.deposit_enabled else 'OFF'}")
        for e in self.sub_engines:
            s = e.stats()
            print(f" - Sub-Engine {e.id} {s['engine']}: {'ON' if s['is_on'] else 'OFF'} | Workers: {s['workers']} | Tasks: {s['tasks_done']} | Earned: €{s['earned']}")
        print("=============================================\n")

# ============ RUN LIVE ============
if __name__ == "__main__":
    engine = CedarsBigEngine()

    # Test the 5 components
    engine.register("admin@cedars.com", "1234")
    engine.register("user1@test.com", "1234", referrer_code=engine.users["admin@cedars.com"]["referral_code"])
    engine.deposit("admin@cedars.com", 100)
    engine.dashboard()

    # LIVE LOOP - Workers work forever
    print("🤖 AI Workers are now LIVE... Press Ctrl+C to stop")
    try:
        while True:
            results = engine.run_tasks(cycles=1)
            for r in results[:3]:  # Show 3 per cycle
                print(f"✅ {r['worker_id']} | {r['region']} | {r['task']} | Conf {r['confidence']}% | +€{r['reward']}")
            time.sleep(4)
            if random.random() < 0.2:
                engine.dashboard()
    except KeyboardInterrupt:
        print("\nEngine Stopped")
        engine.dashboard()
