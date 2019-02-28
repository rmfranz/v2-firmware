import pigpio
import os

class Gpio:

    def __init__(self):
        os.system("sudo killall pigpiod")
        os.system("sudo pigpiod -p 8889")
        self.is_initialized = False
        self.lights_on = False

    def initialize(self):
        self.gpio = pigpio.pi(port=8889)
        self.is_initialized = True
        self.lights_blue()
        self.lights_on = True

    def stop(self):
        self.gpio.stop()
        self.is_initialized = False
        self.lights_on = False

    def lights_off(self):
        self.gpio.write(17, 0)
        self.gpio.write(27, 0)
        self.gpio.write(22, 0)
        self.lights_on = False

    def lights_red(self):
        self.gpio.set_PWM_dutycycle(17, 255)
        self.gpio.set_PWM_dutycycle(27, 0)
        self.gpio.set_PWM_dutycycle(22, 0)
        self.lights_on = True

    def lights_green(self):
        self.gpio.set_PWM_dutycycle(17, 0)
        self.gpio.set_PWM_dutycycle(27, 255)
        self.gpio.set_PWM_dutycycle(22, 0)
        self.lights_on = True

    def lights_blue(self):
        self.gpio.set_PWM_dutycycle(17, 0)
        self.gpio.set_PWM_dutycycle(27, 0)
        self.gpio.set_PWM_dutycycle(22, 255)
        self.lights_on = True

    def lights_other(self):
        self.gpio.set_PWM_dutycycle(17, 209)
        self.gpio.set_PWM_dutycycle(27, 37)
        self.gpio.set_PWM_dutycycle(22, 218)
        self.lights_on = True