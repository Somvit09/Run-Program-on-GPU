from string import *
from itertools import product

def get_password_list_optimized():
    try:
        file_path = "passwords/demo_optimized.txt"
        min_length = 8
        max_length = 9
        batch_size = 100000  # Number of passwords to write in one go
        
        with open(file_path, "w") as file:
            for length in range(min_length, max_length + 1): 
                password_generator = product(digits, repeat=length)
                batch = []
                
                for password_tuple in password_generator:
                    password = ''.join(password_tuple)
                    #print(password)
                    batch.append(password + '\n')
                    
                    # Write passwords in batches
                    if len(batch) >= batch_size:
                        file.writelines(batch)
                        batch = []  # Reset batch
                
                # Write any remaining passwords not fitting into the last batch
                if batch:
                    file.writelines(batch)
                #print(f"words formed - {count}, word is {word}")
    except Exception as e:
        raise e