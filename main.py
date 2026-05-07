from nicegui import ui
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}"
CURRENCIES = ["USD", "EUR", "CAD", "AUD", "JPY", "BGN", "CZK", "DKK", "GBP", "HUF", "PLN", "RON", "SEK", "CHF"]

CACHE = {}
CACHE_TTL = 60  


def get_rates(base):
    now = time.time()

    if base in CACHE:
        data, timestamp = CACHE[base]
        if now - timestamp < CACHE_TTL:
            return data

    try:
        url = f"{BASE_URL}&base_currency={base}&currencies={','.join(CURRENCIES)}"
        res = requests.get(url)
        data = res.json()["data"]

        CACHE[base] = (data, now)
        return data

    except:
        return None






def swap():
    from_select.value, to_select.value = to_select.value, from_select.value
    convert()


def convert():
    ui.run_javascript('document.body.style.cursor="wait"')

    try:
        amount = float(amount_input.value or 0)

        rates = get_rates(from_select.value)
        if not rates:
            result.set_text("API Error")
            return

        rate = rates[to_select.value]
        converted = amount * rate

        
        result.set_text(f"{amount:.2f} {from_select.value} = {converted:.2f} {to_select.value}")

       

    except:
        result.set_text("Error")

    finally:
        ui.run_javascript('document.body.style.cursor="default"')



timer = None





dark_mode = ui.dark_mode()

def toggle_dark():
    dark_mode.toggle()



with ui.column().classes(
    'w-full h-screen items-center justify-center '
    'bg-gradient-to-br from-gray-100 to-gray-200 '
    'dark:from-gray-900 dark:to-gray-800'
):

    with ui.card().classes(
        'relative w-[420px] p-6 rounded-2xl shadow-2xl '
        'transition-all duration-300 hover:shadow-3xl '
        'dark:bg-gray-900 dark:text-white'
    ):

        
        ui.button('🌙', on_click=toggle_dark) \
            .props('flat round') \
            .classes('absolute right-3 top-3')

        
        ui.label('Currency Converter').classes(
            'text-2xl font-bold text-center mb-1'
        )
        ui.label('Live exchange rates').classes(
            'text-sm text-gray-500 dark:text-gray-400 text-center mb-6'
        )

        
        amount_input = ui.input('Amount') \
            .props('outlined') \
            .classes('w-full mb-4 text-lg')

        

        
        with ui.row().classes('items-center gap-3 w-full'):

            from_select = ui.select(CURRENCIES, value='USD') \
                .props('outlined') \
                .classes('w-24')

            ui.button('⇄', on_click=swap) \
                .props('flat round') \
                .classes(
                    'bg-gray-100 hover:bg-gray-200 '
                    'dark:bg-gray-800 dark:hover:bg-gray-700'
                )

            to_select = ui.select(CURRENCIES, value='EUR') \
                .props('outlined') \
                .classes('w-24')

        
        result = ui.label('0.00').classes(
            'text-3xl font-bold text-center mt-6 '
            'text-blue-600 dark:text-blue-400 transition-all'
        )

        ui.label('Converted amount').classes(
            'text-center text-gray-500 dark:text-gray-400 text-sm'
        )

    

        
        ui.button('Convert', on_click=convert) \
            .classes(
                'w-full mt-6 bg-blue-500 text-white rounded-xl py-2'
            ) \
            .props('push')

ui.run()