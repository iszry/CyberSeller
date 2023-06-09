import json
import os.path

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from backendapp.models import Account, Good, ShopCart, Star, Repo
from backendapp.models import Address, Sale, SaleGood, GoodDetail
from django.views.decorators.csrf import csrf_exempt  # 用于忽略scrf攻击
from CyberSellerDjangoBackEnd.settings import IMG_UPLOAD, EXCEL_UPLOAD
from backendapp.UserGoodClass import UserGoodClass
from backendapp.GoodGoodClass import GoodGoodClass
import openpyxl

# 合法身份identity列表
legal_identity = ["admin", "customer", "seller"]

# Create your views here.
def index(request):
	return HttpResponse("Hello!<br/>Welcome to CyberSeller!\n")

test_signup = False
test_json = False

@csrf_exempt
def signup(request):
	# response = HttpResponse()  # 返回HttpResponse对象
	response = {}
	if (request.method == 'POST'):
		if test_signup:
			# return HttpResponse(request.body)
			receive_data = json.loads(request.body)
			ret_name = receive_data['name']
			ret_password = receive_data['password']
			ret_identity = receive_data['identity']
			return HttpResponse("name : " + ret_name + "\npassword:" + ret_password + "\nidentity:" + ret_identity)
		receive_data = json.loads(request.body)  # 解析传入的HttpRequest对象
		if test_json:
			print("ARRIVE HERE")
		name = receive_data['name']  # 注册用户名
		password = receive_data['password']  # 注册密码
		identity = receive_data['identity']  # 注册身份
		if test_json:
			print("name : " + name)
			print("password : " + password)
			print("identity : " + identity)
		if name is None or password is None or identity is None or len(name) == 0 or len(password) == 0:
			response['succeed'] = False
			response['code'] = "010000"  # 空用户名/密码/身份
			response['message'] = "ERROR! Empty name, password or identity, make sure they are legal"
			response['id'] = -1
		if len(name) > 64:
			response['succeed'] = False
			response['code'] = "010002"  # 用户名过长
			response['message'] = "ERROR! Too long name, make sure len <= 64"
			response['id'] = -1
		elif len(password) > 64:
			response['succeed'] = False
			response['code'] = "010003"  # 密码过长
			response['message'] = "ERROR! Too long password, make sure len <= 64"
			response['id'] = -1
		else:
			if identity not in legal_identity:
				response['succeed'] = False
				response['code'] = "010004"  # 非法身份
				response['message'] = "ERROR! Illegal identity, make sure identity is admin, customer or seller"
				response['id'] = -1
			else:
				if test_json:
					print("ARRIVE HERE 2 ")
				accounts = Account.objects.all()  # Account对象列表，每一个元素是一个Account对象
				flag = True  # 标记用户名是否合法（不重名）
				for account in accounts:
					if name == account.name:
						flag = False
						break
				if not flag:
					response['succeed'] = False
					response['code'] = "010005"  # 重名用户名
					response['message'] = "ERROR! This name has been signed up, please choose another name"
					response['id'] = -1
				else:
					if test_json:
						print("ARRIVE HERE 3 ")
					account_new = Account(name=name, password=password, identity=identity, balance=0)  # 生成新的用户行
					account_new.save()  # 保存到数据库
					if test_json:
						print("ARRIVE HERE 4 ")
					account_id = Account.objects.get(name=name).id
					response['succeed'] = True
					response['code'] = "010101"  # 注册成功
					response['message'] = "SUCCESS! Sign up successfully"
					response['id'] = account_id
	else:
		response['succeed'] = False  # 表明请求失败
		response['code'] = "010001"  # 01代表signup方法，00代表错误，01代表错误类型
		response['message'] = "ERROR! This URL accepts POST ONLY!"  # 错误提示信息
		response['id'] = -1  # 用非法id -1 表征当前为错误情况
		# return HttpResponse("ERROR! This URL accepts POST ONLY!")
	# return response
	return JsonResponse({
		'succeed': response['succeed'],
		'code': response['code'],
		'message': response['message'],
		'id': response['id']
	})

try_cross = False
@csrf_exempt
def login(request):
	# response = HttpResponse()
	response = {}
	if request.method == "POST":
		if (try_cross) :
			return JsonResponse({'errno': 0, 'msg': "试验成功!"})
		receive_data = json.loads(request.body)  # 解析传入的HttpRequest对象
		name = receive_data['name']
		password = receive_data['password']
		if name is None or password is None or len(name) == 0 or len(password) == 0:
			response['succeed'] = False
			response['code'] = "020001"
			response['message'] = "ERROR! Empty name or password, make sure they are legal"
			response['id'] = -1
			response['balance'] = -1
			response['identity'] = "FAIL"
		else:
			account = Account.objects.get(name=name)
			if account is None:
				response['succeed'] = False
				response['code'] = "020002"
				response['message'] = "ERROR! Non-exist name, make sure the name is correct"
				response['id'] = -1
				response['balance'] = -1
				response['identity'] = "FAIL"
			else:
				account_id = account.id
				account_identity = account.identity
				if password != account.password:
					response['succeed'] = False
					response['code'] = "020003"
					response['message'] = "ERROR! Wrong password, make sure the password is correct"
					response['id'] = account_id
					response['balance'] = -1
					response['identity'] = account_identity
				else:
					account_balance = account.balance
					response['succeed'] = True
					response['code'] = "020101"
					response['message'] = "SUCCESS! Log in successfully"
					response['id'] = account_id
					response['balance'] = account_balance
					response['identity'] = account_identity
	else:
		response['succeed'] = False
		response['code'] = "020000"
		response['message'] = "ERROR! This URL accepts POST ONLY!"
		response['id'] = -1
		response['balance'] = -1
		response['identity'] = "FAIL"
	return JsonResponse({
		'succeed': response['succeed'],
		'code': response['code'],
		'message': response['message'],
		'id': response['id'],
		'balance': response['balance'],
		'identity': response['identity']
	})
	# return response

testAddGoods = False
DEFAULT_MAKER = 'bank'
DEFAULT_DESCRIPTION = 'This is a nice product'
DEFAULT_DATE = '2022-12-19'
DEFAULT_SHELF_LIFE = '0010-11-12-13'
# 添加商品
@csrf_exempt
def addGoods(request):
	if request.method == 'POST':
		# 获取除了文件之外的数据
		data = request.POST
		# 商品名
		name = data.get('name')
		if name is None:
			return JsonResponse({
				'succeed': False,
				'code': '030000',
				'message': 'ERROR! Need available good name!'
			})
		# 价格
		price = data.get('price')
		if price is None:
			return JsonResponse({
				'succeed': False,
				'code': '030001',
				'message': 'ERROR! Need available good price!'
			})
		# 卖家ID
		seller_id = data.get('seller_id')
		if seller_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '030002',
				'message': 'ERROR! Need available seller id'
			})
		# 制造商名称
		maker = data.get('maker')
		if maker is None:
			maker = DEFAULT_MAKER
		# 商品描述
		description = data.get('description')
		if description is None:
			description = DEFAULT_DESCRIPTION
		# 生产日期
		date = data.get('date')
		if date is None:
			date = DEFAULT_DATE
		# 保质期
		shelf_life = data.get('shelfLife')
		if shelf_life is None:
			shelf_life = DEFAULT_SHELF_LIFE
		# 获取图片文件
		pic_file = request.FILES.get('picture')
		test_non_file = False
		if test_non_file:
			pic_file = data.get('picture')
			print('picfile : ' + str(pic_file) + ' type : ' + str(type(pic_file)))
		print('picfile : ' + str(pic_file) + ' type : ' + str(type(pic_file)))
		if pic_file is None:
			return JsonResponse({
				'succeed': False,
				'code': '030003',
				'message': 'ERROR! Need available pic file'
			})
		# 获取文件全名
		pic_name = pic_file.name
		# 获取文件名
		mobile = os.path.splitext(pic_name)[0]
		# 获取文件后缀
		ext = os.path.splitext(pic_name)[1]
		# 重定义文件名
		pic_name = f'avatar-{mobile}{ext}'
		# 从配置文件中加载图片保存路径
		pic_path = os.path.join(IMG_UPLOAD, pic_name)
		# 保存文件
		print('arrive here')
		with open(pic_path, 'wb') as fp:
			fp.write(pic_file.read())
		# 获取图片URL
		pic_url = 'http://43.143.179.158:8080/img/' + pic_name
		print('price : ' + str(price) + str(type(price)))
		good = Good(name=name, price=price, seller_id=seller_id,
					maker=maker, picture=pic_url, description=description,
					date=date, shelf_life=shelf_life)
		good.save()
		return JsonResponse({
			'succeed': True,
			'code': '030101',
			'message': 'SUCCESS! Add a good successfully!',
			'good_id': good.id
		})

# 添加商品到购物车
@csrf_exempt
def updateShopCart(request):
	if request.method == 'POST':
		data = request.POST
		user_id = data.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '040000',
				'message': 'ERROR! Need available user_id!'
			})
		good_id = data.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '040001',
				'message': 'ERROR! Need available good_id!'
			})
		new_num = data.get('new_num')
		if new_num is None:
			return JsonResponse({
				'succeed': False,
				'code': '040002',
				'message': 'ERROR! Need available new_num!'
			})
		shop_cart_ele = ShopCart.objects.filter(user_id=int(user_id), good_id=int(good_id))
		# print("arrive here")
		# print("shop cart ele type : " + str(type(shop_cart_ele)))
		if shop_cart_ele.count() == 0:
			shop_cart_ele = ShopCart(user_id=user_id, good_id=good_id, num=new_num)
		else:
			shop_cart_ele.num = new_num
			shop_cart_ele = ShopCart.objects.get(user_id=user_id, good_id=good_id)
		shop_cart_ele.save()
		return JsonResponse({
			'succeed': True,
			'code': '040101',
			'message': 'SUCCESS! Update ShopCart successfully!'
		})

# 对给定用户计算推荐商品排序
# 对于加入购物车的商品增加5 * i的权重，其中i是购物车中的数量
# 对于收藏的商品增加3的权重
# 对于其他商品不增加权重


def getMainRecommandGoods(user_id):
	ret_list = []
	goods = Good.objects.all()
	cnt = 0
	# 对于admin账号直接返回所有商品
	if user_id == 1:
		for good in goods:
			good_id = good.id
			like = 0
			num = 0
			ret_list.append(UserGoodClass(id=good_id, name=good.name, price=good.price, seller_id=good.seller_id, maker=good.maker, picture=good.picture, description=good.description, date=good.date, shelf_life=good.shelf_life, like=like, num=num))
		return ret_list
	for good in goods:
		good_id = good.id
		like = 0
		stars = Star.objects.filter(user_id=user_id, good_id=good_id)
		if stars.count() != 0:
			star = Star.objects.get(user_id=user_id, good_id=good_id)
			like = star.like
		num = 0
		shopCarts = ShopCart.objects.filter(user_id=user_id, good_id=good_id)
		if shopCarts.count() != 0:
			shopCart = ShopCart.objects.get(user_id=user_id, good_id=good_id)
			num = shopCart.num
		goodObj = UserGoodClass(id=good_id, name=good.name, price=good.price, seller_id=good.seller_id, maker=good.maker, picture=good.picture, description=good.description, date=good.date, shelf_life=good.shelf_life, like=like, num=num)
		ret_list.append(goodObj)
	ret_list.sort()
	return ret_list
	# return goods

# 获取对用户的个性推荐
@csrf_exempt
def mainRecommendGoods(request):
	if request.method == 'POST':
		# 获取用户名
		id = request.POST.get('user_id')
		# print("arrive here 1")
		if id is None:
			return JsonResponse({
				'succeed': False,
				'code': '050000',
				'message': 'ERROR! Need non-null userid!'
			})
		user = Account.objects.get(id=id)
		# print("arrive here 2")
		if user is None:
			return JsonResponse({
				'succeed': False,
				'code': '050001',
				'message': 'ERROR! Need available userid!'
			})
		# goods = Good.objects.all()
		goods = getMainRecommandGoods(id)
		# n = goods.count()
		n = len(goods)
		ret_json = {'succeed': True,
					'code': '050101',
					'message': 'SUCCESS! Get goods recommended successfully!',
					'n': n}
		goods_json = []
		for good in goods:
			# like = 0
			# stars = Star.objects.filter(user_id=id, good_id=good.id)
			# if stars.count() == 1:
				# star = Star.objects.get(user_id=id, good_id=good.id)
				# like = star.like
			good_json = {
				'id': good.id,
				'name': good.name,
				'price': good.price,
				'seller_id': good.seller_id,
				'seller_name': Account.objects.get(id=good.seller_id).name,
				'maker': good.maker,
				'picture': good.picture,
				'description': good.description,
				'date': good.date,
				'shelf_life': good.shelf_life,
				'like': good.like
			}
			goods_json.append(good_json)
		ret_json['goods'] = goods_json
		return JsonResponse(ret_json)

@csrf_exempt
def getGood(request):
	if request.method == 'POST':
		good_id = request.POST.get('good_id')
		good = Good.objects.get(id=good_id)
		repo = 0
		repos = Repo.objects.filter(good_id=good_id)
		if repos.count() != 0:
			repo = Repo.objects.get(good_id=good_id).repo
		return JsonResponse({
			'id': good.id,
			'name': good.name,
			'price': good.price,
			'seller_id': good.seller_id,
			'maker': good.maker,
			'picture': good.picture,
			'description': good.description,
			'date': good.date,
			'shelf_life': good.shelf_life,
			'repo': repo
		})

@csrf_exempt
def searchShopCart(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		user = Account.objects.get(id=user_id)
		goods = ShopCart.objects.filter(user_id=user_id)
		n = goods.count()
		goods_list = []
		for good_index in goods:
			good_id = good_index.good_id
			good = Good.objects.get(id=good_id)
			repo = 0
			repos = Repo.objects.filter(good_id=good_id)
			if repos.count() != 0:
				repo = Repo.objects.get(good_id=good_id).repo
			goods_list.append({
				'id': good.id,
				'name': good.name,
				'price': good.price,
				'seller_id': good.seller_id,
				'maker': good.maker,
				'picture': good.picture,
				'description': good.description,
				'date': good.date,
				'shelf_life': good.shelf_life,
				'num': good_index.num,
				'repo': repo
			})
		return JsonResponse({
			'n': n,
			'goods': goods_list
		})

@csrf_exempt
def updateStar(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		good_id = request.POST.get('good_id')
		like = request.POST.get('like')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '080000',
				'message': 'ERROR! Need available user_id!'
			})
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '080001',
				'message': 'ERROR! Need available good_id!'
			})
		if like is None:
			return JsonResponse({
				'succeed': False,
				'code': '080002',
				'message': 'ERROR! Need available like!'
			})
	stars = Star.objects.filter(user_id=user_id, good_id=good_id)
	if stars.count() == 0:
		star = Star(user_id=user_id, good_id=good_id)
		star.like = like
		star.save()
	else:
		star = Star.objects.get(user_id=user_id, good_id=good_id)
		star.like = like
		star.save()
	return JsonResponse({
		'succeed': True,
		'code': '080101',
		'message': 'SUCCESS! Star a good successfully!'
	})

@csrf_exempt
def getSixPictures(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '090000',
				'message': 'ERROR! Need available user_id!'
			})
		print('user_id : ' + str(user_id))
		goods = getMainRecommandGoods(user_id)
		n = 6
		pictures = []
		cnt = 0
		for good in goods:
			pictures.append(good.picture)
			cnt += 1
			if cnt >= 6:
				break
		return JsonResponse({
			'succeed': True,
			'code': '090101',
			'message': 'SUCCESS! Got 6 head pictures',
			'n': n,
			'pictures': pictures
		})

@csrf_exempt
def updateRepo(request):
	if request.method == 'POST':
		good_id = request.POST.get('good_id')
		repo = request.POST.get('repo')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '100000',
				'message': 'ERROR! Need available good_id!'
			})
		if repo is None:
			return JsonResponse({
				'succeed': False,
				'code': '100001',
				'message': 'ERROR! Need available repo!'
			})
		repos = Repo.objects.filter(good_id=good_id)
		if repos.count() == 0:
			new_repo_ele = Repo(good_id=good_id, repo=repo)
			new_repo_ele.save()
		else:
			repo_ele = Repo.objects.get(good_id=good_id)
			repo_ele.repo = repo
			repo_ele.save()
		return JsonResponse({
			'succeed': True,
			'code': '100101',
			'message': 'SUCCESS! Update a good\'s repo successfully!'
		})

@csrf_exempt
def getSellGoods(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '110000',
				'message': 'ERROR! Need available user_id!'
			})
		goods = Good.objects.filter(seller_id=user_id)
		n = goods.count()
		goods_list = []
		for good in goods:
			good_id = good.id
			repos = Repo.objects.filter(good_id=good_id)
			repo_num = 0
			if repos.count() == 0:
				repo = Repo(good_id=good_id, repo=0)
				repo.save()
			else:
				repo_num = Repo.objects.get(good_id=good_id).repo
			goods_list.append({
				'id': good.id,
				'name': good.name,
				'price': good.price,
				'seller_id': good.seller_id,
				'maker': good.maker,
				'picture': good.picture,
				'description': good.description,
				'date': good.date,
				'shelf_life': good.shelf_life,
				'repo': repo_num
			})
		return JsonResponse({
			'n': n,
			'goods': goods_list
		})

@csrf_exempt
def goodsRecommendGoods(request):
	if request.method == 'POST':
		good_id = request.POST.get('good_id')
		# print('good_id : ' + str(good_id))
		good = Good.objects.get(id=good_id)
		seller_id = good.seller_id
		price = good.price
		ret_list = []
		goods = Good.objects.all()
		n = goods.count()
		# print('arrive here 1')
		for good_index in goods:
			good_index_id = good_index.id
			value = 0
			if good_index_id == good_id:
				value += 1
			if seller_id == good_index.seller_id:
				value += 1
			if (price - good_index.price) / price < 0.25:
				value += 1
			good_obj = GoodGoodClass(id=good_index_id, name=good_index.name, price=good_index.price, seller_id=good_index.seller_id,
									maker=good_index.maker, picture=good_index.picture, description=good_index.description,
									date=good_index.date, shelf_life=good_index.shelf_life, value=value)
			ret_list.append(good_obj)
		# print('arrive here 2')
		ret_list.sort()
		goods_json = []
		for good in ret_list:
			good_json = {
				'id': good.id,
				'name': good.name,
				'price': good.price,
				'seller_id': good.seller_id,
				'seller_name': Account.objects.get(id=good.seller_id).name,
				'maker': good.maker,
				'picture': good.picture,
				'description': good.description,
				'date': good.date,
				'shelf_life': good.shelf_life,
			}
			goods_json.append(good_json)
		# print('arrive here 3')
		return JsonResponse({
			'n': n,
			'goods': goods_json
		})

@csrf_exempt
def getStarGoods(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		stars = Star.objects.filter(user_id=user_id)
		n = stars.count()
		goods_json = []
		for star in stars:
			good_id = star.good_id
			good = Good.objects.get(id=good_id)
			repos = Repo.objects.filter(id=good_id)
			repo = 0
			if repos.count() != 0:
				repo = Repo.objects.get(id=good_id).repo
			good_json = {
				'id': good.id,
				'name': good.name,
				'price': good.price,
				'seller_id': good.seller_id,
				'seller_name': Account.objects.get(id=good.seller_id).name,
				'maker': good.maker,
				'picture': good.picture,
				'description': good.description,
				'date': good.date,
				'shelf_life': good.shelf_life,
				'repo': repo,
			}
			goods_json.append(good_json)
		return JsonResponse({
			'n': n,
			'goods': goods_json
		})

@csrf_exempt
def deleteGood(request):
	if request.method == 'POST':
		good_id = request.POST.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '140000',
				'message': 'ERROR! Need available good_id!'
			})
		Good.objects.filter(id=good_id).delete()
		ShopCart.objects.filter(good_id=good_id).delete()
		Star.objects.filter(good_id=good_id).delete()
		Repo.objects.filter(good_id=good_id).delete()
		return JsonResponse({
			'succeed': True,
			'code': '140101',
			'message': 'SUCCESS! Delete a good successfully!'
		})

@csrf_exempt
def analyseExcel(request):
	if request.method == 'POST':
		excel_file = request.FILES.get('excel')
		if excel_file is None:
			return JsonResponse({
				'succeed': False,
				'code': '150000',
				'message': 'ERROR! Need available excel file'
			})
		good_id = request.POST.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '150001',
				'message': 'ERROR! Need available good_id!'
			})
		# 获取文件全名
		excel_name = excel_file.name
		# 获取文件名
		mobile = os.path.splitext(excel_name)[0]
		# 获取文件后缀
		ext = os.path.splitext(excel_name)[1]
		# 重定义文件名
		excel_name = f'avatar-{mobile}{ext}'
		# 从配置文件中加载excel保存路径
		excel_path = os.path.join(EXCEL_UPLOAD, excel_name)
		# 保存文件
		with open(excel_path, 'wb') as fp:
			fp.write(excel_file.read())
		# 解析文件
		os.chdir(EXCEL_UPLOAD)
		workbook = openpyxl.load_workbook(excel_name)
		sheet = workbook['Sheet1']
		ret_json = []
		n = 0
		for i in sheet.iter_rows():
			key = 'None'
			value = 'None'
			for j in i:
				print('i = ' + str(i) + ' j = ' + str(j) + ' value = ' + str(j.value))
				if key == 'None':
					key = str(j.value)
				else:
					value = str(j.value)
			ret_json.append({key: value})
			n += 1
			good_detail = GoodDetail(good_id=good_id, key=key, value=value)
			good_detail.save()
		return JsonResponse({
			'n': n,
			'jsons': ret_json
		})

@csrf_exempt
def analyseShopCart(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '160000',
				'message': 'ERROR! Need available user_id!'
			})
		shop_carts = ShopCart.objects.filter(user_id=user_id)
		ret_list = []
		#print("arrive here 1")
		for shop_cart in shop_carts:
			#print("arrive here 2")
			good_id = shop_cart.good_id
			num = shop_cart.num
			seller_id = Good.objects.get(id=good_id).seller_id
			price = Good.objects.get(id=good_id).price * num
			#print("arrive here 3")
			flag = False

			for ele in ret_list:
				if ele['seller_id'] == seller_id:
					flag = True
					ele['price'] = ele['price'] + price
					ele['num'] = ele['num'] + num
					break

			#print("arrive here 4")
			if not flag:
				ele = {}
				ele['seller_id'] = seller_id
				ele['seller_name'] = Account.objects.get(id=seller_id).name
				ele['price'] = price
				ele['num'] = num
				ret_list.append(ele)
		#print("arrive here 5")
		return JsonResponse({
			'tuples': ret_list
		})

DEFAULT_COMMENT = ''
@csrf_exempt
def addAddress(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '170000',
				'message': 'ERROR! Need available user_id!'
			})
		receiver_name = request.POST.get('receiver_name')
		if receiver_name is None:
			return JsonResponse({
				'succeed': False,
				'code': '170001',
				'message': 'ERROR! Need available receiver_name!'
			})
		phone = request.POST.get('phone')
		if phone is None:
			return JsonResponse({
				'succeed': False,
				'code': '170002',
				'message': 'ERROR! Need available phone!'
			})
		addr = request.POST.get('addr')
		if addr is None:
			return JsonResponse({
				'succeed': False,
				'code': '170003',
				'message': 'ERROR! Need available addr!'
			})
		detailed_addr = request.POST.get('detailed_addr')
		if detailed_addr is None:
			return JsonResponse({
				'succeed': False,
				'code': '170004',
				'message': 'ERROR! Need available detailed_addr!'
			})
		comment = request.POST.get('comment')
		if comment is None:
			comment = DEFAULT_COMMENT
		default = request.POST.get('default')
		if default is None:
			return JsonResponse({
				'succeed': False,
				'code': '170005',
				'message': 'ERROR! Need available default!'
			})
		address = Address(user_id=user_id, receiver_name=receiver_name, phone=phone, addr=addr, detailed_addr=detailed_addr, comment=comment, default=default)
		address.save()
		return JsonResponse({
			'succeed': True,
			'code': '170101',
			'message': 'SUCCESS! Add an address successfully!'
		})

@csrf_exempt
def addSale(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '180000',
				'message': 'ERROR! Need available user_id!'
			})
		price = request.POST.get('price')
		if price is None:
			return JsonResponse({
				'succeed': False,
				'code': '180001',
				'message': 'ERROR! Need available price!'
			})
		address_id = request.POST.get('address_id')
		if address_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '180002',
				'message': 'ERROR! Need available address_id!'
			})
		'''
		goods = request.POST.get('goods')
		if goods is None:
			return JsonResponse({
				'succeed': False,
				'code': '180003',
				'message': 'ERROR! Need available goods!'
			})
		'''
		sale = Sale(user_id=user_id, address_id=address_id, price=price)
		sale.save()
		sale_id = sale.id
		'''
		for good in goods:
			good_id = good['good_id']
			num = good['num']
			sale_good = SaleGood(sale_id=sale_id, good_id=good_id, num=num)
			sale_good.save()
		'''
		return JsonResponse({
			'succeed': True,
			'code': '180101',
			'message': 'SUCCESS! Add a sale successfully!',
			'sale_id': sale_id
		})

@csrf_exempt
def addSaleGood(request):
	if request.method == 'POST':
		sale_id = request.POST.get('sale_id')
		if sale_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '190000',
				'message': 'ERROR! Need available sale_id!'
			})
		good_id = request.POST.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '190001',
				'message': 'ERROR! Need available good_id!'
			})
		num = request.POST.get('num')
		if num is None:
			return JsonResponse({
				'succeed': False,
				'code': '190002',
				'message': 'ERROR! Need available num!'
			})
		sale_good = SaleGood(sale_id=sale_id, good_id=good_id, num=num)
		sale_good.save()
		return JsonResponse({
			'succeed': True,
			'code': '190101',
			'message': 'SUCCESS! Add a sale_good successfully!'
		})

@csrf_exempt
def analyseSale(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '200000',
				'message': 'ERROR! Need available user_id!'
			})
		sales = Sale.objects.filter(user_id=user_id)
		ret_list = []
		print('arrive here 1')
		for sale in sales:
			date = str(sale.date.strftime("%Y-%m-%d"))
			price = sale.price
			flag = False
			print('arrive here 2')
			for ele in ret_list:
				if ele['date'] == date:
					ele['price'] = ele['price'] + price
					flag = True
					break
			print('arrive here 3')
			if not flag:
				ele = {}
				ele['date'] = date
				ele['price'] = price
				ret_list.append(ele)
		print('arrive here 4')
		return JsonResponse({
			'tuples': ret_list
		})

@csrf_exempt
def getGoodDetail(request):
	if request.method == 'POST':
		good_id = request.POST.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '210000',
				'message': 'ERROR! Need available good_id!'
			})
		good_details = GoodDetail.objects.filter(good_id=good_id)
		ret_list = []
		for good_detail in good_details:
			key = good_detail.key
			value = good_detail.value
			ret_list.append({
				'key': key,
				'value': value
			})
		return JsonResponse({
			'tuples': ret_list
		})

@csrf_exempt
def getAddress(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '220000',
				'message': 'ERROR! Need available user_id!'
			})
		addresses = Address.objects.filter(user_id=user_id)
		ret_list = []
		for address in addresses:
			ele = {
				'user_id': address.user_id,
				'address_id': address.id,
				'receiver_name': address.receiver_name,
				'phone': address.phone,
				'addr': address.addr,
				'detailed_addr': address.detailed_addr,
				'comment': address.comment,
				'default': address.default
			}
			ret_list.append(ele)
		return JsonResponse({
			'addresses': ret_list
		})

@csrf_exempt
def deleteAddress(request):
	if request.method == 'POST':
		address_id = request.POST.get('address_id')
		if address_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '230000',
				'message': 'ERROR! Need available address_id!'
			})
		address = Address.objects.get(id=address_id)
		address.delete()
		return JsonResponse({
			'succeed': True,
			'code': '230101',
			'message': 'SUCCESS! Delete an address successfully!'
		})

@csrf_exempt
def updateDefaultAddress(request):
	if request.method == 'POST':
		address_id = request.POST.get('address_id')
		if address_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '240000',
				'message': 'ERROR! Need available address_id!'
			})
		default = request.POST.get('default')
		if default is None:
			return JsonResponse({
				'succeed': False,
				'code': '240001',
				'message': 'ERROR! Need available default!'
			})
		user_id = Address.objects.get(id=address_id).user_id
		print('default : ' + str(default) + ' type : ' + str(type(default)))
		if default == '1':
			print('arrive here')
			addresses = Address.objects.filter(user_id=user_id, default=1).update(default=0)
			'''
			for address in addresses:
				new_address_id = address.id
				new_address = Address.objects.get(new_address_id)
				new_address.default = 0
				new_address.save()
			'''
			'''
			for address in addresses:
				if address.default == 1:
					address.default = 0
					address.save()
			'''
		address = Address.objects.get(id=address_id)
		address.default = default
		address.save()

	return JsonResponse({
		'succeed': True,
		'code': '240101',
		'message': 'SUCCESS! Update address default successfully!'
	})

@csrf_exempt
def analyseLike(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '250000',
				'message': 'ERROR! Need available user_id!'
			})
		stars = Star.objects.filter(user_id=user_id)
		ret_list = []
		#print("arrive here 1")
		for star in stars:
			#print("arrive here 2")
			good_id = star.good_id
			num = 1
			seller_id = Good.objects.get(id=good_id).seller_id
			price = Good.objects.get(id=good_id).price * num
			#print("arrive here 3")
			flag = False

			for ele in ret_list:
				if ele['seller_id'] == seller_id:
					flag = True
					ele['price'] = ele['price'] + price
					ele['num'] = ele['num'] + num
					break

			#print("arrive here 4")
			if not flag:
				ele = {}
				ele['seller_id'] = seller_id
				ele['seller_name'] = Account.objects.get(id=seller_id).name
				ele['price'] = price
				ele['num'] = num
				ret_list.append(ele)
		#print("arrive here 5")
		return JsonResponse({
			'tuples': ret_list
		})

@csrf_exempt
def updateShopCartNum(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '250000',
				'message': 'ERROR! Need an available user_id!'
			})
		good_id = request.POST.get('good_id')
		if good_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '250001',
				'message': 'ERROR! Need an available good_id!'
			})
		new_num = request.POST.get('new_num')
		if new_num is None:
			return JsonResponse({
				'succeed': False,
				'code': '250002',
				'message': 'ERROR! Need an available new_num!'
			})
		shop_carts = ShopCart.objects.filter(user_id=user_id, good_id=good_id)
		if shop_carts.count() == 0:
			return JsonResponse({
				'succeed': False,
				'code': '250003',
				'message': 'ERROR! No such good in this user\'s shop cart!'
			})
		elif shop_carts.count() != 1:
			return JsonResponse({
				'succeed': False,
				'code': '250004',
				'message': 'ERROR! Unknown error, please contact YJK!'
			})
		else:
			shop_cart = ShopCart.objects.get(user_id=user_id, good_id=good_id)
			shop_cart.num = new_num
			shop_cart.save()
			return JsonResponse({
				'succeed': True,
				'code': '250101',
				'message': 'SUCCESS! Update ShopCart num successfully!'
			})

@csrf_exempt
def analyseOrder(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '270000',
				'message': 'ERROR! Need available user_id!'
			})
		sales = Sale.objects.filter(user_id=user_id)
		ret_list = []
		print("arrive here 1")
		for sale in sales:
			print("arrive here 2")
			sale_id = sale.id
			goods = SaleGood.objects.filter(sale_id=sale_id)
			for good in goods:
				good_id = good.good_id
				num = good.num
				seller_id = Good.objects.get(id=good_id).seller_id
				price = Good.objects.get(id=good_id).price * num
				print("arrive here 3")
				flag = False

				for ele in ret_list:
					if ele['seller_id'] == seller_id:
						flag = True
						ele['price'] = ele['price'] + price
						ele['num'] = ele['num'] + num
						break

				print("arrive here 4")
				if not flag:
					ele = {}
					ele['seller_id'] = seller_id
					ele['seller_name'] = Account.objects.get(id=seller_id).name
					ele['price'] = price
					ele['num'] = num
					ret_list.append(ele)
		print("arrive here 5")
		return JsonResponse({
			'tuples': ret_list
		})

@csrf_exempt
def checked(request):
	return JsonResponse({
		'checked': False
	})

@csrf_exempt
def getSale(request):
	if request.method == 'POST':
		user_id = request.POST.get('user_id')
		if user_id is None:
			return JsonResponse({
				'succeed': False,
				'code': '290000',
				'message': 'ERROR! Need an available user_id!'
			})
		sales = Sale.objects.filter(user_id=user_id)
		ret_list = []
		for sale in sales:
			ret_ele = []
			sale_id = sale.id
			sale_goods = SaleGood.objects.filter(sale_id=sale_id)
			for sale_good in sale_goods:
				good_id = sale_good.good_id
				num = sale_good.num
				good = Good.objects.get(id=good_id)
				ret_ele.append({
					'id': good_id,
					'name': good.name,
					'price': good.price,
					'seller_id': good.seller_id,
					'maker': good.maker,
					'picture': good.picture,
					'description': good.description,
					'date': good.date,
					'shelf_life': good.shelf_life,
					'num': num
				})
			ret_list.append(ret_ele)
		ret_list.reverse()
		return JsonResponse({
			'sales': ret_list
		})


