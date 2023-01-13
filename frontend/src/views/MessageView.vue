<template>
    <div id="message">
          <el-upload
            class="avatar-uploader"
            action="http://127.0.0.1:5000/user/api/uploadavatar"
            :headers="{'Authorization': this.user.jwt}"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :on-error="handleAvatarError"
            :before-upload="beforeAvatarUpload"
            :disabled="changeText"
          >
            <img v-if="imageUrl" :src="imageUrl" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
        <span class="word">用户id:<input v-model="user.id" disabled style="width:200px;"/></span>
        <div style="margin: 20px 0px" />
        <span class="word">用户名:<input v-model="user.name" :disabled="changeText" style="width:200px"/></span>
        <div style="margin: 20px 0" />
        <span class="word">昵称:<input v-model="user.nickname" :disabled="changeText" style="width:200px;"/></span>
        <div style="margin: 20px 0" />
        <span class="word">电话:<input v-model="user.phone" :disabled="changeText" style="width:200px;"/></span>
        <div style="margin: 20px 0" />
        <span class="word">邮箱地址:<input v-model="user.email" :disabled="changeText" style="width:350px;"/></span>
        <div style="margin: 20px 0" />
        <span class="word">创建时间:<input v-model="user.created" disabled style="width:300px;"/></span>
        <div style="margin: 20px 0" />
        <span class="word">个性签名:<textarea v-model="user.signature" 
        :disabled="changeText" style="width:400px;vertical-align:top;" :rows="4" id="text"
        /></span>
        <div style="margin: 20px 0" />
        <el-button type="primary" class="button" @click="changeText = !changeText;changeData()">
        <p v-if="changeText">修改个人信息</p>
        <p v-if="!changeText">保存</p>
        </el-button>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios"

export default defineComponent({
  data(){
    return{
            changeText:true,
            user:{
                id: 0,
                name:'',
                nickname:'',
                phone:'',
                email:'',
                created: '',
                signature: '',
                jwt:'',
            },
            status: 0,
            msg: '',
            imageUrl: '',
    }
  },
  methods:{   
    // 修改用户信息
    async changeData(){
      if (this.changeText === false)
        return;
      await axios.post("/user/api/changeattr",{
        'username': this.user.name,
        'nickname': this.user.nickname,
        'mobile': this.user.phone,
        'address': this.user.email,
        'signature': this.user.signature
      }, {
        headers: {'Authorization': this.user.jwt},
      }).then((res) => {
        console.log(res);
        this.user.name = res.data.username;
        this.user.nickname = res.data.nickname;
        this.user.phone = res.data.mobile;
        this.user.email = res.data.address;
        this.user.signature = res.data.signature;
        this.status = res.status;
      }).catch((error) => {
        console.log(error)
        this.msg = error.response.data.message
        this.status = error.response.status
      })

      this.$root.getAvatar(this.user.id, this.user.jwt);
      if (this.status == 200)
        ElMessage({
          message: '修改成功',
          type: 'success'
        });  
        
      else
        ElMessage({
          message: this.msg,
          type: 'error',
        })
    },
    // 上传图片钩子
    beforeAvatarUpload(file) {
        // console.log(file)

        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
    },
    // 上传成功钩子
    handleAvatarSuccess(res, file) {
        // console.log(res)
        this.imageUrl = URL.createObjectURL(file.raw);
        console.log(this.imageUrl)
    },
    //失败钩子
    handleAvatarError(err) {
        console.log(err)
    },
    //下载头像
    async downloadAvatar(){
      await axios.get("/user/api/downloadavatar", {
        headers: {'Authorization': this.user.jwt},
        params: {'name': this.user.id.toString() + '.jpg'},
        responseType: "blob"
      }).then((res) => {
        // console.log(res)
        this.imageUrl = URL.createObjectURL(res.data)
      }).catch((err) => {
        console.log(err)
      })
    }
  },

  async mounted(){
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    this.$root.getAvatar(this.user.id, this.user.jwt);
    // console.log(this.user.jwt);
    await axios.get("/user/api/user", {
      headers: {'Authorization': this.user.jwt},
    }).then((res) => {
      console.log(res);
      this.user.id = res.data.id;
      this.user.name = res.data.username;
      this.user.nickname = res.data.nickname;
      this.user.phone = res.data.mobile;
      this.user.email = res.data.address;
      this.user.signature = res.data.signature;
      this.user.created = res.data.created;
    });
    
    await axios.get("/user/api/downloadavatar", {
      headers: {'Authorization': this.user.jwt},
      params: {'name': this.user.id.toString() + '.jpg'},
      responseType: "blob"
    }).then((res) => {
      // console.log(res)
      this.imageUrl = URL.createObjectURL(res.data)
    }).catch((err) => {
      console.log(err)
    })
    
  }
});
</script>

<style scoped>
#message{
    position:absolute;
    left:320px;
    top:160px;
    width:800px;
    height:550px;
    border:2px solid rgb(64,158,255);
    text-align:left;
    border-radius:4px;
}

.avatar-uploader {
  position: absolute;
  right: 50px;
  /* border: 1px dashed var(--el-border-color); */
  border-radius: 50%;
}

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
  border-radius: 50%;
}

.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.button{
    position:relative;
    left:300px;
    top:40px;
    width:200px;
    height:50px;
    font-size:20px;
}

.word{
    font-size:22px;
    position:relative;
    left:50px;
    top:30px;
    
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

#text{
  font-size:20px; 
  resize:none;
  background-color:#FFFFFF;
}

textarea:disabled{
  border:0;
}


</style>