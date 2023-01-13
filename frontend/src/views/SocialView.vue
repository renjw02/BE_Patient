<template>
  <el-container id="postPage">
    <el-header>
      <img src="../assets/postPic.webp" alt="" class="topicon">
    </el-header>
    <el-container>
      <el-main>
        <div id="select">
          <el-button type="info" plain @click="send"><el-icon><Position/></el-icon>发帖</el-button>
          <el-select placeholder="话题种类" size="large" v-model="post" @change="page">
            <el-option v-for="item in posts" :key="item.value" :label="item.label" :value="item.value"/> 
          </el-select>
          <el-select placeholder="排序方式" size="large" v-model="sort" @change="page">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>           
          </el-select>
          <div id="link">
            <postPage v-for="item in ListData" :key="item" class="post" :title="item.title" 
              :content="item.content" :id="item.id" :support_num="item.favor_num" :user_id="item.userId"
              v-on:reload="pageChange">
            </postPage>
          </div>
          <el-pagination id="page" :page-size="10" :pager-count="5" layout="prev, pager, next" 
          :total="totalNum" v-model:currentPage="pageNum" background @current-change="pageChange"/>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { defineComponent } from 'vue'
import axios from "axios"
import postPage from '@/components/Posts.vue'


export default defineComponent({
  name: "SocialView",
  components: {
    postPage
  },
  data() {
    return {
      totalNum: 0,
      pageNum:1,
      user: {
        id: 0,
        jwt: '',
      },
      post:false,
      sort:false,
      options:[
        {
          value:false,
          label:'按发布时间排序',
        },
        {
          value:true,
          label:'按回复时间排序',
        }
      ],
      posts:[
        {
          value:false,
          label:'查看全部',
        },
        {
          value:true,
          label:'仅本人发布',
        }
      ],
      ListData:[],
    }
  },
  methods:{
    send(){
      this.$router.push({path:'/send'});
    },
    // 翻页函数
    pageChange(){
      if(this.sort === false && this.post === false){
        axios.get("/post/api/getpostlist", {
          headers: {'Authorization': this.user.jwt},
          params: {
            page: this.pageNum,
            },   
        }).then((res)=>{
          console.log(res)
          this.ListData = res.data.posts;
          this.totalNum = res.data.total;
        }).catch((err)=>{
          console.log(err);
        })
      }
      else if(this.sort === false && this.post === true)
      {
        axios.get("/post/api/getpostlist", {
            headers: {'Authorization': this.user.jwt},
            params: {
              page: this.pageNum,
              userId: this.user.id,
              },   
          }).then((res)=>{
            console.log(res)
            this.ListData = res.data.posts;
            this.totalNum = res.data.total;
          }).catch((err)=>{
            console.log(err);
          })
      }
      else if(this.post === false){
        axios.get("/post/api/getpostlist", {
            headers: {'Authorization': this.user.jwt},
            params: {
              page: this.pageNum,
              orderByReply: true,
              },   
          }).then((res)=>{
            console.log(res)
            this.ListData = res.data.posts;
            this.totalNum = res.data.total;
          }).catch((err)=>{
            console.log(err);
          })
      }
      else{
        axios.get("/post/api/getpostlist", {
            headers: {'Authorization': this.user.jwt},
            params: {
              page: this.pageNum,
              orderByReply: true,
              userId: this.user.id,
              },   
          }).then((res)=>{
            console.log(res)
            this.ListData = res.data.posts;
            this.totalNum = res.data.total;
          }).catch((err)=>{
            console.log(err);
          })
      }
    },
    page(){
      this.pageChange();
    }
    
  },

  mounted() {
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    this.$root.getAvatar(this.user.id, this.user.jwt);
    this.pageChange();
  }
})
</script>


<style scoped>
#postPage{
    position: relative;
    top:120px;
    text-align: center;
}


#select{
    position:relative;
    width:100%;
    text-align:center;
}

.el-button {
  margin-right: 20px;
  padding: 19px;
  /* box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1) */
}

.el-header, .el-footer {
  color: #333;
  text-align: center;
  line-height: 60px;
  width: auto;
}

.topicon{
  height: 150px;
  width: auto;
}

.el-main {
  /* background-color: #D3DCE6; */
  color: #333;
  text-align: center;
  line-height: 200px;
}

#link {
  /* height: 200px; */
  position: relative;
  top: -60px;
}

.post {
  left: 28%;
}

#page{
  margin-left: 680px;  
}
</style>