# API

## user部分

```
bp = Blueprint('user', __name__, url_prefix='/user')
```

> 用户信息
>
> + id				  系统默认分配，用户没有权限修改
> + username	只能大小写字母、数字、*-_@，5-15字符
> + password    必须字母+数字，不能有其他，6-16字符
> + nickname    任意，1-14字符
> + mobile         不能0开头，11位数字
> + address       qq、163、126、gmail、56、mail
> + signature     任意，不超过150字符，默认为空

### 注册

```
@bp.route('/api/register', methods=['POST'])
def user_register():
```

+ 接收：json
  + 字典content，包含字段
    + username	  只能大小写字母、数字、*-_@
    + password    必须字母+数字，不能有其他
    + nickname    任意，不超过14字符
    + mobile         11位数字
    + address       任意
    + signature     任意，不超过150字符，默认为空
+ 返回：json + 状态码
  + json包含字段
    + message	成功返回ok，错误多种
    + userId
    + username
    + nickname

> username重复   error
>
> 字段错误    invalid arguments: + 字段名

### 登陆

```
@bp.route('/api/login', methods=['POST'])
def login():
```

+ 接收：json
  + 字典content，包含字段
    + username	只能大小写字母、数字、*-_@
    + password    必须字母+数字，不能有其他
+ 返回：json + 状态码
  + json包含字段
    + jwt    字符串，用于识别用户，此后用户访问后端必须在headers中带有jwt
    + userId
    + username
    + nickname

### 登出

```
@bp.route('/api/logout', methods=['POST'])
@login_required
def logout():
```

+ 返回：json + 状态码
  + json包含字段
    + message	

### 修改属性

```
@bp.route('/api/changeattr', methods=['POST'])
@login_required
def change_attr():
```

+ 接收：json
  + 字典content，包含字段
    + username
    + password
    + nickname
    + mobile
    + address
    + signature
+ 返回：json + 状态码
  + json包含字段
    + message	
    + username
    + nickname
    + mobile
    + address
    + signature

### 获取当前登陆用户信息

```
@bp.route('/api/user', methods=['GET'])
@login_required
def get_user_info():
```

+ 返回：json + 状态码
  + json包含字段
    + id
    + username
    + nickname
    + created
    + mobile
    + address
    + signature

### 获取指定用户信息

```
@bp.route('/api/user/<int:userId>', methods=['GET'])
@login_required
def get_user_info_by_id(userId):
```

+ 接收：整形整数userId
+ 返回：json + 状态码
  + json包含字段
    + id
    + nickname
    + created
    + signature

### 重置密码

```
@bp.route('/api/resetpw', methods=['POST'])
def reset_password():
```

+ 接收：json
  + 字典content，包含字段
    + username
    + password
    + mobile
+ 返回：json + 状态码
  + json包含字段
    + id
    + username
    + nickname
    + mobile
    + address
    + signature

### 上传头像

```
@bp.route('/api/uploadavatar', methods=['POST'])
@login_required
def upload_avatar():
```

+ 返回：json + 状态码
  + json包含字段
    + message

### 获取头像

```
@bp.route('/api/downloadavatar', methods=['GET'])
@login_required
def download_avatar():
```

+ 接受：.jpg文件
+ 返回：.jpg文件

## post部分

```
bp = Blueprint('post', __name__, url_prefix='/post')
```

>post
>
>+ id               帖子id
>+ user_id             发帖用户id
>+ title                帖子标题 小于128
>+ content           帖子内容    小于1024
>+ last_replied_user_id         最后回复用户id
>+ last_replied_time          最后回复时间
>+ created          创建时间
>+ updated          更新时间

> reply
>
> + id                 回复id
> + user_id             发帖用户id
> + post_id             回复帖子id
> + reply_id            回复回复id，若回复的是帖子则此项置为0
> + content           帖子内容    小于1024
> + created          创建时间
> + updated          更新时间

### 创建帖子

```
@bp.route('/api/createpost', methods=['POST'])
@login_required
def create_post():
```

+ 接收：json
  + 字典content，包含字段
    + title
    + content
+ 返回：json + 状态码
  + json包含字段
    + message	
    + postId      帖子id
    + userId       发帖用户id
    + title 
    + content



### 获取指定帖子信息

```
@bp.route('/api/getpost/<int:postId>', methods=['GET'])
@login_required
def get_post_detail(postId):
```

+ 接受：整形整数postId
+ 返回：json + 状态码
  + json包含字段
    + id
    + userId
    + nickname
    + title
    + content
    + created
    + updated
    + lastRepliedTime
    + reply          回复列表，每一项是一个字典，包含回复信息。列表包括帖子底下所有的回复，包括对帖子和对回复的

### 获取一页的帖子

```
@bp.route('/api/getpostlist', methods=['GET'])
@login_required
def get_post_list():
```

+ 接受：
  + page		将要显示第几页       默认为1         int
  + size          一页有几个帖子       默认为10       int
  + userId     显示指定用户的帖子   默认为0，即不指定用户         int
  + orderByReply       显示顺序，默认为False，按帖子更新时间排序，传入True按回复时间排序
+ 返回：json+状态码
  + json包含字段
    + posts		帖子列表，每一项是一个字典，包含帖子所有信息
    + page
    + size
    + total         帖子总数，如果传入了userId则是该用户的发帖总数

### 修改帖子

```
@bp.route('/api/modifypost/<int:postId>', methods=['POST'])
@login_required
def modify_post(postId):
```

+ 接收：整形整数postId，json
  + 字典content，包含字段
    + title
    + content
+ 返回：json + 状态码
  + json包含字段
    + message	

### 删除帖子

```
@bp.route('/api/deletepost/<int:postId>', methods=['POST'])
@login_required
def delete_post(postId):
```

+ 返回：json + 状态码
  + json包含字段
    + message	

### 回复帖子

```
@bp.route('/api/reply/<int:postId>', methods=['POST'])
@login_required
def reply_post(postId):
```

+ 接收：json
  + 字典content，包含字段
    + content
    + replyId      可选，默认为0，认为对帖子回复；指定replyId则对指定回复回复
+ 返回：json + 状态码
  + json包含字段
    + message	

### 删除指定回复

```
@bp.route('/api/deletereply/<int:replyId>', methods=['POST'])
@login_required
def delete_reply(replyId):
```

+ 接受：整形整数replyId
+ 返回：json + 状态码
  + json包含字段
    + message	

### 获取回复

```
@bp.route('/api/getreply', methods=['GET'])
@login_required
def get_reply():
```

+ 接收：整形整数replyId
+ 返回：json + 状态码
  + json包含字段
    + message
    + user_id
    + reply_id
    + post_id
    + content
    + favor_num

### 获取回复列表

```
@bp.route('/api/getreplylist', methods=['GET'])
@login_required
def get_reply_list():
```

+ 接收：整形整数replyId
+ 返回：json + 状态码
  + json包含字段
    + message
    + reply_list

### 修改回复

```
@bp.route('/api/modify/<int:postId>/reply/<int:replyId>', methods=['POST'])
@login_required
def modify_reply(postId, replyId):
```

+ 接收：整形整数postId，整形整数replyId，json
  + 字典content，包含字段
    + content
+ 返回：json + 状态码
  + json包含字段
    + message	

### 点赞帖子

```
@bp.route('/api/supportpost/<int:postId>', methods=['POST'])
@login_required
def support_post(postId):
```

+ 接收：整形整数postId，json
  + 字典content，包含字段
    + content
+ 返回：json + 状态码
  + json包含字段
    + message	

### 点赞回复

```
@bp.route('/api/supportreply/<int:replyId>', methods=['POST'])
@login_required
def support_reply(replyId):
```

+ 接收：整形整数replyId，json
  + 字典content，包含字段
    + content
+ 返回：json + 状态码
  + json包含字段
    + message	

## pg部分

```
bp = Blueprint('pg', __name__, url_prefix='/pg')
```

> + id       
> + user_id
> + fpg_morning   血糖数值    float   一位小数
> + fpg_noon
> + fpg_evening
> + p2hpg_morning
> + p2hpg_noon
> + p2hpg_evening
> + date              血糖日期   str    2022-7-19格式
> + created
> + updated

### 创建pg

```
@bp.route('/api/createpg', methods=['POST'])
@login_required
def create_pg():
```

+ 接收：json
  + 字典content，包含字段
    + fpg_morning
    + fpg_noon
    + fpg_evening
    + p2hpg_morning
    + p2hpg_noon
    + p2hpg_evening
    + pg_date      可选，不传入日期则默认是当天
+ 返回：json + 状态码
  + json包含字段
    + message	
    + pg_id
    + fpg_morning
    + fpg_noon
    + fpg_evening
    + p2hpg_morning
    + p2hpg_noon
    + p2hpg_evening
    + pg_date

### 获取pg

```
@bp.route('/api/getpg', methods=['GET'])
@login_required
def get_pg():
```

+ 接收：
  + date     字符串   2022-7-19格式
+ 返回：
  + json
    + message
    + pg

### 更新fpg

```
@bp.route('/api/updatepg', methods=['POST'])
@login_required
def update_pg():
```

+ 接收：json
  + 字典content，包含字段
    + fpg_morning
    + fpg_noon
    + fpg_evening
    + p2hpg_morning
    + p2hpg_noon
    + p2hpg_evening
    + pg_date    
+ 返回：json + 状态码
  + json包含字段
    + message	

### 获取pg列表

```
@bp.route('/api/getpglist', methods=['GET'])
@login_required
def get_pg_list():
```

+ 接收：json
  + page 页数 整形整数 大于等于1
+ 返回：json + 状态码
  + json包含字段
    + message
    + pg_list
    + count

### 获取全部pg

```
@bp.route('/api/getpgall', methods=['GET'])
@login_required
def get_pg_all():
```

+ 接收：json
  + page 页数 整形整数 大于等于1
+ 返回：json + 状态码
  + json包含字段
    + message
    + count
    + fpg_list
    + p2hpg_list

## news部分

```
bp = Blueprint('news', __name__, url_prefix='/news')
```

> + id
> + title
> + address
> + keyword
> + date

### 获取资讯内容

```
@bp.route('/api/news/<int:newsId>', methods=['GET'])
def get_news_detail(newsId):
```

+ 接收：json
  + newsId 整形整数
+ 返回：json + 状态码
  + json包含字段
    + message
    + content
    + id
    + title
    + date

### 获取一页的资讯列表

```
@bp.route('/api/getnewslist', methods=['GET'])
def get_news_list():
```

+ 接收：json
  + page 整形整数
  + keyword 整形整数 默认0 鸡汤为1 常识为2 新闻为3 用药为4
+ 返回：json + 状态码
  + json包含字段
    + message
    + news 即news_list
    + page
    + total 即count

### 搜索获取一页的资讯列表

```
@bp.route('/api/getnewsbysearch', methods=['GET'])
def get_news_list_by_search():
```

+ 接收：json
  + page 整形整数
  + serach_word 搜索关键词 字符串
+ 返回：json + 状态码
  + json包含字段
    + message
    + news 即news_list
    + page
    + total 即count

## log部分

```
bp = Blueprint('log', __name__, url_prefix='/log')
```

> + id
> + user_id
> + title
> + content
> + date
> + created
> + updated

### 创建log

```
@bp.route('/api/createlog', methods=['POST'])
@login_required
def create_log():
```

+ 接收：json
  + content包含字符串
+ 返回：json + 状态码
  + json包含字段
    + logId
    + userId
    + title
    + content
    + date
    + message

### 获取log

```
@bp.route('/api/getlog', methods=['GET'])
@login_required
def get_log():
```

+ 接收：date 日期
+ 返回：json + 状态码
  + json包含字段
    + message
    + log_id
    + title
    + content
    + date
    + created
    + updated

### 更新log

```
@bp.route('/api/updatelog', methods=['POST'])
@login_required
def update_log():
```

+ 接收：json
  + content包含字符串
+ 返回：json + 状态码
  + json包含字段
    + message

## favorite部分

```
bp = Blueprint('favorite', __name__, url_prefix='/favorite')
```

> + id
> + user_id
> + post_id
> + news_id
> + title

### 创建收藏

```
@bp.route('/api/createfavor', methods=['POST'])
@login_required
def create_favor():
```

+ 接收：json
  + content包含
    + title
    + post_id
    + news_id
+ 返回：json + 状态码
  + json包含字段
    + favoriteId
    + userId
    + title
    + message

### 获取收藏列表

```
@bp.route('/api/getfavorlist', methods=['GET'])
@login_required
def get_favor_list():
```

+ 接收：整形整数page
+ 返回：json + 状态码
  + json包含字段
    + message
    + favorite_list
    + count
    + page

### 删除收藏

```
@bp.route('/api/deletefavor', methods=['GET'])
@login_required
def delete_favor():
```

+ 接收：favorite_id
+ 返回：json + 状态码
  + json包含字段
    + message

### 查看收藏

```
@bp.route('/api/getfavorlist', methods=['GET'])
@login_required
def get_favor_list():
```

+ 接收：整形整数post_id，整形整数news_id
+ 返回：json + 状态码
  + json包含字段
    + message
    + favorite_list
