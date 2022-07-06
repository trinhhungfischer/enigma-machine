"""
Enigma M3 with reflector UKW-D: 
"""
import string

class Enigma:

    # Rotors I to V substitution table 
    rotors = [
        [20, 22, 24, 6, 0, 3, 5, 15, 21, 25, 1, 4, 2, 10, 12, 19, 7, 23, 18, 11, 17, 8, 13, 16, 14, 9],
        [0, 9, 15, 2, 25, 22, 17, 11, 5, 1, 3, 10, 14, 19, 24, 20, 16, 6, 4, 13, 7, 23, 12, 8, 21, 18],
        [19, 0, 6, 1, 15, 2, 18, 3, 16, 4, 20, 5, 21, 13, 25, 7, 24, 8, 23, 9, 22, 11, 17, 10, 14, 12],
        [4, 18, 14, 21, 15, 25, 9, 0, 24, 16, 20, 8, 17, 7, 23, 11, 13, 5, 19, 6, 10, 3, 2, 12, 22, 1],
        [21, 25, 1, 17, 6, 8, 19, 24, 20, 15, 18, 3, 13, 7, 11, 23, 0, 22, 12, 9, 16, 14, 5, 4, 2, 10]
    ]
    
    # Reflector is a map from one letter of keyboard to another letter to entry rotors...
    plugboard = [0, 1, 2, 21, 22, 14, 19, 9, 23, 7, 20, 16, 24, 13, 5, 15, 11, 17, 25, 6, 10, 3, 4, 8, 12, 18]
    
    # Reflector is a map from one position of R1 to another...
    reflector = [24, 17, 20, 7, 16, 18, 11, 3, 15, 23, 13, 6, 14, 10, 12, 8, 4, 1, 5, 25, 2, 22, 21, 9, 0, 19]

    # This is turnover positioin for rotor I to V with BP mneumonic is Royal, Flag, Wave, Kings, Above
    turn_over = [17, 4, 22, 10, 0]

    # For reference (and in case I need it later) here's the rotors in letter form:
    LR1 = {'A': 'E', 'B': 'K', 'C': 'M', 'D': 'F', 'E': 'L', 'F': 'G', 'G': 'D', 'H': 'Q', 'I': 'V', 'J': 'Z', 'K': 'N', 'L': 'T', 'M': 'O', 'N': 'W', 'O': 'Y', 'P': 'H', 'Q': 'X', 'R': 'U', 'S': 'S', 'T': 'P', 'U': 'A', 'V': 'I', 'W': 'B', 'X': 'R', 'Y': 'C', 'Z': 'J'}
    LR2 = {'A': 'A', 'B': 'J', 'C': 'D', 'D': 'K', 'E': 'S', 'F': 'I', 'G': 'R', 'H': 'U', 'I': 'X', 'J': 'B', 'K': 'L', 'L': 'H', 'M': 'W', 'N': 'T', 'O': 'M', 'P': 'C', 'Q': 'Q', 'R': 'G', 'S': 'Z', 'T': 'N', 'U': 'P', 'V': 'Y', 'W': 'F', 'X': 'V', 'Y': 'O', 'Z': 'E'} 
    LR3 = {'A': 'B', 'B': 'D', 'C': 'F', 'D': 'H', 'E': 'J', 'F': 'L', 'G': 'C', 'H': 'P', 'I': 'R', 'J': 'T', 'K': 'X', 'L': 'V', 'M': 'Z', 'N': 'N', 'O': 'Y', 'P': 'E', 'Q': 'I', 'R': 'W', 'S': 'G', 'T': 'A', 'U': 'K', 'V': 'M', 'W': 'U', 'X': 'S', 'Y': 'Q', 'Z': 'O'}
    LR4 = {'A': 'E', 'B': 'S', 'C': 'O', 'D': 'V', 'E': 'P', 'F': 'Z', 'G': 'J', 'H': 'A', 'I': 'Y', 'J': 'Q', 'K': 'U', 'L': 'I', 'M': 'R', 'N': 'H', 'O': 'X', 'P': 'L', 'Q': 'N', 'R': 'F', 'S': 'T', 'T': 'G', 'U': 'K', 'V': 'D', 'W': 'C', 'X': 'M', 'Y': 'W', 'Z': 'B'}
    LR5 = {'A': 'V', 'B': 'Z', 'C': 'B', 'D': 'R', 'E': 'G', 'F': 'I', 'G': 'T', 'H': 'Y', 'I': 'U', 'J': 'P', 'K': 'S', 'L': 'D', 'M': 'N', 'N': 'H', 'O': 'L', 'P': 'X', 'Q': 'A', 'R': 'W', 'S': 'M', 'T': 'J', 'U': 'Q', 'V': 'O', 'W': 'F', 'X': 'E', 'Y': 'C', 'Z': 'K'}

    def __init__(self, rotor_order = None, rotor_settings = None):
        # Default rotor order
        if rotor_order is None:
          rotor_order = (1,2,3)
        # Initial rotor positions
        if rotor_settings is None:
          rotor_settings = (0,0,0)
          
        self.set_rotor_order(rotor_order)          
        self.rotor_settings = rotor_settings
        self.reset()

    def set_rotor_order(self, order_tuple):
        # tuple should be of form (I,II,III) or (III,II,I) etc.
        self.rotor_order = order_tuple
        # these just provide a reference to the rotor
        self.R1 = self.rotors[order_tuple[0]-1]
        self.R2 = self.rotors[order_tuple[1]-1]
        self.R3 = self.rotors[order_tuple[2]-1]
        
        self.R1_turnover = self.turn_over[order_tuple[0]-1]
        self.R2_turnover = self.turn_over[order_tuple[1]-1]
        self.R3_turnover = self.turn_over[order_tuple[2]-1]

    def set_rotor_setting(self, rotor_settings):
        self.rotor_settings = rotor_settings
        self.reset()

    def reset(self):
        self.p1, self.p2, self.p3 = self.rotor_settings

    def set_reflector(self, reflectors = None):
      if reflectors is None:
        return
      
      reflectors = reflectors.upper()
      alphabet_list = string.ascii_uppercase

      maping = {}
      letter_pairs = reflectors.split(' ')
      results = [0] * 26
      
      for letter_pair in letter_pairs:
        maping[letter_pair[0]] = letter_pair[1]
        maping[letter_pair[1]] = letter_pair[0]
      
      for (i, letter) in enumerate(alphabet_list):
        if letter in maping:
          results[i] = alphabet_list.index(maping[letter])
        else:
          results[i] = i
      
      return results
  
    def set_plugboard(self, plug_boards = None):
      if plug_boards is None:
        return
      
      plug_boards = plug_boards.upper()
      alphabet_list = string.ascii_uppercase

      maping = {}
      letter_pairs = plug_boards.split(' ')
      results = [0] * 26
      
      for letter_pair in letter_pairs:
        maping[letter_pair[0]] = letter_pair[1]
        maping[letter_pair[1]] = letter_pair[0]
      
      for (i, letter) in enumerate(alphabet_list):
        if letter in maping:
          results[i] = alphabet_list.index(maping[letter])
        else:
          results[i] = i
      
      return results
      

    def encode(self, letter):
        """
        Converts letter to another letter as it gets transposed through the
        rotors and reflector.
        """
        if not letter.upper() in string.ascii_uppercase:
            return ''

        self.p3 = (self.p3 + 1) % 26
        if (self.p3 == self.R3_turnover):
          self.p2 = (self.p2 + 1) % 26
          if (self.p2 == self.R2_turnover):
            self.p1 = (self.p1 + 1) % 26

        print(self.p1, self.p2, self.p3)
        
        letter_index = (ord(letter.upper()) - 65)
        # Letter in keyboard will be mapped to another by plugboard
        letter_index = self.plugboard[letter_index] 
         
        # zero based letter plus rotation mod 26 is 3rd rotor right hand side (RHS)
        r3_r_pos = (letter_index + self.p3) % 26
        
        # Take r3 RHS and get r3 LHS
        r3_l_pos = self.R3.index(r3_r_pos)
        
        # Now find r3_l_pos position in rotor 2
        r2_r_pos = (r3_l_pos - self.p3) % 26
        r2_l_pos = self.R2.index(r2_r_pos)
        
        # Now find r2_l_pos position in rotor 1
        r1_r_pos = (r2_l_pos - self.p2) % 26
        r1_l_pos = self.R1.index(r1_r_pos)
        
        # Now perform reflection
        l0 = self.reflector[(r1_l_pos - self.p1) % 26]
        
        # Now go back to the right...
        r1_l_pos = (l0 + self.p1) % 26
        r1_r_pos = self.R1[r1_l_pos]
        
        r2_l_pos = (r1_r_pos + self.p2) % 26
        r2_r_pos = self.R2[r2_l_pos]
        
        r3_l_pos = (r2_r_pos + self.p3) % 26
        r3_r_pos = self.R3[r3_l_pos]
        
        letter_index = ((r3_r_pos - self.p3) % 26)
        # Letter in keyboard will be mapped to another by plugboard
        letter_index = self.plugboard[letter_index] 

        # Convert back to letter        
        letter = chr(letter_index + 65)
        return letter

    '''
    
    '''
    def get_rotor_positions(self):
      return (self.p1, self.p2, self.p3)

    '''
    
    '''
    def encrypt(self, plaintext):
        ciphertext = ''
        for letter in plaintext:
            ciphertext += self.encode(letter)
        return ciphertext
        

if __name__ == '__main__':

    import sys

    e = Enigma()
    
    print(e.encrypt("ZOFO"))

    if '-rj' in sys.argv:
        e.generate_all_rejewski()
    elif '-zg' in sys.argv:
        e.generate_zygalski()