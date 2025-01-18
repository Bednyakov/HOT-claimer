import time
import requests
from random import randint

from core.log import logger
from config import headers, payload, claim_period



class HotWallet:

    def __init__(self) -> None:

        self.url: str = "https://api0.herewallet.app/api/v1/user/hot/claim"

        self.headers: dict = headers

        self.data: dict = payload

        self.referrals_id: list = []

        self.hot_periodicity: int = claim_period


    def hot_status(self) -> dict | None:
        """
        Функция обновления данных в Hotwallet.
        """

        data: dict = self.data
        url: str = "https://api0.herewallet.app/api/v1/user/hot/claim/status"

        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 200:
            logger.info(f"Update Hot data. Status code: {response.status_code }")
            try:
                values = response.json()
                self.data['game_state']['last_claim'] = values['last_offchain_claim']
                self.data['game_state']['balance'] = values['hot_in_storage']
                referrals = self.get_referrals()
                self.data['game_state']["refferals"] = referrals["total_referals"]
                return self.data
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")

        logger.error(f"Ошибка при отправке POST-запроса на обновление Hot data: {response.status_code, response.text}")


    def get_referrals(self) -> dict | None:
        """
        Функция обновления числа и списка рефералов.
        """
        url: str = "https://api0.herewallet.app/api/v1/user/hot/referrals"

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            try:
                values = response.json()
                total_referrals = values["total_referrals"]

                referrals_id = []

                for referral in values["referrals"]:
                    referrals_id.append(referral["near_account_id"])
                self.referrals_id = referrals_id

                logger.info(f"Total referrals in HOT: {total_referrals}")
                return {"total_referals": total_referrals, "referals_id": referrals_id}
            
            except ValueError as e:
                logger.error(f"Ответ не в формате JSON: {e}")

        logger.error(f"Ошибка при отправке GET-запроса на обновление рефералов: {response.status_code, response.text}")


    def notification(self) -> None:
        """
        Функция уведомления рефералов.
        """
        url: str = "https://api0.herewallet.app/api/v1/user/hot/notification"
        count: int = 0

        for id in self.referrals_id:

            data = {"friend_account_id": id}
            response = requests.post(url, headers=self.headers, json=data)     

            if response.status_code == 200:
                count += 1

        logger.info(f"{count} referrals notification.")


    def claim(self, url_res: str, headers_res: dict, data: dict = None) -> None:
        """
        Функция для отправки POST-запроса синхронизации и клейма монет.
        """
        with requests.Session() as session:

            response = session.post(url=url_res, headers=headers_res, json=data)

            if response.status_code == 200:
                logger.info(f"Claim {url_res[8:]} Status code: {response.status_code }")

                try:
                    data =  response.json()
                    return data
                except ValueError as e:
                    logger.error(f"Ответ не в формате JSON: {e}")
            
            logger.error(f"Ошибка при отправке POST-запроса на клейм: {response.status_code, response.text}")


    def run_hot_claim(self):
        """
        Функции клейма HOT.
        """
        hot_claim_time = time.time()

        hot_periodicity = self.hot_periodicity

        while True:
            try:
                current_time = time.time()
                one_hour = randint(3600, 3900)

                if current_time >= hot_claim_time:
                    data = self.hot_status()
                    result = self.claim(self.url, self.headers, data)
                    balance = result['hot_in_storage']
                    logger.info(f'HOT Wallet balance: {balance}')
                    self.notification()
                    hot_claim_time = current_time + hot_periodicity * one_hour

                time.sleep(600)
            except Exception as e:
                logger.error(e)


if __name__ == "__main__":
    my_hot = HotWallet()
    my_hot.run_hot_claim()