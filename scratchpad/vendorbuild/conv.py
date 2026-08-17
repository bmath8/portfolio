from fontTools.ttLib import TTFont
import glob, os
src = r'C:\Brian\02_Projects\portfolio\vendor\fonts'
dst = os.path.join(src, '_ttf')
n=0
for f in glob.glob(os.path.join(src,'*.woff2')):
    name = os.path.splitext(os.path.basename(f))[0]
    try:
        t = TTFont(f); t.flavor=None
        t.save(os.path.join(dst, name + '.ttf')); n+=1
    except Exception as e:
        print('skip', name, e)
print('converted', n)
