import time
import sys
from unitree_sdk2py.core.channel import ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.default import unitree_go_msg_dds__SportModeState_
from unitree_sdk2py.idl.unitree_go.msg.dds_ import SportModeState_
from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
import math
from dataclasses import dataclass

#This script will be used to manipulate the robot

@dataclass
class TestOption:
    name: str
    id: int

option_list = [
    TestOption(name="damp", id=0),         
    TestOption(name="Squat2StandUp", id=1),     
    TestOption(name="StandUp2Squat", id=2),   
    TestOption(name="move forward", id=3),         
    TestOption(name="move lateral", id=4),    
    TestOption(name="move rotate", id=5),  
    TestOption(name="low stand", id=6),  
    TestOption(name="high stand", id=7),    
    TestOption(name="zero torque", id=8),
    TestOption(name="wave hand1", id=9), # wave hand without turning around
    TestOption(name="wave hand2", id=10), # wave hand and trun around  
    TestOption(name="shake hand", id=11),     
    TestOption(name="Lie2StandUp", id=12),     
]

class UserInterface:
    def __init__(self):
        self.test_option_ = None

    def convert_to_int(self, input_str):
        try:
            return int(input_str)
        except ValueError:
            return None

    def terminal_handle(self):
        input_str = input("Enter id or name: \n")

        if input_str == "list":
            self.test_option_.name = None
            self.test_option_.id = None
            for option in option_list:
                print(f"{option.name}, id: {option.id}")
            return

        for option in option_list:
            if input_str == option.name or self.convert_to_int(input_str) == option.id:
                self.test_option_.name = option.name
                self.test_option_.id = option.id
                print(f"Test: {self.test_option_.name}, test_id: {self.test_option_.id}")
                return

        print("No matching test option found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} networkInterface")
        sys.exit(-1)

    print("WARNING: Please ensure there are no obstacles around the robot while running this example.")
    input("Press Enter to continue...")

    ChannelFactoryInitialize(0, sys.argv[1])

    test_option = TestOption(name=None, id=None) 
    user_interface = UserInterface()
    user_interface.test_option_ = test_option

    sport_client = LocoClient()  #Consider adding the Start() method somewhere in the code to start the client (as mentioned in https://robonomics.network/blog/first-two-weeks-with-unitree-humanoid-robot/)
    sport_client.SetTimeout(10.0)
    sport_client.Init()

    print("Input \"list\" to list all test option ...")
    while True:
        user_interface.terminal_handle()

        print(f"Updated Test Option: Name = {test_option.name}, ID = {test_option.id}")

        if test_option.id == 0:
            sport_client.Damp()
        elif test_option.id == 1:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Squat2StandUp()
        elif test_option.id == 2:
            sport_client.StandUp2Squat()
        elif test_option.id == 3:
            sport_client.Move(0.3,0,0)
        elif test_option.id == 4:
            sport_client.Move(0,0.3,0)
        elif test_option.id == 5:
            sport_client.Move(0,0,0.3)
        elif test_option.id == 6:
            sport_client.LowStand()
        elif test_option.id == 7:
            sport_client.HighStand()
        elif test_option.id == 8:
            sport_client.ZeroTorque()
        elif test_option.id == 9:
            sport_client.WaveHand()
        elif test_option.id == 10:
            sport_client.WaveHand(True)
        elif test_option.id == 11:
            sport_client.ShakeHand()
            time.sleep(3)
            sport_client.ShakeHand()
        elif test_option.id == 12:
            sport_client.Damp()
            time.sleep(0.5)
            sport_client.Lie2StandUp() # When using the Lie2StandUp function, ensure that the robot faces up and the ground is hard, flat and rough.

        time.sleep(1)

# --get_fsm_id           : Get the current FSM (Finite State Machine) ID of the upper controller
# --get_fsm_mode         : Get the current FSM mode of the upper controller
# --get_phase            : Get the current phase of the robot's movement cycle

# --set_fsm_id 1         : Set the FSM state (e.g., to initiate a motion behavior)

# --set_velocity         : Set movement speed [vx vy omega duration]
#                          Example: "0.5 0 0 1" → forward 0.5 m/s for 1 sec

# Basic Motion Commands
# --damp                 : Enter damping mode (resist motion softly)
# --start                : Enter main movement control (enables motion system)
# --squat                : Lower into squat position
# --sit                  : Sit down
# --stand_up            : Stand up to default posture
# --zero_torque          : Enter zero-torque mode (motors off)
# --stop_move            : Stop current movement
# --high_stand           : Stand tall
# --low_stand            : Stand lower
# --balance_stand        : Stand with balance control activated

# Advanced Gait Options
# --continous_gait true  : Enable continuous gait mode
# --switch_move_mode true: Switch between different movement modes
# --move                 : Move at specific velocity [vx vy omega]
#                          Example: "0.5 0 0" → walk forward
# --set_speed_mode N     : Set maximum speed mode: 0 / 1 / 2 / 3