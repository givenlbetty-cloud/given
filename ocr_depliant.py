import pytesseract
from PIL import Image
import os, shutil

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Dossier tessdata local avec français + anglais
local_tessdata = r'C:\Users\AL\Downloads\tessdata_fr'
os.makedirs(local_tessdata, exist_ok=True)

# Copier les fichiers de langue
src_eng = r'C:\Program Files\Tesseract-OCR\tessdata\eng.traineddata'
src_fra = r'C:\Users\AL\Downloads\fra.traineddata'
dst_eng = os.path.join(local_tessdata, 'eng.traineddata')
dst_fra = os.path.join(local_tessdata, 'fra.traineddata')

if not os.path.exists(dst_eng):
    shutil.copy(src_eng, dst_eng)
if not os.path.exists(dst_fra):
    shutil.copy(src_fra, dst_fra)

print("=== OCR DÉPLIANT ATJ ===\n")

for page in [1, 2]:
    img_path = rf'C:\Users\AL\Downloads\depliant_p{page}_img1.png'
    img = Image.open(img_path)
    print(f'--- PAGE {page} ({img.size[0]}x{img.size[1]}) ---')

    # OCR en français avec tessdata local
    text = pytesseract.image_to_string(
        img, 
        lang='fra',
        config=f'--tessdata-dir "{local_tessdata}"'
    )
    print(text)
    print('=' * 50)
    print()

print("Terminé!")