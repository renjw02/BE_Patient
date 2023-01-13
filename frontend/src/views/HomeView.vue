<template>
  <div class="home">
    <!--<HelloWorld msg="Welcome to Your Vue.js + TypeScript App"/>-->
    <div style="text-align:center;">
        <el-carousel height="200px" style="width:800px;margin:0 auto;">
          <el-carousel-item v-for="item in 4" :key="item" @click="jmp(item)">
            <img :src="pic[item - 1]" style="width:800px;height:200px;"/>
          </el-carousel-item>
        </el-carousel>
    </div>
    <div id="link">
        <div v-for="item in newsList" :key="item">
          <NewsVue :msg="item.id" :title="item.title" :time="item.date"></NewsVue>
        </div>
    </div>
    <div style="text-align:center">
        <div style="height:40px;">相关的糖尿病网站:
        </div>
      <a href="https://bbs.tnbz.com/index.php" style="display:inline-block">甜蜜家园</a>
      <div style="display:inline-block;width:20px;" />
      <a href="http://www.tnbzy.com" style="display:inline-block">糖友网</a>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
//import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src
import NewsVue from '@/components/News.vue';
import axios from "axios";

export default defineComponent({
  name: 'HomeView',
  components: {
    NewsVue,
  },
  data(){
    return{
      user: {
        id: 0,
        jwt: '',
      },
      pic:[require("@/assets/pic1.png"),require("@/assets/pic2.png"),require("@/assets/pic3.png"),require("@/assets/pic4.png")],
      newsList:[],
      recommend:[],
    }
  },
  methods:{
    jmp(id){
      this.$router.push({path:'/news/' + id})
    }
  },
  mounted() {
    if (localStorage.getItem('userId') && localStorage.getItem('jwt')){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
    }

    axios.get("/news/api/getnewslist", {
      headers: {'Authorization': this.user.jwt},
      params: {
        page:1,
        },   
    }).then((res) => {
      console.log(res);
      this.newsList = res.data.news;
    })
  }
});
</script>

<style scoped>
.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 150px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100px;
  margin: 20px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

#link{
    width:500px;
    text-align: center;
    margin: 0 auto;
}

.home {
    position:absolute;
    top:120px;
    width:100%;
}

a {
  color: blue;
  text-decoration: none;
}
</style>

