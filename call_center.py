import cmd
import argparse

AVAILABLE = 1
RINGING = 2
BUSY = 3

class CallCenter(cmd.Cmd):

    def do_call(self, id):
        print("Call", id, "received")
        cur_call = Call(id)
        cur_call.search_operator(operators)

    def do_answer(self, id):
        operators[ord(id) - ord('A')].answer()

    
    def do_reject(self, id):
        operators[ord(id) - ord('A')].answer()
    
    def do_hangup(self, id):
        print("you hanged up the call with id", id)

    def do_EOF(self, line):
        return True

class Operator:
    def __init__(self, id, status=AVAILABLE, call_id=None):
        self.id = id
        self.status = status
        self.call_id = call_id
    def ring(self, call_id):
        print ("Call", call_id, "ringing for operator", self.id)
        self.status = RINGING
        self.call_id = call_id
    def answer(self):
        print ("Call", self.call_id, "answered by operator", self.id)
        self.status = BUSY
    def reject(self):
        print("Call", self.call_id, "rejected by operator", self.id)
        self.status = AVAILABLE
    def hangup(self):
        self.status = AVAILABLE

class Call:
    def __init__(self, id, last_operator=0):
        self.id = id
        self.last_operator = last_operator
    def search_operator(self, operators):
        self.last_operator = self.last_operator % len(operators)
        for i in range(self.last_operator, len(operators)):
            if operators[i].status == AVAILABLE:
                operators[i].ring(self.id)
                self.last_operator = i
                break

def create_operators(quantity=1):
    operators = list()
    for i in range(quantity):
        operators.append(Operator(chr(ord('A') + i)))
    return operators

def look_for_operator(id, operators, last_seen):
    for operator in operators:
        if operator.status == AVAILABLE:
            operator.ring(id)
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', 
                        '--operators', 
                        default=2, 
                        type=int, 
                        metavar='', 
                        help='Number of operators'
                        )
    args = parser.parse_args()

    operators = create_operators(args.operators)

    CallCenter().cmdloop()