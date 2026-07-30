import sys
from PyPDF2 import PdfReader
from PIL import Image
import io, os

reader = PdfReader(r'C:\Users\AL\Downloads\Dépliant.pdf')
print(f'Pages: {len(reader.pages)}')

for page_num, page in enumerate(reader.pages):
    count = 0
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].get_object()
        for obj_name in xObject:
            obj = xObject[obj_name].get_object()
            if obj['/Subtype'] == '/Image':
                count += 1
                data = obj.get_data()
                width = obj['/Width']
                height = obj['/Height']
                bits_per_pixel = obj['/BitsPerComponent']
                
                ext = 'png' if bits_per_pixel == 8 else 'jpg'
                fname = rf'C:\Users\AL\Downloads\depliant_p{page_num+1}_img{count}.{ext}'
                
                filter_type = obj.get('/Filter', 'None')
                print(f'Page {page_num+1}, Image {count}: Filter={filter_type}, Size={width}x{height}, Bits={bits_per_pixel}')
                
                if filter_type == '/DCTDecode':
                    with open(fname, 'wb') as f:
                        f.write(data)
                    print(f'  -> JPEG sauvegardé: {fname}')
                elif filter_type == '/FlateDecode':
                    try:
                        img = Image.frombytes('RGB', (width, height), data)
                        img.save(fname)
                        print(f'  -> PNG sauvegardé: {fname}')
                    except Exception as e:
                        print(f'  -> ERREUR: {e}')
                else:
                    try:
                        with open(fname, 'wb') as f:
                            f.write(data)
                        print(f'  -> Brut sauvegardé: {fname}')
                    except:
                        print(f'  -> Échec sauvegarde')
    
    print(f'  Total images page {page_num+1}: {count}')

print('\nTerminé!')