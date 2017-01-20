from pwmled.led.rgb import RgbLed


class RgbwLed(RgbLed):
    """Represents a RGBW led that can be controlled."""
    def _get_pwm_values(self):
        """
        Get the pwm values regarding the current color.

        :return: The pwm values.
        """
        return [x / 255 for x in self._rgb_to_rgbw(self.color)]

    @staticmethod
    def _rgb_to_rgbw(color):
        """
        Convert a RGB color to a RGBW color.

        :param color: The RGB color.
        :return: The RGBW color.
        """
        # Get the maximum between R, G, and B
        max_value = max(color)

        # If the maximum value is 0, immediately return pure black.
        if max_value == 0:
            return [0] * 4

        # Figure out what the color with 100% hue is
        multiplier = 255 / max_value
        hue_red = color.R * multiplier
        hue_green = color.G * multiplier
        hue_blue = color.B * multiplier

        # Calculate the whiteness (not strictly speaking luminance)
        max_hue = max(hue_red, hue_green, hue_blue)
        min_hue = min(hue_red, hue_green, hue_blue)
        luminance = ((max_hue + min_hue) / 2 - 127.5) * 2 / multiplier

        # Calculate the output values
        r = max(0, min(255, int(color.R - luminance)))
        g = max(0, min(255, int(color.G - luminance)))
        b = max(0, min(255, int(color.B - luminance)))
        w = max(0, min(255, int(luminance)))

        return [r, g, b, w]