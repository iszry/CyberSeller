# API

> 多数时候，前端开发人员**只需**阅览本API文档即可获取所有必要信息，无需查阅数据库README

## Django欢迎页

`http://43.143.179.158:8080/`

## 用户注册与登录

### [01] signup用户注册

#### 发送

- 使用`POST`方法向服务器提供注册数据申请，数据格式为`raw`+`json`

- URL:`http://43.143.179.158:8080/signup`

- 具体属性如下：

| 属性     | 说明   | 类型                                              |
  | -------- | ------ | ------------------------------------------------- |
  | name     | 用户名 | 字符串，非空，长度小于`64`                        |
  | password | 密码   | 字符串，非空，长度小于`64`                        |
  | identity | 身份   | 字符串，非空，为`admin, customer, seller`三种之一 |

#### 接收

返回一个`HttpResponse`对象，属性列表如下：

| 属性    | 说明               | 类型                                                         |
| ------- | ------------------ | ------------------------------------------------------------ |
| succeed | 请求是否被成功执行 | 布尔值                                                       |
| code    | 处理结果代码       | 六位字符串，标识不同正确/错误情况，前两位固定为`01`表示是`signup`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息           | 提供更多关于本次请求处理结果的信息                           |
| id      | 注册得到的用户id   | 只有成功注册时返回一个正数，注册失败返回-1                   |

- 正确情况

| succeed | code     | message                         | id                   |
| ------- | -------- | ------------------------------- | -------------------- |
| `True`  | `010101` | `SUCCESS! Sign up successfully` | <数据库自动赋予的id> |

- 错误情况：

| succeed | code     | message                                                      | id   | 说明                                       | 处理方案                       |
| ------- | -------- | ------------------------------------------------------------ | ---- | ------------------------------------------ | ------------------------------ |
| `False` | `010000` | `ERROR! Empty name, password or identity, make sure they are legal` | `-1` | `name,password,identity`中有空值或空字符串 | 不执行请求，对数据库不产生影响 |
| `False` | `010001` | `ERROR! This URL accepts POST ONLY!`                         | `-1` | 使用非POST方法发送请求                     | 不执行请求，对数据库不产生影响 |
| `False` | `010002` | `ERROR! Too long name, make sure len <= 64`                  | `-1` | 用户名过长                                 | 不执行请求，对数据库不产生影响 |
| `False` | `010003` | `ERROR! Too long password, make sure len <= 64`              | `-1` | 密码过长                                   | 不执行请求，对数据库不产生影响 |
| `False` | `010004` | `ERROR! Illegal identity, make sure identity is admin, customer or seller` | `-1` | 非法身份                                   | 不执行请求，对数据库不产生影响 |
| `False` | `010005` | `ERROR! This name has been signed up, please choose another name` | `-1` | 重名用户名                                 | 不执行请求，对数据库不产生影响 |

### [02] login用户登录

#### 发送

- 使用`POST`方法向服务器提供登录申请，数据格式为`raw`+`json`
- URL:`http://43.143.179.158:8080/login`
- 具体属性如下：

| 属性     | 说明   | 类型                       |
| -------- | ------ | -------------------------- |
| name     | 用户名 | 字符串，非空，长度小于`64` |
| password | 密码   | 字符串，非空，长度小于`64` |

#### 接收

返回一个`HttpResponse`对象，属性列表如下：

| 属性     | 说明             | 类型                                                         |
| -------- | ---------------- | ------------------------------------------------------------ |
| succeed  | 是否登陆成功     | 布尔值                                                       |
| code     | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`02`表示是`login`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message  | 提示信息         | 提供更多关于本次请求处理结果的信息                           |
| id       | 登录得到的用户id | 返回数据库中该用户的唯一id，为`int`                          |
| balance  | 该用户账户余额   | 返回余额                                                     |
| identity | 用户身份         | 字符串                                                       |

- 正确情况

| succeed | code     | message                        | id                   | balance          | identity     |
| ------- | -------- | ------------------------------ | -------------------- | ---------------- | ------------ |
| `True`  | `020101` | `SUCCESS! Log in successfully` | <数据库自动赋予的id> | <该用户账户余额> | <该用户身份> |

- 错误情况

| succeed | code     | message                                                    | id                   | balance | identity     | 说明                              |
| ------- | -------- | ---------------------------------------------------------- | -------------------- | ------- | ------------ | --------------------------------- |
| `False` | `020000` | `ERROR! This URL accepts POST ONLY! `                      | -1                   | -1      | `FAIL`       | 使用非POST方法发送请求            |
| `False` | `020001` | `ERROR! Empty name or password, make sure they are legal`  | -1                   | -1      | `FAIL`       | `name,password`中有空值或空字符串 |
| `False` | `020002` | `ERROR! Non-exist name, make sure the name is correct`     | -1                   | -1      | `FAIL`       | 用户名错误                        |
| `False` | `020003` | `ERROR! Wrong password, make sure the password is correct` | <数据库自动赋予的id> | -1      | <该用户身份> | 密码错误                          |

### [03] addGoods添加售卖商品

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/addGoods`

- 具体属性如下：

| 属性        | 说明     | 类型                                                 |
| ----------- | -------- | ---------------------------------------------------- |
| name        | 商品名   | 字符串，**非空**，长度小于`64`                       |
| price       | 价格     | 精确小数（小数点后2位），**非空**，长度小于`20`      |
| seller_id   | 卖家ID   | 整数，**非空**，对应Account表中的ID                  |
| maker       | 制造商   | 字符串，可空，长度小于64                             |
| picture     | 图片     | 文件，**非空**，只能发送一张图片                     |
| description | 描述     | 字符串，可空，长度小于512                            |
| date        | 生产日期 | 字符串，可空，须形如yyyy-mm-dd，如`2021-01-10`       |
| shelf_life  | 保质期   | 字符串，可空，须形如yyyy-mm-dd-hh，如`0001-10-23-03` |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| ------- | ---------------- | ------------------------------------------------------------ |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`03`表示是`addGoods`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |
| good_id | 商品ID           | 与Good中`id`相对应                                           |

- 正确情况

| succeed | code     | message                             |
| ------- | -------- | ----------------------------------- |
| `True`  | `030101` | `SUCCESS! Add a good successfully!` |

- 错误情况

| succeed | code     | message                             |
| ------- | -------- | ----------------------------------- |
| `False` | `030000` | `ERROR! Need available good name! ` |
| `False` | `030001` | `ERROR! Need available good price!` |
| `False` | `030002` | `ERROR! Need available seller id`   |
| `False` | `030003` | `ERROR! Need available pic file`    |

### [04] updateShopCart添加商品到购物车

#### 发送

- 使用`POST`方法向服务器提供添加商品到购物车申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/updateShopCart`

- 具体属性如下：

| 属性    | 说明         | 类型                                          |
| ------- | ------------ | --------------------------------------------- |
| user_id | 用户id       | 整数，**非空**，和Account对应                 |
| good_id | 商品id       | 精确小数（小数点后2位），**非空**，和Good对应 |
| new_num | 更新后的数量 | 整数，**非空**，应当大于等于`0`               |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| ------- | ---------------- | ------------------------------------------------------------ |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`03`表示是`addGoods`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                             |
| ------- | -------- | ----------------------------------- |
| `True`  | `040101` | `SUCCESS! Add a good successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `040000` | `ERROR! Need available user_id! ` |
| `False` | `040001` | `ERROR! Need available good_id!`  |
| `False` | `040002` | `ERROR! Need available new_num!`  |
| `False` | `030003` | `ERROR! Need available pic file`  |



### [05] mainRecommendGoods为用户推荐商品

#### 发送

- 使用`POST`方法向服务器提供为用户推荐商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/mainRecommendGoods`

- 具体属性如下：

| 属性    | 说明   | 类型                          |
| ------- | ------ | ----------------------------- |
| user_id | 用户id | 整数，**非空**，和Account对应 |

#### 接收

| 属性    | 说明           | 类型                                                         |
| ------- | -------------- | ------------------------------------------------------------ |
| succeed | 是否查询成功   | 布尔值                                                       |
| code    | 处理结果代码   | 六位字符串，标识不同正确/错误情况，前两位固定为`05`表示是`mainRecommendGoods`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息       | 字符串，提供更多关于本次请求处理结果的信息                   |
| n       | 返回的商品数量 | 整数，当执行错误时，该值为`-1`，执行正确时，该值为商品数量   |
| goods   | 商品列表       | 包含有`n`个元素，每个元素是一个商品`json`，每个商品`json`结构见下表。 |

**商品`json`**

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| seller_name | 卖家名    | 字符串，与Account对应            |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| like        | 是否收藏  | 整数，为1表示收藏，为0表示不收藏 |

- 正确情况

| succeed | code     | message                                        |
| ------- | -------- | ---------------------------------------------- |
| `True`  | `050101` | `SUCCESS! Get goods recommended successfully!` |

- 错误情况

| succeed | code     | message                         |
| ------- | -------- | ------------------------------- |
| `False` | `050000` | `ERROR! Need non-null userid! ` |
| `False` | `050001` | `ERROR! Need available userid!` |

### [06] getGood获取指定商品所有信息

#### 发送

- 使用`POST`方法向服务器提供获取指定商品所有信息申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getGood`

- 具体属性如下：

| 属性    | 说明   | 类型                         |
| ------- | ------ | ---------------------------- |
| good_id | 商品id | 整数，**非空**，和`Good`对应 |

#### 接收

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| repo        | 库存      | 整数，是商品库存                 |

### [07] searchShopCart获取用户购物车内所有商品和数量

#### 发送

- 使用`POST`方法向服务器提供获取用户购物车内所有商品和数量申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/searchShopCart`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性  | 说明                 | 类型                                                         |
| ----- | -------------------- | ------------------------------------------------------------ |
| n     | 购物车内商品种类数量 | 整数，是`goods`列表的长度                                    |
| goods | 商品列表             | 包含有`n`个元素，每个元素是一个商品`json`，每个商品`json`结构见下表。 |

**商品`json`**

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| num         | 商品数量  | 整数                             |
| repo        | 库存      | 整数，是商品库存                 |

### [08] updateStar更新收藏关系

#### 发送

- 使用`POST`方法向服务器提供更新收藏关系申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/updateStar`

- 具体属性如下：

| 属性    | 说明         | 类型                                       |
| ------- | ------------ | ------------------------------------------ |
| user_id | 用户id       | 整数，**非空**，和`Account`对应            |
| good_id | 商品id       | 整数，**非空**，和`Good`对应               |
| like    | 设定收藏状态 | 整数，非空，为`1`表示收藏，为`0`表示不收藏 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`08`表示是`addStar`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                              |
| ------- | -------- | ------------------------------------ |
| `True`  | `080101` | `SUCCESS! Star a good successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `080000` | `ERROR! Need available user_id! ` |
| `False` | `080001` | `ERROR! Need available good_id!`  |
| `False` | `080002` | `ERROR! Need available like!`     |

### [09] getSixPictures获取首页六张滚播图

#### 发送

- 使用`POST`方法向服务器提供获取首页六张滚播图申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getSixPictures`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性     | 说明        | 类型                                   |
| -------- | ----------- | -------------------------------------- |
| n        | 图片数量    | 整数，执行正确应当是6                  |
| pictures | 图片url列表 | 包含有`n`个元素，每个元素是一个商品url |

### [10] updateRepo 更新库存容量

#### 发送

- 使用`POST`方法向服务器提供更新库存容量申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/updateRepo`

- 具体属性如下：

| 属性    | 说明             | 类型                         |
| ------- | ---------------- | ---------------------------- |
| good_id | 商品id           | 整数，**非空**，和`Good`对应 |
| repo    | 更新后的商品库存 | 整数，**非空**，大于等于0    |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`10`表示是`updateRepo`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                                       |
| ------- | -------- | --------------------------------------------- |
| `True`  | `100101` | `SUCCESS! Update a good's repo successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `100000` | `ERROR! Need available good_id! ` |
| `False` | `100001` | `ERROR! Need available repo!`     |

### [11] getSellGoods 获取正在售卖的商品

#### 发送

- 使用`POST`方法向服务器发送获取正在售卖的商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getSellGoods`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性  | 说明     | 类型                                                  |
| ----- | -------- | ----------------------------------------------------- |
| n     | 商品数量 | 整数，表示该用户售卖的商品数量，是`goods`列表的长度   |
| goods | 商品列表 | 包含有`n`个元素，每个元素是如下表所示的一个`json`元素 |

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| repo        | 商品库存  | 整数                             |

- 正确情况

| succeed | code     | message                                       |
| ------- | -------- | --------------------------------------------- |
| `True`  | `100101` | `SUCCESS! Update a good's repo successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `100000` | `ERROR! Need available good_id! ` |
| `False` | `100001` | `ERROR! Need available repo!`     |

### [12] goodsRecommendGoods 为商品推荐商品

#### 发送

- 使用`POST`方法向服务器发送获取商品推荐商品的申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/goodsRecommendGoods `

- 具体属性如下：

| 属性    | 说明   | 类型                         |
| ------- | ------ | ---------------------------- |
| good_id | 商品id | 整数，**非空**，和`Good`对应 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性  | 说明     | 类型                                                  |
| ----- | -------- | ----------------------------------------------------- |
| n     | 商品数量 | 整数，表示返回的推荐商品数量，是`goods`列表的长度     |
| goods | 商品列表 | 包含有`n`个元素，每个元素是如下表所示的一个`json`元素 |

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| seller_name | 卖家名    | 字符串                           |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |

### [13] getStarGoods 获取收藏商品

#### 发送

- 使用`POST`方法向服务器提供获取首页六张滚播图申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getStarGoods `

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性  | 说明         | 类型                                            |
| ----- | ------------ | ----------------------------------------------- |
| n     | 收藏商品数量 | 整数，是goods列表的长度                         |
| goods | 收藏商品列表 | 包含有`n`个元素，每个元素是一个商品json，见下表 |

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| seller_name | 卖家名    | 字符串                           |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| repo        | 库存      | 整数，返回该商品剩余库存         |

### [14] deleteGood 删除指定商品

#### 发送

- 使用`POST`方法向服务器发送获取商品推荐商品的申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/deleteGood `

- 具体属性如下：

| 属性    | 说明   | 类型                         |
| ------- | ------ | ---------------------------- |
| good_id | 商品id | 整数，**非空**，和`Good`对应 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`14`表示是`deleteGood`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                                |
| ------- | -------- | -------------------------------------- |
| `True`  | `140101` | `SUCCESS! Delete a good successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `140000` | `ERROR! Need available good_id! ` |

### [15] analyseExcel 解析Excel文件

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/analyseExcel`

- 具体属性如下：

| 属性    | 说明   | 类型                                                    |
| ------- | ------ | ------------------------------------------------------- |
| good_id | 商品ID | 和`Good`中的`id`相对应                                  |
| excel   | 表格   | 文件，**非空**，为excel表格，第一列为key，第二列为value |

#### 接收

| 属性  | 说明       | 类型                    |
| ----- | ---------- | ----------------------- |
| n     | 键值对个数 | 返回的jsons列表长度     |
| jsons | 键值对列表 | 有`n`个json作为列表元素 |

### [16] analyseShopCart 分析用户购物车内商品信息

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/analyseShopCart`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性   | 说明     | 类型                                                  |
| ------ | -------- | ----------------------------------------------------- |
| tuples | 数据元组 | 列表，包含若干个形如`(price, seller_name, num)`的json |

### [17] addAddress 添加地址

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/addAddress`

- 具体属性如下：

| 属性          | 说明           | 类型                                 |
| ------------- | -------------- | ------------------------------------ |
| user_id       | 用户id         | 整数，**非空**，和`Account`对应      |
| receiver_name | 收件人姓名     | 字符串，**非空**                     |
| phone         | 收件人电话号   | 字符串，**非空**                     |
| addr          | 收件人地址     | 字符串，**非空**                     |
| detailed_addr | 收件人详细地址 | 字符串，**非空**                     |
| comment       | 备注           | 字符串，可以为空                     |
| default       | 是否为默认地址 | 整数，为1表示是默认地址，为0表示不是 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`17`表示是`addAddress`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                                 |
| ------- | -------- | --------------------------------------- |
| `True`  | `170101` | `SUCCESS! Add an address successfully!` |

- 错误情况

| succeed | code     | message                                 |
| ------- | -------- | --------------------------------------- |
| `False` | `170000` | `ERROR! Need available user_id! `       |
| `False` | `170001` | `ERROR! Need available receiver_name! ` |
| `False` | `170002` | `ERROR! Need available phone! `         |
| `False` | `170003` | `ERROR! Need available addr! `          |
| `False` | `170004` | `ERROR! Need available detailed_addr! ` |
| `False` | `170005` | `ERROR! Need available default! `       |

### [18] addSale 添加订单

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/addSale`

- 具体属性如下：

| 属性       | 说明     | 类型                            |
| ---------- | -------- | ------------------------------- |
| user_id    | 用户id   | 整数，**非空**，和`Account`对应 |
| price      | 订单总价 | 整数，**非空**                  |
| address_id | 地址id   | 整数，**非空**，和`Address`对应 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`18`表示是`addSale`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |
| sale_id | 订单ID           | 用于继续调用`addSaleGood`API                                 |

### [19] addSaleGood 添加订单商品关系

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/addSaleGood`

- 具体属性如下：

| 属性    | 说明   | 类型                                     |
| ------- | ------ | ---------------------------------------- |
| sale_id | 订单id | 整数，**非空**，和`Sale`对应             |
| good_id | 商品id | 整数，**非空**，和`Good`对应             |
| num     | 数量   | 整数，**非空**，表示该订单内有多少该商品 |

### [20] analyseSale 分析订单商品信息

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/analyseSale`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性   | 说明     | 类型                                      |
| ------ | -------- | ----------------------------------------- |
| tuples | 数据元组 | 列表，包含若干个形如`{date, price}`的json |

### [21] getGoodDetail 获取商品详情

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getGoodDetail`

- 具体属性如下：

| 属性    | 说明   | 类型                         |
| ------- | ------ | ---------------------------- |
| good_id | 商品id | 整数，**非空**，和`Good`对应 |

#### 接收

| 属性   | 说明     | 类型                                     |
| ------ | -------- | ---------------------------------------- |
| tuples | 数据元组 | 列表，包含若干个形如`{key, value}`的json |

### [22] getAddress 获取地址

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getAddress`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性      | 说明     | 类型                             |
| --------- | -------- | -------------------------------- |
| addresses | 地址列表 | 列表，每个元素是地址json，如下表 |

| 属性          | 说明           | 类型                                 |
| ------------- | -------------- | ------------------------------------ |
| user_id       | 用户id         | 整数，**非空**，和`Account`对应      |
| address_id    | 地址id         | 整数，**非空**，和`Address`相对应    |
| receiver_name | 收件人姓名     | 字符串，**非空**                     |
| phone         | 收件人电话号   | 字符串，**非空**                     |
| addr          | 收件人地址     | 字符串，**非空**                     |
| detailed_addr | 收件人详细地址 | 字符串，**非空**                     |
| comment       | 备注           | 字符串                               |
| default       | 是否为默认地址 | 整数，为1表示是默认地址，为0表示不是 |

### [23] deleteAddress 删除地址

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/deleteAddress`

- 具体属性如下：

| 属性       | 说明   | 类型                            |
| ---------- | ------ | ------------------------------- |
| address_id | 地址id | 整数，**非空**，和`Address`对应 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`23`表示是`deleteAddress`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

### [24] updateDefaultAddress 设置默认地址

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/updateDefaultAddress`

- 具体属性如下：

| 属性       | 说明       | 类型                                                         |
| ---------- | ---------- | ------------------------------------------------------------ |
| address_id | 地址id     | 整数，**非空**，和`Address`对应                              |
| default    | 设置为0或1 | 整数，**非空**，若为1，数据库将首先搜索是否该用户已经设置过默认地址，如果有，则将其默认地址置0，然后，将本address_id地址置为默认地址；若为0，直接将address_id地址置为非默认地址 |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| :------ | :--------------- | :----------------------------------------------------------- |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`24`表示是`updateDefaultAddress`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

### [25] analyseLike 分析用户收藏商品信息

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/analyseLike`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性   | 说明     | 类型                                                  |
| ------ | -------- | ----------------------------------------------------- |
| tuples | 数据元组 | 列表，包含若干个形如`(price, seller_name, num)`的json |

### [26] updateShopCartNum更新购物车商品数量

#### 发送

- 使用`POST`方法向服务器提供添加商品到购物车申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/updateShopCartNum`

- 具体属性如下：

| 属性    | 说明         | 类型                            |
| ------- | ------------ | ------------------------------- |
| user_id | 用户id       | 整数，**非空**，和Account对应   |
| good_id | 商品id       | 整数，**非空**，和Good对应      |
| new_num | 更新后的数量 | 整数，**非空**，应当大于等于`0` |

#### 接收

返回一个`JsonResponse`对象，属性列表如下：

| 属性    | 说明             | 类型                                                         |
| ------- | ---------------- | ------------------------------------------------------------ |
| succeed | 是否成功添加商品 | 布尔值                                                       |
| code    | 处理结果代码     | 六位字符串，标识不同正确/错误情况，前两位固定为`25`表示是`addGoods`的code；中间两位错误时为`00`，正确时为`01`；最后两位表明是正确/错误情况中的具体情形，可以查阅下方的表 |
| message | 提示信息         | 提供更多关于本次请求处理结果的信息                           |

- 正确情况

| succeed | code     | message                             |
| ------- | -------- | ----------------------------------- |
| `True`  | `040101` | `SUCCESS! Add a good successfully!` |

- 错误情况

| succeed | code     | message                           |
| ------- | -------- | --------------------------------- |
| `False` | `040000` | `ERROR! Need available user_id! ` |
| `False` | `040001` | `ERROR! Need available good_id!`  |
| `False` | `040002` | `ERROR! Need available new_num!`  |
| `False` | `030003` | `ERROR! Need available pic file`  |

### [27] analyseOrder 分析用户订单商品信息

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/analyseOrder`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性   | 说明     | 类型                                                  |
| ------ | -------- | ----------------------------------------------------- |
| tuples | 数据元组 | 列表，包含若干个形如`(price, seller_name, num)`的json |

### [28] checked 返回False

#### 发送

- 使用`POST`方法向服务器提供添加售卖商品申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/checked`

- 具体属性如下：

#### 接收

| 属性    | 说明   | 类型            |
| ------- | ------ | --------------- |
| checked | 布尔值 | 无条件返回False |

### [29] getSale获取用户订单信息

#### 发送

- 使用`POST`方法向服务器提供获取用户订单信息申请，数据格式`form-data`

- URL:`http://43.143.179.158:8080/getSale`

- 具体属性如下：

| 属性    | 说明   | 类型                            |
| ------- | ------ | ------------------------------- |
| user_id | 用户id | 整数，**非空**，和`Account`对应 |

#### 接收

| 属性  | 说明     | 类型                                                         |
| ----- | -------- | ------------------------------------------------------------ |
| sales | 订单列表 | 包含有若干个元素，每个元素是一个列表（下称子列表），每个子列表由若干个商品json组成，每个商品json如下表所示。 |

**商品`json`**

| 属性        | 说明      | 类型                             |
| ----------- | --------- | -------------------------------- |
| id          | 商品`id`  | 互不相同的整数，是标识商品的主码 |
| name        | 商品名    | 字符串，商品名                   |
| price       | 价格      | 字符串，精确到小数点后两位       |
| seller_id   | 卖家`id`  | 互不相同的整数，是标识用户的主码 |
| maker       | 制造商名  | 字符串，制造商名                 |
| picture     | 图片`url` | 字符串，商品图片`url`            |
| description | 商品描述  | 字符串，商品详细描述             |
| date        | 生产日期  | 字符串，形如yyyy-mm-dd           |
| shelf_life  | 保质期    | 字符串，形如yyyy-mm-dd-hh        |
| num         | 商品数量  | 整数                             |
