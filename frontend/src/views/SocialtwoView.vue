<template>
    <div id="father">
      <el-button id="ret_button" @click="ret"><el-icon><Back/></el-icon>点击返回</el-button>
      <el-affix :offset="600" id="go" position: bottom>
        <el-button  type="primary" plain @click="backTop" circle><el-icon><Top /></el-icon></el-button>
        <div style="margin: 10px 0"></div>
        <el-button  type="primary" plain @click="comment" circle><el-icon><Bottom /></el-icon></el-button>
      </el-affix>
      <div id="head">
        <img v-if="imageUrl" :src="imageUrl" style="width:100px;border-radius: 50%;height:100px;"/>
        <img v-else src="../assets/default_avatar.png" />
        <div class="content">
        <h1>{{this.postData.title}}</h1>
        <p>发布者:{{this.postData.nickname}}</p>
        <p class="time">{{this.postData.created}}</p>
        <p>{{this.postData.favor_num}}人点赞</p>
        </div>
      </div>
      <div id="text">
        <div id="markdown">
          <v-md-editor v-model="postData.content" height="600px" mode="preview">
          </v-md-editor>
        </div>
      </div>
      <div id="comments">
        <p>以下是评论区</p>
        <div v-for="item in this.postData.reply" :key="item">
        <CommentVue v-on:reload="getPost" :datas="item" v-if="!item.replyId"/>
        </div>
        <div id="markdown2">
          <v-md-editor v-model="text" height="600px"
                  left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | 
                  link emoji image code | save">
          </v-md-editor>
          <div style="text-align:center;height:50px;">
          <el-button style="margin-top:10px;" @click="reply">发布</el-button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import CommentVue from '@/components/Comment.vue'
import axios from "axios"
import { ElMessage } from 'element-plus';

export default defineComponent({
  name: 'SocialtwoView',
  components:{
    CommentVue,
  },
  props: {
  },
  data(){
    return{
        id: 0,
        time:'2020-01-01',
        imageUrl:'',
        postData: {},
        user: {
          jwt: '',
          name:'user',
        },
        text:'',
        }
  },
  methods:{
    ret(){
        this.$router.back();//push({path:'/social',});
    },
    comment(){
      document.querySelector("#markdown2").scrollIntoView(true);
    },
    backTop(){
      document.querySelector("#father").scrollIntoView(true);
    },
    reply(){
      if(this.text === '')
      {
        this.$message({
                type: 'error',
                message: '内容不能为空'
                });  
        return;
      }
      this.$confirm('即将发布回复, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() =>{
        axios.post("/post/api/reply/" + this.postData.id, {
          'content': this.text,
        },{
          headers: {'Authorization': this.user.jwt},
        }).then(() => {
           ElMessage({
              message: '发布成功',
              type: 'success',
            });
           this.getPost();
           this.text = '';
        })
      }).catch(() => {
        this.$message({
                type: 'info',
                message: '已取消'
                });  
      })
      
    },
    getPost() {
      axios.get("/post/api/getpost/" + this.id.toString(), {
        headers: {'Authorization': this.user.jwt},
      }).then((res)=>{
        console.log(res)
        this.postData = res.data;
      }).catch((err)=>{
        console.log(err);
      })
    }
  },

  async mounted() {
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    this.$root.getAvatar(this.user.id, this.user.jwt);
    this.id = this.$route.params.id;

    await axios.get("/post/api/getpost/" + this.id.toString(), {
      headers: {'Authorization': this.user.jwt},
    }).then((res)=>{
      console.log(res)
      this.postData = res.data;
    }).catch((err)=>{
      console.log(err);
    })

    axios.get("/user/api/downloadavatar", {
            headers: {'Authorization': this.user.jwt},
            params: {'name': this.postData.userId.toString() + '.jpg'},
            responseType: "blob"
        }).then((res) => {
            console.log(res)
            this.imageUrl = URL.createObjectURL(res.data)
        }).catch((err) => {
            console.log(err)
        })


  }
});
</script>

<style scoped>
#father{
    position:absolute;
    top:150px;
    left:200px;
}

#markdown {
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
  border: solid;
}
#markdown2{
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
  border: solid;
}


#head{
  display: inline-block;
}

.content{
  position:relative;
  left:10px;
  top:-20px;
  display:inline-block;
  vertical-align:top;
  width: 800px;
  min-height: 160px;
  border-bottom: 2px solid rgba(0,0,0,0.5);
  white-space: pre;
}

.content2{
  position:relative;
  left:10px;
  top:-15px;
  display:inline-block;
  vertical-align:top;
  width: 700px;
  border-bottom: 2px solid rgba(0,0,0,0.2);
}

.pic{
  width:80px;
}

.time{
  font-size:10px;
  margin-top: -15px;
}

#comments{
  position:relative;
  top:100px;
}
#markdown {
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
  border: solid;
}

#ret_button{
  position:absolute;
  left:-170px;
  top:-20px;
  margin-bottom: 20px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}

#markdown {
  position: relative;
  margin-bottom: 20px;
  width: 1000px;
}

#go{
  position:absolute;
  right:-200px;
}

#go .el-button {
  width: 50px;
  height: 50px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>