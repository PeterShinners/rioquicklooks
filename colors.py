import rio
import math


def swatch(angle, span, brightness):
    """Create swatch on the color wheel"""
    sat = math.sin(span * math.pi)*.9+.1
    color = rio.Color.from_hsv(angle, sat, span)
    if brightness > 0:
        color = color.brighter(brightness)
    elif brightness < 0:
        color = color.darker(-brightness)

    rad = angle * 2 * math.pi + 0.1
    swatch = rio.Rectangle(fill=color)
    swatch.align_x = math.cos(rad) * span * 0.45 + 0.5
    swatch.align_y = math.sin(rad) * span * 0.45 + 0.5
    swatch.min_width = swatch.min_height = swatch.corner_radius = (span ** 2) * 0.5 + 2
    return swatch


class ColorWheel(rio.Component):
    """Wheel of swatches and adjustment slider"""
    brightness: float = 0.0
    def build(self):
        # Generate swatch components        
        wheel = []
        for i, angle in enumerate(range(0, 360, 20)):
            spoke = [swatch(angle/360, step/5, self.brightness) 
                        for step in range(2, 6)]
            wheel.extend(spoke[i%2:])

        # Pack components together
        b = self.bind().brightness
        return rio.Rectangle(
            content=rio.Column(
                rio.Stack(*wheel, grow_x=True, grow_y=True),
                rio.Row(
                    rio.Slider(value=b, minimum=-1.0, maximum=1.0, step=0.05),
                    rio.Text(text=f" Brightness {self.brightness:.2f}"),
                spacing=10), margin_bottom=1),
            fill=rio.LinearGradientFill(
                (rio.Color.from_hsv(0, 0, 0.3), 0),
                (rio.Color.from_hsv(0, 0, 0.7), 1),
                angle_degrees=45,
            )
        )


if __name__ == "__main__":
    app = rio.App(build=ColorWheel)
    app.run_in_window()
