"""
Home Work 1. Task 1.

"""
number = input('Enter, pls, phone number, ex. 0993279078: ')

def is_number_mod( number ):
    if len(number) != 10:
        print('Number has not 10 digits! Check it, pls!')
        return False
    
    conditions = { 'first'  : False,
                   'second' : False,
                   'third'  : False }
    
    # 4 or more equal digits in series
    if '0000' in number or \
       '1111' in number or \
       '2222' in number or \
       '3333' in number or \
       '4444' in number or \
       '5555' in number or \
       '6666' in number or \
       '7777' in number or \
       '8888' in number or \
       '9999' in number:
        conditions['first'] = True
    
    up = '0123456789'
    down = '9876543210'
    for i in range(7):
        if up[ i : i + 4 ] in number or down[ i : i + 4 ] in number:
            conditions['second'] = True
            break

    if int(number[0]) + int(number[1]) + int(number[2]) \
         + int(number[3]) + int(number[4]) == int(number[5]) + int(number[6]) \
         + int(number[7]) + int(number[8]) + int(number[9]):
        conditions['third'] = True

    return conditions
        

conditions = is_number_mod( number )

if conditions['first'] or conditions['second'] or conditions['third']:
    if conditions['first']:
      print('Case 1')
    if conditions['second']:
      print('Case 2')
    if conditions['third']:
      print('Case 3')
    print("Крутий")
else:
    print("Звичайний")
