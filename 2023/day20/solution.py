INPUT = 'input.txt'

from collections import deque

BROADCASTER = 'broadcaster'

# name -> Module
MODULE_MAP = {}

# (source, dest, pulse)
PULSE_QUEUE = deque()

class Pulse:
    LOW = 1
    HIGH = 2

class Module:
    def __init__(self, module_name: str, downstream_nodes: [str]):
        self._name = module_name
        self._ds_nodes = downstream_nodes
    
    def add_source(self, source):
        pass

    def get_name(self):
        return self._name

    def get_ds(self):
        return self._ds_nodes

    def handle_pulse(self, pulse:int, source: str):
        raise Exception("unimplemented")
    
    def _send_to_all(self, pulse:int):
        for ds in self._ds_nodes:
            PULSE_QUEUE.appendleft((self._name, ds, pulse))


class BroadcastModule(Module):
    def handle_pulse(self, pulse: int, source: str):
        self._send_to_all(pulse)

class FlipFlopModule(Module):
    def __init__(self, *args, **kwargs):
        self._state_on = False
        super().__init__(*args, **kwargs)

    def handle_pulse(self, pulse: int, source: str):
        # Ignore HIGH pulses
        if pulse == Pulse.LOW:
            self._state_on = not self._state_on
            if self._state_on:
                self._send_to_all(Pulse.HIGH)
            else:
                self._send_to_all(Pulse.LOW)

class ConjunctionModule(Module):
    def __init__(self, *args, **kwargs):
        self._source_to_pulse = {}
        super().__init__(*args, **kwargs)
    
    def add_source(self, source):
        self._source_to_pulse[source] = Pulse.LOW

    def handle_pulse(self, pulse: int, source: str):
        self._source_to_pulse[source] = pulse
        if not len(self._source_to_pulse) or all(p == Pulse.HIGH for p in self._source_to_pulse.values()):
            self._send_to_all(Pulse.LOW)
        else:
            self._send_to_all(Pulse.HIGH)

lines = [line.strip() for line in open(INPUT).readlines()]
for line in lines:
    source, dest = line.split(' -> ')
    dest_nodes = dest.split(', ')
    if source == BROADCASTER:
        MODULE_MAP[BROADCASTER] = BroadcastModule(BROADCASTER, dest_nodes)
    elif source[0] == '%':
        name = source[1:]
        MODULE_MAP[name] = FlipFlopModule(name, dest_nodes)
    elif source[0] == '&':
        name = source[1:]
        MODULE_MAP[name] = ConjunctionModule(name, dest_nodes)

for module in MODULE_MAP.values():
    for ds in module.get_ds():
        if ds in MODULE_MAP:
            MODULE_MAP[ds].add_source(module.get_name())

HIGH_PULSES = 0
LOW_PULSES = 0


i = 0
tracked_sources = {}
cycle_lengths = {}
while len(cycle_lengths) < 4:
    print(i + 1)
    PULSE_QUEUE.appendleft(('button', BROADCASTER, Pulse.LOW))
    while len(PULSE_QUEUE):
        source, dest, pulse = PULSE_QUEUE.pop()
        if source in ('kl', 'vm', 'kv', 'vb') and pulse == Pulse.HIGH:
            if source in tracked_sources:
                cycle_lengths[source] = i - tracked_sources[source]
            else:
                tracked_sources[source] = i
        if pulse == Pulse.HIGH:
            HIGH_PULSES += 1
            pulse_str = '-high->'
        else:
            LOW_PULSES += 1
            pulse_str = '-low->'
        # print(source, pulse_str, dest)
        if dest in MODULE_MAP:
            MODULE_MAP[dest].handle_pulse(pulse, source)
    i += 1

print('Low:', LOW_PULSES)
print('High:', HIGH_PULSES)
print('Product:', LOW_PULSES * HIGH_PULSES)
print('Tracked sources: ', tracked_sources)

import math
print('LCM:', math.lcm(*(cycle_lengths.values())))

# rx ancestors to check: kl, vm, kv, vb