import matplotlib.pyplot as plt
import numpy as np
from dummy_controller import DummyController
from rocket import Rocket

def pid_plot(target_height=100, animation=True):
    rocket = Rocket()
    controller = DummyController()

    # main loop
    iteration = 0
    max_iteration = 500
    outputs = []
    while True:
        rocket_state = rocket.get_state()
        throttle_cmd = controller.get_throttle_cmd(target_height, rocket_state)

        rocket_state = rocket.update(throttle_cmd)
        outputs.append(rocket_state["height"])

        iteration += 1
        print("-" * 15 + "iteraiton: ", iteration, "-" * 15)
        if iteration > max_iteration:
            break

    if animation:
        plt.axhline(target_height, c = 'red')
        plt.plot(np.arange(max_iteration+1), np.array(outputs), 'w-')
        plt.ylim(min(outputs) - 0.1 * min(outputs), max(outputs) + 0.1 * max(outputs))
        plt.plot(outputs)
        plt.show()

pid_plot()