import logging
import socket
import time
import re


def setup_logging(logfile: str="server.log") -> None:
    """
    Set up the logging configuration for the server.
    """
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def process_string(string: str) -> float:
    """
    Process the received string and calculate a metric based on its content.
    """
    # Check if the string contains any double "a" (case-insensitive)
    if re.search(r"(?i)aa", string):
        # Log a warning if the rule is detected
        logging.warning(f"Double 'a' rule detected >> '{string}'")
        
        return 1000
    
    # Count the number of letters in the string
    letters = sum(c.isalpha() for c in string)
    # Count the number of digits in the string
    digits = sum(c.isdigit() for c in string)
    # Count the number of spaces in the string
    spaces = string.count(' ')
    
    # Avoid division by zero if there are no spaces
    if spaces == 0:
        return float('inf')
    else:
        # Calculate the metric and round to 2 decimal places
        return round((letters * 1.5 + digits * 2) / spaces, 2)
    
def run_server(host: str, port: int) -> None:
    """
    Run the TCP server to process incoming strings from a client.
    """
    setup_logging()
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    logging.info(f"Server listening on {host}:{port}")
    conn, addr = sock.accept()
    logging.info(f"Connection from {addr}")
    
    # Handle the client connection
    with conn:
        while True:
            # Receive data from the client
            data = conn.recv(4096)
            
            # If no data is received, break the loop (client disconnected)
            if not data:
                break
            
            # Decode the received bytes to a string and remove trailing newline
            string = data.decode('utf-8').rstrip("\n")
            # Process the string and calculate the metric
            metric = process_string(string)
            # Send the result back to the client
            conn.sendall(f"{metric}\n".encode('utf-8'))
            
    # Calculate the total processing time
    total = time.time() - start_time
    logging.info(f"Procces completed in {int(total)} seconds.")
    sock.close()

def main() -> None:
    host = "127.0.0.1"
    port = 5000
    
    run_server(host, port)

if __name__ == "__main__":
    main()