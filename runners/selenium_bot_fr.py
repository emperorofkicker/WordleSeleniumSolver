from misc.languages import Language
from runners.selenium_bot import SeleniumBot
from misc.letter_status import LetterStatus
from misc.input_types import InputType
from selenium.webdriver.common.by import By


class SeleniumBotFR(SeleniumBot):
    link = 'https://wordle.louan.me/'
    lang = Language.FR.value

    keyboard_selector = '.keyboard'
    rows_selector = '.attempt'
    letters_selector = '.has-letter'
    game_finished_selector = 'h2'

    letter_status_attr = 'data-state'
    enter_value = 'enter'
    backspace_value = 'backspace'

    def __init__(self):
        SeleniumBot.__init__(self)

        self.letter_absent_class = 'incorrect'
        self.letter_present_class = 'partial'
        self.letter_correct_class = 'correct'

        # both input types are supported
        self.input_type = InputType.KEYBOARD
        # self.input_type = InputType.MOUSE

        self.service_symbols_selector = '.azerty'  # enter - [0], backspace - [1]

    def click_keyboard(self, ch):
        if ch == self.enter_value:
            self.driver.find_elements(By.CSS_SELECTOR, self.service_symbols_selector)[0].click()
        elif ch == self.backspace_value:
            self.driver.find_elements(By.CSS_SELECTOR, self.service_symbols_selector)[1].click()
        else:
            self.driver.find_element_by_xpath(f'//*[@id="key" and contains(text(), "{ch.upper()}")]').click()

    def get_letter_status(self, letter):
        classes = letter.get_attribute('class').split()
        if self.letter_absent_class in classes:
            return LetterStatus.ABSENT
        elif self.letter_present_class in classes:
            return LetterStatus.PRESENT
        elif self.letter_correct_class in classes:
            return LetterStatus.CORRECT
        else:
            return LetterStatus.UNCHECKED

    def is_solved(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, self.game_finished_selector)) > 0
