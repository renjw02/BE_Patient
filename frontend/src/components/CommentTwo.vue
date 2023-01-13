<template>
    <div>
        <el-popover placement="bottom" :width="200" trigger="hover">
                <p>用户ID:{{reply.userId}}</p>
                <p>用户名称:{{reply.nickname}}</p>
                <p>个性签名：{{this.signature}}</p>
                <template #reference>
                <img v-if="imageUrl" :src="imageUrl" style="width:80px;border-radius: 50%;height:80px;"/>
                <img v-else src="../assets/default_avatar.png" style="width:60px;"/>
                </template>
        </el-popover>
        <div class="content2" >
            <h3 @dblclick="add">{{reply.nickname}}</h3>
            <p class="time">{{reply.created}}</p>
            <p>{{reply.content}}</p>
            <el-button type="primary" link @click="favor"><el-icon :size=20 class="el-icon--right"><Pointer /></el-icon>{{this.favor_num}}人点赞</el-button>
            <el-button link type="primary" @click="add"><el-icon :size=20><ChatDotRound /></el-icon>回复</el-button>
            <el-button link type="primary" @click="accusation"><el-icon :size=20 class="el-icon--right"><WarningFilled /></el-icon>举报</el-button>
            <el-button link type="primary" :disabled="this.reply.userId != this.user.id" @click="edit"><el-icon :size=20><Edit /></el-icon>编辑</el-button>
            <el-button link type="primary" @click="del" :disabled="this.reply.userId != this.user.id"><el-icon :size=20 class="el-icon--right"><Delete /></el-icon>删除</el-button>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue';
import { ElMessage } from 'element-plus';
import axios from "axios"

export default defineComponent({
  name: 'CommentTwo',
  props: {
    reply:Object,
    index:Number,
  },
  data(){
    return{
      imageUrl:'',
      myfavor:false,
      favor_num:this.reply.favor_num,
      user:{
        id: 0,
        jwt:'',
      },
      signature:'',
    }
  },
  methods:{
    add(){
      this.$emit('add',this.index);
    },
    edit(){
        this.$router.push({path:'/editreply/' + this.reply.id,})
    },
    favor(){
            let num = 0;
            if(this.myfavor)
                num = -1;
            else
                num = 1;
            this.favor_num += num;
                let data ={
                  num: num,
                  index:this.index,
                }
            this.$emit('fav',data);
            this.myfavor = !this.myfavor;
            axios.post("/post/api/supportreply/" + this.reply.id.toString(),{
            type:num,
            }, {
            headers: {'Authorization': this.user.jwt},
            }).then(() => {
                ElMessage({
                message: '操作成功',
                type: 'success',
            });
            })
    },
    accusation() {
        this.$confirm('你确定要举报此条回复吗？', '举报', {
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
    }, 
    del(){
      this.$confirm('你确定要删除此条回复吗？', '举报', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                dangerouslyUseHTMLString: true,
            }).then(() => {
                axios.post("/post/api/deletereply/"+this.reply.id.toString(), {}, {
                    headers: {'Authorization': this.user.jwt},
                }).then((res) => {
                    console.log(res);
                    this.$emit('reload');
                }).catch((err) => {
                    console.log(err);
                })
            }).catch(() => {
                this.$message({
                type: 'info',
                message: '已取消'
                });  
            })
    }
  },
   mounted(){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');

        axios.get("/user/api/downloadavatar", {
            headers: {'Authorization': this.user.jwt},
            params: {'name': this.reply.userId.toString() + '.jpg'},
            responseType: "blob"
        }).then((res) => {
            console.log(res)
            this.imageUrl = URL.createObjectURL(res.data)
        }).catch((err) => {
            console.log(err)
        })

        axios.get("/user/api/user/" + this.reply.userId.toString(), {
            headers: {'Authorization': this.user.jwt},
        }).then((res) => {
            console.log(res)
            this.signature = res.data.signature;
        }).catch((err) => {
            console.log(err)
        })
        
    },
});
</script>

<style scoped>
.content2{
  position:relative;
  left:10px;
  top:-15px;
  display:inline-block;
  vertical-align:top;
  width: 700px;
  border-bottom: 2px solid rgba(0,0,0,0.2);
}

.time{
  font-size:10px;
  margin-top: -15px;
}
</style>
