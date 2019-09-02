"""
Home Work 2.

Structure:
- methods definitions;
- main function definiton.
"""

initial_text = """Python is an interpreted high-level programming language for general-purpose programming. Created by Guido van Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, notably using significant whitespace. It provides constructs that enable clear programming on both small and large scales.[27] In July 2018, Van Rossum stepped down as the leader in the language community after 30 years.[28][29]

Python features a dynamic type system and automatic memory management. It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural, and has a large and comprehensive standard library.[30]

Python interpreters are available for many operating systems. CPython, the reference implementation of Python, is open source software[31] and has a community-based development model, as do nearly all of Python's other implementations. Python and CPython are managed by the non-profit Python Software Foundation.

Python was conceived in the late 1980s[32] by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands as a successor to the ABC language (itself inspired by SETL)[33], capable of exception handling and interfacing with the Amoeba operating system.[7] Its implementation began in December 1989.[34] Van Rossum's long influence on Python is reflected in the title given to him by the Python community: Benevolent Dictator For Life (BDFL) – a post from which he gave himself permanent vacation on July 12, 2018.[35]"""

def task_1(string, result = None):
    """знайти кількість букв в тексті в розрізі:
       всього, верхній регістр, нижній регістр; результат записати до dict з ключами total, upper, lower."""
    string = string
    letters = {
	'total' : { 'letters' : [], 'counts' : 0 },
	'upper' : { 'letters' : [], 'counts' : 0 },
	'lower' : { 'letters' : [], 'counts' : 0 }
        }
    for letter in string:
        if letter.isalpha():
            letters['total']['letters'].append( letter )
            letters['total']['counts'] += 1
            if letter.isupper():
                letters['upper']['letters'].append( letter )
                letters['upper']['counts'] += 1
            else:
                letters['lower']['letters'].append( letter )
                letters['lower']['counts'] += 1
    return letters

def task_2(string, result = None):
    """знайти кількість по кожній букві в тексті; результат записати в list,
       де кожний елемент - це tuple(letter, count);"""
    string = string
    small_input_string = string.lower()
    all_small_letters = "abcdefghijklmnopqrstuvwxyz"
    letters = []
    for letter in all_small_letters:
        letters.append( (letter, small_input_string.count(letter) ) )
    return letters

def task_3(result):
    """сформувати list на основі list з п.2,
       в якому елементи відсортовані по кількості букв (від найменшої до найбільшої кількості);"""
    letters = result.copy()
    letters.sort( key = lambda letter: letter[1] )
    return letters

def make_words_and_numbers(string):
    """знайти загальну кількість слів в тексті, результат записати як int;
       знайти кількість чисел в тексті, результат записати як int;"""
    string = string
    inner_string = string.replace('[', ' ').replace(']', ' ').replace('\n', ' ').\
                   replace('(', ' ').replace(')', ' ').replace('–', ' ').\
                   replace('"', ' ').replace("'s", " ").replace('-', ' ')
    pre_words = inner_string.split(' ')
    
    words_and_numbers = {
            'words'   : { 'values' : [], 'counts' : 0 },
            'numbers' : { 'values' : [], 'counts' : 0 },
            'etc'     : { 'values' : [], 'counts' : 0 }
        }
    
    for pre_word in pre_words:
       word = pre_word.lstrip('.,-?!:;*/\n\t@$%&~"').rstrip('.,-?!:;*/\n\t@$%&~"')
       if len(word) > 0:
           if word.isalpha():
               words_and_numbers['words']['values'].append(word)
               words_and_numbers['words']['counts'] += 1
           elif word.isdigit():
               words_and_numbers['numbers']['values'].append(int(word))
               words_and_numbers['numbers']['counts'] += 1
           else:
               words_and_numbers['etc']['values'].append(word)
               words_and_numbers['etc']['counts'] += 1
       # voting: are "etc" members words or numbers
       if words_and_numbers['etc']['counts'] > 0:
           for i in range(words_and_numbers['etc']['counts']):
               alpha_counter = 0
               digit_counter = 0
               for j in range(len(words_and_numbers['etc']['values'][i])):
                   if words_and_numbers['etc']['values'][i][j].isalpha():
                       alpha_counter += 1
                   elif words_and_numbers['etc']['values'][i][j].isdigit():
                       digit_counter += 1
               if alpha_counter > digit_counter:
                   words_and_numbers['words']['values'].append( words_and_numbers['etc']['values'][i] )
                   words_and_numbers['words']['counts'] += 1
               else:
                   number_is = ''
                   for character in words_and_numbers['etc']['values'][i]:
                       if character.isdigit():
                           number_is += character
                   words_and_numbers['numbers']['values'].append( int(number_is) )
                   words_and_numbers['numbers']['counts'] += 1
           # clear "etc" members
           words_and_numbers['etc']['values'].clear()
           words_and_numbers['etc']['counts'] = 0
           
    return words_and_numbers

def task_4(words_and_numbers):
	"""знайти загальну кількість слів в тексті, результат записати як int;"""
	return words_and_numbers['words']['counts']

def task_5(words_and_numbers):
	"""знайти кількість чисел в тексті, результат записати як int;"""
	return words_and_numbers['numbers']['counts']

def task_6(words_and_numbers):
    """створити dict, де ключ - це довжина слова, а значення - це кількість слів з такою довжиною;"""
    words = words_and_numbers['words']['values'].copy()
    words.sort( key = lambda word: len(word) )
    
    words_length_and_quantity = {}

    # creating dictionary
    for prop in range( 1, len(words[len(words) - 1]) + 1 ):
        words_length_and_quantity[ prop ] = 0
    # counting words
    for word in words:
        words_length_and_quantity[ len(word) ] += 1
        
    return words_length_and_quantity

def task_7(string):
    """знайти відсоток речень, в яких зустрічається слово Python; результат записати як float (на 100 не множимо)."""
    string = string
    sentences = string.split(".")
    sentences_with_Python_word = 0
    for sentence in sentences:
        if sentence.count('Python') > 0:
            sentences_with_Python_word += 1
    return sentences_with_Python_word / float(len(sentences))
            
def task_8(string):
    """"знайти кількість спеціальних символів в тексті;
        результат записати до dict, де ключ - це спеціальний символ, а значення - кількість;"""
    string = string
    special_characters = ".,:;!?-*~@#$%^&()_+=|[]'–"
    special_characters_dict = {}
    for character in special_characters:
        # creating property and counting number of character
        special_characters_dict[ character ] = string.count( character )
    return special_characters_dict

def task_9(string):
    """створити list, в якому речення відсортовані по кількості букв в верхньому регістрі;"""
    string = string
    sentences = string.split(".")
    
    def evalFunc(string):
        counts = 0
        for character in string:
            if character.isalpha() and not character.islower():
                counts += 1
        return counts
        
    sentences.sort(key = evalFunc)
    return sentences

def task_10(string, result):
    """знайти букву, яка зустрічається найчастіше і найрідше; результат записати як tuple(max, min);"""
    input_string = result.copy()
    input_string.sort( reverse = True, key = lambda character: character[1])
    # return tuple( max, min )
    return ( input_string[0], input_string[len(input_string) - 1] )
    
def task_11(words_and_numbers):
    """знайти всі числа та записати їх до list, відсортувавши від найбільшого до найменшого;"""
    numbers = words_and_numbers['numbers']['values'].copy()
    numbers.sort( reverse = True )
    return numbers

def task_12(result):
    """знайти мінімальне і максимальне число; результат записати як tuple(min, max);"""
    numbers = result.copy() # <- copy data, returned from task_11
    return (numbers[len(numbers) - 1], numbers[0])

def task_13(string):
    """знайти абзац, в якому Python зустрічається найчастіше; результат записати як str."""
    string = string
    paragraphs = string.split('\n\n')
    paragraph_with_max_num_of_word_Python = ""
    word_Python_counts = 0
    for paragraph in paragraphs:
        if paragraph.count('Python') > word_Python_counts:
            word_Python_counts = paragraph.count('Python')
            paragraph_with_max_num_of_word_Python = paragraph
    return paragraph_with_max_num_of_word_Python

def task_14(words_and_numbers):
    """створити dict, де ключ - це слово, а значення - кількість разів, з якою слово зустрічається в тексті;"""
    words = words_and_numbers['words']['values'].copy()
    words_and_quantity = {}
    for word in words:
        if word in words_and_quantity:
            words_and_quantity[word] += 1
        else:
            words_and_quantity[word] = 1
    return words_and_quantity

def task_15(result):
    """знайти слово, яке зустрічається найчастіше і найрідше;
       результат записати як tuple(tuple(word, count), tuple(word, count))."""
    words_and_quantity_dict = result.copy() # <- result from task_14
    words_and_quantity_list = []
    for item, value in words_and_quantity_dict.items():
        words_and_quantity_list.append( (item, value) )
    words_and_quantity_list.sort( reverse = True, key = lambda item: item[1] )
    max_frequent_and_min_frequent_words = [ words_and_quantity_list[0], words_and_quantity_list[len(words_and_quantity_list) - 1] ]
    return max_frequent_and_min_frequent_words


def analyze_text(text):

	words_and_numbers = make_words_and_numbers( text )

	handlers = {
		1  : task_1,
		2  : task_2,
		3  : task_3,
		4  : task_4,
		5  : task_5,
		6  : task_6,
		7  : task_7,
		8  : task_8,
		9  : task_9,
		10 : task_10,
		11 : task_11,
		12 : task_12,
		13 : task_13,
		14 : task_14,
		15 : task_15
	}

	result = {
		1  : None,
		2  : None,
		3  : None,
		4  : None,
		5  : None,
		6  : None,
		7  : None,
		8  : None,
		9  : None,
		10 : None,
		11 : None,
		12 : None,
		13 : None,
		14 : None,
		15 : None
	}

	# for prop in handlers:
	# 	result[prop] = handlers[prop]()

	for prop in range(1,16):
		if prop == 1:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 2:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 3:
			result[ prop ] = handlers[ prop ]( result[ prop - 1] )
		elif prop == 4:
			result[ prop ] = handlers[ prop ]( words_and_numbers )
		elif prop == 5:
			result[ prop ] = handlers[ prop ]( words_and_numbers )
		elif prop == 6:
			result[ prop ] = handlers[ prop ]( words_and_numbers )
		elif prop == 7:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 8:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 9:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 10:
			result[ prop ] = handlers[ prop ]( text, result[ prop - 8 ] )
		elif prop == 11:
			result[ prop ] = handlers[ prop ]( words_and_numbers )
		elif prop == 12:
			result[ prop ] = handlers[ prop ]( result[ prop - 1] )
		elif prop == 13:
			result[ prop ] = handlers[ prop ]( text )
		elif prop == 14:
			result[ prop ] = handlers[ prop ]( words_and_numbers )
		elif prop == 15:
			result[ prop ] = handlers[ prop ]( result[ prop - 1] )

	return result

result = analyze_text( initial_text )
# print(result)