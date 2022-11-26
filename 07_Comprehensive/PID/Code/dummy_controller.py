class DummyController(object):
    """
    This is the Dummy Controller Class
    """
    def __init__(self):
        self.kp = 0.032510    # proportionality coefficient
        self.ki = 0.001443   # integral coefficient
        self.kd = -0.06800   # differential coefficient
        self.dt = 0.1  # time step size [s]
        self.e_i = 0  # integral item initial value

    def get_throttle_cmd(self, target_height:float, rocket_state:dict) -> float:
        """_summary_
        Get throttle command values based on the target and current states to control the rocket

        Args:
            target_height (float): target height you want the rocket be at
            rocket_height (float): current rocket state

        Returns:
            throttle_cmd(float): throttle command value based on the target and current states
        """

        e = target_height - rocket_state['height']   # error, i.e. height difference

        self.e_i = self.e_i + self.ki * e * self.dt  # error accumulation for integral item

        if rocket_state['height'] < target_height:
            # Formula for calculating PID
            throttle_cmd = self.kp * e + self.e_i + self.kd * rocket_state['velocity']
        else:
            throttle_cmd = self.e_i

        throttle_cmd = min(throttle_cmd, 1)
        throttle_cmd = max(throttle_cmd, 0)

        return throttle_cmd