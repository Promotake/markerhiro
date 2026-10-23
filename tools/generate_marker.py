"""Create a high-contrast HIRO marker image and print-ready A4 PDF.

This local vector reconstruction follows the standard HIRO marker layout.
For the exact upstream bitmap, see the README official marker URL.
"""
from PIL import Image, ImageDraw
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

root=Path(__file__).resolve().parents[1]
out=root/'marker'; out.mkdir(exist_ok=True)
scale=2
im=Image.new('RGB',(1000*scale,1000*scale),'white')
d=ImageDraw.Draw(im)
def rc(box,color): d.rectangle(tuple(round(v*scale) for v in box),fill=color)
def el(box,color): d.ellipse(tuple(round(v*scale) for v in box),fill=color)
def poly(points,color): d.polygon([(round(x*scale),round(y*scale)) for x,y in points],fill=color)
# Marker: white quiet zone, black outside, centered white identification patch.
rc((40,40,959,959),'black')
rc((270,270,729,729),'white')
# Hiro logotype traced at the geometry and proportions of ARToolKit's classic image.
rc((289,542,321,707),'black')
rc((387,542,419,707),'black')
rc((312,604,398,633),'black')
# 'i' and its square dot
rc((446,542,481,573),'black')
rc((447,584,481,707),'black')
# 'r' curved shoulder
rc((506,583,538,707),'black')
poly([(533,596),(545,585),(556,580),(570,578),(577,580),(574,612),(562,608),(553,611),(544,617),(537,633)],'black')
# 'o' round letter with negative space
el((584,578,711,710),'black')
el((617,607,680,679),'white')
# Nearest-neighbour sampling preserves clean, hard edges to aid detection.
im.resize((1000,1000), Image.Resampling.LANCZOS).save(out/'hiro.png',compress_level=9)

# Train the actual marker printed above as a LOCAL ARToolKit pattern (16x16,
# 4 rotations, 3 BGR channels). Main page uses this .patt file, so the marker
# and the training pattern match exactly, not just visually.
inner=im.crop((270*scale,270*scale,730*scale,730*scale))
blocks=[]
for angle in (0,90,180,270):
    small=inner.rotate(angle, expand=False, resample=Image.Resampling.BICUBIC).resize((16,16), Image.Resampling.BOX).convert('RGB')
    for channel in (2,1,0):
        for y in range(16):
            blocks.append(' '.join(str(small.getpixel((x,y))[channel]).rjust(3) for x in range(16)))
    blocks.append('')
(out/'hiro_local.patt').write_text('\n'.join(blocks)+'\n',encoding='ascii')

reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',reg))
pdfmetrics.registerFont(TTFont('DejaVu-Bold',bold))
p=canvas.Canvas(str(out/'hiro_print_A4.pdf'),pagesize=A4)
w,h=A4
p.setFillColor(HexColor('#1C2A40'))
p.setFont('DejaVu-Bold',21)
p.drawCentredString(w/2,h-73,'AR.js / A-Frame - лабораторная работа 4')
p.setFont('DejaVu',11)
p.setFillColor(HexColor('#526173'))
p.drawCentredString(w/2,h-99,'Маркер HIRO для отслеживания 3D-модели')
# 150mm square printed unchanged and centred.
side=150/25.4*72
x=(w-side)/2
y=(h-side)/2-10
p.drawImage(ImageReader(str(out/'hiro.png')),x,y,width=side,height=side,mask='auto')
p.setFont('DejaVu',10)
p.setFillColor(HexColor('#1C2A40'))
p.drawCentredString(w/2, y-29, 'Печатать без обрезки. Держать маркер целиком в кадре камеры.')
p.setFillColor(HexColor('#6E7E91'))
p.setFont('DejaVu',9)
p.drawCentredString(w/2, 53, 'Можно также открыть hiro.png на экране второго устройства.')
p.setTitle('LR4 - HIRO marker A4')
p.setAuthor('LR4 AR.js project')
p.save()
print('created', out/'hiro.png', out/'hiro_print_A4.pdf')
