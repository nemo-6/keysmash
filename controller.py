#!/usr/bin/env python3

# Interfaces the libraries pygame for our convenience.
# Basically an events manager.


import pygame
import serial
import threading


class Controller:
    """Model representation of a gamecube controller."""

    # default values
    STICK_MIDDLE = 0b10000000

    STICK_LEFT = 0b00000000
    STICK_RIGHT = 0b11111111
    STICK_UP = 0b11111111
    STICK_DOWN = 0b00000000

    TRIGGER_DOWN = 0b00000000  # verify
    TRIGGER_UP = 0b11111111  # verify

    # BYTE 0
    BUTTON_START = 0b00001000
    BUTTON_Y = 0b00010000
    BUTTON_X = 0b00100000
    BUTTON_B = 0b01000000
    BUTTON_A = 0b10000000

    # BYTE 1
    BUTTON_L = 0b00000010
    BUTTON_R = 0b00000100
    BUTTON_Z = 0b00001000
    BUTTON_D_UP = 0b00010000
    BUTTON_D_DOWN = 0b00100000
    BUTTON_D_RIGHT = 0b01000000
    BUTTON_D_LEFT = 0b10000000

    # buttons down (saves cycles)
    BUTTON_START_DOWN = ~BUTTON_START
    BUTTON_Y_DOWN = ~BUTTON_Y
    BUTTON_X_DOWN = ~BUTTON_X
    BUTTON_B_DOWN = ~BUTTON_B
    BUTTON_A_DOWN = ~BUTTON_A
    BUTTON_L_DOWN = ~BUTTON_L
    BUTTON_R_DOWN = ~BUTTON_R
    BUTTON_Z_DOWN = ~BUTTON_Z
    BUTTON_D_UP_DOWN = ~BUTTON_D_UP
    BUTTON_D_DOWN_DOWN = ~BUTTON_D_DOWN
    BUTTON_D_RIGHT_DOWN = ~BUTTON_D_RIGHT
    BUTTON_D_LEFT_DOWN = ~BUTTON_D_LEFT

    # BYTE 2
    # STICK_X = 0X00  # unused

    # BYTE 3
    # stick_y = 0x00  # unused

    # BYTE 4
    # cstick_x = 0x00  # unused

    # BYTE 5
    # cstick_y = 0x00  # unused

    # BYTE 6
    # shoulder_l = 0x00  # unused

    # BYTE 7
    # shoulder_r = 0x00  # unused

    def __init__(self):
        self.button_state = [0b00000000,
                             0b00000001,  # this bit should be always 1
                             0b10000000,  # 10000000 = 128 (centered stick)
                             0b10000000,  # 10000000 = 128 (centered stick)
                             0b10000000,  # 10000000 = 128 (centered stick)
                             0b10000000,  # 10000000 = 128 (centered stick)
                             0b00000000,  # todo I don't know if the triggers start 0 or 255
                             0b00000000, ]

    def get_button_state(self):
        return self.button_state

    # regular binary buttons

    def button_start_press(self):
        self.button_state[0] |= Controller.BUTTON_START

    def button_start_release(self):
        self.button_state[0] &= Controller.BUTTON_START_DOWN

    def button_y_press(self):
        self.button_state[0] |= Controller.BUTTON_Y

    def button_y_release(self):
        self.button_state[0] &= Controller.BUTTON_Y_DOWN

    def button_x_press(self):
        self.button_state[0] |= Controller.BUTTON_X

    def button_x_release(self):
        self.button_state[0] &= Controller.BUTTON_X_DOWN

    def button_b_press(self):
        self.button_state[0] |= Controller.BUTTON_B

    def button_b_release(self):
        self.button_state[0] &= Controller.BUTTON_B_DOWN

    def button_a_press(self):
        self.button_state[0] |= Controller.BUTTON_A

    def button_a_release(self):
        self.button_state[0] &= Controller.BUTTON_A_DOWN

    def button_l_press(self):
        self.button_state[1] |= Controller.BUTTON_L

    def button_l_release(self):
        self.button_state[1] &= Controller.BUTTON_L_DOWN

    def button_r_press(self):
        self.button_state[1] |= Controller.BUTTON_R

    def button_r_release(self):
        self.button_state[1] &= Controller.BUTTON_R_DOWN

    def button_z_press(self):
        self.button_state[1] |= Controller.BUTTON_Z

    def button_z_release(self):
        self.button_state[1] &= Controller.BUTTON_Z_DOWN

    def button_d_up_press(self):
        self.button_state[1] |= Controller.BUTTON_D_UP

    def button_d_up_release(self):
        self.button_state[1] &= Controller.BUTTON_D_UP_DOWN

    def button_d_down_press(self):
        self.button_state[1] |= Controller.BUTTON_D_DOWN

    def button_d_down_release(self):
        self.button_state[1] &= Controller.BUTTON_D_DOWN_DOWN

    def button_d_right_press(self):
        self.button_state[1] |= Controller.BUTTON_D_RIGHT

    def button_d_right_release(self):
        self.button_state[1] &= Controller.BUTTON_D_RIGHT_DOWN

    def button_d_left_press(self):
        self.button_state[1] |= Controller.BUTTON_D_LEFT

    def button_d_left_release(self):
        self.button_state[1] &= Controller.BUTTON_D_LEFT_DOWN

    # sticks and shoulders

    # stick
    def stick_x_middle(self):
        self.button_state[2] = Controller.STICK_MIDDLE

    def stick_x_up(self):
        self.button_state[2] = Controller.STICK_UP

    def stick_x_down(self):
        self.button_state[2] = Controller.STICK_DOWN

    def stick_y_middle(self):
        self.button_state[3] = Controller.STICK_MIDDLE

    def stick_y_right(self):
        self.button_state[3] = Controller.STICK_RIGHT

    def stick_y_left(self):
        self.button_state[3] = Controller.STICK_LEFT

    # cstick
    def c_stick_x_middle(self):
        self.button_state[4] = Controller.STICK_MIDDLE

    def c_stick_x_up(self):
        self.button_state[4] = Controller.STICK_UP

    def c_stick_x_down(self):
        self.button_state[4] = Controller.STICK_DOWN

    def c_stick_y_middle(self):
        self.button_state[5] = Controller.STICK_MIDDLE

    def c_stick_y_right(self):
        self.button_state[5] = Controller.STICK_RIGHT

    def c_stick_y_left(self):
        self.button_state[5] = Controller.STICK_LEFT

    # triggers
    def trigger_right_press(self):
        self.button_state[6] = Controller.TRIGGER_DOWN

    def trigger_right_release(self):
        self.button_state[6] = Controller.TRIGGER_UP

    def trigger_left_press(self):
        self.button_state[7] = Controller.TRIGGER_DOWN

    def trigger_left_release(self):
        self.button_state[7] = Controller.TRIGGER_UP


class StickManager:
    """Manages the translation of keyboard input to stick movement input"""
    VECTOR_DOWN = 0
    VECTOR_UP = 1
    VECTOR_RIGHT = 0
    VECTOR_LEFT = 1

    def __init__(self, managed_controller: Controller):
        self.controller = managed_controller
        self.stick_x_vectors = [0, 0]  # DONW, UP
        self.stick_y_vectors = [0, 0]  # RIGHT, LEFT
        self.c_stick_x_vectors = [0, 0]  # DONW, UP
        self.c_stick_y_vectors = [0, 0]  # RIGHT, lEFT

    # stick X axis
    def up_key_press(self):
        self.stick_x_vectors[StickManager.VECTOR_UP] = 1
        self.controller.stick_x_up()

    def up_key_release(self):
        self.stick_x_vectors[StickManager.VECTOR_UP] = 0
        if self.stick_x_vectors[StickManager.VECTOR_DOWN]:
            self.controller.stick_x_down()
        else:
            self.controller.stick_x_middle()

    def down_key_press(self):
        self.stick_x_vectors[StickManager.VECTOR_DOWN] = 1
        self.controller.stick_x_down()

    def down_key_release(self):
        self.stick_x_vectors[StickManager.VECTOR_DOWN] = 0
        if self.stick_x_vectors[StickManager.VECTOR_UP]:
            self.controller.stick_x_up()
        else:
            self.controller.stick_x_middle()

    # stick Y axis
    def right_key_press(self):
        self.stick_y_vectors[StickManager.VECTOR_RIGHT] = 1
        self.controller.stick_y_right()

    def right_key_release(self):
        self.stick_y_vectors[StickManager.VECTOR_RIGHT] = 0
        if self.stick_y_vectors[StickManager.VECTOR_LEFT]:
            self.controller.stick_y_left()
        else:
            self.controller.stick_y_middle()

    def left_key_press(self):
        self.stick_y_vectors[StickManager.VECTOR_LEFT] = 1
        self.controller.stick_y_left()

    def left_key_release(self):
        self.stick_y_vectors[StickManager.VECTOR_LEFT] = 0
        if self.stick_y_vectors[StickManager.VECTOR_RIGHT]:
            self.controller.stick_y_right()
        else:
            self.controller.stick_y_middle()

    # c-stick X axis
    def c_up_key_press(self):
        self.c_stick_x_vectors[StickManager.VECTOR_UP] = 1
        self.controller.c_stick_x_up()

    def c_up_key_release(self):
        self.c_stick_x_vectors[StickManager.VECTOR_UP] = 0
        if self.c_stick_x_vectors[StickManager.VECTOR_DOWN]:
            self.controller.c_stick_x_down()
        else:
            self.controller.c_stick_x_middle()

    def c_down_key_press(self):
        self.c_stick_x_vectors[StickManager.VECTOR_DOWN] = 1
        self.controller.c_stick_x_down()

    def c_down_key_release(self):
        self.c_stick_x_vectors[StickManager.VECTOR_DOWN] = 0
        if self.c_stick_x_vectors[StickManager.VECTOR_UP]:
            self.controller.c_stick_x_up()
        else:
            self.controller.c_stick_x_middle()

    # c-stick Y axis
    def c_right_key_press(self):
        self.c_stick_y_vectors[StickManager.VECTOR_RIGHT] = 1
        self.controller.c_stick_y_right()

    def c_right_key_release(self):
        self.c_stick_y_vectors[StickManager.VECTOR_RIGHT] = 0
        if self.c_stick_y_vectors[StickManager.VECTOR_LEFT]:
            self.controller.c_stick_y_left()
        else:
            self.controller.c_stick_x_middle()

    def c_left_key_press(self):
        self.c_stick_y_vectors[StickManager.VECTOR_LEFT] = 1
        self.controller.c_stick_y_left()

    def c_left_key_release(self):
        self.c_stick_y_vectors[StickManager.VECTOR_LEFT] = 0
        if self.c_stick_y_vectors[StickManager.VECTOR_RIGHT]:
            self.controller.c_stick_y_right()
        else:
            self.controller.c_stick_y_middle()


# Interfaces library PySerial for our convenience.

class Broker:
    def __init__(self, port_name, controller_handle):
        self.running = True
        self.controller = controller_handle
        self.port = serial.Serial(port=port_name,
                                  baudrate=2000000,
                                  # bytesize=,
                                  # parity=serial.PARITY_NONE,
                                  # stopbits=serial.STOPBITS_ONE,
                                  # timeout=0.005,
                                  # xonxoff=False,
                                  # rtscts=False,
                                  # write_timeout=None,
                                  # dsrdtr=False,
                                  # inter_byte_timeout=None
                                  )
        print(f'Broker: successfully created port {self.port.name}.')

    def send_button_data(self):
        self.port.write(self.controller.get_button_state())
        # print(f'Broker: sending:{bytes_to_send}')

    def wait_for_question(self):
        x = self.port.read()  # reads one byte
        print(f"Broker: heard character << {x} >>.")

    def port_service(self):
        while self.running:
            self.wait_for_question()
            self.send_button_data()

    def stop(self):
        self.running = False
        self.port.close()


if __name__ == "__main__":
    running = True


    def cleanup_quit():
        print("Cleaning up and quitting...")
        global running  # gives access to "running", declared globally
        running = False


    # here we try to make it pretty
    print("Welcome to keysmash.")
    pygame.time.wait(100)
    print("Initializing virtual controller...")
    controller = Controller()
    pygame.time.wait(100)
    print("Initializing virtual sticks manager...")
    stick_manager = StickManager(controller)

    print("Initializing keymap...")
    key_map = {
        # start
        (pygame.KEYDOWN, pygame.K_KP_ENTER): controller.button_start_press,
        (pygame.KEYUP, pygame.K_KP_ENTER): controller.button_start_release,

        # y
        (pygame.KEYDOWN, pygame.K_y): controller.button_y_press,
        (pygame.KEYUP, pygame.K_y): controller.button_y_release,

        # x
        (pygame.KEYDOWN, pygame.K_x): controller.button_x_press,
        (pygame.KEYUP, pygame.K_x): controller.button_x_release,

        # b
        (pygame.KEYDOWN, pygame.K_b): controller.button_b_press,
        (pygame.KEYUP, pygame.K_b): controller.button_b_release,

        # a
        (pygame.KEYDOWN, pygame.K_a): controller.button_a_press,
        (pygame.KEYUP, pygame.K_a): controller.button_a_release,

        # l
        (pygame.KEYDOWN, pygame.K_l): controller.button_l_press,
        (pygame.KEYUP, pygame.K_l): controller.button_l_release,

        # r
        (pygame.KEYDOWN, pygame.K_r): controller.button_r_press,
        (pygame.KEYUP, pygame.K_r): controller.button_r_release,

        # z
        (pygame.KEYDOWN, pygame.K_z): controller.button_z_press,
        (pygame.KEYUP, pygame.K_z): controller.button_z_release,

        # stick!
        (pygame.KEYDOWN, pygame.K_UP): stick_manager.up_key_press,
        (pygame.KEYUP, pygame.K_UP): stick_manager.up_key_release,

        (pygame.KEYDOWN, pygame.K_DOWN): stick_manager.down_key_press,
        (pygame.KEYUP, pygame.K_DOWN): stick_manager.down_key_release,

        (pygame.KEYDOWN, pygame.K_LEFT): stick_manager.left_key_press,
        (pygame.KEYUP, pygame.K_LEFT): stick_manager.left_key_release,

        (pygame.KEYDOWN, pygame.K_RIGHT): stick_manager.right_key_press,
        (pygame.KEYUP, pygame.K_RIGHT): stick_manager.right_key_release,

        # c_stick!
        (pygame.KEYDOWN, pygame.K_UP): stick_manager.up_key_press,
        (pygame.KEYUP, pygame.K_UP): stick_manager.up_key_release,

        (pygame.KEYDOWN, pygame.K_DOWN): stick_manager.down_key_press,
        (pygame.KEYUP, pygame.K_DOWN): stick_manager.down_key_release,

        (pygame.KEYDOWN, pygame.K_LEFT): stick_manager.left_key_press,
        (pygame.KEYUP, pygame.K_LEFT): stick_manager.left_key_release,

        (pygame.KEYDOWN, pygame.K_RIGHT): stick_manager.right_key_press,
        (pygame.KEYUP, pygame.K_RIGHT): stick_manager.right_key_release,

        # L shoulder trigger
        # TODO

        # R shoulder trigger
        # TODO

        # quitting, the most important thing
        (pygame.KEYDOWN, pygame.K_ESCAPE): cleanup_quit
    }
    pygame.time.wait(100)

    # init a window to have the system's focus and capture user input.
    print("Initializing graphical user interface...")
    pygame.init()
    pygame._display_surf = pygame.display.set_mode((200, 200),
                                                   pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.time.wait(100)

    print("Sorting out events...")
    # block the events we don't care about
    pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.ACTIVEEVENT)
    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    pygame.event.set_blocked(pygame.JOYAXISMOTION)
    pygame.event.set_blocked(pygame.JOYBALLMOTION)
    pygame.event.set_blocked(pygame.JOYHATMOTION)
    pygame.event.set_blocked(pygame.JOYBUTTONUP)
    pygame.event.set_blocked(pygame.JOYBUTTONDOWN)
    pygame.event.clear()  # ?????
    pygame.time.wait(100)

    print("Initializing serial broker...")

    # start serving controller data through serial port.
    # We listen to one byte, and respond
    #  with controller.controller_data
    port_number = input('Broker: Please enter a port number: \n>>>')
    port_name = f"/dev/ttyUSB{port_number}"  # lol please don't kill me
    broker = Broker(port_name=port_name, controller_handle=controller)

    service_thread = threading.Thread(target=broker.port_service)
    print("Initializing broker service thread")
    service_thread.start()
    pygame.time.wait(100)

    # all this is needed because pygame.event.wait() is
    # not blocking as it should. Or maybe it is and I'm stupid.
    # By the way this is the event treating part.
    print("Initializing event treatment loop...")
    print("(all ready)")
    while running:
        while pygame.event.peek((pygame.KEYDOWN, pygame.KEYUP)):
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                try:
                    key_map[(event.type, event.key)]()
                except KeyError as e:
                    print(e)
            else:
                if event.type == pygame.QUIT:
                    print("Stopping broker...")
                    broker.stop()

                    cleanup_quit()
                    exit()
                print(f"Unhandled event caught:\n {event}")
        print(controller.get_button_state())

        # delay a bit so we give CPU a breather. See last comment.
        pygame.time.wait(2)  # TODO see above
