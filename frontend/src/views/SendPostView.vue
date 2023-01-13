<template>
  <div id="father"> 
    <el-button @click="ret"><el-icon><Back/></el-icon>返回上一页</el-button>
    <el-input type="text" clearable placeholder="请输入标题" v-model="title" maxlength="30" show-word-limit></el-input>
    <div id="markdown">
      <v-md-editor v-model="text" height="600px"
              left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | 
              link emoji image code | save">
      </v-md-editor>
    </div>
    <el-button type ="primary" @click="createPost">发帖</el-button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios"

export default defineComponent({
  name: 'SendPostView',
  props: {
  },
  data(){
    return{
      text:'',
      title:'',
      user: {
        id: 0,
        jwt: '',
      },
      imageUrl: '',
      msg: '',
      status: 0
  }
  },
  methods:{
    // 返回上一页
    ret() {
      this.$router.push({path:'/social'})
    },
    // 创建帖子
    createPost() {
      if (this.text.length == 0 || this.title.length == 0) {
        ElMessage({
            message: '标题或内容为空',
            type: 'error',
        })
        return;
      }
      this.$confirm('此操作将创建一个帖子, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {      
        await axios.post("/post/api/createpost", {
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
            message: '创建成功!'
          });
          this.ret();
        }
        else {
          ElMessage({
            message: '标题或内容为空',
            type: 'error',
          })
        }
        
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消创建'
        });          
      });
    },
      
  },
  mounted() {
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    this.$root.getAvatar(this.user.id, this.user.jwt);
  }
});
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

.el-button {
  margin-bottom: 20px;
  padding: 20px;
}

.el-input {
  margin-bottom: 20px;
  display: block;
}

#markdown {
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
}

</style>