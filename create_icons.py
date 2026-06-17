import struct
import zlib

def create_png(width, height, color, filename):
    # Color RGB
    r, g, b = color
    
    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (image header)
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    ihdr_chunk = b'IHDR' + ihdr_data
    ihdr_crc = struct.pack('>I', zlib.crc32(ihdr_chunk) & 0xffffffff)
    ihdr = struct.pack('>I', len(ihdr_data)) + ihdr_chunk + ihdr_crc
    
    # IDAT chunk (image data)
    scanlines = b''
    for y in range(height):
        scanlines += b'\x00'  # filter type
        scanlines += (bytes([r, g, b]) * width)
    
    idat_data = zlib.compress(scanlines, 9)
    idat_chunk = b'IDAT' + idat_data
    idat_crc = struct.pack('>I', zlib.crc32(idat_chunk) & 0xffffffff)
    idat = struct.pack('>I', len(idat_data)) + idat_chunk + idat_crc
    
    # IEND chunk (end)
    iend_chunk = b'IEND'
    iend_crc = struct.pack('>I', zlib.crc32(iend_chunk) & 0xffffffff)
    iend = struct.pack('>I', 0) + iend_chunk + iend_crc
    
    # Combine all chunks
    png_data = png_signature + ihdr + idat + iend
    
    with open(filename, 'wb') as f:
        f.write(png_data)

# Color azul #4A8FD4
color = (74, 143, 212)

create_png(192, 192, color, 'icon-192.png')
print('OK: icon-192.png')

create_png(512, 512, color, 'icon-512.png')
print('OK: icon-512.png')
