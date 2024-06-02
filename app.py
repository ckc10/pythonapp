
import tkinter as tk
import requests
import json

# Webhook URL
WEBHOOK_URL = 'https://your-webhook-url.com/'

# Function to send POST request
def send_post_request(action):
    data = {
            "action": action
                }
                    try:
                            response = requests.post(WEBHOOK_URL, json=data)
                                    if response.status_code == 200:
                                                print(f"Success: {action}")
                                                        else:
                                                                    print(f"Failed: {action} with status code {response.status_code}")
                                                                        except Exception as e:
                                                                                print(f"Exception: {e}")

                                                                                # Create the main window
                                                                                root = tk.Tk()
                                                                                root.title("Webhook Trigger")

                                                                                # Create buttons
                                                                                buttons = [
                                                                                    ("Buy", "Buy"),
                                                                                        ("Sell", "Sell"),
                                                                                            ("S1", "S1"),
                                                                                                ("S2", "S2"),
                                                                                                    ("S3", "S3"),
                                                                                                        ("S4", "S4"),
                                                                                                            ("S5", "S5"),
                                                                                                                ("EXIT", "EXIT"),
                                                                                                                    ("U.Exit", "U.Exit")
                                                                                                                    ]

                                                                                                                    for text, action in buttons:
                                                                                                                        button = tk.Button(root, text=text, command=lambda a=action: send_post_request(a))
                                                                                                                            button.pack(pady=5)

                                                                                                                            # Run the application
                                                                                                                            root.mainloop()