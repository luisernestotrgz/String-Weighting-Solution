import socket
from generate_string import create_strings
import sys


def main() -> None:
    # Generate the input file with random strings
    if len(sys.argv) > 1:
        host = sys.argv[1]
        port = int(sys.argv[2])
        string_count = int(sys.argv[3])
    else:
        host = "127.0.0.1"
        port = 5000
        string_count = 1000000
        
    input_f = "chains.txt"
    output_f = "results.txt"
    create_strings(string_count)
    
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the server
    sock.connect((host, port))
    
    # Open the input file for reading and output file for writing
    with open(input_f, "r", encoding="utf-8") as  fin, \
        open(output_f, "w", encoding="utf-8") as fout:
            # For each line in the input file
            for line in fin:
                # Send the string to the server
                sock.sendall(line.encode('utf-8'))
                # Receive the response from the server
                resp = sock.recv(4096).decode('utf-8').strip()
                # Write the original string and the result to the output file
                fout.write(f"{line.strip()} ==> {resp}\n")
    
    sock.close()
    
if __name__ == "__main__":
    main()