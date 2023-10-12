import gmpy2,binascii,math
from functools import reduce

def get_nce():  # 获取所有数据
	n,e,c=[],[],[]
	for i in range(21):
		with open('./3-2/Frame' + str(i), 'r') as file0:
			data = file0.readlines()
			N0 = data[0][0:256]
			e0 = data[0][256:512]
			c0 = data[0][512:768]
			n.append(int(N0,16))
			e.append(int(e0,16))
			c.append(int(c0,16))
	return n,e,c

n,e,c=get_nce()

def normal_rsa(p,q,n,e,c):  # 常规rsa解法，即知道了所有参数p,q,n,e,c求d和m
	phi_n = (p - 1) * (q - 1)
	d = gmpy2.invert(e, phi_n)
	m = pow(c,d,n)
	return m

# 欧几里得算法
def gcd(a, b):
	if a==0:
		return b,0,1
	else:
		g,y,x=gcd(b%a,a)
		return (g,x-(b//a)*y,y)

def crt(items):  # 利用中国剩余定理进行低加密指数广播攻击
	N = 1
	for a, n in items:
		N *= n
		result = 0
	for a, n in items:
		m = N//n
		d, r, s = gcd(n, m)
		if d != 1:
			N = N//n
			continue
		result += a*s*m
	return result % N, N


def lowe_attack(c,n,e):  # 单个明文的低加密指数攻击，没成功
	t=1
	while t<20000000000:
		m, b = gmpy2.iroot((c +(t-1) * n), e)
		t=t+1
		if b:
			print(m)
			break

# 公共模数攻击
def same_modnum(n,e,c):
	index1=0
	index2=0
	for i in range(21):
		for j in range(i+1,21):
			if n[i]==n[j]:
				print("Same modulus!",i,j)
				index1=i
				index2=j
				break
	e1,e2=e[index1],e[index2]
	n0=n[index1]
	c1,c2=c[index1],c[index2]
	s = gcd(e1, e2)
	s1 ,s2= s[1],s[2]
	# 求模逆
	if s1<0:
		s1 = - s1
		c1 = gmpy2.invert(c1, n0)
	elif s2<0:
		s2 = - s2
		c2 = gmpy2.invert(c2, n0)
	m = pow(c1,s1,n0)*pow(c2,s2,n0) % n0
	print('m:',m)
	print(binascii.a2b_hex(hex(m)[2:]))
	result = binascii.a2b_hex(hex(m)[2:])
	return result

# 同因数碰撞法
def same_factor(n,e,c):
	plaint=[]
	index=[]
	for i in range(21):
		for j in range(i+1,21):
			if n[i]==n[j]:
				continue
			prime=gmpy2.gcd(n[i],n[j])
			if prime!=1:
				print("same factor:",i,j)
				index.append(i)
				index.append(j)
				p=prime

	q1=n[index[0]]//p
	q18=n[index[1]]//p
	print(p)
	print(q1,q18)
	plaint.append(normal_rsa(p,q1,n[index[0]],e[index[0]],c[index[0]]))
	plaint.append(normal_rsa(p, q18, n[index[1]], e[index[1]], c[index[1]]))
	return binascii.a2b_hex(hex(plaint[0])[2:]),binascii.a2b_hex(hex(plaint[1])[2:])



lowe5=[[],[],[]]
lowe3=[[],[],[]]
for i in range(len(e)):
	if e[i]==5:
		lowe5[0].append(i)
		lowe5[1].append(n[i])
		lowe5[2].append(c[i])
	if e[i]==3:
		lowe3[0].append(i)
		lowe3[1].append(n[i])
		lowe3[2].append(c[i])

def spread_lowe5(n,c):
	sessions=[{"c": c[3],"n": n[3] },
    {"c":c[8] ,"n":n[8] },
    {"c":c[12] ,"n":n[12] },
    {"c":c[16] ,"n":n[16] },
    {"c":c[20] ,"n":n[20] }]
	data = []
	for session in sessions:
		data = data+[(session['c'], session['n'])]
	x, y = crt(data)

	plaintext3_8_12_16_20 = gmpy2.iroot(x,5)
	print(binascii.a2b_hex(hex(plaintext3_8_12_16_20[0])[2:]))

def p_and_q(n):
	B=math.factorial(2**14)
	u=0;v=0;i=0
	u0=gmpy2.iroot(n,2)[0]+1
	while(i<=(B-1)):
		u=(u0+i)*(u0+i)-n
		if gmpy2.is_square(u):
			v=gmpy2.isqrt(u)
			break
		i=i+1
	p=u0+i+v
	return p

def fm(N):  # 费马定理的使用
	p = p_and_q(N)
	print(p)
	return p
# 		10

def Pollard_p1(n):
	B=2**20
	a=2
	for i in range(2,B+1):
		a=pow(a,i,n)
		d=gmpy2.gcd(a-1,n)
		if (d>=2)and(d<=(n-1)):
			q=n//d
			n=q*d
	return d

def pollard(n,c,e):
	index_list = [2,6,19]
	plaintext = []
	for i in range(3):
		N = n[index_list[i]]
		C = c[index_list[i]]
		E = e[index_list[i]]
		p = Pollard_p1(N)
		m=normal_rsa(p,N//p,N,E,C)
		plaintext.append(binascii.a2b_hex(hex(m)[2:]))
	return plaintext

if __name__=='__main__':
	# print(lowe3)
	# print(n[7])
	# 使用Pollard p-1分解法爆破得出Frame2,Frame6,Frame19
	# result=(pollard(n,c,e))
	# for i in result:
	# 	print(i)
	# frame2：That is
	# frame6："Logic
	# frame19：instein.
	# 使用费马定理分解N，可以获得frame10的p
	# p=fm(n[10])
	# print(binascii.a2b_hex(hex(normal_rsa(p,n[10]//p,n[10],e[10],c[10]))[2:]))
	# frame10：will get
	# same_modnum(n,e,c)
	# 利用共模攻击，获得了0和4的结果：My secre
	# spread_lowe5(n,c)
	# 利用低加密指数且明文相同的攻击，获得了3,8,12,16,20的结果：t is a f
	# plaintext1_and_18 = same_factor(n,e,c)
	# print(plaintext1_and_18)
	# 得到了1和18的结果：
	# 1：. Imagin
	# 18：m A to B
# 0,1,2,3,4,6,8,10,12,16,18,19,20已出
# 5,9,13,14,17 未出
# 7,11,15 待定