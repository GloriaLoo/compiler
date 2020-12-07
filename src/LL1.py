# LL1文法
# https://www.cnblogs.com/standby/p/6792814.html
from src.GrammarAnalyzer import GrammarAnalyzer

g = GrammarAnalyzer(['E->TM', 'M->+TM', 'M->ε', 'T->FN', 'N->*FN', 'N->ε', 'F->(E)', 'F->i'])
print(g.getFirst())
print(g.getFollow())
