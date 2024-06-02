import tkinter as tk
from tkinter import ttk
import requests
import json
import textwrap

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

# Function to send POST request and update the label with the response
def send_post_request(action, response_label_to_show, response_label_to_hide):
    data = {
        "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
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

    # Update the label with the response message
    response_label_to_show.config(text=wrapped_response)
    response_label_to_show.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

    # Hide the other response label
    response_label_to_hide.config(text="")

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
label_put.grid(row=0, column=0, columnspan=4, pady=10)

label_call = tk.Label(left_frame, text="CALL", font=("Arial", 14, "bold"))
label_call.grid(row=0, column=0, columnspan=4, pady=10)

# Add response labels to the frames
response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")

# First line: Buy, Sell (Left Frame)
button_buy_ce = tk.Button(left_frame, text="Buy", command=lambda: send_post_request("Buy_CE", response_label_ce, response_label_pe), bg="green")
button_buy_ce.grid(row=1, column=1, padx=10, pady=10)

button_sell_ce = tk.Button(left_frame, text="SL", command=lambda: send_post_request("Sell_CE", response_label_ce, response_label_pe), bg="red")
button_sell_ce.grid(row=1, column=3, padx=10, pady=10)

# Second line: S1, S2, S3 (Left Frame)
button_s1_ce = tk.Button(left_frame, text="S1", command=lambda: send_post_request("CE_Sell_1", response_label_ce, response_label_pe), bg="orange")
button_s1_ce.grid(row=2, column=1, padx=10, pady=10)

button_s2_ce = tk.Button(left_frame, text="S2", command=lambda: send_post_request("CE_Sell_2", response_label_ce, response_label_pe), bg="orange")
button_s2_ce.grid(row=2, column=2, padx=10, pady=10)

button_s3_ce = tk.Button(left_frame, text="S3", command=lambda: send_post_request("CE_Sell_3", response_label_ce, response_label_pe), bg="orange")
button_s3_ce.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT, U.Exit (Left Frame)
button_exit_ce = tk.Button(left_frame, text="EXIT", command=lambda: send_post_request("CE_Exit", response_label_ce, response_label_pe), bg="blue")
button_exit_ce.grid(row=3, column=1, padx=10, pady=10)

button_u_exit_ce = tk.Button(left_frame, text="U.Exit", command=lambda: send_post_request("UN_Exit", response_label_ce, response_label_pe), bg="grey")
button_u_exit_ce.grid(row=3, column=3, padx=10, pady=10)

# First line: Buy, Sell (Right Frame)
button_buy_pe = tk.Button(right_frame, text="Buy", command=lambda: send_post_request("Buy_PE", response_label_pe, response_label_ce), bg="green")
button_buy_pe.grid(row=1, column=1, padx=10, pady=10)

button_sell_pe = tk.Button(right_frame, text="SL", command=lambda: send_post_request("Sell_PE", response_label_pe, response_label_ce), bg="red")
button_sell_pe.grid(row=1, column=3, padx=10, pady=10)

# Second line: S1, S2, S3 (Right Frame)
button_s1_pe = tk.Button(right_frame, text="S1", command=lambda: send_post_request("PE_Sell_1", response_label_pe, response_label_ce), bg="orange")
button_s1_pe.grid(row=2, column=1, padx=10, pady=10)

button_s2_pe = tk.Button(right_frame, text="S2", command=lambda: send_post_request("PE_Sell_2", response_label_pe, response_label_ce), bg="orange")
button_s2_pe.grid(row=2, column=2, padx=10, pady=10)

button_s3_pe = tk.Button(right_frame, text="S3", command=lambda: send_post_request("PE_Sell_3", response_label_pe, response_label_ce), bg="orange")
button_s3_pe.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT, U.Exit (Right Frame)
button_exit_pe = tk.Button(right_frame, text="EXIT", command=lambda: send_post_request("PE_Exit", response_label_pe, response_label_ce), bg="blue")
button_exit_pe.grid(row=3, column=1, padx=10, pady=10)

button_u_exit_pe = tk.Button(right_frame, text="U.Exit", command=lambda: send_post_request("UN_Exit", response_label_pe, response_label_ce), bg="grey")
button_u_exit_pe.grid(row=3, column=3, padx=10, pady=10)

# Run the application
root.mainloop()
