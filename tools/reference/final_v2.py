# -*- coding: utf-8 -*-
import os, glob, json, shutil
MOV=r'E:/Game/Steam/steamapps/common/KillerIsDead/KidGame/Movies'
BAK=r'E:/Temp/kid/backup_movies_before_glyphfix'
CS=set(chr(c) for c in json.load(open(r'E:/Temp/kid/font_full.json')))
def miss(ch):
    o=ord(ch)
    if o<0x80 or ch in '·—‘’“”…': return False
    return ch not in CS

SIM=[
 ('深♂入♀了解你','深入了解你'),
 ('纵横南北','走遍南北'),('成为了历史','成为了过去'),
 ('时光流逝','时光流去'),('抹杀','消除'),
 ('左撇子','用左手'),('搞砸了','搞坏了'),
 ('蒙德·扎帕','蒙德·札帕'),('阁下','先生'),
 ('臆测','猜测'),('恶徒','恶人'),('难以忘怀','难以忘记'),
 ('闇暗','黑暗'),('吃饱了撑的慌','吃饱了没事做'),
 ('虎已逝','虎已不在'),('龙犹存','龙还在'),
 ('忽略这么个东西','无视这么个东西'),
]
# 繁体：只替换确定缺的字，替换目标全部是字库内字；其余繁体字一律不动
TRAD=[
 ('深♂入♀瞭解你','深入了解你'),
 ('時光流逝','時光流去'),('抹殺','消除'),
 ('誘拐','拐走'),('很誘人','很吸引人'),('左撇子','用左手'),
 ('搞砸了','失手了'),('蒙德·扎帕','蒙德·札帕'),('閣下','先生'),
 ('臆測','猜測'),('惡徒','惡人'),('難以忘怀','忘不了'),('難以忘懷','忘不了'),
 ('闇暗','黑暗'),('吃飽了撐的慌','吃太飽了'),
 ('虎已逝','虎已去'),('龍猶存','龍仍在'),
 ('忽略這麼個東西','不理這麼個東西'),
 ('縱橫南北','走遍南北'),('成為了歷史','成為了過去'),
 ('♀','女'),('♂','男'),
]
# 恢复原点
for p in glob.glob(os.path.join(MOV,'*.txt')):
    s=os.path.join(BAK,os.path.basename(p))
    if os.path.exists(s): shutil.copy2(s,p)

for suf,rules in (('INT',SIM),('JPN',TRAD)):
    n=0
    for p in sorted(glob.glob(os.path.join(MOV,'*_%s.txt'%suf))):
        raw=open(p,'rb').read(); bom=raw[:2]==b'\xff\xfe'
        text=raw.decode('utf-16'); out=[]
        for line in text.splitlines(True):
            nl=''
            if line.endswith('\r\n'): nl='\r\n'; line=line[:-2]
            elif line.endswith('\n'): nl='\n'; line=line[:-1]
            if ',' in line:
                a=line.split(',',2); body=a[2]
                for x,y in rules: body=body.replace(x,y)
                if body!=a[2]: n+=1
                line=a[0]+','+a[1]+','+body
            out.append(line+nl)
        nt=''.join(out)
        if nt!=text: open(p,'wb').write((b'\xff\xfe' if bom else b'')+nt.encode('utf-16-le'))
    print('%s 改写 %d 行' % (suf,n))

print('\n=== 用户点名处 ===')
for f in ('KID_EP1_EN_INT.txt','KID_EP1_EN_JPN.txt'):
    for l in open(os.path.join(MOV,f),'rb').read().decode('utf-16','ignore').splitlines():
        if '12000' in l: print(' ',f,'|',l)
print('\n=== 简体零缺字校验 ===')
bad=[]
for p in glob.glob(os.path.join(MOV,'*_INT.txt')):
    for l in open(p,'rb').read().decode('utf-16','ignore').splitlines():
        if ',' not in l: continue
        h=set(c for c in l.split(',',2)[-1] if miss(c))
        if h: bad.append((os.path.basename(p),''.join(h)))
print('简体仍缺字行数',len(bad), bad[:5])
print('\n=== 繁体：原缺字是否清干净 ===')
target=set('撇逝抹砸扎臆徒闇慌撑犹忽誘纵历阁怀♀♂')
rem=[]
for p in glob.glob(os.path.join(MOV,'*_JPN.txt')):
    for l in open(p,'rb').read().decode('utf-16','ignore').splitlines():
        if ',' not in l: continue
        h=set(c for c in l.split(',',2)[-1] if c in target)
        if h: rem.append((os.path.basename(p),''.join(h),l[:70]))
print('残留行数',len(rem))
for r in rem[:10]: print('   ',r)
