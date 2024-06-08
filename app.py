import tkinter as tk
from tkinter import ttk
import textwrap
import asyncio
import aiohttp
from threading import Thread

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

# Function to send POST request and update the label with the response
async def send_post_request(session, token, action, value):
    data = {
        "auth-token": token,
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
async def reset_all(token):
    actions = ["Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2", "CE_Sell_3", "CE_Exit", "CE_Lot", "CE_Lot_1",
               "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2", "PE_Sell_3", "PE_Exit", "PE_Lot", "PE_Lot_1", "UN_Exit"]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[send_post_request(session, token, action, "0") for action in actions])
    response_message = "All buttons reset to value 0."
    response_label_ce.config(text=response_message)
    response_label_pe.config(text=response_message)

def run_asyncio_task(task):
    asyncio.run_coroutine_threadsafe(task, asyncio_loop)

async def button_action(token, action):
    async with aiohttp.ClientSession() as session:
        await send_post_request(session, token, action, value="1")
        await asyncio.sleep(3)  # Wait for 3 seconds
        await send_post_request(session, token, action, "0")  # Send reset request

# Function to call all the tokens at the same time
def multi_token(action):
    run_asyncio_task(button_action(token1, action))
    run_asyncio_task(button_action(token2, action))
    run_asyncio_task(button_action(token3, action))
    run_asyncio_task(button_action(token4, action))

# Function for multi token reset 
def multi_token_reset():
    run_asyncio_task(reset_all(token1))
    run_asyncio_task(reset_all(token2))
    run_asyncio_task(reset_all(token3))
    run_asyncio_task(reset_all(token4))

# Create the main window
root = tk.Tk()
root.title("Trading Client")
root.geometry("800x600")

# Create the notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# BNIFTY-Client tab
bnifty_tab = ttk.Frame(notebook)
notebook.add(bnifty_tab, text="BNIFTY-Client")

# FNIFTY-Client tab
fnifty_tab = ttk.Frame(notebook)
notebook.add(fnifty_tab, text="FNIFTY-Client")

# Tokens (Example values, update as needed)
token1 = "f18769ad-818c-41c6-929d-7f1608730000"
token2 = "f18769ad-818c-41c6-929d-7f1608730000"
token3 = "f18769ad-818c-41c6-929d-7f1608730000"
token4 = "f18769ad-818c-41c6-929d-7f1608730000"

# BNIFTY-Client UI setup
def setup_bnifty_tab():
    left_frame = tk.Frame(bnifty_tab)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(bnifty_tab)
    right_frame.pack(side="right", fill="both", expand=True)

    # Add a vertical separator
    separator = ttk.Separator(bnifty_tab, orient='vertical')
    separator.pack(side="left", fill="y", padx=5)

    # Add static labels
    label_put = tk.Label(right_frame, text="PUT", font=("Arial", 14, "bold"))
    label_put.grid(row=0, column=3, columnspan=6, pady=10)

    label_call = tk.Label(left_frame, text="CALL", font=("Arial", 14, "bold"))
    label_call.grid(row=0, column=0, columnspan=4, pady=10)

    # Reset button
    button_reset = tk.Button(bnifty_tab, text="Reset", command=lambda: multi_token_reset(), bg="grey")
    button_reset.place(relx=0.5, rely=0.05, anchor="center")

    # First line: Buy, Sell
    button_buy = tk.Button(left_frame, text="Buy", command=lambda: multi_token("Buy_CE"), bg="green")
    button_buy.grid(row=1, column=1, padx=10, pady=10)

    button_add_ce = tk.Button(left_frame, text="+1", command=lambda: multi_token("CE_Lot"), bg="yellow")
    button_add_ce.grid(row=1, column=2, padx=10, pady=10)

    button_add_ce_1 = tk.Button(left_frame, text="LT+", command=lambda: multi_token("CE_Lot_1"), bg="yellow")
    button_add_ce_1.grid(row=1, column=3, padx=10, pady=10)

    button_sell = tk.Button(left_frame, text="SL", command=lambda: multi_token("Sell_CE"), bg="red")
    button_sell.grid(row=1, column=4, padx=10, pady=10)

    # Second line: S1, S2, S3
    button_s1 = tk.Button(left_frame, text="S1", command=lambda: multi_token("CE_Sell_1"), bg="orange")
    button_s1.grid(row=2, column=1, padx=10, pady=10)

    button_s2 = tk.Button(left_frame, text="S2", command=lambda: multi_token("CE_Sell_2"), bg="orange")
    button_s2.grid(row=2, column=2, padx=10, pady=10)

    button_s3 = tk.Button(left_frame, text="S3", command=lambda: multi_token("CE_Sell_3"), bg="orange")
    button_s3.grid(row=2, column=3, padx=10, pady=10)

    # Third line: EXIT
    button_exit = tk.Button(left_frame, text="EXIT", command=lambda: multi_token("CE_Exit"), bg="blue")
    button_exit.grid(row=3, column=2, padx=10, pady=10)

    # U.Exit button
    button_u_exit = tk.Button(bnifty_tab, text="U.Exit", command=lambda: multi_token("UN_Exit"), bg="grey")
    button_u_exit.place(relx=0.5, rely=0.95, anchor="center")

    # Response label for CE side
    global response_label_ce
    response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
    response_label_ce.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

    # First line: Buy, Sell
    button_buy = tk.Button(right_frame, text="Buy", command=lambda: multi_token("Buy_PE"), bg="green")
    button_buy.grid(row=1, column=1, padx=10, pady=10)

    button_add_pe = tk.Button(right_frame, text="LT+", command=lambda: multi_token("PE_Lot"), bg="yellow")
    button_add_pe.grid(row=1, column=2, padx=10, pady=10)

    button_add_pe_1 = tk.Button(right_frame, text="+1", command=lambda: multi_token("PE_Lot_1"), bg="yellow")
    button_add_pe_1.grid(row=1, column=3, padx=10, pady=10)

    button_sell = tk.Button(right_frame, text="SL", command=lambda: multi_token("Sell_PE"), bg="red")
    button_sell.grid(row=1, column=4, padx=10, pady=10)

    # Second line: S1, S2, S3
    button_s1 = tk.Button(right_frame, text="S1", command=lambda: multi_token("PE_Sell_1"), bg="orange")
    button_s1.grid(row=2, column=1, padx=10, pady=10)

    button_s2 = tk.Button(right_frame, text="S2", command=lambda: multi_token("PE_Sell_2"), bg="orange")
    button_s2.grid(row=2, column=2, padx=10, pady=10)

    button_s3 = tk.Button(right_frame, text="S3", command=lambda: multi_token("PE_Sell_3"), bg="orange")
    button_s3.grid(row=2, column=3, padx=10, pady=10)

    # Third line: EXIT
    button_exit = tk.Button(right_frame, text="EXIT", command=lambda: multi_token("PE_Exit"), bg="blue")
    button_exit.grid(row=3, column=2, padx=10, pady=10)

    # Response label for PE side
    global response_label_pe
    response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")
    response_label_pe.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

setup_bnifty_tab()

# FNIFTY-Client UI setup
def setup_fnifty_tab():
    left_frame = tk.Frame(fnifty_tab)
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(fnifty_tab)
    right_frame.pack(side="right", fill="both", expand=True)

    # Add a vertical separator
    separator = ttk.Separator(fnifty_tab, orient='vertical')
    separator.pack(side="left", fill="y", padx=5)

    # Add static labels
    label_put = tk.Label(right_frame, text="PUT", font=("Arial", 14, "bold"))
    label_put.grid(row=0, column=3, columnspan=6, pady=10)

    label_call = tk.Label(left_frame, text="CALL", font=("Arial", 14, "bold"))
    label_call.grid(row=0, column=0, columnspan=4, pady=10)

    # Reset button
    button_reset = tk.Button(fnifty_tab, text="Reset", command=lambda: multi_token_reset(), bg="grey")
    button_reset.place(relx=0.5, rely=0.05, anchor="center")

    # First line: Buy, Sell
    button_buy = tk.Button(left_frame, text="Buy", command=lambda: multi_token("Buy_CE"), bg="green")
    button_buy.grid(row=1, column=1, padx=10, pady=10)

    button_add_ce = tk.Button(left_frame, text="+1", command=lambda: multi_token("CE_Lot"), bg="yellow")
    button_add_ce.grid(row=1, column=2, padx=10, pady=10)

    button_add_ce_1 = tk.Button(left_frame, text="LT+", command=lambda: multi_token("CE_Lot_1"), bg="yellow")
    button_add_ce_1.grid(row=1, column=3, padx=10, pady=10)

    button_sell = tk.Button(left_frame, text="SL", command=lambda: multi_token("Sell_CE"), bg="red")
    button_sell.grid(row=1, column=4, padx=10, pady=10)

    # Second line: S1, S2, S3
    button_s1 = tk.Button(left_frame, text="S1", command=lambda: multi_token("CE_Sell_1"), bg="orange")
    button_s1.grid(row=2, column=1, padx=10, pady=10)

    button_s2 = tk.Button(left_frame, text="S2", command=lambda: multi_token("CE_Sell_2"), bg="orange")
    button_s2.grid(row=2, column=2, padx=10, pady=10)

    button_s3 = tk.Button(left_frame, text="S3", command=lambda: multi_token("CE_Sell_3"), bg="orange")
    button_s3.grid(row=2, column=3, padx=10, pady=10)

    # Third line: EXIT
    button_exit = tk.Button(left_frame, text="EXIT", command=lambda: multi_token("CE_Exit"), bg="blue")
    button_exit.grid(row=3, column=2, padx=10, pady=10)

    # U.Exit button
    button_u_exit = tk.Button(fnifty_tab, text="U.Exit", command=lambda: multi_token("UN_Exit"), bg="grey")
    button_u_exit.place(relx=0.5, rely=0.95, anchor="center")

    # Response label for CE side
    global response_label_ce
    response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
    response_label_ce.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

    # First line: Buy, Sell
    button_buy = tk.Button(right_frame, text="Buy", command=lambda: multi_token("Buy_PE"), bg="green")
    button_buy.grid(row=1, column=1, padx=10, pady=10)

    button_add_pe = tk.Button(right_frame, text="LT+", command=lambda: multi_token("PE_Lot"), bg="yellow")
    button_add_pe.grid(row=1, column=2, padx=10, pady=10)

    button_add_pe_1 = tk.Button(right_frame, text="+1", command=lambda: multi_token("PE_Lot_1"), bg="yellow")
    button_add_pe_1.grid(row=1, column=3, padx=10, pady=10)

    button_sell = tk.Button(right_frame, text="SL", command=lambda: multi_token("Sell_PE"), bg="red")
    button_sell.grid(row=1, column=4, padx=10, pady=10)

    # Second line: S1, S2, S3
    button_s1 = tk.Button(right_frame, text="S1", command=lambda: multi_token("PE_Sell_1"), bg="orange")
    button_s1.grid(row=2, column=1, padx=10, pady=10)

    button_s2 = tk.Button(right_frame, text="S2", command=lambda: multi_token("PE_Sell_2"), bg="orange")
    button_s2.grid(row=2, column=2, padx=10, pady=10)

    button_s3 = tk.Button(right_frame, text="S3", command=lambda: multi_token("PE_Sell_3"), bg="orange")
    button_s3.grid(row=2, column=3, padx=10, pady=10)

    # Third line: EXIT
    button_exit = tk.Button(right_frame, text="EXIT", command=lambda: multi_token("PE_Exit"), bg="blue")
    button_exit.grid(row=3, column=2, padx=10, pady=10)

    # Response label for PE side
    global response_label_pe
    response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")
    response_label_pe.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

setup_fnifty_tab()

# Start the asyncio event loop in a separate thread
async def asyncio_event_loop(loop):
    asyncio.set_event_loop(loop)
    await loop.run_forever()

asyncio_loop = asyncio.new_event_loop()
thread = Thread(target=lambda: asyncio.run(asyncio_event_loop(asyncio_loop)))
thread.start()

# Start the Tkinter event loop
root.mainloop()
