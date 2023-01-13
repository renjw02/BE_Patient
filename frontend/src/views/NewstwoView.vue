<template>
    <div>
      <div id="father">
        <el-affix :offset="600" id="go" position:bottom>
        <el-button  type="primary" plain @click="backTop" circle><el-icon><Top /></el-icon></el-button>
        </el-affix>
          <h1 style="text-align:center">{{title}}</h1>
          <div id="con"></div>
          <div style="margin:100px 0"/>
      </div>
      <el-button id="ret_button" @click="ret"><el-icon><Back/></el-icon>点击返回</el-button>
      </div>
</template>

<script>
import { defineComponent } from 'vue';
import axios from "axios";

export default defineComponent({
  name: 'NewstwoView',
  props: {
  },
  data(){
    return{
      user:{
        jwt:'',
        id:'',
      },
      title:'',
      content:'<p>1</p>',
    }
  },
  methods:{
    ret(){
        this.$router.back();
    },
    backTop(){
      document.querySelector("#father").scrollIntoView(true);
    },
  },
  mounted() {
    if (localStorage.getItem('userId') && localStorage.getItem('jwt')){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
    }

    axios.get("/news/api/news/" + this.$route.params.id, {
      headers: {'Authorization': this.user.jwt},  
    }).then((res) =>{
      console.log(res);
      this.content = res.data.content;
      this.title = res.data.title;
      this.content += "<style scoped>body{width:100%;word-wrap: break-word;word-break: break-all;}</style>";
      document.querySelector('#con').innerHTML = this.content;
      // document.querySelector('#con').innerHTML = '<p>随后IBM进行了员工结构调整，用更低的工资雇用新员工，并且辞退老员工。2018年9月ProPubllica的一项调查显示，该公司涉嫌年龄歧视，解雇了大约20,000名40岁以上的员工，占当时美国国内裁员总数的60%左右。</p>'
    })
    
  }
});
</script>

<style scoped>
#ret_button{
  position:absolute;
  top:130px;
  left:20px;
  margin-bottom: 20px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
}

#father{
  position:absolute;
  top:150px;
  width: 1420px;
}

#con {
  position: relative;
  width: 80%;
  left: 13%;
  word-break: break-all;
  white-space: normal;
}

#go{
  position:absolute;
  right:5px;
}

#go .el-button {
  width: 50px;
  height: 50px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
}
</style>

