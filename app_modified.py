import tkinter as tk
from tkinter import ttk
import requests
import json
import textwrap

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

# Function to send POST request and update the label with the response
def send_post_request(action):
    data = {
        "auth-token": "36c8ee23-5db6-48b8-9584-6fa34e098da0",
        "key": action,
        "value": "1"
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

    # Update the label with the response message based on the button clicked
    if "CE" in action:
        response_label_ce.config(text=wrapped_response)
        response_label_pe.config(text="")
    else:
        response_label_pe.config(text=wrapped_response)
        response_label_ce.config(text="")

# Function to reset all values to 0
def reset_all():
    actions = ["Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2", "CE_Sell_3", "CE_Exit","CE_Lot"
               "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2", "PE_Sell_3", "PE_Exit","PE_Lot","UN_Exit"]
    for action in actions:
        send_post_request_reset(action)
    

# Function to send POST request with value 0 for reset
def send_post_request_reset(action):
    data = {
        "auth-token": "36c8ee23-5db6-48b8-9584-6fa34e098da0",
        "key": action,
        "value": "0"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 200:
            response_message = f"Reseted all buttons"
        else:
            response_message = f"Failed: {action} with status code {response.status_code}"
    except Exception as e:
        response_message = f"Exception: {e}"

    # Wrap the response message to fit the UI window
    wrapped_response = "\n".join(textwrap.wrap(response_message, width=50))

    # Update the label with the response message based on the button clicked
    if "CE" in action:
        response_label_ce.config(text=wrapped_response)
        response_label_pe.config(text="")
    else:
        response_label_pe.config(text=wrapped_response)
        response_label_ce.config(text="")

# Create the main window
root = tk.Tk()
root.title("BNK-Client-60")

window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="both", expand=True)

right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)

# Add a vertical separator
separator = ttk.Separator(root, orient='vertical')
separator.pack(side="left", fill="y", padx=5)

# Add static labels
label_put = tk.Label(right_frame, text="PUT", font=("Arial", 14, "bold"))
label_put.grid(row=0, column=3, columnspan=6, pady=10)

label_call = tk.Label(left_frame, text="CALL", font=("Arial", 14, "bold"))
label_call.grid(row=0, column=0, columnspan=4, pady=10)

# Reset button
button_reset = tk.Button(root, text="Reset", command=reset_all, bg="grey")
button_reset.place(relx=0.5, rely=0.05, anchor="center")

# First line: Buy, Sell
button_buy = tk.Button(left_frame, text="Buy", command=lambda: send_post_request("Buy_CE"), bg="green")
button_buy.grid(row=1, column=1, padx=10, pady=10)

button_add_ce = tk.Button(left_frame, text="+1", command=lambda: send_post_request("CE_Lot"), bg="yellow")
button_add_ce.grid(row=1, column=2, padx=10, pady=10)

button_sell = tk.Button(left_frame, text="SL", command=lambda: send_post_request("Sell_CE"), bg="red")
button_sell.grid(row=1, column=3, padx=10, pady=10)

# Second line: S1, S2, S3
button_s1 = tk.Button(left_frame, text="S1", command=lambda: send_post_request("CE_Sell_1"), bg="orange")
button_s1.grid(row=2, column=1, padx=10, pady=10)

button_s2 = tk.Button(left_frame, text="S2", command=lambda: send_post_request("CE_Sell_2"), bg="orange")
button_s2.grid(row=2, column=2, padx=10, pady=10)

button_s3 = tk.Button(left_frame, text="S3", command=lambda: send_post_request("CE_Sell_3"), bg="orange")
button_s3.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(left_frame, text="EXIT", command=lambda: send_post_request("CE_Exit"), bg="blue")
button_exit.grid(row=3, column=2, padx=10, pady=10)

# Response label for CE side
response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_ce.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

# First line: Buy, Sell
button_buy = tk.Button(right_frame, text="Buy", command=lambda: send_post_request("Buy_PE"), bg="green")
button_buy.grid(row=1, column=6, padx=10, pady=10)

button_add_pe = tk.Button(right_frame, text="+1", command=lambda: send_post_request("PE_Lot"), bg="yellow")
button_add_pe.grid(row=1, column=7, padx=10, pady=10)

button_sell = tk.Button(right_frame, text="SL", command=lambda: send_post_request("Sell_PE"), bg="red")
button_sell.grid(row=1, column=8, padx=10, pady=10)

# Second line: S1, S2, S3
button_s1 = tk.Button(right_frame, text="S1", command=lambda: send_post_request("PE_Sell_1"), bg="orange")
button_s1.grid(row=2, column=6, padx=10, pady=10)

button_s2 = tk.Button(right_frame, text="S2", command=lambda: send_post_request("PE_Sell_2"), bg="orange")
button_s2.grid(row=2, column=7, padx=10, pady=10)

button_s3 = tk.Button(right_frame, text="S3", command=lambda: send_post_request("PE_Sell_3"), bg="orange")
button_s3.grid(row=2, column=8, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(right_frame, text="EXIT", command=lambda: send_post_request("PE_Exit"), bg="blue")
button_exit.grid(row=3, column=7, padx=10, pady=10)

# Response label for PE side
response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_pe.grid(row=4, column=6, columnspan=5, padx=10, pady=10)

# UN_Exit button
button_u_exit = tk.Button(root, text="U.Exit", command=lambda: send_post_request("UN_Exit"), bg="grey")
button_u_exit.place(relx=0.5, rely=0.95, anchor="center")

# Run the application
root.mainloop()
