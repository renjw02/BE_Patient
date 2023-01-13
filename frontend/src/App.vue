<template>
  <div id="father">
      <div id="head">
      <div id="top">
          <img alt="Vue logo" src="../src/assets/logo.png" id="title">
          <h1 id="word1">糖斗人</h1>
          <p id="word2">--糖尿病人互助网站</p>
          
      </div>
      <div id="bar">
          <nav>
            <router-link to="/">首页</router-link>
            <router-link to="/news">资讯</router-link>
            <router-link to="/social">社区</router-link>
            <router-link to="/person">个人</router-link>
            <router-link to="/food">食谱</router-link>
            <div id="search">
              <el-input v-model="input" placeholder="请输入内容" style="width: 200px"></el-input>
              <el-button type="primary" id="searchButton" @click="search"><el-icon><Search /></el-icon>搜索</el-button>
            </div>
            <router-link to="/message" id="photo">
              <img v-if="imageUrl" :src="imageUrl" class="avatar">
              <img v-else src="./assets/default_avatar.png" class="avatar">
            </router-link>
          </nav>
      </div>

          <!--<el-affix position="bottom" :offset="20" target="#head">
            <p>广告</p>
          </el-affix>-->
          <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component"  v-if="$route.meta.keepAlive"/>
            </keep-alive>
            <component :is="Component"  v-if="!$route.meta.keepAlive"/>
          </router-view>

      </div>

  </div>



</template>

<script>
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'HomeView',
  components: {
  },
  data(){
    return{
        search_input: '',
        state: 'out',
        user:{
                id:0,
                name:'',
                nickname:'',
                phone:'',
                email:'',
                jwt:'',
            },
        imageUrl: '',
        input:'',
    }
  },
  methods:{
    async getAvatar(id, jwt){
      await axios.get("/user/api/downloadavatar", {
          headers: {'Authorization': jwt},
          params: {'name': id.toString() + '.jpg'},
          responseType: "blob"
        }).then((res) => {
          console.log(res)
          this.imageUrl = URL.createObjectURL(res.data)
        }).catch((err) => {
          console.log(err)
        })
    },

    async search(){
      if(this.input === '')
      {
        this.$message({
          type: 'warning',
          message: '请输入关键词'
          });
      }
      else
      {
        
        await this.$router.push({path:'/search/' + this.input});
        window.location.reload();
      }
    },

    clearAvatar(){
      this.imageUrl = '';
    }
  },

  mounted(){
    // localStorage.clear();
    return;
  },

  // mounted() {
  //   // console.log(123)
  //   if (localStorage.getItem('userId') && localStorage.getItem('jwt'))
  //   {
  //     this.imageUrl = '';
  //     this.user.id = localStorage.getItem('userId');
  //     this.user.jwt = localStorage.getItem('jwt');
  //     console.log(this.user.id);
  //     console.log(this.user.jwt);
  //     // this.getAvatar(this.user.id, this.user.jwt);
  //     axios.get("/user/api/downloadavatar", {
  //         headers: {'Authorization': this.user.jwt},
  //         params: {'name': this.user.id.toString() + '.jpg'},
  //         responseType: "blob"
  //       }).then((res) => {
  //         console.log(res)
  //         // this.imageUrl = URL.createObjectURL(res.data)
  //       }).catch((err) => {
  //         console.log(err)
  //       })
  //   }
  // },
});
</script>

<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    font-size: 20px;
    padding:35px;
    color: #000000;
    text-decoration:none;

    &.router-link-exact-active:not(#photo) {
      background-color:#FFFFFF;
      color: #000000;
      border-radius:2px;
    }
  }
}

#title{
    position:absolute;
    left:50px;
    top:10px;
    width:100px;
    height:100px;
}

#head{
    white-space:nowrap;
    position:absolute;
    top:0px;
    left:0px;
    min-width:100%;
    width:1420px;
    height:120px;
    background-color:#409EFF;
}

#top{
    left:20px;
    top:20px;
    width:30%;
    color:#000000;
}

#bar{
    position:absolute;
    top:20px;
    left:380px;;
}

#search{
    position:absolute;
    left:600px;
    top:30px;
}

#searchButton{
    color:#000000;
    font-size:20px;
}

#photo{
    position:absolute;
    top:-30px;
    left:880px;
}

#word1{
    position:absolute;
    top:10px;
    left:180px;
}
#word2{
    position:absolute;
    top:60px;
    left:160px;
}
div {
    white-space:nowrap;
}

.avatar{
    position:absolute;
    left:50px;
    top:20px;
    width:100px;
    height:100px;
    border-radius: 50%;
}

</style>
