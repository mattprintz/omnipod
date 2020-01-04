# Helper functions

def clean_string(string):
    output = []
    for i in string:
        if i == 0:
            break
        output.append(chr(i))
    return ''.join(output)

