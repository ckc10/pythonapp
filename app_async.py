import tkinter as tk
from tkinter import ttk
import textwrap
import asyncio
import aiohttp

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

token1="f18769ad-818c-41c6-929d-7f1608730000"
token2="f18769ad-818c-41c6-929d-7f1608730000"
token3="f18769ad-818c-41c6-929d-7f1608730000"
token4="f18769ad-818c-41c6-929d-7f1608730000"


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
    actions = ["Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2","CE_Sell_3","CE_Exit", "CE_Lot1_Exit", "CE_Lot2_Exit", "CE_Lot1", "CE_Lot2",
               "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2","PE_Sell_3","PE_Exit","PE_Lot1_Exit", "PE_Lot2_Exit","PE_Lot1", "PE_Lot2", "UN_Exit"]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[send_post_request(session, token, action, "0") for action in actions])
    response_message = "All buttons reset to value 0."
    response_label_ce.config(text=response_message)
    response_label_pe.config(text=response_message)

def run_asyncio_task(task):
    asyncio.run(task)

async def button_action(token,action):
    async with aiohttp.ClientSession() as session:
        await send_post_request(session, token, action, value="1")
        await asyncio.sleep(3)  # Wait for 5 seconds
        await send_post_request(session,token, action, "0")  # Send reset request
        

# Function to call all the tokens at the same time

def multi_token(action):
    run_asyncio_task(button_action(token1,action))
    run_asyncio_task(button_action(token2,action))
    run_asyncio_task(button_action(token3,action))
    run_asyncio_task(button_action(token4,action))


# Function for multi token reset 

def multi_token_reset():
    run_asyncio_task(reset_all(token1))
    run_asyncio_task(reset_all(token2))
    run_asyncio_task(reset_all(token3))
    run_asyncio_task(reset_all(token4))


# Create the main window
root = tk.Tk()
root.title("BNK-Client-60")

window_width = 650
window_height = 500
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
button_reset = tk.Button(root, text="Reset", command=lambda: multi_token_reset(), bg="grey")
button_reset.place(relx=0.5, rely=0.05, anchor="center")

# First line: Buy, SL
button_buy = tk.Button(left_frame, text="Buy", command=lambda: multi_token("Buy_CE"), bg="green")
button_buy.grid(row=1, column=1, padx=10, pady=10)

button_sell = tk.Button(left_frame, text="SL", command=lambda: multi_token("Sell_CE"), bg="red")
button_sell.grid(row=1, column=3, padx=10, pady=10)

# Second line: S1, S2, 
button_s1 = tk.Button(left_frame, text="S1", command=lambda: multi_token("CE_Sell_1"), bg="orange")
button_s1.grid(row=2, column=1, padx=10, pady=10)

button_s2 = tk.Button(left_frame, text="S2", command=lambda: multi_token("CE_Sell_2"), bg="orange")
button_s2.grid(row=2, column=2, padx=10, pady=10)

button_s3 = tk.Button(left_frame, text="S3", command=lambda: multi_token("CE_Sell_3"), bg="orange")
button_s3.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(left_frame, text="EXIT", command=lambda: multi_token("CE_Exit"), bg="blue")
button_exit.grid(row=3, column=2, padx=10, pady=10)

#Fourth Line
button_add_ce = tk.Button(left_frame, text="LT+1", command=lambda: multi_token("CE_Lot1"), bg="yellow")
button_add_ce.grid(row=4, column=1, padx=10, pady=10)

button_exit_ce = tk.Button(left_frame, text="EXIT LT1", command=lambda: multi_token("CE_Lot1_Exit"), bg="blue")
button_exit_ce.grid(row=4, column=3, padx=10, pady=10)

#Fifth Line
button_add_ce_1 = tk.Button(left_frame, text="LT+2", command=lambda: multi_token("CE_Lot2"), bg="yellow")
button_add_ce_1.grid(row=5, column=1, padx=10, pady=10)

button_exit_ce_1 = tk.Button(left_frame, text="EXIT LT2", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
button_exit_ce_1.grid(row=5, column=3, padx=10, pady=10)

# Response label for CE side
response_label_ce = tk.Label(left_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_ce.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

# Buttons for taking manual SL CE
label_nifty = tk.Label(left_frame, text="NIFTY", font=("Arial", 9))
label_nifty.grid(row=8, column=1, padx=10,pady=10)

nftsl = tk.Entry(left_frame,width=10)
nftsl.grid(row=8, column=2, padx=10,pady=10)

btn_add = tk.Button(left_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=8, column=3, padx=10, pady=10)

btn_exit = tk.Button(left_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=8, column=4, padx=10, pady=10)

label_bnknifty = tk.Label(left_frame, text="B.NIFTY", font=("Arial", 9))
label_bnknifty.grid(row=9, column=1, padx=10,pady=10)

bnftsl = tk.Entry(left_frame,width=10)
bnftsl.grid(row=9, column=2, padx=10,pady=10)

btn_add = tk.Button(left_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=9, column=3, padx=10, pady=10)

btn_exit = tk.Button(left_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=9, column=4, padx=10, pady=10)

label_finnifty = tk.Label(left_frame, text="F.NIFTY", font=("Arial", 9))
label_finnifty.grid(row=10, column=1, padx=10,pady=10)

fnftsl = tk.Entry(left_frame,width=10)
fnftsl.grid(row=10, column=2, padx=10,pady=10)

btn_add = tk.Button(left_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=10, column=3, padx=10, pady=10)

btn_exit = tk.Button(left_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=10, column=4, padx=10, pady=10)

# #######PE Side buttons below

# First line: Buy, Sell
button_buy = tk.Button(right_frame, text="Buy", command=lambda: multi_token("Buy_PE"), bg="green")
button_buy.grid(row=1, column=1, padx=10, pady=10)

button_sell = tk.Button(right_frame, text="SL", command=lambda: multi_token("Sell_PE"), bg="red")
button_sell.grid(row=1, column=4, padx=10, pady=10)

# Second line: S1, S2
button_s1 = tk.Button(right_frame, text="S1", command=lambda: multi_token("PE_Sell_1"), bg="orange")
button_s1.grid(row=2, column=1, padx=10, pady=10)

button_s2 = tk.Button(right_frame, text="S2", command=lambda: multi_token("PE_Sell_2"), bg="orange")
button_s2.grid(row=2, column=2, padx=10, pady=10)

button_s3 = tk.Button(right_frame, text="S3", command=lambda: multi_token("PE_Sell_3"), bg="orange")
button_s3.grid(row=2, column=3, padx=10, pady=10)

# Third line: EXIT
button_exit = tk.Button(right_frame, text="EXIT", command=lambda: multi_token("PE_Exit"), bg="blue")
button_exit.grid(row=3, column=2, padx=10, pady=10)

# Fourth Line: LT+1 Exit LT1

button_add_pe = tk.Button(right_frame, text="LT+1", command=lambda: multi_token("PE_Lot1"), bg="yellow")
button_add_pe.grid(row=4, column=1, padx=10, pady=10)

button_exit_pe = tk.Button(right_frame, text="EXIT_LT1", command=lambda: multi_token("PE_Lot1_Exit"), bg="blue")
button_exit_pe.grid(row=4, column=3, padx=10, pady=10)

#Fift line LT+2 EXIT_LT2
button_add_pe_1 = tk.Button(right_frame, text="LT+2", command=lambda: multi_token("PE_Lot2"), bg="yellow")
button_add_pe_1.grid(row=5, column=1, padx=10, pady=10)

button_exit_pe_1 = tk.Button(right_frame, text="EXIT_LT2", command=lambda: multi_token("PE_Lot2_Exit"), bg="blue")
button_exit_pe_1.grid(row=5, column=3, padx=10, pady=10)

# Response label for PE side
response_label_pe = tk.Label(right_frame, text="", fg="blue", wraplength=400, justify="left")
response_label_pe.grid(row=6, column=1, columnspan=5, padx=10, pady=10)

# Buttons for taking manual SL PE
label_nifty = tk.Label(right_frame, text="NIFTY", font=("Arial", 9))
label_nifty.grid(row=8, column=1, padx=10,pady=10)

nftsl = tk.Entry(right_frame,width=10)
nftsl.grid(row=8, column=2, padx=10,pady=10)

btn_add = tk.Button(right_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=8, column=3, padx=10, pady=10)

btn_exit = tk.Button(right_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=8, column=4, padx=10, pady=10)

label_bnknifty = tk.Label(right_frame, text="B.NIFTY", font=("Arial", 9))
label_bnknifty.grid(row=9, column=1, padx=10,pady=10)

bnftsl = tk.Entry(right_frame,width=10)
bnftsl.grid(row=9, column=2, padx=10,pady=10)

btn_add = tk.Button(right_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=9, column=3, padx=10, pady=10)

btn_exit = tk.Button(right_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=9, column=4, padx=10, pady=10)

label_finnifty = tk.Label(right_frame, text="F.NIFTY", font=("Arial", 9))
label_finnifty.grid(row=10, column=1, padx=10,pady=10)

fnftsl = tk.Entry(right_frame,width=10)
fnftsl.grid(row=10, column=2, padx=10,pady=10)

btn_add = tk.Button(right_frame, text="Add", command=lambda: multi_token("CE_Lot2"), bg="yellow")
btn_add.grid(row=10, column=3, padx=10, pady=10)

btn_exit = tk.Button(right_frame, text="RST", command=lambda: multi_token("CE_Lot2_Exit"), bg="blue")
btn_exit.grid(row=10, column=4, padx=10, pady=10)

# UN_Exit button
button_u_exit = tk.Button(root, text="U.Exit", command=lambda: multi_token("UN_Exit"), bg="grey")
button_u_exit.place(relx=0.5, rely=0.95, anchor="center")

# Run the application
root.mainloop()
