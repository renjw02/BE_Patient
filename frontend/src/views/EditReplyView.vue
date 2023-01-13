<template>
  <div id="father">
    <el-button class="return" @click="ret"><el-icon><Back/></el-icon>返回上一页</el-button>
    <div id="markdown">
      <v-md-editor v-model="text" height="600px"
              left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | 
              link emoji image code | save">
      </v-md-editor>
    </div>
    <el-button type ="primary" @click="changereply">修改回复</el-button>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios"

export default defineComponent({
    name: 'EditReplyView',
    props: {
    },
    data(){
        return{
            imageUrl:'',
            text:'',
            postId:0,
            id:'',
            user:{
                jwt:'',
                id:0,
                nickname:'',
            },
            status:'',
            msg:'',
        }
    },
    methods:{
        ret(){
            this.$router.push({path:'/social/' + this.postId})
        },
        changereply(){
            this.$confirm('此操作将修改该帖子, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(async() => {
                await axios.post("/post/api/modify/"+this.postId.toString()+"/reply/"+this.id.toString(), {
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
            })
        }
    },
    async mounted(){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
        this.id = this.$route.params.id;
        await axios.get("/post/api/getreply", {
            headers: {'Authorization': this.user.jwt},
            params: {'reply_id': this.id},
        }).then((res) => {
            this.postId = res.data.post_id;
            this.text = res.data.content;
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
    },
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