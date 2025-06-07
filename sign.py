import sys

"""符計算に必要な情報取得 """
#親か子を確認
print("親（y）子（n）入力してください")
oya = input()
if oya =="y":
    print("親です")
elif oya =="n":
    print("子です")
else:
    print("yかnを入力してください")
    sys.exit()
#例外の確認(平和か七対子)
print("七対子か平和です（y）違います（n）入力してください")
reigai = input()
if reigai =="y":
    print("七対子（y）平和（n）入力してください")
    reigai1 =input()
    if reigai1 =="y":
        print("七対子です")
    elif reigai1 =="n":
        print("平和です")
    else:
        print("yかnを入力してください")
        sys.exit()
elif reigai =="n":
    print("七対子・平和以外です")
else:
    print("yかnを入力してください")
    sys.exit()