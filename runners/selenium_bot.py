from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from misc.input_types import InputType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from misc.letter_status import LetterStatus
from selenium_solver.solver import Solver


class SeleniumBot:
    @property
    def link(self):
        raise NotImplementedError

    @property
    def lang(self):
        raise NotImplementedError

    @property
    def rows_selector(self):
        raise NotImplementedError

    @property
    def letters_selector(self):
        raise NotImplementedError

    @property
    def keyboard_selector(self):
        raise NotImplementedError

    @property
    def letter_key_attr(self):
        return None

    @property
    def game_finished_selector(self):
        raise NotImplementedError

    @property
    def enter_value(self):
        raise NotImplementedError

    @property
    def backspace_value(self):
        raise NotImplementedError

    def __init__(self):
        self.n = 5
        self.turn = 0
        self.limit = 6

        self.input_type = InputType.MOUSE  # default input type

        options = Options()
        options.add_argument("--start-maximized")  # works for Windows; mandatory for correct ActionChains work

        self.driver = webdriver.Chrome(options=options)

    def open(self):
        self.driver.get(self.link)

    def begin(self):
        pass

    def close(self):
        self.driver.close()

    def parse_letter_status(self, row, j):
        letter = row.find_elements(By.CSS_SELECTOR, self.letters_selector)[j]
        return self.get_letter_status(letter)

    def parse_ith_move(self, i):
        res = [None for _ in range(self.n)]
        row = self.driver.find_elements(By.CSS_SELECTOR, self.rows_selector)[i]
        for j in range(self.n):
            res[j] = self.parse_letter_status(row, j)

        return res

    def get_letter_status(self, letter):
        pass

    def is_solved(self):
        raise NotImplementedError

    def send_word_by_keyboard(self, w):
        ActionChains(self.driver).send_keys(w).send_keys(Keys.RETURN).perform()

    def send_word_by_mouse(self, w):
        for ch in w:
            self.click_keyboard(ch)

        self.click_keyboard(self.enter_value)

    def send_word(self, w):
        if self.input_type == InputType.KEYBOARD:
            self.send_word_by_keyboard(w)
        elif self.input_type == InputType.MOUSE:
            self.send_word_by_mouse(w)

    def click_keyboard(self, ch):
        self.driver.find_element(By.CSS_SELECTOR, f'[{self.letter_key_attr}="{ch}"]').click()

    def clear_word(self):
        for _ in range(self.n):
            self.click_keyboard(self.backspace_value)

    def solve_daily(self):
        try:
            self.open()
            self.begin()

            solver = Solver(self.n, self.limit, self.lang)
            while not self.is_solved() and self.turn < self.limit:
                w = solver.best_word()
                if w is None:
                    raise Exception("Hidden word not found in the dictionary!")
                self.send_word(w)
                ans = self.parse_ith_move(self.turn)
                if solver.v:
                    print(ans)
                if ans[0] != LetterStatus.UNCHECKED:
                    solver.update_information_about_word(w, ans)
                    sleep(2)
                    self.turn += 1
                else:
                    self.clear_word()

        finally:
            self.close()
