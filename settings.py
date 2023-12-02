class Settings:
    drumDiameter = 22
    drumThickness = 1.1
    drumFootThickness = drumThickness + 0.4
    drumNeedleCount = 134
    drumFloorHeight = 2.0
    camAngle = 53

    # ramp=(rampangle*120/Csize)-3;
    @classmethod
    def ramp(self):
        return (self.camAngle*120/(self.drumDiameter*10))-3

