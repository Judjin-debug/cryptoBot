import telebot.types
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        flag = False
        error_msg = []

        if quote == base:
            flag = True
            error_msg.append(f"Can't convert the same currencies {base}")

        if quote not in keys:
            flag = True
            error_msg.append(f"Currency {quote} to convert from isn't listed")

        if base not in keys:
            flag = True
            error_msg.append(f"Currency {base} to convert to isn't listed")

        try:
            num_amount = float(amount)
            if num_amount < 0:
                flag = True
                error_msg.append(f'Amount {amount} is a negative number')
        except ValueError:
            flag = True
            error_msg.append(f"Amount {amount} isn't a number or not an acceptable number")

        if flag:
            error_msg = "; ".join(error_msg)
            raise APIException(error_msg)
        else:
            return (quote, base, amount)