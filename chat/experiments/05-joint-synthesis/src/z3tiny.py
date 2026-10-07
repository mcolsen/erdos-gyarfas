"""Small ctypes adapter for an installed Z3 C library (no Python binding needed)."""
import ctypes as C
import ctypes.util
P=C.c_void_p; I=C.c_int; U=C.c_uint; B=C.c_bool; S=C.c_char_p
lib=C.CDLL(C.util.find_library('z3') or 'libz3.so.4')
def fn(name,restype,*args):
 f=getattr(lib,'Z3_'+name);f.restype=restype;f.argtypes=list(args);return f
mk_config=fn('mk_config',P);del_config=fn('del_config',None,P)
set_param=fn('set_param_value',None,P,S,S);mk_context=fn('mk_context',P,P);del_context=fn('del_context',None,P)
mk_symbol=fn('mk_string_symbol',P,P,S);mk_bool=fn('mk_bool_sort',P,P);mk_const=fn('mk_const',P,P,P,P)
mk_or=fn('mk_or',P,P,U,C.POINTER(P));mk_not=fn('mk_not',P,P,P)
mk_pbeq=fn('mk_pbeq',P,P,U,C.POINTER(P),C.POINTER(I),I)
mk_solver=fn('mk_solver',P,P);solver_ref=fn('solver_inc_ref',None,P,P);solver_unref=fn('solver_dec_ref',None,P,P)
solver_assert=fn('solver_assert',None,P,P,P);solver_check=fn('solver_check',I,P,P)
get_model=fn('solver_get_model',P,P,P);model_ref=fn('model_inc_ref',None,P,P);model_unref=fn('model_dec_ref',None,P,P)
model_eval=fn('model_eval',B,P,P,P,B,C.POINTER(P));get_bool=fn('get_bool_value',I,P,P)
reason=fn('solver_get_reason_unknown',S,P,P);solver_str=fn('solver_to_string',S,P,P)
mk_params=fn('mk_params',P,P);params_ref=fn('params_inc_ref',None,P,P);params_unref=fn('params_dec_ref',None,P,P)
params_uint=fn('params_set_uint',None,P,P,P,U);solver_params=fn('solver_set_params',None,P,P,P)
class Solver:
 def __init__(self,seed=0,timeout_ms=2000):
  q=mk_config();set_param(q,b'model',b'true');self.c=mk_context(q);del_config(q)
  self.s=mk_solver(self.c);solver_ref(self.c,self.s);self.sort=mk_bool(self.c);self.v=[None];self.nv=[None];self.model=None
  p=mk_params(self.c);params_ref(self.c,p)
  for k,v in [('timeout',timeout_ms),('random_seed',seed)]:params_uint(self.c,p,mk_symbol(self.c,k.encode()),v)
  solver_params(self.c,self.s,p);params_unref(self.c,p)
 def var(self,name):
  a=mk_const(self.c,mk_symbol(self.c,name.encode()),self.sort);self.v.append(a);self.nv.append(mk_not(self.c,a));return len(self.v)-1
 def clause(self,lits):
  a=[self.v[x] if x>0 else self.nv[-x] for x in lits]
  solver_assert(self.c,self.s,mk_or(self.c,len(a),(P*len(a))(*a)))
 def exactly(self,xs,k=1):
  a=(P*len(xs))(*(self.v[x] for x in xs));b=(I*len(xs))(*([1]*len(xs)))
  solver_assert(self.c,self.s,mk_pbeq(self.c,len(xs),a,b,k))
 def check(self):
  if self.model:model_unref(self.c,self.model);self.model=None
  r=solver_check(self.c,self.s)
  if r==1:self.model=get_model(self.c,self.s);model_ref(self.c,self.model)
  return r
 def val(self,v):
  out=P();assert model_eval(self.c,self.model,self.v[v],True,C.byref(out));return get_bool(self.c,out)==1
 def dump(self):return solver_str(self.c,self.s).decode()
 def close(self):
  if self.model:model_unref(self.c,self.model);self.model=None
  solver_unref(self.c,self.s);del_context(self.c)
if __name__=='__main__':
 s=Solver();x=[s.var(str(i)) for i in range(3)];s.exactly(x);s.clause(x[:2]);assert s.check()==1;assert sum(s.val(v) for v in x)==1
 s.clause([-x[0]]);s.clause([-x[1]]);assert s.check()==-1;s.close();print('Z3 wrapper regression passed')
mk_and=fn('mk_and',P,P,U,C.POINTER(P));mk_true=fn('mk_true',P,P);mk_false=fn('mk_false',P,P)
def _or(self,asts):return mk_or(self.c,len(asts),(P*len(asts))(*asts))
def _and(self,asts):return mk_and(self.c,len(asts),(P*len(asts))(*asts))
def _assert_ast(self,a):solver_assert(self.c,self.s,a)
Solver.OR=_or;Solver.AND=_and;Solver.assert_ast=_assert_ast
Solver.TRUE=lambda self:mk_true(self.c)
Solver.FALSE=lambda self:mk_false(self.c)
solver_from_string=fn('solver_from_string',None,P,P,S)
Solver.load=lambda self,text:solver_from_string(self.c,self.s,text.encode())
get_assertions=fn('solver_get_assertions',P,P,P)
vec_size=fn('ast_vector_size',U,P,P);vec_get=fn('ast_vector_get',P,P,P,U)
vec_ref=fn('ast_vector_inc_ref',None,P,P);vec_unref=fn('ast_vector_dec_ref',None,P,P)
ast_str=fn('ast_to_string',S,P,P)
def clean_dump(self):
 """Export original assertions, NOT solver_to_string's model-converter state."""
 vec=get_assertions(self.c,self.s);vec_ref(self.c,vec)
 out=['(set-logic ALL)']
 out += ['(declare-fun '+ast_str(self.c,v).decode()+' () Bool)'for v in self.v[1:]]
 out += ['(assert '+ast_str(self.c,vec_get(self.c,vec,i)).decode()+')'for i in range(vec_size(self.c,vec))]
 vec_unref(self.c,vec);return '\n'.join(out)+'\n'
Solver.dump=clean_dump
