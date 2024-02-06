import pandas as pd
from collections import Counter
import itertools
import matplotlib.pyplot as plt

"""arrangment"""
def A(a,b):
    S=1
    while b!=0:
        S=a*S
        b=b-1
        a=a-1
    return S
"""combination"""
def C(x,y):
    if x<y:
        print("numbers error!")
        print(x,y)
        return 
    S=int(A(x,y)/A(y,y))
    return S


class Card:
    def __init__(self,CardDeck={}) -> None:
        """定义卡牌的数量,种类,
        """
        self.cardNums=27
        self.cardKind=17
        self.FirstTurn=4
        # self.SecondTurn=5
        
        """cardname:  卡名
            Quantity: 单一卡牌数量
            ID       :卡牌序号作为卡牌的唯一标识,从0开始一一对应
        """
        self.deck=CardDeck
        #以下为例子
        # *************************************************************************************************
        
        self.deck = {"CardName": ["深渊白龙", "深渊之青眼龙", "青眼亚白龙","青眼装甲龙",
                                "效果遮蔽者","太古的白石","白之灵龙","青之眼闲士","青眼白龙",
                                "死者苏生","月之书","禁忌的圣枪","究极结合","黑洞","龙之觉醒旋律",
                                "禁忌的圣杯","神之慑理"],
        "Quantity": [1, 2, 2, 1, 2, 2, 1, 2, 3, 1, 1, 1, 1, 2, 2, 1, 2],
        "ID":       [0, 1, 2, 3, 4, 5, 6, 7 ,8 , 9, 10, 11, 12 ,13, 14, 15, 16]
        }
        #**************************************************************************************************
    def Info_Print(self):
        print(f"牌数{self.cardNums}")
        print(f"种类:{self.cardKind}")
        print(f"卡组信息{self.deck}")
        
    def Save_Info(self):
        #暂且只计算一回合的排列组合
        r=self.FirstTurn
        all_combination=list(itertools.product(range(0,17), repeat=r))
        sort_combination={tuple(sorted(c)) for c in all_combination}
        df=pd.DataFrame(sort_combination,columns=['card1','card2','card3','card4'])
        df.to_excel('./DB/originalData.xlsx',index=False)
        print('save finish')

class DataProcess:
    def __init__(self) -> None:
        self.card=Card()
        self.list_of_probability=[]
        self.coefficient=[]
    

        
    
# print(df.loc[0])

    def clear_data(self):
        try:
            df=pd.read_excel('./DB/originalData.xlsx')
        except FileNotFoundError:
            print("请先执行保存信息程序,获得全部组合且无重复文件!!")
            return
        deck=self.card.deck
        for i in range(len(df)):
            list_of_data=list(df.loc[i].values)
            element_counts=Counter(list_of_data)
            for element, count in element_counts.items():
                if deck['Quantity'][element]<count:
                    try:
                        df.drop(i,inplace=True)
                        break
                    except KeyError:
                        print(f"该列不符合要求{i}")
        df.to_excel("./DB/clearedData.xlsx",index=False)

    def probability_cardComb(self):
        all=0
        cardNums=self.card.cardNums
        FirstTurn=self.card.FirstTurn
        list_of_probability=[]
        coefficient=[]
        deck=self.card.deck
        try:
            df=pd.read_excel('./DB/clearedData.xlsx')
        except FileNotFoundError:
            print("请先获得清理文件!!")
            return
        all=0
        for i in range(len(df)):
            S=1
            list_of_data=list(df.loc[i].values)
            element_counts=Counter(list_of_data)
            for element, count in element_counts.items():
                
                try:
                    S=S*C(deck['Quantity'][element],count)
                except :
                    print(i,element,count)
            list_of_probability.append(S*100/C(cardNums,FirstTurn))
            coefficient.append(S)
            all=all+S
        Xx=C(cardNums,FirstTurn)
        if all==Xx:
            df.to_excel('./DB/PCC.xlsx',index=False)
            print("保存至DB目录下PCC.xlsx文件")
            self.list_of_probability=list_of_probability
            self.coefficient=coefficient
            # print(all,Xx)
            return 
        else:
            print("数据处理不规范")
            df.to_excel('./DB/nonstPCC.xlsx',index=False)
            self.list_of_probability=list_of_probability
            self.coefficient=coefficient
            # print(all,Xx)
            return 
    
    def Id2Name():
        pass
    
    def Save_Comb_Info(self):
        try :
            df=pd.read_excel('./DB/PCC.xlsx')
        except FileNotFoundError:
            print('尝试处理不规范文件')
            df=pd.read_excel('./DB/nonstPCC.xlsx')
        df['probability']=self.list_of_probability
        df_sorted = df.sort_values(by='probability', ascending=False)
        """按照概率大小排序"""
        df_sorted.to_excel('./DB/modPCC.xlsx',index=False)

    def draw_pic_hist(self):
        try :
            df_sorted=pd.read_excel('./DB/modPCC.xlsx')
        except FileNotFoundError:
            print('找不到文件')
            return
        # 绘制直方图
        plt.hist(df_sorted['probability'], bins=50, color='blue', alpha=0.7)
        plt.xlabel('Probability')
        plt.ylabel('Count')
        plt.title('Histogram of Probability')
        plt.savefig("./image/hist.png")
        plt.show()
        return


if __name__=='__main__':
    c=Card()
    dp=DataProcess()
    c.Info_Print()
    c.Save_Info()
    dp.clear_data()
    dp.probability_cardComb()
    dp.Save_Comb_Info()
    dp.draw_pic_hist()