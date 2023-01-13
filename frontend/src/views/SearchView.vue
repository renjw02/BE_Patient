<template>
    <div id="father">
        <h1>搜索 "{{this.$route.params.id}}",一共 {{page.total}} 条结果</h1>
        <el-button id="ret_button" @click="ret"><el-icon><Back/></el-icon>点击返回</el-button>
        <div v-for="item in newsList" :key="item">
          <NewsVue :msg="item.id" :title="item.title" :time="item.date"></NewsVue>
        </div>
        <el-pagination id="page" :page-size="10" :pager-count="5" layout="prev, pager, next" 
            :total="page.total" v-model:currentPage="page.num" background @current-change="pageChange"/>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import NewsVue from '@/components/News.vue';
import axios from 'axios';

export default defineComponent({
  name: 'SearchView',
  components:{
    NewsVue,
  },
  props: {
  },
  data(){
    return{
      user:{
        jwt:'',
        id:'',
      },
      page:{
        num:1,
        total:0,
      },
      newsList:[],
    }
  },
  methods:{
    ret(){
        this.$router.back();
    },
    pageChange(){
      axios.get("/news/api/getnewsbysearch", {
        headers: {'Authorization': this.user.jwt},
        params: {
          page:this.page.num,
          search_word:this.$route.params.id,
          },   
      }).then((res) => {
        console.log(res);
        this.newsList = res.data.news;
        this.page.total = res.data.total;
      })
    },
  },
  mounted() {
    if (localStorage.getItem('userId') && localStorage.getItem('jwt')){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
    }

    this.pageChange();
  }
});
</script>

<style scoped>
#ret_button{
    position:absolute;
    top:150px;
    left:20px;
    margin-bottom: 20px;
    padding: 20px;
}

#page{
    margin-left:120px;
}

#father{
    width:500px;
    margin:200px auto;
    text-align: center;
}
</style>
