<template>
  <div id="father">
    <LogInt ref="myson" v-if="not_login" v-on:login="Login" v-on:register="Register"/>
    <div v-if="!not_login">
      <el-row>
        <el-col :span="5" style="background-color:rgba(64,158,255,0.5); height:700px;">
        <el-menu style="width:280px; position:relative;left:17px;top:-20px;font-size:30px;" default-active="1">
            <div id="head1">
            <h3>用户主页</h3>
            </div>
            <el-menu-item index="1" @click="now = 1">
              <el-icon><icon-menu /></el-icon>
              <span class="menus">我的收藏</span>
            </el-menu-item>
            <el-menu-item index="2" @click="now = 2">
              <el-icon><icon-menu /></el-icon>
              <span class="menus">血糖记录</span>
            </el-menu-item>
            <el-menu-item index="3" @click="now = 3">
              <el-icon><icon-menu /></el-icon>
              <span class="menus">血糖走势</span>
            </el-menu-item>
            
        </el-menu>
        <el-button type="primary" @click="logout">退出登录</el-button>
        </el-col>

        <div v-if="now === 2" id="message">
        <el-table :data="tableData" style="{width: 100%;font-size:15px;}" stripe border>
        <el-table-column prop="date" label="日期" width="360" />
        <el-table-column prop="name" label="完成状况" width="360" />
            <el-table-column fixed="right" label="编辑" width="80">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="open(scope.$index)">编辑</el-button>
              </template>
            </el-table-column>
        </el-table>
        <el-pagination :page-size="10" :pager-count="5" layout="prev, pager, next" :total="page.total" 
        v-model:currentPage="page.num" background @current-change="pageChange" class="page"/>
        <el-button type="primary" @click="dialogVisible = true;" id="add">新增</el-button>
        <el-dialog v-model="dialogVisible">
          <input type="date" v-model="newData.date" style="width:540px;"/>
          <div style="margin: 20px 0" />
          <span>早餐前血糖</span>
          <input type="number" v-model="newData.fpg_morning" step="0.1" style="width:200px;"/>
          <span>早餐后血糖</span>
          <input type="number" v-model="newData.p2hpg_morning" step="0.1" style="width:200px;"/>
          <div style="margin: 20px 0" />
          <span>午餐前血糖</span>
          <input type="number" v-model="newData.fpg_noon" step="0.1" style="width:200px;"/>
          <span>午餐后血糖</span>
          <input type="number" v-model="newData.p2hpg_noon" step="0.1" style="width:200px;"/>
          <div style="margin: 20px 0" />
          <span>晚餐前血糖</span>
          <input type="number" v-model="newData.fpg_evening" step="0.1" style="width:200px;"/>
          <span>晚餐后血糖</span>
          <input type="number" v-model="newData.p2hpg_evening" step="0.1" style="width:200px;"/>
          <div style="margin: 20px 0" />
          <el-button @click="dialogVisible = false;add_flag = 0;" class="buttons">取消</el-button>
          <el-button type="primary" @click="add" class="buttons">确认</el-button>
        </el-dialog>
        </div>
        <!-- edit 页面 -->
        <div v-if="now === 4" id="message">
          <span class="data">日期:<input v-model="pgData.date" disabled style="width:200px;"/></span>
          <div style="margin: 20px 0px" />
          <span class="data">早餐前血糖:<input v-model="pgData.fpg_morning" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />
          </span>
          <div style="margin: 20px 0px" />
          <span class="data">早餐后血糖:<input v-model="pgData.p2hpg_morning" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />
          </span>
          <div style="margin: 20px 0px" />
          <span class="data">午餐前血糖:<input v-model="pgData.fpg_noon" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />
          </span>
          <div style="margin: 20px 0px" />
          <span class="data">午餐后血糖:<input v-model="pgData.p2hpg_noon" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />
          </span>
          <div style="margin: 20px 0px" />
          <span class="data">晚餐前血糖:<input v-model="pgData.fpg_evening" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />  
          </span>
          <div style="margin: 20px 0px" />
          <span class="data">晚餐后血糖:<input v-model="pgData.p2hpg_evening" :disabled="!changeText" style="width:200px;" type="number" step="0.1" />
        
          </span>
          <div style="margin: 20px 0px" />
            <el-button type="primary" @click="save" class="button" v-if="changeText">保存</el-button>
            <el-button type="primary" @click="changeText = true;" class="button" v-if="!changeText">编辑</el-button>
            <el-button type="primary" @click="ret" class="button">返回</el-button>
          </div>
        <div v-if="now === 3">
            <pgChart class="chart">mychart</pgChart>
        </div>
        <div v-if="now === 1" id="message">
          <el-select v-model="list"  placeholder="收藏种类" size="large" @change="get_favors">
            <el-option
              v-for="item in chosen"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
          <el-table :data="favors.list" style="width:100%;font-size:15px;" stripe border>
            <el-table-column label="标题" width="800">
                <template #default="scope">
                  <div v-if="list === 1">
                    <div v-if="scope.row.postId" @click="jmppost(scope.row.postId)" style="cursor: pointer; display:inline-block;">
                    帖子
                    </div>
                    <div v-if="scope.row.postId" style="display:inline-block;margin-left:200px;">
                      {{scope.row.title}}
                    </div>
                  </div>
                  <div v-else-if="list === 2">
                    <div v-if="scope.row.newsId" @click="jmpnews(scope.row.newsId)" style="cursor: pointer; display:inline-block;">
                    资讯
                    </div>
                    <div style="display:inline-block;margin-left:200px;" v-if="scope.row.newsId">
                      {{scope.row.title}}
                    </div>
                  </div>
                  <div v-else-if="list === 0">
                    <div v-if="scope.row.newsId" @click="jmpnews(scope.row.newsId)" style="cursor: pointer; display:inline-block;">
                    资讯
                      <div style="display:inline-block; margin-left:200px;">
                        {{scope.row.title}}
                      </div>
                    </div>
                    <div v-if="scope.row.postId" @click="jmppost(scope.row.postId)" style="cursor: pointer; display:inline-block;">
                    帖子
                      <div style="display:inline-block; margin-left:200px;">
                        {{scope.row.title}}
                      </div>
                    </div>
                  </div>
                </template>
            </el-table-column>
          </el-table>
          <el-pagination :page-size="10" :pager-count="5" layout="prev, pager, next" 
          :total="favors.total" v-model:currentPage="favors.num" background @current-change="get_favors" class="page"/>
        </div>
      </el-row>
        
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import LogInt from '@/components/LogInt.vue'; // @ is an alias to /src
import pgChart from '@/components/Charts.vue';
import { ElMessage,ElMessageBox } from 'element-plus';
import axios from 'axios';

export default defineComponent({
  name: 'HomeView',
  components: {
    LogInt,
    pgChart,
  },
  prop:{
  },
  data(){
    return{
            list:0,
            chosen:[
              {
                value:1,
                label:'只显示帖子',
              },
              {
                value:2,
                label:'只显示资讯',
              },
              {
                value:0,
                label:'显示全部'
              }
            ],
            favors:{
              list:[],
              newslist:[],
              postlist:[],
              total:10,
              num:1,
            },
            changeText:false,
            index:'',
            add_flag:0,
            newData:{
              date:'',
              fpg_morning:0.0,
              p2hpg_morning:0.0,
              fpg_noon:0.0,
              p2hpg_noon:0.0,
              fpg_evening:0.0,
              p2hpg_evening:0.0,
              name:0,
            },
            dialogVisible:false,
            pgData:
              {
              date:'',
              fpg_morning:0,
              p2hpg_morning:0,
              fpg_noon:0,
              p2hpg_noon:0,
              fpg_evening:0,
              p2hpg_evening:0,
              name:'',
            },
            page:{
              total:100,
              num:1,
            },
            not_login: true,
            now: 1,
            user:{
                id:0,
                name:'',
                nickname:'',
                jwt:'',
            },
            tableData:[],
            status: 0,
            msg: '',
    } 
  },
  methods:{
        async Login(data){     
          await axios.post("/user/api/login", data)
              .then((response) =>  {
                this.user.jwt = response.data.jwt;
                this.user.id = response.data.userId;
                this.user.nickname = response.data.nickname;
                this.user.name = response.data.username;
                this.status = response.status;
                if(data.remember === true)
                {
                  localStorage.setItem('user1',data.username);
                  localStorage.setItem('password1',data.password);
                }
                })
              .catch((error) => {
                this.msg = error.response.data.message
                this.status = error.response.status
                console.log(error.response.data.message)
              })

          let that = this;
          if (this.status == 200){
            this.not_login = false;
            localStorage.setItem("jwt",this.user.jwt);
            localStorage.setItem("userId",this.user.id);
            this.pageChange(); 
            this.get_favors();
            that.$root.getAvatar(this.user.id, this.user.jwt);
            ElMessage({
              message: '登录成功',
              type: 'success'
            });
          }
          else if(this.status == 300){
            ElMessage({
              message: '用户已在别处登录',
              type: 'error',
            })
          }
          else
            ElMessage({
              message: '用户名或密码错误，请重试',
              type: 'error',
            })
        },

        async Register(data){  
          await axios.post("/user/api/register", data)
              .then((response) => {
                this.user.id = response.data.userId;
                this.user.nickname = response.data.nickname;
                this.user.name = response.data.username;
                this.status = response.status;
                this.msg = response.data.message;
                console.log(this.msg);
                })
              .catch((error) => {
                this.msg = error.response.data.message
                this.status = error.response.status
                console.log(error.response.data.message)
              });
            
          if (this.status == 200){
            this.$refs.myson.mod = 'first';
            this.$refs.myson.remake();
            ElMessage({
              message: '注册成功',
              type: 'success'
            });
          }
          else
            ElMessage({
              message: this.msg,
              type: 'error',
            })
        },

        async logout(){
            await axios.post("/user/api/logout",1,{
                headers: {'Authorization': this.user.jwt},
              })

            localStorage.removeItem("jwt");
            localStorage.removeItem("userId");
            this.not_login = true;
            this.$root.clearAvatar();
            
        },

        async pageChange(){
          await axios.get("/pg/api/getpglist", {
            headers: {'Authorization': this.user.jwt},
            params: {page: this.page.num},   
           }).then((res)=>{
            console.log(res)
            this.tableData = res.data.pg_list;
            this.page.total = res.data.count;
            for(let i = 0; i < this.tableData.length; i++)
            {
              this.tableData[i]['pg_id'] = this.tableData[i]['id'];
              if(this.tableData[i]['fpg_morning'] && this.tableData[i]['fpg_noon'] && this.tableData[i]['fpg_evening']
                && this.tableData[i]['p2hpg_morning'] && this.tableData[i]['p2hpg_noon']&& this.tableData[i]['p2hpg_evening'])
              {
                this.tableData[i]['name'] = '已完成';
              }
              else this.tableData[i]['name'] = '未完成';
            }
          }).catch((err)=>{
              console.log(err);
          })
        },

        add(){
          if(
            ((this.newData.fpg_morning && (this.newData.fpg_morning > 8 || this.newData.fpg_morning < 3.9))  ||
            (this.newData.p2hpg_morning && (this.newData.p2hpg_morning > 9 || this.newData.p2hpg_morning < 5)) ||
            (this.newData.fpg_noon && (this.newData.fpg_noon > 8 || this.newData.fpg_noon < 3.9)) ||
            (this.newData.p2hpg_noon && (this.newData.p2hpg_noon > 9 || this.newData.p2hpg_noon < 5)) ||
            (this.newData.fpg_evening && (this.newData.fpg_evening > 8 || this.newData.fpg_evening < 3.9)) ||
            (this.newData.p2hpg_evening && (this.newData.p2hpg_evening > 9 || this.newData.p2hpg_evening < 5)))
            && (this.add_flag === 0)
          )
          {
            ElMessageBox.confirm(
              '血糖值异常，是否确认？',
              'Warning',
              {
                confirmButtonText: '确认',
                cancelButtonText: '取消',
                type: 'warning',
              }
            ).then(() => {
              this.add_flag = 1;
              }).catch(() => {
              ElMessage({
                type: 'info',
                message: '取消',
              });
              return;
            })
          }
          else{
            this.dialogVisible = false;
            this.add_flag = 0;
            let pg_data = {
              pg_date:this.newData.date,
              fpg_morning:this.newData.fpg_morning,
              fpg_noon:this.newData.fpg_noon,
              fpg_evening:this.newData.fpg_evening,
              p2hpg_morning:this.newData.p2hpg_morning,
              p2hpg_noon:this.newData.p2hpg_noon,
              p2hpg_evening:this.newData.p2hpg_evening,
            };
            axios.post("/pg/api/createpg", pg_data,
              {
                headers: {'Authorization': this.user.jwt},
              })
              .then((res) =>{
                console.log(res)
                this.pageChange();
                ElMessage({
                  message:'创建成功',
                  type:'success',
                });
              }).catch((error) => {
                  ElMessage({
                    message:error.response.data.message,
                    type:'error',
                  });
                })
          }
        },

        open(num){
          this.now = 4;
          this.pgData = this.tableData[num];
          this.index = num;
        },

        save(){
          this.changeText = false;
          axios.post("/pg/api/updatepg", this.pgData,{headers: {'Authorization': this.user.jwt},})
          .then(() => {
             ElMessage({
                    message:'修改成功',
                    type:'success',
                  });
          })
          .catch((error) => {
            ElMessage({
                    message:error,
                    type:'error',
                  });
          }) 
        },

        ret(){
          this.changeText = false;
          this.now = 2;
          this.pageChange();
        },

        get_favors(){
          axios.get("/favorite/api/getfavorlist", {
              headers: {'Authorization': this.user.jwt},
              params: { 'page': this.favors.num,
              'type': this.list},
          }).then((res) => {
              console.log(res);
              this.favors.list = res.data.favorite_list;
              this.favors.total = res.data.count;
          }).catch((err) => {
              console.log(err);
          })
        },
        jmppost(id){
          this.$router.push({path:'/Social/' + id})
        },
        jmpnews(id){
          this.$router.push({path:'/news/' + id})
        },
        
  },
  mounted(){
    if(localStorage.getItem('jwt'))
    {
      this.not_login = false;
      this.user.jwt = localStorage.getItem('jwt');
      this.user.id = localStorage.getItem('userId');
      this.pageChange();
      this.$root.getAvatar(this.user.id, this.user.jwt);
      this.get_favors();
    }

    Date.prototype.Format = function (fmt) {
      var o = {
      "M+": this.getMonth() + 1, //月份
      "d+": this.getDate(), //日
      "H+": this.getHours(), //小时
      "m+": this.getMinutes(), //分
      "s+": this.getSeconds(), //秒
      "q+": Math.floor((this.getMonth() + 3) / 3), //季度
      "S": this.getMilliseconds() //毫秒
      };
      if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
      for (var k in o)
      if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      return fmt;
    }
      
    this.newData.date = new Date().Format("yyyy-MM-dd");
    
  },

});
</script>

<style scoped>
#message{
    position:relative;
    left:200px;
    top:50px;
    width:800px;
    height:550px;
    border:2px solid rgb(64,158,255);
    text-align:left;
    border-radius:4px;
}

.word{
    font-size:22px;
    position:relative;
    left:50px;
    top:30px;
}


.button{
    position:relative;
    left:200px;
    top:40px;
    width:200px;
    height:50px;
    font-size:20px;
}


.menus{
    position:relative;
    left:60px;
}

#father{
    position:absolute;
    top:120px;
    width:100%;
    text-align:center;
}

input{
  font-size:20px;
  height:26px;
}

input:disabled{
  border:0;
  height:30px;
  background-color:#FFFFFF;
}

.page{
  width:200px;
  margin-top:10px;
  margin-left:260px;
}

#add{
  position:absolute;
  top:450px;
  left:720px;
}

.buttons{
  position:relative;
  left:240px;
}

.data{
  position:relative;
  left:50px;
  top:20px;
}

.chart{
  position:relative;
  left:100px;
  top:100px;
}




</style>
