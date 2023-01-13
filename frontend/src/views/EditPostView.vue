<template>
  <div id="father">
    <el-button @click="ret" class="return"><el-icon><Back/></el-icon>返回上一页</el-button>
    <img v-if="imageUrl" :src="imageUrl" class="avatar">
    <img v-else src="../assets/default_avatar.png" class="avatar">
    <h1>发布者：{{user.nickname}}</h1>
    <p class="p1">Created: {{created}}</p>
    <p class="p2">Updated: {{updated}}</p>
    <el-input type="text" clearable placeholder="请输入标题" v-model="title" maxlength="30" show-word-limit></el-input>
    <div id="markdown">
      <v-md-editor v-model="text" height="600px"
              left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | 
              link emoji image code | save">
      </v-md-editor>
    </div>
    <el-button type ="primary" @click="modifiedPost">修改帖子</el-button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios"

export default defineComponent({
  name: 'EditPostView',
  props: {
  },
  data(){
    return{
      id: 0,
      text:'',
      title:'',
      created: '',
      updated: '',
      user: {
        id: 0,
        nickname: '',
        jwt: '',
      },
      imageUrl: '',
      msg: '',
      status: 0
    }
  },
  methods:{
    ret() {
      this.$router.push({path:'/social'})
    },
    // update post
    modifiedPost() {
      this.$confirm('此操作将修改该帖子, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {      
        await axios.post("/post/api/modifypost/"+this.id.toString(), {
          'title': this.title,
          'content': this.text,
        },{
          headers: {'Authorization': this.user.jwt},
        }).then((res) => {
          console.log(res);
          this.msg = res.data.message;
          this.status = res.status;
        }).catch((err) => {
          console.log(err)
        })

        if (this.status == 200) {
          this.$message({ 
            type: 'success',
            message: '修改成功!'
          });
          this.ret();
        }
        else {
          ElMessage({
            message: this.msg,
            type: 'error',
        })
        }
        
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消修改'
        });          
      })
    }    
  },
  async mounted() {
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    this.$root.getAvatar(this.user.id, this.user.jwt);
    this.id = this.$route.params.id;

    await axios.get("/post/api/getpost/"+this.id.toString(), {
      headers: {'Authorization': this.user.jwt},
    }).then((res) => {
      console.log(res);
      this.text = res.data.content;
      this.title = res.data.title;
      this.created = res.data.created;
      this.updated = res.data.updated;
      this.user.nickname = res.data.nickname;
      this.user.id = res.data.userId;
    }).catch((err) => {
      console.log(err);
    })

    axios.get("/user/api/downloadavatar", {
      headers: {'Authorization': this.user.jwt},
      params: {'name': this.user.id.toString() + '.jpg'},
      responseType: "blob"
    }).then((res) => {
      console.log(res)
      this.imageUrl = URL.createObjectURL(res.data)
    }).catch((err) => {
      console.log(err)
    })
  }
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}

#father {
    position: absolute;
    top:150px;
    left:16%;
    /* border: solid; */
}

#father .return {
  position: absolute;
  left: -180px;
}

#father .avatar {
  height: 100px;
  width: 100px;
  margin: 10px 0;
  border-radius: 50%;
}

#father h1 {
  position: absolute;
  left: 150px;
  top: 10px;
}

.p1 {
  position: absolute;
  left: 150px;
  top: 60px;
}

.p2 {
  position: absolute;
  left: 150px;
  top: 90px;
}

.el-button {
  margin-bottom: 20px;
  padding: 20px;
}

.el-input {
  margin-bottom: 20px;
  display: block;
  width: 100%;
}

#markdown {
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
}

</style>