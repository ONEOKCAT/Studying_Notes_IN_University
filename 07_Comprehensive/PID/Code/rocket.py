import random
import time
import signal
import matplotlib.pyplot as plt

plt.style.use("dark_background")

from dummy_controller import DummyController

GRAVITY = 9.8  # acceleration of gravity [m/s^2]

class Rocket(object):
    """
    This is the main Rocket Class
    """

    def __init__(self):
        self.state = dict()  # rocket state dictionary
        self.state["height"] = 0  # rocket height [m]
        self.state["velocity"] = 0  # rocket velocity [m/s]
        self.state["acceleration"] = 0  # rocket acceleration [m/s^2]
        self.state["time"] = 0  # time accumulation
        self.MASS = 10000  # rocket mass [kg]
        self.THROTTLE_RATIO = (
            200000  # throttle command to force ratio, 200,000 [N] at full throttle
        )
        self.dt = 0.1  # time step size [s]


    def update(self, throttle_cmd: float, force_noise_sigma: float = 0) -> dict:
        """_summary_
        Args:
            throttle_cmd (float): throttle command value in [0, 1]

        Returns:
            state (dict): rocket state dictionary
        """
        # constrain throttle command to [0,1]
        throttle_cmd = min(throttle_cmd, 1)
        throttle_cmd = max(throttle_cmd, 0)

        # calculate net force
        throttle_force = throttle_cmd * self.THROTTLE_RATIO
        noise_force = random.gauss(0, force_noise_sigma)
        net_force = throttle_force + noise_force - self.MASS * GRAVITY
        print(
            "[Rocket INFO] throttle force: %.1f N, noise force: %.1f N, net force: %.1f N"
            % (throttle_force, noise_force, net_force)
        )

        # update state
        self.state["acceleration"] = net_force / self.MASS
        self.state["velocity"] += self.state["acceleration"] * self.dt
        self.state["height"] += self.state["velocity"] * self.dt
        self.state["time"] = self.state["time"] + self.dt
        self.state["height"] = max(self.state["height"], 0)


        if self.state["height"] == 0:
            self.state_velocity = 0

        return self.state

    def get_state(self):
        return self.state


def plot_animation(axis, target_height: float, rocket_state: dict, throttle_cmd: float):
    axis.clear()
    axis.set_xlim([-10, 10])
    axis.set_ylim([0, 200])
    axis.set_axis_off()
    axis.arrow(0, rocket_state["height"], 0, 6, width=1, head_width=1, color="r")
    axis.text(
        2,
        rocket_state["height"] + 2,
        " height: %.1f m, vel: %.1f m/s \n acc: %.1f m/s^2, time: %.1f s \n throttle_cmd: %.1f"
        % (
            rocket_state["height"],
            rocket_state["velocity"],
            rocket_state["acceleration"],
            rocket_state["time"],
            throttle_cmd,
        ),
    )
    axis.text(-2, rocket_state["height"] - 4, "I am A rocket")

    axis.plot([-10, 10], [target_height, target_height], "b--")
    axis.plot([-10, 10], [0, 0], "w-")

    plt.draw()
    plt.pause(0.05)


def rocket_run(target_height=100, animation=True):
    rocket = Rocket()

    if animation:
        plt.ion()
        fig, axis = plt.subplots(figsize=(6, 10))

    # """
    # TODO: REPLACE THIS DummyController with your controller and try to achieve a better performance of rocket control
    controller = DummyController()
    # """

    # main loop
    iteration = 0
    max_iteration = 1e4
    while True:
        rocket_state = rocket.get_state()
        throttle_cmd = controller.get_throttle_cmd(target_height, rocket_state)

        rocket_state = rocket.update(throttle_cmd)
        print(
            "[Rocket INFO] height: %.2f m, vel: %.2f m/s, acc: %.2f m/s^2,  time: %.1f s, throttle_cmd: %.1f"
            % (
                rocket_state["height"],
                rocket_state["velocity"],
                rocket_state["acceleration"],
                rocket_state["time"],
                throttle_cmd,
            )
        )
        if animation:
            plot_animation(
                axis,
                target_height,
                rocket_state,
                throttle_cmd,
            )
        else:
            time.sleep(0.1)

        iteration += 1
        print("-" * 15 + "iteraiton: ", iteration, "-" * 15)
        if iteration > max_iteration:
            break


def handler():
    exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)

    rocket_run()