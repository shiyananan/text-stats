import re
import random
from string import punctuation, ascii_uppercase
import collections


# DOUBLE CHECKING
# сюда добавить, что если есть слово1&слово2, то автоматически сплит
# test_text = 'Alpha&Beta 15th of October 33parrots hel10 you're dogs' tales story:the beginning U.S.S.R.'
def check_spelling_errors(element):
    match_1 = re.match(r'([a-z]*)([\d]+|[\W]+|[_]+)([a-z]*)', element, re.I)

    ans = 'q'

    while ans.lower()[0] not in ('ynr'):
        if match_1:
            s = f'{match_1.group(2)} {match_1.group(3)}'
            if match_1.group(1):
                s = f'{match_1.group(1)} {s}'

            print(f'The word \'{element}\' seems strange. Did you mean \'{s}\'?')

            ans = input('y - yes / n - no, keep it as is / r - rewrite this word/s ')

            if ans.lower().lstrip().startswith('y'):
                a = [match_1.group(2), match_1.group(3)]
                if match_1.group(1):
                    a = [match_1.group(1)] + a
                return a
            elif ans.lower().lstrip().startswith('n'):
                return [element]
            elif ans.lower().lstrip().startswith('r'):
                return input('Enter the corrected word/s here: ').split()
            else:
                print('Wrong input. Please use y or n or r')
        else:
            print(f'The word \'{element}\' seems strange. Are you sure it\'s grammatically correct?')

            ans = input('y - yes / r - rewrite this word/s ')

            if ans.lower().lstrip().startswith('y'):
                return [element]
            elif ans.lower().lstrip().startswith('r'):
                return input('Enter the corrected word/s here: ').split()
            else:
                print('Wrong input. Please use y or r')


# CREATE A LIST OF ELEMENTS
def create_elements_list(text):
    text_els = []
    for x in text.split():
        if not x.rstrip(punctuation).isalpha() and not x.rstrip(punctuation).isdigit():
            text_els.extend(check_spelling_errors(x))
        else:
            text_els.append(x)
    return text_els


# LETTERS
def count_chars(text):
    count_letters = 0
    count_digits = 0
    count_punct = 0
    chars_count = {}
    for x in text.split():
        for y in x:
            if y.isalpha():
                count_letters += 1
            elif y.isdigit():
                count_digits += 1
            else:
                count_punct += 1

    letter_or_letters = '' if count_letters == 1 else 's'
    digit_or_digits = '' if count_digits == 1 else 's'
    mark_or_marks = '' if count_punct == 1 else 's'

    return f'There are {count_letters} letter{letter_or_letters}, {count_digits} digit{digit_or_digits} and {count_punct} punctuation mark{mark_or_marks} in this text.'


def calc_ltr_freq():
    global text
    calc_freq = {x: text.upper().count(x) for x in ascii_uppercase}
    max_freq_ltr = max(list(calc_freq.values()))
    most_freq = {k: v for k, v in calc_freq.items() if v == max_freq_ltr}
    return most_freq, calc_freq


def get_letter_stat(input_letter):
    global words_only
    letter_freq = freq_letters[1][input_letter]
    words_with_letter = [x for x in words_only if input_letter in x]
    wwl_upper = []
    for word in words_with_letter:
        the_word = "".join([char if char == input_letter else char.lower() for char in word])
        wwl_upper.append(the_word)

    time_or_times = 'once' if letter_freq == 1 else 'times'
    word_or_words = '' if len(words_with_letter) == 1 else 's'
    if letter_freq > 0:
        return f"""Letter '{input_letter}' is used {letter_freq} {time_or_times}.
Word{word_or_words} containing the letter: {', '.join(wwl_upper)}"""
    else:
        return f"""There"s no letter '{input_letter}' in this text."""


def count_words(words_only):
    counted_words = collections.Counter(words_only)
    max_words = max(counted_words.values())
    filt_most_fr_w = filter(lambda x: x[1] == max_words, counted_words.items())
    most_freq_words = ', '.join([f"'{k}'" for k, v in filt_most_fr_w])
    is_are = 'word is' if max(counted_words.values()) == 1 else 'words are'
    return 'All words are used only once.' if max(counted_words.values()) == 1 else f'The most frequently used {is_are}: {most_freq_words} ({max(counted_words.values())} times)'


def get_word_length():
    global words_only
    max_length = len(max(words_only, key=len))
    for i in range(max_length, 0, -1):
        same_length_words = [f"'{x}'" for x in words_only if len(x) == i]
        if not same_length_words:
            continue
        else:
            word_or_words = 's' if len(same_length_words) > 1 else ''
            same_amt = ', '.join(same_length_words)
            yield f"{i}-letter word{word_or_words}: {same_amt}"


def is_palindrome(words_only):
    pals = [x for x in words_only if x == x[::-1] and len(x)>1]
    return 'There are no palindromes in this text.' if len(pals) == 0 else f'\'{random.choice(pals).upper()}\' is a palindrome.'
#
#
# def longest_palin_substr(txt):
#     pass


def in_100(words_only):
    with open('100_words.txt', mode='r') as file:
        hund_words = [line.split()[0].upper() for line in file.readlines()]
        found_in_100 = sorted(list(set(hund_words) & set(sum([x.split("'") for x in words_only], []))))
        words_in_100 = ', '.join(["'" + x + "'" for x in found_in_100])
    is_are = 'is' if len(found_in_100) == 1 else 'are'

    return 'None of the words is in 100 most used English words.' if len(words_in_100) == 0 else f'{words_in_100} {is_are} among 100 most used English words.'



examples = ('When life gives you lemons, make lemonade. When life gives you a kidney, remember your mother.',
            'Float like a butterfly, sting like a bee. Do you want to have children?',
            'Big Brother is watching you. In the bedroom, in the bathroom, everywhere. I\'ve tried to hide my computer behind the bookshelf, but he knew. He\'s everywhere.',
            'Life is 10% what happens to us and 90% how we react to it. My reaction was: I\'m not going anywhere.',
            'Life is like a box of chocolate. When you eat too much, you get fat. When they freeze you, you die.')

print(f'''---This is a text statistics generator---
Enter your text to know everything about it, for example:
{random.choice(examples)}''')

text = input('Your text: ')

checked_els = create_elements_list(text)

words_only = [x.strip(punctuation).upper() for x in checked_els if x.upper() != x.lower()]
counted_chars = count_chars(text)
palindromes = is_palindrome(words_only)

for_random_facts = [is_palindrome(words_only), in_100(words_only)]

all_words_length = get_word_length()
freq_letters = calc_ltr_freq()
words_info = "\n".join(list(get_word_length()))

print(f'''---Text statistics:---
--Checked {checked_els}
--Words {words_only}
{counted_chars}

Word statistics:
There are {len(words_only)} words.
{count_words(words_only)}

{words_info}
Longest word: '{max(words_only, key=len)}', {len(max(words_only, key=len))} letters.
Shortest word: '{min(words_only, key=len)}', {len(min(words_only, key=len))} letters.
The average word length: 

Most frequently used letters: {', '.join(["'" + k.upper() + "'" for k in freq_letters[0]])} ({freq_letters[0].get(list(freq_letters[0].keys())[0])} times).
There are no letters {', '.join(["'" +  k.upper() + "'" for k, v in freq_letters[1].items() if v == 0])}.

Do you want to see the statistics of a specific letter?''')
letter_stat_for_user = 'idk'
while letter_stat_for_user.strip() not in ('YN'):
    letter_stat_for_user = input('y - yes / n - no ').upper()
    input_letter = 'a1*'
    if letter_stat_for_user.lstrip().startswith('Y'):
        input_letter = input('Please type in the letter: ').upper()
        while input_letter.strip() not in ascii_uppercase:
            input_letter = input('Wrong input. Please type in 1 letter: ').upper()
        else:
            print(get_letter_stat(input_letter))
            letter_stat_for_user = 'idk'
            print('Do you want to see the statistics of another letter?')

    elif letter_stat_for_user.lstrip().startswith('N'):
        print(f'''Ok, here's a random fact for you then:
{random.choice(for_random_facts)}''')
        break
    else:
        print('Wrong input. Please use y or n ')




#{int(count_chars.get('*', 0)/len(words_only))} letters.