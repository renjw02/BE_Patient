<template>
    <div id="father">
        <el-button id="ret_button" @click="ret"><el-icon><Back/></el-icon>点击返回</el-button>
        <h1>找回密码</h1>
        <el-input v-model="user" placeholder="请输入用户名" style="width: 200px"/>
        <div style="margin:15px 0"/>
        <el-input v-model="mobile" placeholder="请输入手机号" style="width: 200px"/>
        <div style="margin:15px 0"/>
        <el-popover placement="bottom-start" :width="200" trigger="hover" content="6-16数字或字母">
            <template #reference>
            <el-input v-model="password" placeholder="请输入新密码" style="width: 200px" type="password" show-password/>
            </template>
        </el-popover>
        <div style="margin:15px 0"/>
        <el-input v-model="password_again" placeholder="请再次输入新密码" style="width: 200px" type="password" show-password/>
        <div style="margin:30px 0"/>
        <el-button type="primary" style="margin:0 40px" @click="sub">确认</el-button>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'ForgetView',
  props: {
  },
  data(){
    return{
        user:'',
        mobile:'',
        password:'',
        password_again:'',
    }
  },
  methods:{
    ret(){
        this.$router.push({path:'/person'});//push({path:'/social',});
    },
    sub(){
        if(this.password === this.password_again)
        {
            let data ={
                username:this.user,
                password:this.password,
                mobile:this.mobile,
            }
            axios.post("/user/api/resetpw", data)
            .then(() => {
                this.$message({
                type:'success',
                message: '修改成功',
                })
                this.$router.push({path:'/person'});
            })
        }
        else{
            this.$message({
                type:'error',
                message: '两次密码输入不一致',
            })
        }
    },
  }
});
</script>

<style scoped>
#father{
    margin:200px 600px;
    text-align: center;
}
#ret_button{
  position:absolute;
  left:300px;
  top:170px;
  margin-bottom: 20px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}
</style>