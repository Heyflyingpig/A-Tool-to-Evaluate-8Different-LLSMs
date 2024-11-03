import json

data = {
 "math_question": [
        {
            "id": 1,  # 题目id
            "year": 2019,  # 题目所属年份
            "difficulty": "ez",  # 题目难度
            "type": "choice" ,  # 题型
            "number": "N1",  # 编号
            "Source": "新课标1", # 题目所属卷型
            "Description": [
                {
                    "Qu" : "已知集合M={x|-4<x<2}，N={x|x^2-x-6< 0}，则M∩N = () A．{x|-4<x<3}	B．{x|-4<x< 2}	C．{x|-2<x<2}	D．{x|2<x<3}  "
                }
            ],  # 题目描述
            "An": "C"  # 题目答案
        },  # 201901,1,ez
        {
            "id": 2,
            "year": 2019,
            "difficulty": "av",
            "type": "choice" ,
            "number": "N4",
            "Source": "新课标1",
            "Description": [
                {
                    "Qu" : "古希腊时期，人们认为最美人体的头顶至肚脐的长度与肚脐至足底的长度之比是:$a = \\log_{2} 0.2$,b=2^0.2,c=0.2^0.3（a<b<c≈0.618，称为黄金分割比例)，著名的“断臂维纳斯”便是如此．此外，最美人体的头顶至咽喉的长度与咽喉至肚脐的长度之比也是a<c<b．若某人满足上述两个黄金分割比例，且腿长为105 cm，头顶至脖子下端的长度为26 cm，则其身高可能是A. 165 cm B. 175 cm C. 185 cm D. 190cm"

                }
            ],
            "An": "B"
        },  # 201901,4,av
        {
            "id": 3,
            "year": 2019,
            "difficulty": "me",
            "type": "choice" ,
            "number": "N10",
            "Source": "新课标1",
            "Description": [
                {
                    "Qu" :r"""已知椭圆 \( C \) 的焦点为 \( F_1(-1,0)，F_2(1,0) $，过 \( F_2 $ 的直线与 \( C $ 交于 \( A $，$ B $ 两点．若 \( |AF_2| = 2|F_2B| $，\( |AB| = |BF_1| $，则 \( C $ 的方程为
\[ \begin{cases}
    \frac{x^2}{2} + y^2 = 1 \\
    \frac{x^2}{3} + \frac{y^2}{2} \\
    \frac{x^2}{4} + \frac{y^2}{3} \\
    \frac{x^2}{5} + \frac{y^2}{4}
\end{cases} \]
A．$\frac{x^2}{2} + y^2 = 1$ & B．$\frac{x^2}{3} + \frac{y^2}{2}$ & C．$\frac{x^2}{4} + \frac{y^2}{3}$ & D．$\frac{x^2}{5} + \frac{y^2}{4}$"
"""
                }
            ],
            "An": "B"
        },  # 201901,10,me
        {
            "id": 4,
            "year": 2019,
            "difficulty": "ha",
            "type": "choice" ,
            "number": "N12",
            "Source": "新课标1",
            "Description": [
                {
                    "Qu": r"""已知三棱锥 \( P -ABC $ 的四个顶点在球 \( O $ 的球面上，\( PA = PB = PC $，△\( ABC $ 是边长为 \( 2 $ 的正三角形，\( E $，\( F $ 分别是 \( PA $，\( PB $ 的中点，∠\( CEF $=90°，则球 \( O $ 的体积为
\[ \begin{cases}
    8\sqrt{6}\pi \\
    4\sqrt{6}\pi \\
    2\sqrt{6}\pi \\
    \sqrt{6}\pi
\end{cases} \]
A．$8\sqrt{6}\pi$ & B．$4\sqrt{6}\pi$ & C．$2\sqrt{6}\pi$ & D．$\sqrt{6}\pi$
"""
                }
            ],
            "An": "D"
        },  # 201901,12,ha

        {
            "id": 5,
            "year": 2019,
            "difficulty": "ez",
            "type": "gap" ,
            "number": "N13",
            "Source": "新课标1",
            "Description": [
                {
                    "Qu" :r"""13．曲线 \( y = 3(x^2 + x)e^{-x} $ 在点 $(0,0)$ 处的切线方程为 ____________．"""
                }
            ],
            "An": "y=3x"
        },  # 201901,13,ez
        {
            "id": 6,
            "year": 2019,
            "difficulty": "av",
            "type": "gap" ,
            "number": "N14",
            "Source": "新课标1",
            "Description": [
                {
                    "Qu" :r"""14．记 \( S_n $ 为等比数列 $\left\{a_n\right\}$ 的前 \( n $ 项和． 若 \( a_1=\frac{1}{3} $， \( a_4^2=a_6 $， 则 \( S_5=$______________．"""
                }
            ],
            "An": "121/3"
        },  # 201901,14,av
        {
                    "id": 7,
                    "year": 2019,
                    "difficulty": "me",
                    "type": "gap" ,
                    "number": "N15",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu" :r"""甲、乙两队进行篮球决赛，采取七场四胜制（当一队赢得四场胜利时，该队获胜，决赛  
结束）．根据前期比赛成绩，甲队的主客场安排依次为“主主客客主客主”．设甲队主场取
胜的概率为0.6，客场取胜的概率为0.5，且各场比赛结果相互独立，则甲队以4∶1获胜的概
率是____________
"""
                        }
                    ],
                    "An": "0.216"
                },  # 201901,15,me
        {
                    "id": 8,
                    "year": 2019,
                    "difficulty": "ha",
                    "type": "gap" ,
                    "number": "N16",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu" :r"""16．已知双曲线 \( C $：$\frac{x^2}{a^2}-\frac{y^2}{b^2}=1(a>0,b>0)$ 的左、右焦点分别为 \( F_1 $，\( F_2 $，过 \( F_1 $ 的直线与 \( C $ 的两条渐近线分别交于 \( A $，\( B $ 两点．若 \( \overrightarrow{{F}_{1}A}=\overrightarrow{AB} $，\( \overrightarrow{{F}_{1}B}⋅\overrightarrow{{F}_{2}B}=0 $，则 \( C $ 的离心率为 ____________．
"""
                        }
                    ],
                    "An": "2"
                },  # 201901,16,ha

        {
                    "id": 9,
                    "year": 2019,
                    "difficulty": "ez",
                    "type": "comprehensive" ,
                    "number": "N17",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu" :r"""17．$\triangle ABC $ 的内角 \( A $，\( B $，\( C $ 的对边分别为 \( a $，\( b $，\( c $， 设
\[ (\sin B-\sin C)^2=sin^2 A-sin B sin C $．
\[ （1）求 \( A $；
\[ （2）若 $\sqrt{2a+b}=2c $， 求 \( sin C $.

"""
                        }
                    ],
                    "An": r"""\[ 【答案】 （1）$A=\frac{\pi}{3}$；（2）$sin C=\frac{\sqrt{6}+\sqrt{2}}{4}$．．
                    """
                },  # 201901,17,ez
        {
                    "id": 10,
                    "year": 2019,
                    "difficulty": "ez",
                    "type": "comprehensive" ,
                    "number": "N19  ",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu" :r"""19．已知抛物线 \( C $：$y^2=3x$ 的焦点为 \( F $， 斜率为$-\frac{3}{2}$ 的直线 \( l $ 与 \( C $ 的交点为 \( A $，\( B $， 与x轴的交点为 \( P $．
\[ （1）若 \( |AF|+|BF|=4 $，求 \( l $ 的方程；
\[ （2）若 $\overrightarrow{AP}=3\overrightarrow{PB}$， 求 \( |AB|$．
"""
                        }
                    ],
                    "An": r"""\[ 【答案】（1）$12x-8y-7=0$；（2）$\frac{4\sqrt{13}}{3}$．
                    """
                },  # 201901,19,av
        {
                    "id": 11,
                    "year": 2019,
                    "difficulty": "me",
                    "type": "comprehensive" ,
                    "number": "N20",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu" :r"""20．已知函数 \( f(x)=sin x-ln(1+x) $， \( f'(x) $ 为 \( f(x) $ 的导数．证明：
\[ （1）f'(x) $ 在区间$ (-1,\frac{\pi}{2}) $存在唯一极大值点；
\[ （2）\( f(x) $有且仅有2个零点．
"""
                        }
                    ],
                    "An": r"""20．[详解]（1）由意得：\( f(x)=cos x+\frac{1}{x+1} $， \( x∈(-1,\frac{\pi}{2}) $
\[ ∴g'(x)=-sin x+\frac{1}{(x+1)^2} $， \( x∈(-1,\frac{\pi}{2}) $，
\[ ∴\frac{1}{(x+1)^2} $在$ (-1,\frac{\pi}{2}) $上单调递减， \( a_{n+1}-a_n=\frac{1}{n(n+1)} $， \( a_n $在$ (-1,\frac{\pi}{2}) $上单调递增， \( a_n $在$ (-1,\frac{\pi}{2}) $上单调递减
\[ 又∵g'(\frac{\pi}{2})=-sin \frac{\pi}{2}+\frac{1}{(\frac{\pi}{2}+1)^2}=-1+\frac{1}{(\frac{\pi}{2}+1)^2} < 0 $， \( g'(0)=-sin 0+1=1 > 0 $， \( g'(\frac{\pi}{2})=-\sin \frac{\pi}{2}+\frac{4}{\pi+2}=\frac{4}{\pi+2}-1 < 0 $，
\[ ∴∃x_0∈(0,\frac{\pi}{2}) $，使得\( g'(x_0)=0 $，
\[ 即\( g(x) $在$ (-1,x_0) $上单调递增，在$ (x_0,\frac{\pi}{2}) $上单调递减
\[ 则\( x=x_0 $为\( g(x) $唯一的极大值点
\[ 即\( f'(x) $在区间$ (-1,\frac{\pi}{2}) $存在唯一的极大值点\( x_0 $．
\[ （2）由（1）知：\( f'(x)=cos x+\frac{1}{x+1} $， \( x∈(-1,∞)
\[ ①当\( x∈(-1,0] $时，由（1）可知\( f'(x) $在$ (-1,0] $上单调递增
\[ ∴\( f'(x)\leqslant f'(0)=0 $∴\( f'(x) $在$ (-1,0] $上单调递减
\[ 又\( f'(0)=0 $∴\( f(x) $在$ (-1,0] $上的唯一零点
\[ ②当\( x∈(0,\frac{\pi}{2}] $时，\( f'(x) $在$ (0,x_0) $上单调递增，在$ (x_0,\frac{\pi}{2}) $上单调递减
\[ 又\( f'(x_0)=0 $∴\( f'(x) $在$ (0,x_0) $上单调递增，此时\( f(x)>f(0)=0 $，不存在零点
\[ 又\( f'(\frac{\pi}{2})=\cos \frac{\pi}{2}-\frac{2}{\pi+2}=-\frac{2}{\pi+2} < 0 $，
\[ ∴∃x_0∈(0,\frac{\pi}{2}) $，使得\( f'(x_0)=0 $，
\[ 即\( f(x) $在$ (x_0,\frac{\pi}{2}) $上单调递减，在$ (\frac{\pi}{2},π) $上单调递增
\[ 又\( f(x_0)>f(0)=0 $， \( f(\frac{\pi}{2})=sin \frac{\pi}{2}-ln(\pi+1)=-ln(\pi+1) < 0 $，
\[ ∴\( f(x) $在$ (\frac{\pi}{2},π) $上存在唯一零点
\[ ③当\( x∈[\frac{\pi}{2},π] $时，\( sin x $单调递减， \( -ln(x+1) $单调递减
\[ ∴\( f(x) $在$ [\frac{\pi}{2},π] $上单调递减
\[ 又\( f(\frac{\pi}{2}) > 0 $， \( f(π)=sin π-ln(\pi+1)=-ln(\pi+1) < 0 $，
\[ 即\( f(x) $在$ (\frac{\pi}{2},π) $上存在唯一零点
\[ ④当\( x∈(π,∞) $时，\( sin x∈[-1,1] $， \( ln(x+1)>ln(\pi+1)>ln e=1 $，
\[ ∴sin x-ln(x+1) < 0 $即\( f'(x) $在$ (π,∞) $上不存在零点
\[ 综上所述：\( f(x) $有且仅有两个零点
                    """
                },  # 201901,20,me
        {
                    "id": 12,
                    "year": 2019,
                    "difficulty": "ha",
                    "type": "comprehensive" ,
                    "number": "N21",
                    "Source": "新课标1",
                    "Description": [
                        {
                            "Qu": r"""21．为了治疗某种疾病，研制了甲、乙两种新药，希望知道哪种新药更有效，为此进行动物试验．试验方案如下：每一轮选取两只白鼠对药效进行对比试验．对于两只白鼠，随机选一只施以甲药，另一只施以乙药．一轮的治疗结果得出后，再安排下一轮试验．当其中一种药治愈的白鼠比另一种药治愈的白鼠多4只时，就停止试验，并认为治愈只数多的药更有效．为了方便描述问题，约定：对于每轮试验，若施以甲药的白鼠治愈且施以乙药的白鼠未治愈则甲药得1分，乙药得−1分；若施以乙药的白鼠治愈且施以甲药的白鼠未治愈则乙药得1分，甲药得−1分；若都治愈或都未治愈则两种药均得0分．甲、乙两种药的治愈率分别记为 \( α $和 \( β $，一轮试验中甲药的得分记为 \( X $．
\[ （1）求 \( X $的分布列；
\[ （2）若甲药、乙药在试验开始时都赋予4分， \( p_i(i=0,1,…,8) $表示“甲药的累计得分为 \( i $时最终认为甲药比乙药更有效”的概率，则 \( p_0=0 $， \( p_8=1 $， \( p_i=aP(X=-1)+bP(X=0)+cP(X=1) $（\( i=1,2,…,7），其中 \( a=P(X=-1)， \( b=P(X=0)， \( c=P(X=1) $．假设 \( α=0.5 $， \( β=0.8 $．
\[ （i）证明： \( {p}_{i+1}-{p}_{i}(i=0,1,2,…,7) $为等比数列；
\[ （ii）求 \( p_4 $，并根据 \( p_4 $的值解释这种试验方案的合理性．
"""
                        }
                    ],
                    "An": r"""首先确定X所有可能的取值，再来计算出每个取值对应的概率，从而可得分布列；
（2）（i）求解出, , abc的取值，可得p_i = 0.4 * p_{i-1} + 0.5 * p_i + 0.1 * p_{i+1}  # (i = 1, 2, ..., 7)从而
整理出符合等比数列定义的形式，问题得证；（ii）列出证得的等比数列的通项公式，采
用累加的方式，结合p_8和P_0
 p的值可求得p_1,再次利用累加法可求出p_4
\begin{table}[h]
    \centering
    \begin{tabular}{|c|c|}
        \hline
        $X$ & $-1$ & $0$ & $1$ \\
        \hline
        $P(X)$ & $\left(1-\alpha\right)\beta$ & $\alpha\beta+\left(1-\alpha\right)\left(1-\beta\right)$ & $\alpha\left(1-\beta\right)$ \\
        \hline
    \end{tabular}
    \caption{分布列}
\end{table}

\begin{equation*}
    (2) \quad \because \alpha=0.5, \quad \beta=0.8
\end{equation*}

\begin{equation*}
    \therefore a=0.5\times0.8=0.4, \quad b=0.5\times0.8+0.5\times0.2=0.5, \quad c=0.5\times0.2=0.1
\end{equation*}

\begin{equation*}
    (\text{i}) \quad \because p_i=aq_{i-1}+bp_i+cq_{i+1}(i=1,2,\cdots,7)
\end{equation*}

\begin{equation*}
    \text{即 }p_i=0.4q_{i-1}+0.5p_i+0.1q_{i+1}(i=1,2,\cdots,7)
\end{equation*}

\begin{equation*}
    \text{整理可得: }5p_i=4q_{i-1}+q_{i+1}(i=1,2,\cdots,7) \quad \therefore p_{i+1}-p_i=4(p_i-p_{i-1})(i=1,2,\cdots,7)
\end{equation*}
                    """
                },  # 201901,21,ha

    ]
}
with open('question_example.json', 'w', encoding='utf-8') as f:  # 打开question_data.json文件用于写入操作，with保证一直连续写入
    json.dump(data, f, ensure_ascii=False, indent=4)  # ensure_ascii=False表示输出的JSON字符串可以包含非ASCII字符，且保证格式为缩进为4个字符