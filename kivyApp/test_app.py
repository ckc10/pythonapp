import asyncio
import aiohttp
import textwrap
import json
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
# from kivy.uix.label import Label
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
# from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
# from kivy.uix.filechooser import FileChooserIconView

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'


def setToken(index):
    tokens =[]
    if index == 'BNFT':
        tokens = BN_tokens
    elif index == 'NFT':
        tokens = NFT_tokens
    elif index == 'FNFT':
        tokens = FNFT_tokens
    elif index == 'Sensex':
        tokens = Sensex_tokens
    elif index == 'MNFT':
        tokens = MNFT_tokens

    return tokens        


  
class TradeOption(App):
    response_label_ce_text = StringProperty("")
    response_label_pe_text = StringProperty("")
    response_label_token_text = StringProperty("")
    
    

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

#app.run_asyncio_task(app.manual_sl('BNF_CE_SL', ce_sl_input.text,index='BNFT'))
    async def manual_sl(self, action, value,index):
        tokens = setToken(index)
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request(session, token, action, value) for token in tokens])

    async def multi_token(self, action,index):
        tokens= setToken(index)
        
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.send_post_request(session, token, action, "1") for token in tokens])
            await asyncio.sleep(3)  # Wait for 3 seconds
            await asyncio.gather(*[self.send_post_request(session, token, action, "0") for token in tokens])

    async def multi_token_reset(self,index):
        tokens = setToken(index)
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*[self.reset_all(token) for token in tokens])

    def run_asyncio_task(self, task):
        asyncio.run(task)

    # def getTokens(self,tokenvalue,index):
    #     if index == 'BNFT':
    #         BN_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to Bank Nifty token array"
    #         self.root.ids.bnf_token_input.text =''
    #         print(BN_tokens)
    #     elif index == 'NFT':
    #         NFT_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to  Nifty token array"
    #         self.root.ids.nft_token_input.text=''
    #     elif index == 'FNFT':
    #         FNFT_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to Fin Nifty token array"
    #         self.root.ids.fnft_token_input.text =''
    #     elif index == 'Sensex':
    #         Sensex_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to Sensex array"
    #         self.root.ids.snx_token_input.text =''
    #     elif index == 'MNFT':
    #         MNFT_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to Mid Cap Nifty token array"
    #         self.root.ids.mnft_token_input.text =''
    #     elif index == 'HeroZero':
    #         HeroZero_tokens.append(tokenvalue)
    #         self.response_label_token_text = f"Token added to HEroZero token array"
    #         self.root.ids.hz_token_input.text =''    

    def load_json(self, path, filename):
        if filename:
            filepath = filename[0]  #path + '/' + 
            self.process_json_file(filepath)

    def process_json_file(self, filepath):
        global BN_tokens, NFT_tokens, FNFT_tokens, Sensex_tokens, MNFT_tokens
        with open(filepath, 'r') as file:
            try:
                data = json.load(file)
                BN_tokens = data.get('BNFT', [])
                NFT_tokens = data.get('NFT', [])
                FNFT_tokens = data.get('FNFT', [])
                Sensex_tokens = data.get('Sensex', [])
                MNFT_tokens = data.get('MNFT', [])
                self.response_label_token_text = "Tokens loaded from JSON file successfully."
                self.root.ids.token_label.text=f'Loaded tokens from file are\nBNFT:{BN_tokens}\nNFT:{NFT_tokens}\nFNFT:{FNFT_tokens}\nMNFT:{MNFT_tokens}\nSensex:{Sensex_tokens}'
            except json.JSONDecodeError as e:
                self.response_label_token_text = f"Error loading JSON file: {e}"

    
        self.response_label_token_text = "Tokens loaded from JSON file."

    def build(self):
        return TradeAppUI()

class TradeAppUI(TabbedPanel):
    def build(self):
        self.root = Builder.load_file("TradeOption.kv")
        return self.root

if __name__ == "__main__":
    TradeOption().run()