<template>
    <div class="comment">
        <el-popover placement="bottom" :width="200" trigger="hover" >
                <p>用户ID:{{datas.userId}}</p>
                <p>用户名称:{{datas.nickname}}</p>
                <p>个性签名:{{this.signature}}</p>
                <template #reference>
                <img v-if="imageUrl" :src="imageUrl" style="width:100px;border-radius: 50%;height:100px;"/>
                <img v-else src="../assets/default_avatar.png" class="pic"/>
                </template>
        </el-popover>
        <div class="content">
            <h3 @dblclick="open =!open">{{datas.nickname}}</h3>
            <p class="time">{{datas.created}}</p>
            <div>
                <v-md-editor v-model="content" mode="preview">
                </v-md-editor>
            </div>
            <el-button type="primary" link @click="favor"><el-icon :size=20><Pointer /></el-icon>{{favor_num}}人点赞</el-button>
            <el-button link type="primary" @click="open =! open"><el-icon :size=20><ChatDotRound /></el-icon>回复</el-button>
            <el-button link type="primary" @click="accusation"><el-icon :size=20><WarningFilled /></el-icon>举报</el-button>
            <el-button link type="primary" :disabled="this.datas.userId != this.user.id" @click="edit"><el-icon :size=20><Edit /></el-icon>编辑</el-button>
            <el-button link type="primary" @click="del" :disabled="this.datas.userId != this.user.id"><el-icon :size=20><Delete /></el-icon>删除</el-button>
            <div style="margin: 10px 0" />
            <div v-if="open">
                <div v-for="(item,index) in replys" :key="item">
                    <CommentTwo :reply="item" :index="index" v-on:add="reply" v-on:fav="favor2" v-on:reload="update"/>
                </div>
                <div>
                    <div class="markdown">
                        <v-md-editor v-model="replyText" height="260px"
                                left-toolbar="undo redo clear | h bold italic strikethrough quote | ul ol table hr | 
                                link emoji image code | save">
                        </v-md-editor>
                        <div style="text-align:center;height:50px;">
                            <el-button style="margin-top:10px;" @click="send">发送</el-button>
                        </div>
                    </div>
                </div>
            </div>
            <div style="margin: 10px 0" />
        </div>
            <div style="margin: 20px 0" />
        </div>
</template>

<script>
import { defineComponent } from 'vue';
import axios from "axios"
import { ElMessage } from 'element-plus';
import CommentTwo from './CommentTwo.vue';

export default defineComponent({
    components: { CommentTwo },
    name: 'CommentVue',
    props:{
        datas:Object,
    },
    data(){
        return{
            user:{
                id: 0,
                jwt:'',
            },
            imageUrl:'',
            open:false,
            myfavor:false,
            favor_num:this.datas.favor_num,
            content:this.datas.content,
            replyText:'',
            replys:[],
            signature:'',
        }
    },
    methods:{
        update(){
            axios.get("/post/api/getreplylist", {
                    headers: {'Authorization': this.user.jwt},
                    params: {'reply_id': this.datas.id},
                }).then((res) => {
                    console.log(res);
                    this.replys = res.data.reply_list;
                }).catch((err) => {
                    ElMessage({
                        message: err,
                        type: 'error',
                    });
                })
        },
        reply(index){
            this.replyText += '@';
            this.replyText += this.replys[index].nickname;
            this.replyText += ' ';
        },
        send(){
            if(this.replyText === '')
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
            }).then(() => {
                axios.post("/post/api/reply/" + this.datas.postId,{
                replyId: this.datas.id,
                content: this.replyText,
                }, {
                headers: {'Authorization': this.user.jwt},
                }).then(() => {
                    ElMessage({
                    message: '操作成功',
                    type: 'success',
                    });
                    this.update();
                    this.replyText = '';
            }).catch(() => {
                this.$message({
                type: 'info',
                message: '已取消'
                });  
            })
            })
           
        },
        favor(){
            let num = 0;
            if(this.myfavor)
            {
                num = -1;
                this.favor_num -= 1;
            }
            else
            {
                num = 1;
                this.favor_num += 1;
            }
            this.myfavor = !this.myfavor;
            axios.post("/post/api/supportreply/" + this.datas.id.toString(),{
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
        favor2(data){
            this.replys[data.index].favor_num += data.num;
        },
        edit(){
            this.$router.push({path:'/editreply/' + this.datas.id,})
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
        del() {
            this.$confirm('你确定要删除此条回复吗？', '举报', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                dangerouslyUseHTMLString: true,
            }).then(() => {
                axios.post("/post/api/deletereply/"+this.datas.id.toString(), {}, {
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
    async mounted(){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        await axios.get("/user/api/downloadavatar", {
            headers: {'Authorization': this.user.jwt},
            params: {'name': this.datas.userId.toString() + '.jpg'},
            responseType: "blob"
        }).then((res) => {
            console.log(res)
            this.imageUrl = URL.createObjectURL(res.data)
        }).catch((err) => {
            console.log(err)
        })

        axios.get("/post/api/getreplylist", {
            headers: {'Authorization': this.user.jwt},
            params: {'reply_id': this.datas.id},
        }).then((res) => {
            console.log(res);
            this.replys = res.data.reply_list;
        }).catch((err) => {
            ElMessage({
                message: err,
                type: 'error',
            });
        })

        axios.get("/user/api/user/" + this.datas.userId.toString(), {
            headers: {'Authorization': this.user.jwt},
        }).then((res) => {
            console.log(res)
            this.signature = res.data.signature;
        }).catch((err) => {
            console.log(err)
        })
    }
});
</script>

<style scoped>
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

.markdown {
  width: 800px;
  border: solid;
}
</style>