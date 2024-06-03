import asyncio
import aiohttp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from threading import Thread

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

class TradeLayout(BoxLayout):
    def __init__(self, loop, **kwargs):
        super().__init__(**kwargs)
        self.loop = loop

    def button_action(self, action):
        asyncio.run_coroutine_threadsafe(self.send_post_request(action), self.loop)
        Clock.schedule_once(lambda dt: asyncio.run_coroutine_threadsafe(self.reset_action(action), self.loop), 5)

    def reset_all(self):
        actions = [
            "Buy_CE", "Sell_CE", "CE_Sell_1", "CE_Sell_2", "CE_Sell_3", "CE_Exit", "CE_Lot", "CE_Lot_1",
            "Buy_PE", "Sell_PE", "PE_Sell_1", "PE_Sell_2", "PE_Sell_3", "PE_Exit", "PE_Lot", "PE_Lot_1", "UN_Exit"
        ]
        asyncio.run_coroutine_threadsafe(self.send_reset_all_requests(actions), self.loop)

    async def send_reset_all_requests(self, actions):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request_reset(session, action) for action in actions])
        response_message = "All buttons reset to value 0."
        Clock.schedule_once(lambda dt: self.update_label('response_label_ce', response_message))
        Clock.schedule_once(lambda dt: self.update_label('response_label_pe', response_message))

    async def send_post_request(self, action):
        data = {
            "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
            "key": action,
            "value": "1"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(WEBHOOK_URL, json=data) as response:
                    if response.status == 200:
                        response_message = f"Success: {action}"
                    else:
                        response_message = f"Failed: {action} with status code {response.status}"
        except Exception as e:
            response_message = f"Exception: {e}"

        if "CE" in action:
            Clock.schedule_once(lambda dt: self.update_label('response_label_ce', response_message))
            Clock.schedule_once(lambda dt: self.update_label('response_label_pe', ""))
        else:
            Clock.schedule_once(lambda dt: self.update_label('response_label_pe', response_message))
            Clock.schedule_once(lambda dt: self.update_label('response_label_ce', ""))

    async def reset_action(self, action):
        data = {
            "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
            "key": action,
            "value": "0"
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(WEBHOOK_URL, json=data) as response:
                    if response.status == 200:
                        response_message = f"Reset: {action}"
                    else:
                        response_message = f"Failed: {action} with status code {response.status}"
        except Exception as e:
            response_message = f"Exception: {e}"

        if "CE" in action:
            Clock.schedule_once(lambda dt: self.update_label('response_label_ce', response_message))
            Clock.schedule_once(lambda dt: self.update_label('response_label_pe', ""))
        else:
            Clock.schedule_once(lambda dt: self.update_label('response_label_pe', response_message))
            Clock.schedule_once(lambda dt: self.update_label('response_label_ce', ""))

    async def send_post_request_reset(self, session, action):
        data = {
            "auth-token": "f18769ad-818c-41c6-929d-7f1608730000",
            "key": action,
            "value": "0"
        }
        try:
            async with session.post(WEBHOOK_URL, json=data) as response:
                if response.status == 200:
                    response_message = f"Reset: {action}"
                else:
                    response_message = f"Failed: {action} with status code {response.status}"
        except Exception as e:
            response_message = f"Exception: {e}"

    def update_label(self, label_id, text):
        self.ids[label_id].text = text

class TradeApp(App):
    def build(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.trade_layout = TradeLayout(loop=self.loop)
        self.thread = Thread(target=self.run_loop)
        self.thread.start()
        return self.trade_layout

    def run_loop(self):
        self.loop.run_forever()

    def on_stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

if __name__ == "__main__":
    TradeApp().run()
