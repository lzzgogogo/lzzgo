# Aozora文庫のテキストファイルを読み取るライブラリ
# 山内長承, "Pythonによるテキストマイニング入門," オーム社, 2017.によるプログラム
# 学習以外で用いるとき、注意が必要　著作権は山内長承さんのもの
import re
import os

# class Aozoraをimportしたいファイルと同じディレクトリ内に置く
class Aozora:
    decoration = re.compile(r"(［[^［］]*］)|(《[^《》]*》)|[｜\n]")
    def __init__(self, filename):
        self.filename = filename
        # 青空文庫はShift-JISなので
        with open(filename, "r", encoding="shift-jis") as afile:
            self.whole_str = afile.read()
        paragraphs = self.whole_str.splitlines()
        # 最後の3行の空白行以降のコメント行を除く
        c = 0
        position = 0
        for (i, u) in enumerate(reversed(paragraphs)):
            if len(u) != 0:
                c = 0
            else:
                c += 1
                if c >= 3:
                    position = i
                    break
        if position != 0:
            paragraphs = paragraphs[:-(position+1)]
 
        # 先頭の----行で囲まれたコメント領域の行を除く
        newparagraphs = []
        addswitch = True
        for u in paragraphs:
            if u[:2] != '--':
                if addswitch:
                    newparagraphs.append(u)
            else:
                addswitch = not addswitch
 
        self.cleanedparagraphs = []
        for u in newparagraphs:
            v = re.sub(self.decoration, '', u)
            self.cleanedparagraphs.append(v)
 
    def read(self):
        return self.cleanedparagraphs


# MeCabの分かち書きの関数化
#
import MeCab
import urllib.request

def parsewithelimination(sentense):
  # 有名な日本語ストップワードリスト
  # SlothLib(http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt)のストップワードリストを使う

  slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
  slothlib_file = urllib.request.urlopen(slothlib_path)
  stopwords=[]
  for line in slothlib_file:
    ss=line.decode("utf-8").strip()
    if not ss==u'':
      stopwords.append(ss)

  elim=['数','非自立','接尾']
  part=['名詞', '動詞', '形容詞']

  m=MeCab.Tagger()
  m.parse('')
  node=m.parseToNode(sentense)
    
  result=''
  while node:
    if node.feature.split(',')[6] == '*': # 原形を取り出す
      term=node.surface
    else :
      term=node.feature.split(',')[6]
        
    if term in stopwords:
      node=node.next
      continue
    
    if node.feature.split(',')[1] in elim:
      node=node.next
      continue

    if node.feature.split(',')[0] in part:
      if result == '':
        result = term
      else:
        result=result.strip() + ' '+ term
        
    node=node.next

  return result


# コサイン類似度を求める関数
#
import numpy as np

def comp_sim(qvec,tvec):
    return np.dot(qvec, tvec) / (np.linalg.norm(qvec) * np.linalg.norm(tvec))