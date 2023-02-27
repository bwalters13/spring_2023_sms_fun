from bin.handle_input import handle_input
from classes.actor import Actor
import os
java_path = "C:/Program Files/Common Files/Oracle/Java/javapath/java.exe"
os.environ['JAVAHOME'] = java_path

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
