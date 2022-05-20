import time
# https://wave1994.tistory.com/47

def time_checker(func):
  def inner_func(*args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    work = end_time - start_time
    print(f"{func.__name__} work : {work}s")
  return inner_func

A="aaa난모르겠어요"
B="bbbr길어지면뭐가달라지나요"

@time_checker
def joiner(a,b):
	c=[]
	c.append(a)
	c.append(b)
	print(''.join(c))
	time.sleep(1)
@time_checker
def plus_operation(a,b):
	c= a+b
	print(c)
	time.sleep(1)
	
@time_checker
def operation(a,b):
	print("%s%s"%(a,b))
	time.sleep(1)

@time_checker
def fstring(a,b):
	print(f"{a}{b}")
	time.sleep(1)

@time_checker
def format_string(a,b):
	print("{}{}".format(a,b))
	time.sleep(1)

joiner(A,B)
plus_operation(A,B)
operation(A,B)
fstring(A,B)
format_string(A,B)
