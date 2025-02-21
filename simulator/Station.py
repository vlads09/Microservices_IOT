import random


class Station:
    def __init__(self, name):
        self.name = name
        self.battery = 100
        self.humidity = random.uniform(30, 70)
        self.temperature = random.uniform(15, 25)

    def get_values(self):
        self.battery -= random.uniform(0.05, 0.2)
        self.battery = max(self.battery, 0)

        self.humidity += random.uniform(-0.5, 0.5)
        self.humidity = max(0, min(self.humidity, 100))

        self.temperature += random.uniform(-0.2, 0.2)
        self.temperature = max(-20, min(self.temperature, 50))

        return {
            "BAT": round(self.battery, 2),
            "HUMID": round(self.humidity, 2),
            "TMP": round(self.temperature, 2)
        }
        