from runners.selenium_bot_ru import SeleniumBotRU
from runners.selenium_bot_fr import SeleniumBotFR
from console_example.wordle_console import WordleConsole


if __name__ == '__main__':
    WordleConsole(5, w='спурт', v=True).solve()
    SeleniumBotRU().solve_daily()
    SeleniumBotFR().solve_daily()
