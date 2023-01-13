<template>
  <div id="main">
        <div @click="jmp" id="head">
          <h3>{{title}}</h3>
          <div>
            {{time}}
          </div>
        </div>
    <div class="button">
      <el-button link type="primary" class="btn" @click="star" :disabled="!this.user.id"><el-icon :size=20 class="el-icon--right">
          <Star v-if="myStar === false"></Star>
          <StarFilled v-else></StarFilled>
      </el-icon>收藏</el-button>
      <el-button link type="primary" class="btn" @click="accusation">
        <el-icon :size=20 class="el-icon--right"><WarningFilled /></el-icon>举报</el-button>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import axios from "axios"

export default defineComponent({
  name: 'NewsVue',
  props: {
    msg:Number,
    title:String,
    time:String,
  },
  data(){
    return{
      user:{
        jwt:'',
        id:'',
      },
      text:'',
      myStar:false,
      favorite:{
        id:'',
      }
    }
  },
  methods:{
      jmp(){
        this.$router.push({path:'/news/' + this.msg,})
      },
      favor(){
        if(this.myFavor){
          this.supportNum--;
        }
        else{
          this.supportNum++;
        }
        this.myFavor = !this.myFavor;
      },
      star(){
        if (this.myStar) {
                this.myStar = false;

                axios.get("favorite/api/deletefavor", {
                    headers: {'Authorization': this.user.jwt},
                    params: {'favorite_id': this.favorite.id},
                }).then((res) => {
                    console.log(res);
                }).catch((err) => {
                    console.log(err)
                })
            }
            // 收藏
            else {
                this.myStar = true;

                axios.post("favorite/api/createfavor", {
                    'news_id': this.$props.msg,
                    'title': this.$props.title,
                }, {
                    headers: {'Authorization': this.user.jwt},
                }).then((res) => {
                    console.log(res);
                    this.favorite.id = res.data.favoriteId;
                    this.$message({
                        type: 'success',
                        message: '收藏成功！'
                        });
                }).catch((err) => {
                    console.log(err);
                    this.$message({
                        type: 'error',
                        message: err,
                        });
                })
            }
      },
      
      accusation(){
        this.$confirm('你确定要举报此条帖子吗？', '举报', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                dangerouslyUseHTMLString: true,
            }).then(() => {
                this.$message({
                type: 'success',
                message: '举报成功，系统将会尽快核实！'
                });
            }).catch(() => {
                this.$message({
                type: 'info',
                message: '已取消举报'
                });          
            })
      }
  },
  mounted(){
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    if(this.user.id){
      axios.get("favorite/api/checkfavor", {
            headers: {'Authorization': this.user.jwt},
            params: {'news_id':this.msg,
                'post_id':0},
        }).then((res) => {
            console.log(res)
            this.myStar = true;
            this.favorite.id = res.data.favorite_id;
        }).catch((err) => {
            console.log(err)
        })
    }
  },
  activated(){
    this.user.jwt = localStorage.getItem('jwt');
    this.user.id = localStorage.getItem('userId');
    if(this.user.id){
      axios.get("favorite/api/checkfavor", {
            headers: {'Authorization': this.user.jwt},
            params: {'news_id':this.msg,
                'post_id':0},
        }).then((res) => {
            console.log(res)
            this.myStar = true;
            this.favorite.id = res.data.favorite_id;
        }).catch((err) => {
            console.log(err)
        })
    }
    this.myStar = false;
  }
});
</script>

<style scoped>
#main{
  border: 2px dashed gainsboro;
  overflow: hidden;
  margin: 20px;
  padding: 0 20px;
  border-radius: 20px
}

#head{
  cursor: pointer;
}

h3{
  overflow: hidden;
  text-overflow: ellipsis;
}

</style>