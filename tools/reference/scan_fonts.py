import os, array, struct
G = r'E:/Game/Steam/steamapps/common/KillerIsDead/KidGame/CookedPC'
needle_chars = set('館發說誘闆隻週歷歸懷巔闖')
results=[]
for dp,_,fs in os.walk(G):
    for f in fs:
        if not f.endswith(('.upk','.u')): continue
        p=os.path.join(dp,f)
        sz=os.path.getsize(p)
        if sz > 40*1024*1024: continue
        try: d=open(p,'rb').read()
        except: continue
        a=array.array('H'); a.frombytes(d[:len(d)//2*2]); n=len(a)
        run=0; start=0; found=[]
        for i in range(0,n-1,2):
            c=a[i]
            if 0x3000<=c<=0x9FFF and (run==0 or a[i+1]==a[i-1]+1):
                if run==0: start=i
                run+=1
            else:
                if run>=300:
                    chars=set(chr(a[start+k*2]) for k in range(run) if 0x4E00<=a[start+k*2]<=0x9FFF)
                    trad=len(chars & needle_chars)
                    found.append((start*2,run,len(chars),trad))
                run=0
        if run>=300:
            chars=set(chr(a[start+k*2]) for k in range(run) if 0x4E00<=a[start+k*2]<=0x9FFF)
            found.append((start*2,run,len(chars),len(chars & needle_chars)))
        if found:
            results.append((os.path.relpath(p,G), sz, found))
for rel,sz,found in results:
    print('==',rel,'%.1fMB'%(sz/1048576))
    for off,cnt,uniq,trad in found[:8]:
        print('    off=%d 对数=%d 唯一汉字=%d 繁体样例命中=%d' % (off,cnt,uniq,trad))
print('含映射表的文件数', len(results))
