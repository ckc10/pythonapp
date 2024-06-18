import asyncio
import aiohttp
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.textinput import TextInput

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

token1 = "f18769ad-818c-41c6-929d-7f1608730000"
token2 = "f18769ad-818c-41c6-929d-7f1608730000"
token3 = "f18769ad-818c-41c6-929d-7f1608730000"
token4 = "f18769ad-818c-41c6-929d-7f1608730000"

tokens = [token1, token2, token3, token4]

class BankNiftyClientApp(App):
    response_label_ce_text = StringProperty("")
    response_label_pe_text = StringProperty("")
    stopLoss = ObjectProperty(None)

    async def send_post_request(self, session, token, action, value):
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

        wrapped_response = "\n".join(textwrap.wrap(response_message, width=50))

        if "CE" in action:
            self.response_label_ce_text = wrapped_response
            self.response_label_pe_text = ""
        else:
            self.response_label_pe_text = wrapped_response
            self.response_label_ce_text = ""

    async def reset_all(self, token):
        actions = ["Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2", "CE_Sell_3", "CE_Exit", "CE_Lot1_Exit", "CE_Lot2_Exit", "CE_Lot1", "CE_Lot2",
                   "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2", "PE_Sell_3", "PE_Exit", "PE_Lot1_Exit", "PE_Lot2_Exit", "PE_Lot1", "PE_Lot2", "UN_Exit"]
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request(session, token, action, "0") for action in actions])
        response_message = "All buttons reset to value 0."
        self.response_label_ce_text = response_message
        self.response_label_pe_text = response_message

    async def manual_sl(self, action, value):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request(session, token, action, value) for token in tokens])

    async def multi_token(self, action):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request(session, token, action, "1") for token in tokens])

    async def multi_token_reset(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.reset_all(token) for token in tokens])

    def run_asyncio_task(self, task):
        asyncio.run(task)

    def build(self):
        return BankNiftyClient()

class BankNiftyClient(TabbedPanel):
    pass

if __name__ == "__main__":
    BankNiftyClientApp().run()