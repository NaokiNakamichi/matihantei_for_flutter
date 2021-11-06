import collections
import random
import copy
import time


# 入力に対して待ちを判定するクラス。
class hantei:
    def __init__(self):
        self.hantei_time = 0
    # 三つの数字（牌）が連番かどうかをCheck
    def renban_check(self, x):
        x.sort()
        if (x[0] + 1 == x[1]) and (x[1] + 1 == x[2]):
            return True
        else:
            return False

    # ４枚の牌に対して待ちを確認する。
    def check_4(self, nyuryoku):
        k = str(nyuryoku)
        tehai = []
        hora = []
        for i in k:
            tehai.append(int(i))
        # 手牌が一種理になることはないのでその場合はPass
        if len(set(tehai)) == 1:
            return []
        # :TODO 絶対もっとスマートな書き方がある。
        else:
            for i in range(1, 10):
                kari_tehai = tehai + [i]
                if len(set(kari_tehai)) != len(kari_tehai):
                    c = collections.Counter(kari_tehai)
                    for key, value in c.items():
                        # ここで同じ種類が2枚以上あるものについて雀頭として抜き出す。
                        if value > 1:
                            kari_tehai.remove(key)
                            kari_tehai.remove(key)
                            # 刻子があれば和了
                            if len(set(kari_tehai)) == 1:
                                hora.append(i)
                            # 順子があれば和了
                            if self.renban_check(kari_tehai):
                                hora.append(i)
                            kari_tehai.append(key)
                            kari_tehai.append(key)
            return set(hora)

    # 連番（順子）を取り除く. １３枚の入力なら１０枚の返り値
    def remove_3_syuntsu(self, x, i):
        x.remove(i)
        x.remove(i + 1)
        x.remove(i + 2)
        return x

    # 同じ三つの数字（刻子）を取り除く。上と同様
    def remove_3_kotsu(self, x, i):
        x.remove(i)
        x.remove(i)
        x.remove(i)
        return x

    # リストから数字に変換
    # :TODO リストから数字に変換したり文字列に変換したりとしているがそんなことやる必要がない気がする。
    def list_to_int(self, x):
        k = ""
        for j in x:
            k += str(j)
        l = int(k)
        return l
    """
    現在の手配から刻子もしくは順子を抜き出す。
    全ての抜き出し方について考え、抜き出したあと全ての候補をリストにして返り値にする。
    １３枚の手牌なら10枚の手牌の複数候補を返す。
    """

    def sweap_3(self, x):
        tehai = []
        sweap_list = []
        for i in str(x):
            tehai.append(int(i))
        tehai.sort()
        c = collections.Counter(tehai)
        syurui = set(tehai)
        for i in range(1, 8):
            kari_tehai = copy.deepcopy(tehai)
            if (i in syurui) and (i + 1 in syurui) and (i + 2 in syurui):
                k = self.remove_3_syuntsu(kari_tehai, i)
                sweap_list.append(self.list_to_int(k))
        for i in range(1, 10):
            kari_tehai = copy.deepcopy(tehai)
            if c[i] > 2:
                k = self.remove_3_kotsu(kari_tehai, i)
                sweap_list.append(self.list_to_int(k))
        return sweap_list

    """
    上記の関数を用いて主にsweap_3を使って全パターンを抜き出していきその論理和を最終の待ちとしている。
    :TODO 七対子が判定できていない。
    """
    def hanteikun(self, x):
        start = time.time()
        kouho_1 = self.sweap_3(x)
        hora = set()
        for k in kouho_1:
            kouho_2 = self.sweap_3(k)
            for j in kouho_2:
                kouho_3 = self.sweap_3(j)
                for l in kouho_3:
                    hora = hora | set(self.check_4(l))
        self.hantei_time = time.time() - start
        return hora

class nanikiru(hantei):
    def __init__(self):
        super(nanikiru, self).__init__()

    def maisuu_check(self,tehai, mati):
        col = collections.Counter(list(str(tehai)))
        maisuu = 0
        for c in mati:
            maisuu += (4 - col[str(c)])

        return maisuu

    def nanikiru_check(self,sample):
        for k, v in sample:
            print("手配:{}".format(k), "待ち:{}".format(v))
            current_maisu = self.maisuu_check(k, v)
            for tasu_i in range(1, 10):
                if tasu_i not in v:
                    for herasu_i in range(1, 10):
                        tmp = list(str(k))
                        tmp.append(str(tasu_i))
                        col = collections.Counter(tmp)
                        if str(herasu_i) in tmp:
                            tmp.remove(str(herasu_i))
                            tmp = self.list_to_int(tmp)
                            h = hantei().hanteikun(tmp)
                            if h:
                                maisuu = self.maisuu_check(tmp, h)
                                if current_maisu < maisuu:
                                    print("自摸:{}".format(tasu_i), "切り:{}".format(herasu_i), tmp, h,
                                          "枚数:{}".format(maisuu))


class generate_mondai(hantei):
    def __init__(self, sakuseisuu):
        super(generate_mondai, self).__init__()
        self.sakuseisuu = sakuseisuu
        self.result = {}

    def generate_q(self):
        question = []
        for _ in range(13):
            question.append(str(random.randint(1, 9)))
        c = collections.Counter(question)
        kaisuu = c.most_common()[0][1]
        if kaisuu > 3:
            question = False
        else:
            question = int("".join(sorted(question)))
        return question

    def generate_a(self):
        while len(self.result) < self.sakuseisuu:
            q = self.generate_q()
            if q:
                k = self.hanteikun(q)
                if len(k) > 2:
                    self.result[q] = k
        return self.result

    def generate_swift(self):
        if self.result:
            for key, value in self.result.items():
                tmp = []
                for i in range(1, 10):
                    if i in value:
                        tmp.append(True)
                    else:
                        tmp.append(False)

                # swiftの構文
                # self.list.append(QuestionAnswer(imageList: ["2","2","2","3","4","4","4","5","6","6","7","7","8"], boolList: [false,false,false,false,false,true,true,false,true]))
                print("self.list.append(QuestionAnswer(imageList: {}, boolList: {}))".format(list(str(key)), tmp))
        else:
            print("解答を作ってません")