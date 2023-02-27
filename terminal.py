from bin.handle_input import handle_input
from classes.actor import Actor

def main():
    actor = Actor("terminal")
    print("Terminal SMS Started")

    while True:
        message = input('>>> ')

        out_msgs = handle_input(actor, message)

        for msg in out_msgs:
            print(msg)

if __name__ == "__main__": 
    main() 
