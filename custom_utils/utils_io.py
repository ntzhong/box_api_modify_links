def read_txt_file(source_file):
    """
    reads contents of a .txt file. returns data.
    """
    data = ''
    with open(source_file, 'r') as file:
        data = file.read()
    return data


def txt_to_list(source_file):
    """
    converts text file to list. one line per list item
    """
    with open(source_file, 'r') as file:
        array = [ipaddress.IPv4Address(line.strip('\n')) for line in file]
    return array


def write_to_txtfile(message, outfile):
    with open(outfile, 'w') as file:
        file.write(str(message))
    print('written out to ' + str(outfile))
    return outfile


def pprint_REQ(req):
    """    
    pretty prints raw prepared request
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
