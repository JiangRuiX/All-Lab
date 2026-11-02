def calculate_area(width, height):
    """Calculate and return the area of a rectangle.

    Args:
        width:  The width of the rectangle (number).
        height: The height of the rectangle (number).

    Returns:
        The area as a number (width * height).
    """
    return width * height


def calculate_perimeter(width, height):
    """Calculate and return the perimeter of a rectangle.

    Args:
        width:  The width of the rectangle (number).
        height: The height of the rectangle (number).

    Returns:
        The perimeter as a number: 2 * (width + height).
    """
    return 2 * (width + height)


print(calculate_area(5, 3))
print(calculate_perimeter(5, 3))