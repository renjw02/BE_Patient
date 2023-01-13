<template>
    <div style="text-align: center;">
        <div id="head1">
            <h1>糖斗人</h1>
            <p>--糖尿病人互助网站</p>

        </div>
        <div id="mid">
            <el-tabs v-model="mod" id="select1" stretch=True>
            <el-tab-pane label="登录" name="first"></el-tab-pane>
            <el-tab-pane label="注册" name="second"></el-tab-pane>
          </el-tabs>
        </div>
            <div class="bottom" v-if="mod === 'first'">
                <el-form>
                    <div style="margin: 15px 0" />
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><User /></el-icon>
                    <el-input v-model="login.name" style="width: 200px" placeholder="请输入账号" @input="login.password = '';"></el-input>
                    <div style="margin: 15px 0" />
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><Lock /></el-icon>
                    <el-input v-model="login.password" style="width: 200px" placeholder="请输入密码" type="password" show-password></el-input>
                    <div style="margin: 5px 0" />
                    <el-checkbox v-model="login.remember" label="记住密码" id="remember" style="position:relative;left:-40px;" @change="rem"/>
                    <a id="forget" href="/forget">忘记密码?</a>
                    <div style="margin: 5px 0" />
                <el-button type="submit" @click="toLogin">
                登录
                </el-button>
                <div style="margin: 15px 0" />
                </el-form>
            </div>
            <div class="bottom" v-if="mod === 'second'">
                <el-form>
                    <div style="margin: 15px 0" />
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><User /></el-icon>
                    <el-popover placement="bottom-start" :width="200" trigger="hover" content="5-15个数字,字母或其他">
                        <template #reference>
                            <el-input v-model="register.name" style="width: 200px" placeholder="请输入用户名"></el-input>
                        </template>
                    </el-popover>
                    <div class="prompt"/>
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><Lock /></el-icon>
                    <el-popover placement="bottom-start" :width="200" trigger="hover" content="6-16数字或字母">
                        <template #reference>
                    <el-input v-model="register.password" style="width: 200px" placeholder="请输入密码" type="password" show-password></el-input>
                        </template>
                    </el-popover>
                    <div class="prompt"/>
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><Lock /></el-icon>
                    <el-input v-model="register.password_again" style="width: 200px" placeholder="请再次输入密码" type="password" show-password/>
                    <div class="prompt">
                    </div>
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><Iphone /></el-icon>
                    <el-popover placement="bottom-start" :width="200" trigger="hover" content="11位数字">
                        <template #reference>
                        <el-input v-model="register.phone" style="width: 200px" placeholder="请输入手机号"></el-input>
                        </template>
                    </el-popover>
                    <div class="prompt">
                    </div>
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><Message /></el-icon>
                    <el-input v-model="register.email" style="width: 200px" placeholder="请输入邮箱地址"></el-input>
                    <div class="prompt">
                    </div>
                    <el-icon :size="25" style="position:relative;top:8px;left:-10px;"><MoreFilled /></el-icon>
                    <el-popover placement="bottom-start" :width="200" trigger="hover" content="最多14位">
                        <template #reference>
                            <el-input v-model="register.nickname" style="width: 200px" placeholder="请输入昵称"></el-input>
                        </template>
                    </el-popover>
                    <div class="prompt">
                    </div>
                    <div class="prompt"/>
                <el-button type="submit" @click="toRegister">
                注册
                </el-button>
                <div style="margin: 15px 0" />
                </el-form>
            </div>

    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'LogInt',
  props: {
  },
  data(){
     return{
        mod:"first",
        login:{
            name:"",
            password:"",
            remember:false,
        },
        register:{
            name:"",
            password:"",
            password_again:"",
            phone:"",
            email:"",
            nickname:"",
        }
     }
  },
  methods:{
        toLogin(){
            let pattern = /^[\da-zA-z*_\-@]*$/;
            let pattern2 = /^[\da-zA-Z]*$/
            if(this.login.name.match(pattern) == null || this.login.password.match(pattern2) == null)
            {
                ElMessage({
                message: '用户名或密码错误，请重试',
                type: 'warning',
                  });
                  return;
            }
            let data = {
                username:this.login.name,
                password:this.login.password,
                remember:this.login.remember,
            }
            this.$emit('login',data);
        },
        toRegister(){
            if(this.register.name.match(/^[\da-zA-z*_\-@]*$/) == null
                ||this.register.password.match(/^[\da-zA-Z]*$/) == null
                ||this.register.password != this.register.password_again
                ||this.register.phone.match(/^[1-9]\d*$/) == null
                ||this.register.nickname.match(/^.*$/) == null
            )
            {
                ElMessage({
                    message: '两次输入密码不一致',
                    type: 'warning',
                      });
            }
            let data = {
                username:this.register.name,
                password:this.register.password,
                nickname:this.register.nickname,
                mobile:this.register.phone,
                address:this.register.email
            }
            this.$emit('register',data);
        },
        remake(){
            this.register.name = '';
            this.register.password="";
            this.register.password_again="";
            this.register.phone="";
            this.register.email="";
            this.register.nickname="";
        },
        rem(){
            if(this.login.remember === false)
            {
                localStorage.removeItem('user1');
                localStorage.removeItem('password1');
            }
        }
  },
  mounted()
  {
        this.login.name = localStorage.getItem('user1') || '';
        this.login.password = localStorage.getItem('password1') || '';
        if(this.login.name && this.login.password)
            this.login.remember = true;
  },
});
</script>

<style scoped lang="less">
a{
    font-size:14px;
}
#head1{
    position:absolute;
    top:120px;
    left:550px;
    width:304px;
    background-color:rgba(64,158,255,0.5);
}
.bottom{
    position:absolute;
    top:280px;
    left:550px;
    width:300px;
    background-color:#FFFFFF;
    border-left:2px solid rgba(64,158,255,0.5);
    border-right:2px solid rgba(64,158,255,0.5);
    border-bottom:2px solid rgba(64,158,255,0.5);
    border-radius:4px;
}
#mid{
    position:absolute;
    top:240px;
    left:550px;
    width:300px;
    border-left:2px solid rgba(64,158,255,0.5);
    border-right:2px solid rgba(64,158,255,0.5);
}
#select1{
    position:relative;
}

#forget{
    position:relative;
    top:-2px;
    left:35px;
}

.prompt{
    height: 15px;
    font-size:1px;
    text-align: left;
}

.prompt p{
    margin-left:70px;
}

</style>