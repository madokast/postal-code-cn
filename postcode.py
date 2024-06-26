import json
import bisect

_Data = None
_Data_List = None

def resolve(postcode):
    postcode = str(postcode)
    if len(postcode) > len('100032'):
        postcode = postcode[:len('100032')]
    while len(postcode) < len('100032'):
        postcode = postcode + '0'

    global _Data
    global _Data_List
    if _Data is None:
        with open("data.json", mode='r', encoding='utf-8') as f:
            _Data = json.load(f)
            _Data_List = [int(code) for code in _Data]
            _Data_List.sort()
    area = _Data.get(str(postcode), ('', '', ''))
    if not any(area):
        postcode = int(postcode)
        index = bisect.bisect_left(_Data_List, postcode)
        if index == 0:
            area = _Data[str(_Data_List[index])]
        else: # 找左侧的
            if _Data_List[index] // 100 == _Data_List[index-1] // 100: # 必须同区
                area = _Data[str(_Data_List[index-1])]
            else:
                area = _Data[str(_Data_List[index])]
                area = (area[0], area[1], '')

        if postcode % 10000 == 0:
            area = (area[0], area[1], '')
        
    return tuple(area)


if __name__ == '__main__':
    print(resolve(100032)) # ('北京市', '', '西城区')
    print(resolve(100000)) # ('北京市', '', '')

    print(resolve(518109)) # ('广东省', '深圳市', '龙华区')
    print(resolve(518110)) # ('广东省', '深圳市', '龙华区')
    print(resolve(518000)) # ('广东省', '深圳市', '罗湖区')
    print(resolve(518001)) # ('广东省', '深圳市', '罗湖区')


    