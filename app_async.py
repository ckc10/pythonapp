import tkinter as tk
from tkinter import ttk
import textwrap
import asyncio
import aiohttp

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

# Function to send POST request and update the label with the response
async def send_post_request(session, action, value):
    data = {
        "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
        "key": action,
        "value": value
    }
    try:
        async with session.post(WEBHOOK_URL, json=data) as response:
            if response.status == 200:
                response_message = f"Success: {action} set to {value}"
            else:
                response_message = f"Failed: {action} with status code {response.status}"
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
async def reset_all():
    actions = ["Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2", "CE_Sell_3", "CE_Exit", "CE_Lot", "CE_Lot_1",
               "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2", "PE_Sell_3", "PE_Exit", "PE_Lot", "PE_Lot_1", "UN_Exit"]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[send_post_request(session, action, "0") for action in actions])
    response_message = "All buttons reset to value 0."
    response_label_ce.config(text=response_message)
    response_label_pe.config(text=response_message)

def run_asyncio_task(task):
    asyncio.run(task)

async def button_action(action):
    async with aiohttp.ClientSession() as session:
        await send_post_request(session, action, "1")
        await asyncio.sleep(5)  # Wait for 5 seconds
        await send_post_request(session, action, "0")  # Send reset request
        


# Create the main window
root = tk.Tk()
root.title("BNK-Client-60")

window_width = 420
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
button_reset = tk.Button(root, text="Reset", command=lambda: run_asyncio_task(reset_all()), bg="grey")
button_reset.place(relx=0.5, rely=0.05, anchor="center")

# First line: Buy, SL, S1
button_buy = tk.Button(left_frame, text="Buy", command=lambda: run_asyncio_task(button_action("Buy_CE")), bg="green")
button_buy.grid(row=1, column=1, padx=10, pady=10)

button_add_ce = tk.Button(left_frame, text="LT+1", command=lambda: run_asyncio_task(button_action("CE_Lot")), bg="yellow")
button_add_ce.grid(row=1, column=2, padx=10, pady=10)

button_add_ce_1 = tk.Button(left_frame, text="LT+2", command=lambda: run_asyncio_task(button_action("CE_Lot_1")), bg="yellow")
button_add_ce_1.grid(row=1, column=3, padx=10, pady=10)

button_sell = tk.Button(left_frame, text="SL", command=lambda: run_asyncio_task(button_action("Sell_CE")), bg="red")
button_sell.grid(row=1, column=4, padx=10, pady=10)

# Second line: S1, S2, S3
button_s1 = tk.Button(left_frame, text="S1", command=lambda: run_asyncio_task(button_action("CE_Sell_1")), bg="orange")
button_s1.grid(row=2, column=1, padx=10, pady=10)

button_s2 = tk.Button(left_frame, text="S2", command=lambda: run_asyncio_task(button_action("CE_Sell_2")), bg="orange")
button_s2.grid(row=2, column=2, padx=10, pady=10)

button_s3 = tk.Button(left_frame, text="S3", command=lambda: run_asyncio_task(button_action("CE_Sell_3")), bg="orange")
button_s3.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(left_frame, text="EXIT", command=lambda: run_asyncio_task(button_action("CE_Exit")), bg="blue")
button_exit.grid(row=3, column=2, padx=10, pady=10)

# Response label for CE side
response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_ce.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

# First line: Buy, Sell
button_buy = tk.Button(right_frame, text="Buy", command=lambda: run_asyncio_task(button_action("Buy_PE")), bg="green")
button_buy.grid(row=1, column=6, padx=10, pady=10)

button_add_pe = tk.Button(right_frame, text="+1", command=lambda: run_asyncio_task(button_action("PE_Lot")), bg="yellow")
button_add_pe.grid(row=1, column=7, padx=10, pady=10)

button_add_pe_1 = tk.Button(right_frame, text="LT+", command=lambda: run_asyncio_task(button_action("PE_Lot_1")), bg="yellow")
button_add_pe_1.grid(row=1, column=8, padx=10, pady=10)

button_sell = tk.Button(right_frame, text="SL", command=lambda: run_asyncio_task(button_action("Sell_PE")), bg="red")
button_sell.grid(row=1, column=9, padx=10, pady=10)

# Second line: S1, S2, S3
button_s1 = tk.Button(right_frame, text="S1", command=lambda: run_asyncio_task(button_action("PE_Sell_1")), bg="orange")
button_s1.grid(row=2, column=6, padx=10, pady=10)

button_s2 = tk.Button(right_frame, text="S2", command=lambda: run_asyncio_task(button_action("PE_Sell_2")), bg="orange")
button_s2.grid(row=2, column=7, padx=10, pady=10)

button_s3 = tk.Button(right_frame, text="S3", command=lambda: run_asyncio_task(button_action("PE_Sell_3")), bg="orange")
button_s3.grid(row=2, column=8, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(right_frame, text="EXIT", command=lambda: run_asyncio_task(button_action("PE_Exit")), bg="blue")
button_exit.grid(row=3, column=7, padx=10, pady=10)

# Response label for PE side
response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_pe.grid(row=4, column=6, columnspan=5, padx=10, pady=10)

# UN_Exit button
button_u_exit = tk.Button(root, text="U.Exit", command=lambda: run_asyncio_task(button_action("UN_Exit")), bg="grey")
button_u_exit.place(relx=0.5, rely=0.95, anchor="center")

# Run the application
root.mainloop()
