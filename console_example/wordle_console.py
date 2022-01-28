from random import sample
from termcolor import cprint


n = 5
dct = set(line.rstrip() for line in open('dictionaries/dictionary_ru.txt', encoding='utf-8') if len(line.rstrip()) == n)
letters = sorted(list(set(open('dictionaries/dictionary_ru.txt', encoding='utf-8').read())))
letters.remove('\n')


class WordleConsole:
    def __init__(self, n, w=None, v=False):
        self.n = n
        self.word = sample(dct, 1)[0] if w is None else w  # w=... - use given word
        self.guess = '?' * n

        self.turn = 0
        self.v = v  # verbose output

        self.good_letters = set()
        self.bad_letters = set()
        self.new_letters = set(letters)

        self.restricted_positions = dict()

        self.words = sorted(list(dct))
        self.suitable_words = self.words.copy()

        self.count_stat_letters()

        print(self.word)

    def count_stat_letters(self):
        self.stat_letters = {l: 0 for l in self.new_letters}
        for w in self.suitable_words:
            for ch in w:
                if ch in self.new_letters:
                    self.stat_letters[ch] += 1

    def best_word_by_new_letters(self):
        best_scores = [0 for _ in range(self.n + 1)]
        best_words = [None for _ in range(self.n + 1)]

        # choose strategy - find the most of new letters or try to guess the word
        wrds = self.words if len(self.suitable_words) >= 13 and len(self.good_letters) <= 2 else self.suitable_words

        for w in wrds:
            score = 0
            used_letters = 0
            for i, ch in enumerate(w):
                if ch in self.stat_letters:
                    score += self.stat_letters[ch]
                if ch not in self.new_letters or ch in w[:i]:
                    used_letters += 1

            if best_words[used_letters] is None or best_scores[used_letters] < score:
                best_scores[used_letters] = score
                best_words[used_letters] = w

        for i in range(self.n + 1):
            if best_words[i] is not None:
                return best_words[i]

    def remove_unsuitable_words(self):
        for w in self.suitable_words.copy():
            is_suitable = True
            for i, ch in enumerate(w):
                if ch in self.bad_letters or (self.guess[i] != '?' and ch != self.guess[i]) or \
                   (ch in self.restricted_positions and i in self.restricted_positions[ch]):
                    is_suitable = False
                    break

            if is_suitable:
                for ch in self.good_letters:
                    if ch not in w:
                        is_suitable = False
                        break

            if not is_suitable:
                self.suitable_words.remove(w)

    def print(self, w):
        for i, ch in enumerate(w):
            if ch not in self.word:
                cprint(f'{ch}', 'white', f'on_grey', attrs=['bold'], end='')
            elif ch == self.word[i]:
                cprint(f'{ch}', 'grey', f'on_green', attrs=['bold'], end='')
            else:
                cprint(f'{ch}', 'grey', f'on_yellow', attrs=['bold'], end='')

        print(' ' + str(self.turn))

    def make_move(self):
        self.turn += 1
        w = self.best_word_by_new_letters()
        self.print(w) #
        self.words.remove(w)

        for i, ch in enumerate(w):
            if ch in self.new_letters:
                self.new_letters.remove(ch)

            if ch in self.word:
                self.good_letters.add(ch)
                if ch == self.word[i]:
                    self.guess = self.guess[:i] + ch + self.guess[i + 1:]
                else:
                    if ch not in self.restricted_positions:
                        self.restricted_positions[ch] = {i}
                    else:
                        self.restricted_positions[ch].add(i)

            else:
                self.bad_letters.add(ch)

        self.remove_unsuitable_words()
        if self.v:
            print(f'{len(self.suitable_words)}:', *self.suitable_words)

    def solve(self):
        while self.guess.count('?') > 0:
            self.make_move()
