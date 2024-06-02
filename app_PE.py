import tkinter as tk
import requests
import json
import textwrap

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

# Function to send POST request and update the label with the response
def send_post_request(action):
    data = {
        "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
        "key":action,
        "value":"1"
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
root.title("BNK-Client-60-PUT")

window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# First line: Buy, Sell
button_buy = tk.Button(root, text="Buy", command=lambda: send_post_request("Buy_PE"),bg="green")
button_buy.grid(row=1, column=1, padx=10, pady=10)

button_sell = tk.Button(root, text="SL", command=lambda: send_post_request("Sell_PE"),bg="red")
button_sell.grid(row=1, column=3, padx=10, pady=10)

##updating for the buttons in second line
button_s1 = tk.Button(root, text="S1", command=lambda: send_post_request("PE_Sell_1"),bg="orange")
button_s1.grid(row=2, column=1, padx=10, pady=10)

button_s2 = tk.Button(root, text="S2", command=lambda: send_post_request("PE_Sell_2"),bg="orange")
button_s2.grid(row=2, column=2, padx=10, pady=10)

button_s3 = tk.Button(root, text="S3", command=lambda: send_post_request("PE_Sell_3"),bg="orange")
button_s3.grid(row=2, column=3, padx=10, pady=10)


# Second line: S1, S2, S3, S4, S5
# buttons_second_line = ["S1", "S2", "S3", "S4", "S5"]
# for idx, text in enumerate(buttons_second_line):
#     button = tk.Button(root, text=text, command=lambda a=text: send_post_request(a),bg="orange")
#     button.grid(row=1, column=idx, padx=10, pady=10)

# Third line: EXIT, U.Exit
button_exit = tk.Button(root, text="EXIT", command=lambda: send_post_request("PE_Exit"), bg="blue")
button_exit.grid(row=3, column=1, padx=10, pady=10)

button_u_exit = tk.Button(root, text="U.Exit", command=lambda: send_post_request("UN_Exit"), bg="grey")
button_u_exit.grid(row=3, column=3, padx=10, pady=10)

# Response label
response_label = tk.Label(root, text="", fg="blue", wraplength=400, justify="left")
response_label.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

# Run the application
root.mainloop()
