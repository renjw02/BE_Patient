<template>
    <div id="select" v-if="now===0">
         <el-select v-model="value"  placeholder="资讯种类" size="large" @change="pageChange">
            <el-option
              v-for="item in type"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
         <div id="link">
                <div v-for="item in newsList" :key="item">
                  <NewsVue :msg="item.id" :title="item.title" :time="item.date"></NewsVue>
                </div>
                <el-pagination id="page" :page-size="10" :pager-count="5" layout="prev, pager, next" 
                :total="page.total" v-model:currentPage="page.num" background @current-change="pageChange"/>
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
      page:{
        num:1,
        total:100,
      },
      user: {
        id: 0,
        jwt: '',
      },
        now:0,
        value:0,
        newsList:[],
        type:[
          {
            value:0,
            label:'全部'
          },
          {
            value:1,
            label:'鸡汤',
          },
          {
            value:2,
            label:'常识',
          },
          {
            value:3,
            label:'新闻',
          },
          {
            value:4,
            label:'用药',
          }
        ],
    }
  },
  methods:{
    pageChange(){
        axios.get("/news/api/getnewslist", {
        headers: {'Authorization': this.user.jwt},
        params: {
          page:this.page.num,
          keyword:this.value,
          },   
      }).then((res) => {
        console.log(res);
        this.newsList = res.data.news;
        this.page.total = res.data.total;
      })
    }
  },
  mounted(){
    if (localStorage.getItem('userId') && localStorage.getItem('jwt')){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
    }

    this.pageChange();
  },

});
</script>

<style scoped>
#select{
    position:absolute;
    top:120px;
    width:100%;
    text-align:center;
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

#page{
  margin-left:120px;
}
</style>