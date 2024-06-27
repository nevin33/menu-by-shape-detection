import cv2
import numpy as np
import os

# The MenuOrderProcessor class processes a menu and evaluates orders.
class MenuOrderProcessor:
    def __init__(self):
        # Define the menu with food items, shapes, and prices for each color.
        self.menu = {
            "green": { #Starters
                "rectangle": ("Soup", 15),
                "pentagon": ("Cheese Platter", 16),
                "triangle": ("Garlic Bread", 22)
            },
            "yellow": { #Snacks
                "rectangle": ("Crispy Chicken", 20),
                "pentagon": ("Fish&Chips", 18),
                "triangle": ("Omlet", 12)
            },
            "orange": { #Main Course
                "rectangle": ("Meatballs", 30),
                "pentagon": ("Casseroles", 28),
                "triangle": ("Fajitas", 25)
            },
            "blue": { #Desserts
                "rectangle": ("Souffle", 17),
                "pentagon": ("Tiramisu", 19),
                "triangle": ("Cheesecake", 21)
            }
        }

    # The main function that processes orders.
    def process_order(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Unable to load image from '{image_path}'.")
            return

        # Convert the image to HSV color space.
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define color ranges for each food category.
        color_ranges = {
            "yellow": (np.array([20, 100, 100]), np.array([30, 255, 255])),
            "blue": (np.array([75, 100, 100]), np.array([130, 255, 255])),
            "green": (np.array([50, 100, 100]), np.array([70, 255, 255])),
            "orange": (np.array([0, 100, 100]), np.array([20, 255, 255]))
        }

        # Instantiate classes for shape detection and order processing.
        shape_detector = ShapeDetector()
        order_processor = OrderProcessor(self.menu)

        # Process orders and get error messages.
        detected_orders, error_messages = order_processor.process_orders(img, hsv, color_ranges, shape_detector)

        # Confirm the order and print information.
        self.confirm_order(detected_orders, error_messages)

        # Print error messages.
        for message in error_messages:
            print(message)

        # Display the processed order image.
        cv2.imshow("Processed Order", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Confirm the order operations.
    def confirm_order(self, detected_orders, error_messages):
        if not detected_orders:
            print("Error: No valid orders detected.")
            return

        # Generate an order summary and calculate the total amount.
        order_summary = OrderProcessor.generate_order_summary(detected_orders)
        total_amount = OrderProcessor.calculate_total_amount(detected_orders)

        print(f"Your order is: {order_summary}. ")

        # If there are no error messages, ask for confirmation.
        if error_messages == []:
            confirmation = input("Do you confirm your order? (yes/no): ").strip().lower()

            # Process confirmation response.
            if confirmation == "yes":
                print(f"Your food is being prepared. The total amount you have to pay: {total_amount} TL.")
            else:
                print("Your order has been canceled.")


# The OrderProcessor class processes orders and calculates the total amount.
class OrderProcessor:
    def __init__(self, menu):
        self.menu = menu

    # Function to process orders.
    def process_orders(self, img, hsv, color_ranges, shape_detector):
        detected_orders = {}
        multiple_selection_error = False
        required_selections = {"green": False, "orange": False}
        error_messages = []

        for color, (lower, upper) in color_ranges.items():
            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                epsilon = 0.04 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                x, y, w, h = cv2.boundingRect(contour)
                shape = shape_detector.identify_shape(len(approx))
                if shape:
                    if color in detected_orders:
                        multiple_selection_error = True
                        error_messages.append("Caution: You can only choose one food from the same group.")
                        break

                    order, price = self.menu[color].get(shape, ("Unknown Dish", 0))
                    detected_orders[color] = (order, shape, price)
                    required_selections[color] = True

                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, f"{order} ({price} TL)", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if not required_selections["green"] and not required_selections["orange"]:
            error_messages.append("Caution: To continue, you must select one main course and one starter.")
        else:
            if not required_selections["green"]:
                error_messages.append("Caution: To continue, you must select one starter.")
            if not required_selections["orange"]:
                error_messages.append("Caution: To continue, you must select one main course.")
            if len(detected_orders) == 1:
                error_messages.append("Caution: To continue, you must select more than one dish.")

        return detected_orders, error_messages

    # Static method to generate an order summary.
    @staticmethod
    def generate_order_summary(detected_orders):
        return ", ".join([f"{order} ({price} TL)" for _, (order, _, price) in detected_orders.items()])

    # Static method to calculate the total amount.
    @staticmethod
    def calculate_total_amount(detected_orders):
        return sum([price for _, (_, _, price) in detected_orders.items()])


# The ShapeDetector class identifies shapes based on the number of vertices.
class ShapeDetector:
    @staticmethod
    def identify_shape(vertices):
        if vertices == 3:
            return "triangle"
        elif vertices == 4:
            return "rectangle"
        elif vertices == 5:
            return "pentagon"
        return None


# Usage
processor = MenuOrderProcessor()
image_path = r"C:\Users\HP\Downloads\no main course no starter.png"  # Path to the image file
if os.path.exists(image_path):  # Check if the file exists
    processor.process_order(image_path)
else:
    print(f"Error: '{image_path}' file does not found.")
