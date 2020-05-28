"""
physical process

Water Tank has an inflow pipe and outflow pipe, both are modeled according
to the equation of continuity from the domain of hydraulics
(pressurized liquids) and a drain orefice modeled using the Bernoulli's
principle (for the trajectories).
"""


from minicps.devices import Tank

from utils import PUMP_FLOWRATE_IN, PUMP_FLOWRATE_OUT
from utils import TANK_SECTION
from utils import LIT_101_M, RWT_INIT_LEVEL
from utils import STATE, PP_PERIOD_SEC, PP_PERIOD_HOURS

import time


# SPHINX_SWAT_TUTORIAL TAGS(
MV001 = ('MV001', 0)
P201 = ('P201', 2)
LIT101 = ('LIT101', 1)
FIT101 = ('FIT101', 1)
# SPHINX_SWAT_TUTORIAL TAGS)


# TODO: implement orefice drain with Bernoulli/Torricelli formula
class WaterTank(Tank):

    def pre_loop(self):

        # SPHINX_SWAT_TUTORIAL STATE INIT(
        self.set(MV001, 1)
        self.set(P201, 2)
        self.level = self.set(LIT101, 0.500)
        # SPHINX_SWAT_TUTORIAL STATE INIT)

    def main_loop(self):

        while True: # Do not stop the flow of water 
            new_level = self.level

            # compute water volume
            water_volume = self.section * new_level

            # inflows volumes
            mv001 = int(self.get(MV001))
            if mv001 == 1:
                inflow = PUMP_FLOWRATE_IN * PP_PERIOD_HOURS
                print("[DEBUG] Water Tank inflow ")
                water_volume += inflow
            else:
                pass

            # outflows volumes
            p201 = int(self.get(P201))
            if p201 == 1:
                outflow = PUMP_FLOWRATE_OUT * PP_PERIOD_HOURS
                print("[DEBUG] Water Tank outflow ")
                water_volume -= outflow
            else:
                pass

            # compute new water_level
            new_level = water_volume / self.section

            # level cannot be negative
            if new_level <= 0.0:
                new_level = 0.0

            # update internal and state water level
            print("[DEBUG] New level: %.5f \t delta: %.5f" % (new_level, new_level - self.level))
            self.level = self.set(LIT101, new_level)

            # TODO add more warnings
            if new_level >= LIT_101_M['HH']:
                print('[DEBUG] Water Tank above Highest limit: ', LIT_101_M['HH'])
                #break

            # TODO underflow
            elif new_level <= LIT_101_M['LL']:
                print('[DEBUG] Water Tank below Lowest limit: ', LIT_101_M['LL'])
                #break

            time.sleep(PP_PERIOD_SEC)


if __name__ == '__main__':

    wt = WaterTank(
        name='rwt',
        state=STATE,
        protocol=None,
        section=TANK_SECTION,
        level=RWT_INIT_LEVEL
    )
