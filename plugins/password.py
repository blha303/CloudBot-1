import string
import random as std_random

from cloudbot import hook


try:
    from Crypto.Random import random

    gen = random.StrongRandom()
except ImportError:
    # Just use the regular random module, not the strong one
    gen = std_random.SystemRandom()

with open("data/password_words.txt") as f:
    common_words = [line.strip() for line in f.readlines()]


@hook.command(autohelp=False)
def password(text, notice):
    """[length [types]] - generates a password of <length> (default 10). [types] can include 'alpha', 'no caps',
    'numeric', 'symbols' or any combination: eg. 'numbers symbols'"""
    okay = []

    # find the length needed for the password
    numb = text.split(" ")

    try:
        length = int(numb[0])
    except ValueError:
        length = 12

    # add alpha characters
    if "alpha" in text or "letter" in text:
        okay += list(string.ascii_lowercase)
        # adds capital characters if not told not to
        if "no caps" not in text:
            okay += list(string.ascii_uppercase)

    # add numbers
    if "numeric" in text or "number" in text:
        okay += list(string.digits)

    # add symbols
    if "symbol" in text or "special" in text:
        sym = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '=', '_', '+', '[', ']', '{', '}', '\\', '|', ';',
               ':', "'", '.', '>', ',', '<', '/', '?', '`', '~', '"']
        okay += sym

    # defaults to lowercase alpha + numbers password if the okay list is empty
    if not okay:
        okay = list(string.ascii_lowercase) + list(string.digits)

    # extra random lel
    random.shuffle(okay)
    chars = random.sample(okay, length)

    pw = "".join(chars)
    notice(pw)


@hook.command("wpass", "wordpass", "wordpassword", autohelp=False)
def word_password(text, notice):
    """[length] - generates an easy to remember password with [length] (default 4) commonly used words"""
    if text:
        try:
            length = int(text)
        except ValueError:
            notice("Invalid input '{}'".format(text))
            return
    else:
        length = 4
    words = []
    # generate password
    for x in range(length):
        words.append(gen.choice(common_words))

    notice("Your password is '{}'. Feel free to remove the spaces when using it.".format(" ".join(words)))

