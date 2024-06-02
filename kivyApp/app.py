import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests
import textwrap

kivy.require('2.3.0')

# Webhook URL
WEBHOOK_URL = 'https://api.tradetron.tech/api/'

class MainApp(App):

    def build(self):
        layout = MainLayout()
        return layout

    def send_post_request(self, action, response_label_to_show, response_label_to_hide):
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
        response_label = self.root.ids[response_label_to_show]
        response_label.text = wrapped_response

        # Hide the other response label
        other_response_label = self.root.ids[response_label_to_hide]
        other_response_label.text = ""

class MainLayout(BoxLayout):
    pass

if __name__ == "__main__":
    MainApp().run()
