from misc.letter_status import LetterStatus


class Solver:
    def __init__(self, n, limit, lang, v=False):
        self.n = n
        self.lang = lang
        self.guess = '?' * n

        self.dct = set(line.rstrip() for line in open(f'dictionaries/dictionary_{lang}.txt', encoding='utf-8') \
                       if len(line.rstrip()) == n and not line.startswith('#'))
        self.letters = sorted(list(set(open(f'dictionaries/dictionary_{lang}.txt', encoding='utf-8').read())))
        self.letters.remove('\n')
        if '#' in self.letters:
            self.letters.remove('#')  # symbol for "deleting" words with proper len which are not in game dictionary

        self.turn = 0
        self.limit = limit  # available turns number
        self.v = v  # verbose output

        self.good_letters = set()
        self.bad_letters = set()
        self.new_letters = set(self.letters)

        self.restricted_positions = dict()

        self.words = sorted(list(self.dct))
        self.suitable_words = self.words.copy()

        self.count_stat_letters()

    # count frequencies of letters that haven't been checked yet
    def count_stat_letters(self):
        self.stat_letters = {l: 0 for l in self.new_letters}
        for w in self.suitable_words:
            for ch in w:
                if ch in self.new_letters:
                    self.stat_letters[ch] += 1

    def best_word(self):
        best_scores = [0 for _ in range(self.n + 1)]
        best_words = [None for _ in range(self.n + 1)]

        # choose strategy - find the most of new letters or try to guess the word
        explore_new_letters = len(self.suitable_words) >= 13 and len(self.good_letters) <= 2

        for w in (self.words if explore_new_letters else self.suitable_words):
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
                if best_words[i] in self.suitable_words:
                    self.suitable_words.remove(best_words[i])
                self.words.remove(best_words[i])
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

    def update_information_about_word(self, w, ans):
        for i in range(self.n):
            if w[i] in self.new_letters:
                self.new_letters.remove(w[i])

            if ans[i] == LetterStatus.ABSENT:
                s = set(ans[j] for j in range(self.n) if w[j] == w[i])
                if len(s) == 1:
                    self.bad_letters.add(w[i])
            elif ans[i] == LetterStatus.CORRECT:
                self.good_letters.add(w[i])
                self.guess = self.guess[:i] + w[i] + self.guess[i + 1:]
            elif ans[i] == LetterStatus.PRESENT:
                self.good_letters.add(w[i])
                if w[i] not in self.restricted_positions:
                    self.restricted_positions[w[i]] = {i}
                else:
                    self.restricted_positions[w[i]].add(i)

        self.remove_unsuitable_words()
        self.count_stat_letters()

        if self.v:
            print(f'{len(self.suitable_words)}:', *self.suitable_words)
