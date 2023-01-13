<template>
    <div id="dad">
        <el-container @click="jmp">
            <el-aside>
                <el-popover placement="bottom" :width="200" trigger="hover" >
                <p>用户ID:{{poster.id}}</p>
                <p>用户名称:{{poster.nickname}}</p>
                <p>个性签名:{{poster.signature}}</p>
                <template #reference>
                    <img v-if="imageUrl" :src="imageUrl">
                    <img v-else src="../assets/default_avatar.png"> 
                </template>
                </el-popover>
            </el-aside>
            <el-main>
                <!-- <p class="content">{{content}}</p> -->
                <div class="content">
                    {{this.content}}
                </div>
                <div class="title">
                <h1 class="text">{{title}}</h1>
                </div>
            </el-main>
        </el-container>
        <div id="button">
            <el-button link type="primary" class="btn" @click="jmp"><el-icon :size=20 class="el-icon--right"><ChatDotRound/></el-icon>评论</el-button>
            <el-button link type="primary" class="btn" @click="favor"><el-icon :size=20 class="el-icon--right"><Pointer /></el-icon>{{supportNum}}人点赞</el-button>
            <el-button link type="primary" class="btn" @click="star"><el-icon :size=20 class="el-icon--right">
                <Star v-if="myStar === false"></Star>
                <StarFilled v-else></StarFilled>
            </el-icon>收藏</el-button>
            <el-button link type="primary" class="btn" @click="accusation"><el-icon :size=20 class="el-icon--right"><WarningFilled /></el-icon>举报</el-button>
            <el-button link type="primary" class="btn" :disabled="this.user_id != this.user.id" @click="edit"><el-icon :size=20 class="el-icon--right"><Edit /></el-icon>编辑</el-button>
            <el-button link type="primary" class="btn" :disabled="this.user_id != this.user.id" @click="del"><el-icon :size=20 class="el-icon--right"><Delete /></el-icon>删除</el-button>
        </div>
    </div>
</template>

<script>
import { defineComponent } from 'vue'
import axios from "axios"


export default defineComponent({
    name: "postPage",
    props:{
        title:String,
        content:String,
        id:Number,
        support_num: Number,
        user_id: Number,
    },  
    data() {
        return {
            supportNum: 0,
            myFavor: false,
            myStar: false,
            user: {
                id: 0,
                jwt: '',
            },
            imageUrl: '',
            poster: {
                id:'',
                nickname:'',
                created:'',
                signature:'',
            },
            favorite: {
                id: 0,
            }
        }
    },
    methods: {
        async favor() {
            if (this.myFavor)
            {
                this.supportNum -= 1;
                this.myFavor = false;
                await axios.post("/post/api/supportpost/" + this.$props.id.toString(), {
                    'type': -1
                }, {
                    headers: {'Authorization': this.user.jwt},
                }).then((res) => {
                    console.log(res);
                }).catch((err) => {
                    console.log(err)
                })
            }
            else 
            {
                this.supportNum += 1;
                this.myFavor = true;
                await axios.post("/post/api/supportpost/" + this.$props.id.toString(), {
                    'type': 1
                }, {
                    headers: {'Authorization': this.user.jwt},
                }).then((res) => {
                    console.log(res);
                }).catch((err) => {
                    console.log(err)
                })
            }
        },
        async star() {
            // 取消收藏
            if (this.myStar) {
                this.myStar = false;

                await axios.get("/favorite/api/deletefavor", {
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

                await axios.post("/favorite/api/createfavor", {
                    'post_id': this.$props.id,
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
        accusation() {
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
        }, 
        jmp(){
            this.$router.push({path:'/Social/' + this.id})
        },
        edit() {
            this.$router.push({path:'/edit/' + this.id,})
        },
        del() {
            this.$confirm('你确定要删除此帖吗？', '删除', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                dangerouslyUseHTMLString: true,
            }).then(() => { 
                axios.post("/post/api/deletepost/"+this.$props.id.toString(), {}, {
                    headers: {'Authorization': this.user.jwt},
                }).then((res) => {
                    console.log(res);
                    this.$emit('reload');
                }).catch((err) => {
                    console.log(err);
                })}).catch(() => {
                    this.$message({
                    type: 'info',
                    message: '已取消'
                    });  
            })
            
            
        }
    },

    mounted() {
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.supportNum = this.$props.support_num;

        axios.get("/user/api/downloadavatar", {
            headers: {'Authorization': this.user.jwt},
            params: {'name': this.$props.user_id.toString() + '.jpg'},
            responseType: "blob"
        }).then((res) => {
            console.log(res)
            this.imageUrl = URL.createObjectURL(res.data)
        }).catch((err) => {
            console.log(err)
        })

        axios.get("/user/api/user/" + this.$props.user_id.toString(), {
            headers: {'Authorization': this.user.jwt},
        }).then((res) => {
            console.log(res)
            this.poster.id = res.data.id;
            this.poster.nickname = res.data.nickname;
            this.poster.created = res.data.created;
            this.poster.signature = res.data.signature;
        }).catch((err) => {
            console.log(err)
        })

        axios.get("/favorite/api/checkfavor", {
            headers: {'Authorization': this.user.jwt},
            params: {'news_id':0,
                'post_id':this.$props.id},
        }).then((res) => {
            console.log(res)
            this.myStar = true;
            this.favorite.id = res.data.favorite_id;

        }).catch((err) => {
            console.log(err)
        })
    }
})
</script>

<style scoped>
* {
    margin: 0;
    padding: 0;
}
#dad {
    position: relative;
    height: 150px;
    border: 2px dashed lightblue;
    border-radius: 35px;
    width: 600px;
    /* left: 300px; */
    overflow: hidden;
    padding: 0 20px;
}

.el-container {
    position: relative;
    width: 600px;
    height: 110px;
    cursor: pointer;
}

.el-aside {
    height: 110px;
    width: 30%;
    overflow: hidden;
}

.el-aside img {
    height: 100px;
    width: 100px;
    border-radius: 50%;
}

.el-main {
    height: 110px;
    overflow: hidden;
}

.el-main .title{
    position: absolute;
    top: -80px;
    font-size: 2em;
    height: 10px;
    text-align: left;
}

.el-main .content{
    position: absolute;
    top: -35px;
    left: 165px;
    font-size: 1em;
    width: 400px;
    text-align: left;
    overflow: hidden;
    text-overflow:ellipsis;
}

#button {
    position: relative;
    width: 600px;
    height: 40px;
    display: flex;
    justify-content: space-around;
}

#button .btn {
    width: 100px;
}

.text{
    text-overflow:ellipsis;
    width:350px;
    height:200px;
    overflow:hidden;
}
</style>