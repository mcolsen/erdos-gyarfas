"""Regression for assertion-only exports after a model has been requested."""
from z3tiny import Solver
s=Solver();x=[s.var('x'+str(i))for i in range(3)];s.exactly(x);s.clause(x[:2])
assert s.check()==1 and sum(s.val(v)for v in x)==1
text=s.dump();assert '(model-'not in text
r=Solver();y=[r.var('x'+str(i))for i in range(3)];r.load(text)
assert r.check()==1 and sum(r.val(v)for v in y)==1
r.clause([-y[0]]);r.clause([-y[1]]);assert r.check()==-1
s.close();r.close();print('Native Z3 model evaluation and assertion-only export/reload verified.')
