import math

def read_null_term(openfile, encoding='utf-8'):
    stor = ''

    while True:
        read = openfile.read(1)
        if read == b'\x00':
            break

        stor += read.decode(encoding)
    
    openfile.read(1)
    return stor

#trims leading zeroes off of binary numbers represented as strings
def binary_trim(b_str):
    while len(b_str) > 0 and b_str[0] == '0':
        b_str = b_str[1:]
    return b_str

#returns an array containing the individual bits of the number in binary. length of the array is rounded up to the nearest multiple of 8
def bit_array(num):
    if num == 0:
        return [0] * 8
    blen = math.ceil(math.log(num,2)/8)*8
    out = []
    for i in range(blen-1, -1, -1):
        out.append((num >> i) & 1)
    return out

#parses ID3v2 header and returns relevant data in dict
def parse_header(_file):
    head_data = {}

    with open(_file, 'rb') as f:
        head_b = f.read(20)
        
        #parsing regular header
        try:
            head_s = head_b[0:3].decode("utf-8")

            if (head_s != 'ID3'):
                raise Exception('Invalid ID3v2 format')

            #version, two bytes, signifies: v2.{first byte}.{second byte}
            head_data['version'] = list(head_b[3:5])

            #flags, one byte, only first 3 bits are used
            #1st bit: unsynchronization, 2nd bit: extended header used, 3rd bit: experimental indicator
            flags = []
            for i in range(7,-1,-1):
                flags.append((head_b[5] >> i) & 1)
            
            head_data['flags'] = flags

            #tag size, four bytes in format %0xxxxxxx where 1st bit is ignored
            container = []
            for b in head_b[6:10]:
                container.extend(bit_array(b)[1:])
            head_data['size'] = int(''.join([str(a) for a in container]), 2)

        except Exception as e:
            print('Error decoding ID3v2 header: {}'.format(str(e)))

    return head_data

def parse_extended_header(_file):
    with open(_file, 'rb') as f:
        f.seek(10)
        #todo: parse extended header

def parse_frames(_file, off, size):
    if off < 10:
        return

    frames = []

    with open(_file, 'rb') as f:
        f.seek(off)
        
        _count = 0

        while _count < size:
            frames.append({})
            cf = frames[-1]

            frame_id_b = f.read(4)
            frame_size_b = f.read(4)
            frame_flags_b = f.read(2)

            try:
                #frame id, four character bytes
                cf['id'] = frame_id_b.decode('utf-8')
                #frame size, four bytes
                cf['size'] = int(''.join([binary_trim('{0:b}'.format(a)) for a in list(frame_size_b)]), 2)
                #frame flags, two bytes, first byte is for status messages, second byte is for encoding
                cf['flags'] = [bit_array(frame_flags_b[0]), bit_array(frame_flags_b[1])]
            except Exception as e:
                print('Frame header parsing error: {}'.format(str(e)))

            if not 'size' in cf or cf['size'] <= 0:
                continue
            
            if cf['id'] == 'APIC':
                apic_encoding = f.read(1)
                text_encoding = 'latin_1' if apic_encoding == b'\x00' else 'utf-8'
                apic_mime = read_null_term(f, 'latin_1')
                apic_type = f.read(1)
                apic_desc = read_null_term(f, text_encoding)

                try:
                    cf['apic_encoding'] = text_encoding
                    cf['apic_mime'] = str(apic_mime)
                
                    typemap = {
                        b'\x00': '32x32 pixels \'file icon\' (PNG only)',
                        b'\x01': 'Other file icon',
                        b'\x02': 'Cover (front)',
                        b'\x03': 'Cover (back)',
                        b'\x04': 'Leaflet page',
                        b'\x05': 'Media (e.g. lable side of CD)',
                        b'\x06': 'Lead artist/lead performer/soloist',
                        b'\x07': 'Artist/performer',
                        b'\x09': 'Conductor',
                        b'\x0A': 'Band/Orchestra',
                        b'\x0B': 'Composer',
                        b'\x0C': 'Lyricist/text writer',
                        b'\x0D': 'Recording Location',
                        b'\x0E': 'During recording',
                        b'\x0F': 'During performance',
                        b'\x10': 'Movie/video screen capture',
                        b'\x11': 'A bright coloured fish',
                        b'\x12': 'Illustration',
                        b'\x13': 'Band/artist logotype',
                        b'\x14': 'Publisher/Studio logotype'
                    }

                    cf['apic_type'] = typemap[apic_type] if apic_type in typemap else ''
                    cf['apic_desc'] = str(apic_desc)
                    print(str(cf['apic_encoding']) + ', ' + str(cf['apic_mime']) + ', ' + str(cf['apic_type']) + ', ' + cf['apic_desc'])
                except Exception as e:
                    print('Frame parsing error: {}'.format(str(e)))
            elif cf['id'] == 
            frame_body = f.read(cf['size'])
            _count += 10 + cf['size']



if __name__ == '__main__':
    header = parse_header("chromakey.mp3")
    frames = parse_frames("chromakey.mp3", 10, header['size'])
