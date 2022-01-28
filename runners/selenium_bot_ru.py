from misc.languages import Language
from runners.selenium_bot import SeleniumBot
from misc.letter_status import LetterStatus
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBotRU(SeleniumBot):
    link = 'https://wordle.belousov.one/'
    lang = Language.RU.value

    keyboard_selector = '.container.w-full.flex-col'
    rows_selector = '.grid-cols-5'
    letters_selector = '.react-card-back > div'
    game_finished_selector = 'h3'

    letter_key_attr = 'aria-label'
    enter_value = 'ввод'
    backspace_value = 'Удалить букву'

    def __init__(self):
        SeleniumBot.__init__(self)

        self.close_help_selector = 'button.top-0'

        self.letter_absent_class = 'bg-absent'
        self.letter_present_class = 'bg-present'
        self.letter_correct_class = 'bg-correct'

    def begin(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.close_help_selector))).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.rows_selector)))

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
