import random
import string

class RandomNumberUtils:
    
    #Class for generation of random numbers
    
    @staticmethod
    def generate_random_id() -> str:

        #Generates a random ID number of length 6 as a string
        print("f".join(random.choices(string.ascii_uppercase, k=6)))
        return "".join(random.choices(string.ascii_uppercase, k=6))