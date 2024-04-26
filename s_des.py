import sys
import time

#Διάνυσμα βάσει του οποίου προκύπτει η αντιμετάθεση P10:
p10vector = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
#Διάνυσμα βάσει του οποίου προκύπτει η αντιμετάθεση P8:
p8vector = (6, 3, 7, 4, 8, 5, 10, 9)
#Διάνυσμα βάσει του οποίου προκύπτει η αντιμετάθεση IP:
ipvector = (2, 6, 3, 1, 4, 8, 5, 7)
#Διάνυσμα βάσει του οποίου προκύπτει η αντιμετάθεση E/P:
epvector = (4, 1, 2, 3, 2, 3, 4, 1)
#Κουτί S0:
s0box = [[1,0,3,2], [3,2,1,0], [0,2,1,3], [3,1,3,2]]
#Κουτί S1:
s1box = [[0,1,2,3], [2,0,1,3], [3,0,1,0], [2,1,0,3]]
#Διάνυσμα βάσει του οποίου προκύπτει η αντιμετάθεση P4:
p4vector = (2, 4, 3, 1)
inverseipvector = (4, 1, 3, 5, 7, 2, 8, 6)

#Γενική μέθοδος υποποίησης αντιμεταθέσεων, όταν δίνεται το αντίστοιχο διάνυσμα:
def permutation(key, vector):
    permutation_key = ""
    for i in vector:
        permutation_key += key[i-1]
    return permutation_key

#Μέθοδος υλοποίησης αριστερής (κυκλικής) ολίσθησης υποκλειδιού των 5 bits κατά 1:
def leftShift1(subkey):
    shifted_subkey = ""
    shifted_subkey += subkey[1]
    shifted_subkey += subkey[2]
    shifted_subkey += subkey[3]
    shifted_subkey += subkey[4]
    shifted_subkey += subkey[0]
    return shifted_subkey

#Μέθοδος υλοποίησης αριστερής (κυκλικής) ολίσθησης υποκλειδιού των 5 bits κατά 2:
def leftShift2(subkey):
    shifted_subkey = ""
    shifted_subkey += subkey[2]
    shifted_subkey += subkey[3]
    shifted_subkey += subkey[4]
    shifted_subkey += subkey[0]
    shifted_subkey += subkey[1]
    return shifted_subkey

#Μέθοδος διχοτόμησης αλφαριθμητικού:
def splitString(string):
    #Αρχικοποίηση των δύο τμημάτων του αλφαριθμητικού:
    str1 = ""
    str2 = ""
    #Διχοτόμηση:
    for i in range(int(len(string)/2)):
        str1 += string[i]
    for j in range(int(len(string)/2), len(string)):
        str2 += string[j]
    return str1, str2

#Μέθοδος υλοποίησης XOR μεταξύ δυαδικών αριθμών, εκφρασμένων σε μορφή αλφαριθμητικού:
def xor(str1, str2):
    xor_str = ""
    #Έλεγχος ώστε τα δύο αλγαριθμητικά να έχουν το ίδιο μήκος:
    if len(str1) != len(str2):
        print('XOR cannot be excecuted between strings with deferent length...')
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            xor_str += '0'
        else:
            xor_str += '1'
    return xor_str

#Μέθοδος υλοποίησης της αντιμετάθεσης E/P:
def ep(message):
    return permutation(message, epvector)

#Μέθοδος υλοποίησης αντιμετάθεσης P4:
def p4(message):
    return permutation(message, p4vector)

#Μέθοδος μετατροπής ακέραιου αριθμού στο αλφαριθμητικό του αντίστοιχου δυαδικού, με συγκεκριμένο αριθμό bits:
def intToBinStr(int_num, bits):
    zeros = ""
    tmp_str_num = str(bin(int_num))
    str_num = zeros + tmp_str_num[2:]
    if len(str_num) < bits:
        for i in range(bits-len(str_num)):
            zeros += '0'
        str_num = zeros + str_num
    return str_num

#Μέθοδος υλοποίησης της αρχικής αντιμετάθεσης:
def ip(message):
    return permutation(message, ipvector)

#Μέθοδος αντιστροφής δεξιού και αριστερού μέλους:
def sw(string):
    return splitString(string)[1] + splitString(string)[0]

#Μέθοδος αντίστροφης αντιμετάθεσης από την IP:
def ipInverse(message):
    return permutation(message, inverseipvector)

#Σύνθετη μέθοδος αντιμεταθέσεων και εφαρμαγής του κλειδιού στο μήνυμα:
def fk(message, subkey):
    #Διχοτόμηση του μηνύματος που εξήχθη από την αντιμετάθεση IP:
    mess_part1 = splitString(message)[0]
    mess_part2 = splitString(message)[1]
    #Αντιμετάθεση E/P:
    ep_mess = ep(mess_part2)
    #Εφαρμογή XOR μεταξύ του μηνύματος που εξάγεται από την E/P και του υποκλειδιού:
    xor_mess = xor(ep_mess, subkey)
    #Διχοτόμηση του xor_mess:
    xor_mess1 = splitString(xor_mess)[0]
    xor_mess2 = splitString(xor_mess)[1]
    #Εισαγωγή πρώτου τμήματος (xor_mess1) στο κουτί S0:
    row0 = int((xor_mess1[0]+xor_mess1[3]), 2)
    column0 = int((xor_mess1[1]+xor_mess1[2]), 2)
    s0_num = s0box[row0][column0]
    #2-bit έξοδος του πρώτου κουτιού, ως αλφαριθμητικό:
    s0_output = intToBinStr(s0_num, 2)
    #Εισαγωγή δεύτερου τμήματος (xor_mess2) στο κουτί S1:
    row1 = int((xor_mess2[0]+xor_mess2[3]), 2)
    column1 = int((xor_mess2[1]+xor_mess2[2]), 2)
    s1_num = s1box[row1][column1]
    #2-bit έξοδος του δεύτερου κουτιού, ως αλφαριθμητικό:
    s1_output = intToBinStr(s1_num, 2)
    #Ενοποίηση των εξόδων των δύο κουτιών:
    s_united_output = s0_output + s1_output
    #Αμτιμετάθεση P4:
    p4_output = p4(s_united_output)
    #Εκτέλεση XOR με το πρώτο (αριστερό) μέρος του αρχικού μηνύματος:
    xor_output = xor(p4_output, mess_part1)
    return xor_output + mess_part2

#Μέθοδος που ελέγχει την ορθότητα του δυαδικού αριθμού που έδωσε ο χρήστης:
def checkInput(input_string, desire_length):
    if(len(input_string) != desire_length):
        return False
    for i in input_string:
        if(i!='0' and i!='1'):
            return False
    return True

#Μέθοδος παραγωγής υποκλειδιών από το δοθέν κλειδί:
def generateSubkeys(key):
    #Εφαρμογή της αντιμετάθεσης P10:
    p10key = permutation(key, p10vector)
    #Διχοτόμηση του p10key:
    key_part1 = splitString(p10key)[0]
    key_part2 = splitString(p10key)[1]
    #Εφαρμογή αριστερής κυκλικής ολίσθησης κατά ένα στα δύο τμήματα του κλειδιού (ls1):
    key_part1 = leftShift1(key_part1)
    key_part2 = leftShift1(key_part2)
    #Διατήρηση της τιμής των δύο τμημάτων στα οποία διχοτομήθηκε το κλειδί, ώστε να χρησιμοποιηθούν στην παραγωγή του δεύτερου υποκλειδιού:
    stored_part1 = key_part1
    stored_part2 = key_part2
    #Ενώνουμε τα δύο υποκλειδιά που προέκυψαν, ώστε να πάρουμε ένα ενιαίο κλειδί, στο οποίο θα εφαρμοστεί η P8:
    united_key1 = key_part1 + key_part2
    #Με την εφαρμογή της αντιμετάθεσης P8, προκείπτει το πρώτο υποκλειδί:
    subkey1 = permutation(united_key1, p8vector)
    #Εφαρμογή αριστερής κυκλικής ολίσθησης κατά δύο στα δύο τμήματα του κλειδιού (ls2), την τιμή των οποίων κρατήσαμε παραπάνω:
    stored_part1 = leftShift2(stored_part1)
    stored_part2 = leftShift2(stored_part2)
    #Ενώνουμε τα δύο υποκλειδιά που προέκυψαν, ώστε να πάρουμε ένα ενιαίο κλειδί, στο οποίο θα εφαρμοστεί η P8:
    united_key2 = stored_part1 + stored_part2
    #Με την εφαρμογή της αντιμετάθεσης P8, προκείπτει το δεύτερο υποκλειδί:
    subkey2 = permutation(united_key2, p8vector)
    return subkey1, subkey2

#Μέθοδος κρυπτογράφησης 8-bit μηνύματος με τον αλγόριθμο s-des:
def sdesEncryption(plain_text, key):
    #Παραγωγή των δύο απαραίτητων υποκλειδιών από το δοθέν κλειδί:
    subkey1 = generateSubkeys(key)[0]
    subkey2 = generateSubkeys(key)[1]

    #Κρυπτογράφηση:
    #Βήμα 1: Αντιμετάθεση IP:
    ip_output = ip(plain_text)
    #Βήμα 2: Εφαρμογή σύνθετης συνάρτησης fk, ώστε να συνδυαστεί το μύνημα με το κλειδί:
    fk1_output = fk(ip_output, subkey1)
    #Βήμα 3: Αντιμετάθεση SW: αντιμετάθεση δεξιού και αριστερού μέρους της εξόδου της συνάρτησς fk:
    sw_output = sw(fk1_output)
    #Βήμα 4: Εφαρμογή της fk, αυτή την φορά στην έξοδο της SW:
    fk2_output = fk(sw_output, subkey2)
    #Βήμα 5: Τελική αντιμετάθεση (αντίστροφη της αρχικής IP-1):
    cipher_text = ipInverse(fk2_output)
    return cipher_text

#Μέθοδος αποκρυπτογράφισης 8-bit s-des κρυπτογραφήματος:
def sdesDecryption(cipher_text, key):
    #Παραγωγή των δύο απαραίτητων υποκλειδιών από το δοθέν κλειδί:
    subkey1 = generateSubkeys(key)[0]
    subkey2 = generateSubkeys(key)[1]

    #Αποκρυπτογράφηση:
    #Βήμα 1: Αντιμετάθεση IP:
    ip_output = ip(cipher_text)
    #Βήμα 2: Εφαρμογή σύνθετης συνάρτησης fk, με το subkey2:
    fk2_output = fk(ip_output, subkey2)
    #Βήμα 3: Αντιμετάθεση SW:
    sw_output = sw(fk2_output)
    #Βήμα 4: Εφαρμογή σύνθετης συνάρτησης fk, με το subkey1:
    fk1_output = fk(sw_output, subkey1)
    #Βήμα 5: Αντιμετάθεση IP-1:
    plain_text = ipInverse(fk1_output)
    return plain_text

#Μέθοδος υλοποίησης επίθεσης βίαιης αναζήτησης κλειδιού:
def sdesBruteForceAttack(plain_text, cipher_text):
    keys = []
    #Εξαντλητική αναζήτηση όλων των πιθανών κλειδιών και έλεγχος ώστε να ανιχνευθεί ποια από αυτά αποτελούν όντως κλειδιά:
    #Διατήρηση της χρονικής στιγμής έναρξης του βρόχου:
    start_time = time.time_ns()
    for i in range(1023):
        if plain_text == sdesDecryption(cipher_text, intToBinStr(i, 10)):
            keys.append(intToBinStr(i, 10))
    #Διατήρηση της χρονικής στιγμής λήξης του βρόχου:
    end_time = time.time_ns()
    #Χρονική διάρκεια βίαιης επίθεσης:
    duration = end_time - start_time
    return keys, duration

#Κύρια συνάρτηση:
if __name__ == '__main__':
    #Τύπωση μενού επιλογών χρήστη:
    print('S-DES encryption: option = 1')
    print('S-DES decryption: option = 2')
    print('S-DES brute force attack: option = 3')
    print('exit: option = 0')

    while True:
        #Επιλογή χρήστη και εκτέλεση αντίστοιχης ενέργειας:
        option = input('option: ')
        #Τερματισμός του προγράμματος:
        if int(option) == 0:
            exit()
        #Διαδικασία κρυπτογράφησης:
        elif int(option) == 1:
            #Είσοδοι από το χρήστη και έλεγχος:
            plain_text = input('Message for encryptinon (8-bit binary): ')
            while(checkInput(plain_text, 8) == False):
                print('Invalid input...')
                plain_text = input('Message for encryptinon (8-bit binary): ')
            key = input('Encryption key (10-bit binary): ')
            while(checkInput(key, 10) == False):
                print('Invalid input...')
                key = input('Encryption key (10-bit binary): ')
            #Κλήση μεθόδου κρυπτογράφησης:
            print('Encrypted message: ' + sdesEncryption(plain_text, key))
        #Διαδικασία αποκρυπτογράφησης:
        elif int(option) == 2:
            #Είσοδοι από το χρήστη και έλεγχος:
            cipher_text = input('Encrypted message: ')
            while(checkInput(cipher_text, 8) == False):
                print('Invalid input...')
                cipher_text = input('Encrypted message: ')
            key = input('Decryption key (10-bit binary): ')
            while(checkInput(key, 10) == False):
                print('Invalid input...')
                key = input('Encryption key (10-bit binary): ')
            #Κλήση μεθόδου αποκρυπτογράφησης:
            print('Decrypted message: ' + sdesDecryption(cipher_text, key))
        #Διαδικασία βίαιης επίθεσης:
        elif int(option) == 3:
            #Είσοδοι από το χρήστη και έλεγχος:
            plain_text = input('Message for encryptinon: ')
            while(checkInput(plain_text, 8) == False):
                print('Invalid input...')
                plain_text = input('Message for encryptinon (8-bit binary): ')
            cipher_text = input('Encrypted message: ')
            while(checkInput(cipher_text, 8) == False):
                print('Invalid input...')
                cipher_text = input('Encrypted message: ')
            #Κλήση μεθόδου που υλοποιεί τη βίαιη επίθεση:
            brute_force = sdesBruteForceAttack(plain_text, cipher_text)
            #Τύπωση των κλειδιών που βρέθηκαν:
            finded_keys = brute_force[0]
            for i in finded_keys:
                print('Founed key: ' + i)
            #Τύπωση χρόνου εκτέλεσης εξαντλητικής αναζήτησης κλειδιών:
            brute_force_duration = brute_force[1]
            print('Brute force time: {} nsec'.format(brute_force_duration))
        else:
            print('Invalid option...')