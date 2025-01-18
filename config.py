from dotenv import load_dotenv
import os

load_dotenv()

# полезная нагрузка для функции клейма, первоначально нужно настроить вручную, запрос для автообновления не вытащил
payload: dict = {
                    "game_state": {
                                    "refferals":29,
                                    "inviter":None,
                                    "village":"85691.village.hot.tg",
                                    "last_claim": 1737198242044833300,
                                    "firespace": 2,
                                    "boost": 14,
                                    "storage": 22,
                                    "balance": 58262262
                                }
                }

claim_period = 4 # переодичность клейма в часах


# Заголовки запроса с jwt-токеном авторизации и telegram-data
headers: dict = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
                    'Content-Type': 'application/json',
                    "Authorization": f"{os.getenv('HOT_TOKEN', 'default_token_if_not_set')}",
                    "Telegram-Data": f"user={os.getenv('TELEGRAM_DATA')}",
                }