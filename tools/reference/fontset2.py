import array, json
p = r'E:/Game/Steam/steamapps/common/KillerIsDead/KidGame/CookedPC/Startup_LOC_INT.upk'
d = open(p,'rb').read()
a = array.array('H'); a.frombytes(d[:len(d)//2*2])
OFF = 2583964//2
N = 1746
pairs = [(a[OFF+k*2], a[OFF+k*2+1]) for k in range(N)]
cs = set(c for c,_ in pairs)
print('完整映射条目', len(pairs), '唯一码点', len(cs))
print('索引是否连续递增:', all(pairs[k][1]==pairs[k-1][1]+1 for k in range(1,N)))
print('非CJK字符:', ''.join(chr(c) for c in sorted(cs) if not (0x4E00<=c<=0x9FFF)))
json.dump(sorted(cs), open(r'E:/Temp/kid/font_full.json','w'))
print('已保存 font_full.json')
