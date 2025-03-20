import json, re
from collections import OrderedDict
print("Loading entre2013e2014.json...")
with(open('entre2013e2024.json', 'r', encoding='utf-8')) as file:
    info = json.load(file)
print("Done.")
newinfo = {
    f"{x} {i}".strip(): y
    for i, j in info.items()
    for x, y in j.items()
}
newinfo = [{
        'cargo': matches.groups()[1],
        'nivel': matches.groups()[0],
        'periodo': matches.groups()[2],
        'contagem': y
    } for x, y in newinfo.items()
    if (matches := re.match(r'^([ABCS][I]{0,3}) (.+) (\d{6})$', x))
]
newinfo = {
    x['cargo']: {
        x2['periodo']: {
            x3['nivel']: x3['contagem']            
            for x3 in newinfo
            if x2['cargo'] == x['cargo'] and x2['cargo'] == x3['cargo'] and x3['periodo'] == x2['periodo']
        }
        for x2 in newinfo
        if x2['cargo'] == x['cargo']}
    for x in newinfo
}
newinfo = OrderedDict(sorted(newinfo.items()))
for cargo in newinfo:
    newinfo[cargo] = OrderedDict(sorted(newinfo[cargo].items()))
    for periodo in newinfo[cargo]:
        newinfo[cargo][periodo] = OrderedDict(sorted(newinfo[cargo][periodo].items()))
        newinfo[cargo][periodo]['total'] = sum(newinfo[cargo][periodo].values())
print("Creating newinfo.json...")
with(open('newinfo.json', 'w', encoding='utf-8')) as file:
    json.dump(newinfo, file, indent=4)
print("Done.")