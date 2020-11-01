class checkJSON(object):
    keysAll_list = []
    def getKeys(self,data={}):   #遍历json所有key
        if(type(data)==type({})):
            keys=data.keys()
            for key in keys:
                value=data.get(key)
                if(type(value) != type({}) and type(value) != type([])):
                    self.keysAll_list.append( key)
                elif (type(value) == type({})):
                    self.keysAll_list.append(key)
                    self.getKeys(value)
                elif(type(value) == type([])):
                    self.keysAll_list.append(key)
                    for para in value:
                        if (type(para) == type({}) or type(para) == type([])):
                            self.getKeys(para)
                        else:
                            self.keysAll_list.append(para)
        return self.keysAll_list

    def isExtend(self,data,tagkey):   #检测目标字段tagkey是否在data(json数据)中
        if(type(data)!=type({})):
            print('please input a json!')
        else:
            key_list=self.getKeys(data)
            for key in key_list:
                if(key==tagkey):
                    return True
        return False

if __name__ == '__main__':
    cjson=checkJSON()
    data={
        "code": 0,
        "msg": "ok",
        "data": {
            "list": [
                {
                    "stock_id0": "601318.SH",
                    "stock_code0": "601318",
                    "stock_name0": "中国平安",
                },{
                    "stock_id1": "600000.SH",
                    "stock_code1": "600000",
                    "stock_name1": "浦发银行",
                }
            ]
        },
        "pass":{
            "stock_id2": "600000.SH",
            "stock_code2": "600000",
            "stock_name2": "浦发银行",
        },
        "call_stack": ""
    }
    list=cjson.getKeys(data)
    print(type(data))
    print(cjson.isExtend(data,'stock_name0'))
