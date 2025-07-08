import random
import string


def generate_string(min_len: int=50, max_len: int=100, min_spaces: int=3, max_spaces: int=5) -> str:
    """
    Generates a random alphanumeric string with a specified length and non-consecutive internal spaces.
    """
    chars: list[str] = []
    string_length: int = random.randint(min_len, max_len)
    space_count: int = random.randint(min_spaces, max_spaces)
    posible_positions: list[int] = list(range(1, string_length - 1))
    space_positions: list[int] = random.sample(posible_positions, space_count)
    
    # Ensure no consecutive spaces by checking and re-sampling if needed
    while any((i + 1) in space_positions for i in space_positions):
        space_positions = random.sample(posible_positions, space_count) 
        
    # Build the string character by character
    for i in range(string_length):
        if i in space_positions:
            # Insert a space at the selected positions
            chars.append(' ')
        else:
            # Insert a random letter or digit
            chars.append(random.choice(string.ascii_letters + string.digits))
    
    # Join the list into a single string and return
    return ''.join(chars)

def main() -> None:
    # Number of strings to generate
    strings_q: int = 1000000
    # Output file name
    file_name: str = "strings.txt"
    
    with open(file_name, "w", encoding="utf-8") as f:
        for _ in range(strings_q):
            f.write(generate_string() + "\n")
    
if __name__ == "__main__":
    main()
