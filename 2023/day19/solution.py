INPUT = 'test_input.txt'

class Part:
    def __init__(self, line):
        line = line[1:-1]
        attribute_strs = line.split(',')
        self.attributes = {}
        for attr_str in attribute_strs:
            attr, value = attr_str.split('=')
            self.attributes[attr] = int(value)
    
    def __str__(self) -> str:
        return str(self.attributes)
    
    def rating(self):
        return sum(self.attributes.values())

class Workflow:
    def __init__(self, line):
        self.name, instructions_str = line.split('{')
        instructions_str = instructions_str[:-1]
        self.instructions = instructions_str.split(',')

    def __str__(self) -> str:
        return '%s: %s' % (self.name, str(self.instructions))
    
    def process_part(self, part: Part) -> str:
        for instr in self.instructions:
            if '<' in instr:
                check, dest = instr.split(':')
                attr, value = check.split('<')
                if part.attributes[attr] < int(value):
                    return dest
            elif '>' in instr:
                check, dest = instr.split(':')
                attr, value = check.split('>')
                if part.attributes[attr] > int(value):
                    return dest
            else:
                return instr

WORKFLOWS = {}
PARTS = []

# Build up data objects
hit_blank_line = False
for line in open(INPUT).readlines():
    line = line.strip()
    if not line:
        hit_blank_line = True
        continue
    if not hit_blank_line:
        workflow = Workflow(line)
        WORKFLOWS[workflow.name] = workflow
    else:
        PARTS.append(Part(line))

# Part 1
total_rating = 0
for part in PARTS:
    result = 'in'
    results = [result]
    while result not in ('A', 'R'):
        result = WORKFLOWS[result].process_part(part)
        results.append(result)
    if result == 'A':
        total_rating += part.rating()
print('Part 1:', total_rating)

# Part 2
from collections import deque
backtrace_q = deque()
for wf in WORKFLOWS.values():
    for i, instr in enumerate(wf.instructions):
        if instr[-1] == 'A':
            backtrace_q.append((wf.name, i))