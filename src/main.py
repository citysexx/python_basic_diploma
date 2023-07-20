from src.bin.telegramapi import bot


if __name__ == '__main__':
    print('Bot is running...')
    bot.infinity_polling()
    print('Bot has been stopped.')
