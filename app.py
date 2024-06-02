import tkinter as tk
import requests
import json
import textwrap

# Webhook URL
WEBHOOK_URL = 'https://your-webhook-url.com/'

# Function to send POST request and update the label with the response
def send_post_request(action):
    data = {
        "action": action
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            response_message = f"Success: {action}"
        else:
            response_message = f"Failed: {action} with status code {response.status_code}"
    except Exception as e:
        response_message = f"Exception: {e}"

    # Wrap the response message to fit the UI window
    wrapped_response = "\n".join(textwrap.wrap(response_message, width=50))

    # Update the label with the response message
    response_label.config(text=wrapped_response)

# Create the main window
root = tk.Tk()
root.title("Webhook Trigger")

# First line: Buy, Sell
button_buy = tk.Button(root, text="Buy", command=lambda: send_post_request("Buy"),bg="green")
button_buy.grid(row=0, column=1, padx=10, pady=10)

button_sell = tk.Button(root, text="Sell", command=lambda: send_post_request("Sell"),bg="red")
button_sell.grid(row=0, column=3, padx=10, pady=10)

# Second line: S1, S2, S3, S4, S5
buttons_second_line = ["S1", "S2", "S3", "S4", "S5"]
for idx, text in enumerate(buttons_second_line):
    button = tk.Button(root, text=text, command=lambda a=text: send_post_request(a),bg="orange")
    button.grid(row=1, column=idx, padx=10, pady=10)

# Third line: EXIT, U.Exit
button_exit = tk.Button(root, text="EXIT", command=lambda: send_post_request("EXIT"), bg="blue")
button_exit.grid(row=2, column=1, padx=10, pady=10)

button_u_exit = tk.Button(root, text="U.Exit", command=lambda: send_post_request("U.Exit"), bg="grey")
button_u_exit.grid(row=2, column=3, padx=10, pady=10)

# Response label
response_label = tk.Label(root, text="", fg="blue", wraplength=400, justify="left")
response_label.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# Run the application
root.mainloop()
