from __future__ import print_function
import cmd
import argparse
import Queue

AVAILABLE = 1
RINGING = 2
BUSY = 3
FOUND = True

class CallCenter(cmd.Cmd):

    def do_call(self, id):
        print("Call", id, "received")
        cur_call = Call(id)
        status = cur_call.search_operator()
        if status == (not FOUND):
            print("Call", id, "waiting in queue")
            q.append(cur_call)

    def do_answer(self, id):
        operators[ord(id) - ord('A')].answer()

    
    def do_reject(self, id):
        operators[ord(id) - ord('A')].reject()
    
    def do_hangup(self, id):
        for operator in operators:
            if operator.call != None:
                if operator.call.id == id and operator.status == BUSY:
                    operator.hangup()
                    return
                if operator.call.id == id and operator.status == RINGING:
                    print("Call", id, "missed")
                    operator.hangup()
                    return

        print("Call", id, "missed")
        for call in q:
            if call.id == id:
                q.remove(call)


    def do_EOF(self, line):
        return True

class Operator:
    def __init__(self, id, status=AVAILABLE, call=None):
        self.id = id
        self.status = status
        self.call = call
    def ring(self, call):
        print ("Call", call.id, "ringing for operator", self.id)
        self.status = RINGING
        self.call = call
    def answer(self):
        print ("Call", self.call.id, "answered by operator", self.id)
        self.status = BUSY
    def reject(self):
        print("Call", self.call.id, "rejected by operator", self.id)
        self.status = AVAILABLE
        if self.call.search_operator() == (not FOUND):
            print("Call", self.call.id, "waiting in queue")
            q.append(self.call)
        if len(q) > 0:
            queue_call = q[0]
            q.remove(queue_call)
            queue_call.search_operator()

    def hangup(self):
        if self.status == BUSY:
            print("Call", self.call.id, "finished and operator", self.id, "available")
        self.status = AVAILABLE
        if len(q) > 0:
            queue_call = q[0]
            q.remove(queue_call)
            queue_call.next_operator = ord(self.id) - ord('A')
            queue_call.search_operator()


class Call:
    def __init__(self, id, next_operator=0):
        self.id = id
        self.next_operator = next_operator
    def search_operator(self):
        i = self.next_operator
        for i in range(self.next_operator, len(operators)):
            if operators[i].status == AVAILABLE:
                operators[i].ring(self)
                return FOUND
            else:
                self.next_operator = i + 1
        return not FOUND
            

def create_operators(quantity=1):
    operators = list()
    for i in range(quantity):
        operators.append(Operator(chr(ord('A') + i)))
    return operators

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
    q = list()
    CallCenter().cmdloop()