import mido
mido.set_backend('mido.backends.rtmidi')
print(mido.get_input_names())
"""
['Midi Through 14:0']
>>> mido.get_output_names()
['Midi Through 14:0']
These should be unique
"""