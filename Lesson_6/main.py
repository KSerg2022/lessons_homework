'''This code finds the longest word in the given text file and outputs its length.
And also displays all words that have such a length.'''
import re


def check_file_txt(file_txt):
    try:
        open(file_txt, mode='rt').readline()
    except UnicodeDecodeError:
        print('App can use only text files')
    except FileNotFoundError:
        print('File not found.')
        exit()


def search_longest_word(words: list) -> list:
    words.sort(key=lambda x: len(x), reverse=True)
    return words[0]


def find_all_longest_words(words: list, longest_word: list) -> list:
    return [word for word in words if len(word) == len(longest_word)]


def main():
    working_file = 'example.txt'
    check_file_txt(working_file)

    with open(working_file) as f:
        file = f.read()

        all_words = re.findall(r'\w+', file)

        longest_word = search_longest_word(all_words)
        print(f'Longest word in file is "{longest_word}" and it has {len(longest_word)} chars.')

        all_longest_words = find_all_longest_words(all_words, longest_word)
        print(f'\nWe have {len(all_longest_words)} words with length {len(longest_word)} chars are:\n' +
              '\n'.join(map(str, all_longest_words)))


if __name__ == '__main__':
    main()
