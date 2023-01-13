<template >
    <div id="father">
    <el-affix :offset="600" id="go" position:bottom>
        <el-button  type="primary" plain @click="backTop" circle><el-icon><Top /></el-icon></el-button>
    </el-affix>
     <el-table class='recommend' :header-cell-style="{'text-align':'center', 'font-size':'20px'}" :data="weekRecipe" :cell-style="{height:'150px',}">
        <el-table-column :label=dateLabel >
            <el-table-column label="早餐推荐" >
                <template #default="scope">
                     <span class="menu">{{ scope.row.breakfast[this.date] }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="lunch" label="中餐推荐" >
                <template #default="scope">
                     <span class="menu">{{ scope.row.lunch[this.date] }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="dinner" label="晚餐推荐" >
                <template #default="scope">
                     <span class="menu">{{ scope.row.dinner[this.date] }}</span>
                </template>
            </el-table-column>
        </el-table-column>
     </el-table>
     <el-table style="width: 90%"
     stripe border :data="tableData" class="recipe" :cell-style="{height:'150px',}">
            <el-table-column prop="food1" label="食物">
            <template v-slot="scope">
                <img :src="scope.row.food1" style="height:100px;width:100px;"/>
            </template>
            </el-table-column>
            <el-table-column prop="name1" label="名称"/>
            <el-table-column prop="gi1" label="GI">
            </el-table-column>
            <el-table-column prop="food2" label="食物">
            <template v-slot="scope">
                <img :src="scope.row.food2" style="height:100px;width:100px;"/>
            </template>
            </el-table-column>
            <el-table-column prop="name2" label="名称"/>
            <el-table-column prop="gi2" label="GI">
            </el-table-column>
     </el-table>
     </div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  data(){
    return{
        user: {
            id: 0,
            jwt: '',
        },
        date:'',
        dateLabel:'',
        weekRecipe:[{
            breakfast:['牛奶240ml，鸡蛋1个，馒头50克',
            '窝头1个(50克)，牛奶1杯(250毫升)，鸡蛋1个，凉拌豆芽1小蝶。',
            '全麦面包片(50克)，豆浆1杯(400毫升)，茶鸡蛋1个，凉拌苦瓜1小蝶。',
            '蔬菜包子1个(50克)，米粥1碗，鸡蛋1个，拌白菜心1小蝶。',
            '豆包1个(50)，荷叶绿豆粥1碗，鸡蛋1个，凉拌三丝1小蝶。',
            '牛奶燕麦粥(牛奶250毫升，燕麦25克)，鸡蛋羹(鸡蛋1个)，海米拌芹菜1小蝶。',
            '全麦小馒头1个(50克)，薏苡仁粥1碗，鸡蛋1个，拌莴笋丝1小蝶。'],
            lunch:['烙饼150克，酱牛肉80克，醋烹豆芽菜',
            '米饭一碗(100克)，雪菜豆腐，肉丝炒芹菜。',
            '烙饼2块(100块)，口蘑冬瓜，牛肉丝炒胡萝卜。',
            '荞麦面条1碗(100克)，西红柿炒鸡蛋，素鸡菠菜。',
            '玉米面馒头1个(100克)，炒鱿鱼卷芹菜，素烧茄子。',
            '荞麦大米饭1碗(100克)，青椒肉丝，香菇豆腐汤。',
            '茭白鳝丝面(含面条100克)，醋溜大白菜'],
            dinner:['米饭150克，肉末烧豆腐，蒜茸菠菜',
            '馒头1个(100克)，盐水大虾，鸡片炒油菜。',
            '米饭1碗(100克)，鸡汤豆腐小白菜，清炒虾仁黄瓜。',
            '紫米馒头1个(100克)，香菇菜心，沙锅小排骨。',
            '米饭1碗(100克)，葱花烧豆腐，椒油圆白菜。',
            '花卷1个(100克)，醋椒鱼，西红柿炒扁豆。',
            '葱油饼(含面粉100克)，芹菜香干，紫菜冬瓜汤。'],
        }],
        tableData:[
        {
            food1:require("@/assets/1.jpeg"),
            gi1:"35",
            name1:"面条",
            food2:require("@/assets/2.jpeg"),
            gi2:"46",
            name2:"米饭",
        },
        {
            food1:require("@/assets/3.jpeg"),
            gi1:"69.4",
            name1:"粥",
            food2:require("@/assets/4.jpeg"),
            gi2:"74.9",
            name2:"油条",
        },
        {
            food1:require("@/assets/5.jpeg"),
            gi1:"88.1",
            name1:"馒头",
            food2:require("@/assets/6.jpeg"),
            gi2:"55",
            name2:"燕麦",
        },
        {
            food1:require("@/assets/7.jpeg"),
            gi1:"55",
            name1:"玉米",
            food2:require("@/assets/8.jpeg"),
            gi2:"47.7",
            name2:"芋头",
        },
        {
            food1:require("@/assets/9.jpeg"),
            gi1:"51",
            name1:"山药",
            food2:require("@/assets/10.jpeg"),
            gi2:"62",
            name2:"马铃薯",
        },
        {
            food1:require("@/assets/11.jpeg"),
            gi1:"54",
            name1:"红薯",
            food2:require("@/assets/12.jpeg"),
            gi2:"49",
            name2:"巧克力",
        },
        {
            food1:require("@/assets/13.jpeg"),
            gi1:"73",
            name1:"蜂蜜",
            food2:require("@/assets/14.jpeg"),
            gi2:"80",
            name2:"软糖",
        },
        {
            food1:require("@/assets/15.jpeg"),
            gi1:"83.8",
            name1:"绵砂糖",
            food2:require("@/assets/16.jpeg"),
            gi2:"105",
            name2:"麦芽糖",
        },
        {
            food1:require("@/assets/17.jpeg"),
            gi1:"14",
            name1:"黄豆",
            food2:require("@/assets/18.jpeg"),
            gi2:"14",
            name2:"花生",
        },
        {
            food1:require("@/assets/19.jpeg"),
            gi1:"16.9",
            name1:"蚕豆",
            food2:require("@/assets/20.jpeg"),
            gi2:"20",
            name2:"黑豆",
        },
        {
            food1:require("@/assets/21.jpeg"),
            gi1:"22",
            name1:"腰果",
            food2:require("@/assets/22.jpeg"),
            gi2:"23.7",
            name2:"豆腐干",
        },
        {
            food1:require("@/assets/23.jpeg"),
            gi1:"27",
            name1:"四季豆",
            food2:require("@/assets/24.jpeg"),
            gi2:"27.2",
            name2:"绿豆",
        },
        {
            food1:require("@/assets/25.jpeg"),
            gi1:"35",
            name1:"粉丝",
            food2:require("@/assets/26.jpeg"),
            gi2:"44",
            name2:"布丁",
        },
        {
            food1:require("@/assets/27.jpeg"),
            gi1:"47",
            name1:"龟苓膏",
            food2:require("@/assets/28.jpeg"),
            gi2:"50",
            name2:"春卷",
        },
        {
            food1:require("@/assets/29.jpeg"),
            gi1:"54",
            name1:"绿豆沙",
            food2:require("@/assets/30.jpeg"),
            gi2:"57",
            name2:"混合麦片",
        },
        {
            food1:require("@/assets/31.jpeg"),
            gi1:"60",
            name1:"披萨",
            food2:require("@/assets/32.jpeg"),
            gi2:"61",
            name2:"马来糕",
        },
        {
            food1:require("@/assets/33.jpeg"),
            gi1:"61",
            name1:"汉堡",
            food2:require("@/assets/34.jpeg"),
            gi2:"66",
            name2:"叉烧包",
        },
        {
            food1:require("@/assets/35.jpeg"),
            gi1:"69",
            name1:"粽子",
            food2:require("@/assets/36.jpeg"),
            gi2:"89",
            name2:"肠粉",
        },
        {
            food1:require("@/assets/37.jpeg"),
            gi1:"97",
            name1:"年糕",
            food2:require("@/assets/38.jpeg"),
            gi2:"32.6",
            name2:"藕粉",
        },
        {
            food1:require("@/assets/39.jpeg"),
            gi1:"41.1",
            name1:"莲子",
            food2:require("@/assets/40.jpeg"),
            gi2:"50.3",
            name2:"百合",
        },
        {
            food1:require("@/assets/41.jpeg"),
            gi1:"55",
            name1:"薏米",
            food2:require("@/assets/42.jpeg"),
            gi2:"34",
            name2:"面包",
        },
        {
            food1:require("@/assets/43.jpeg"),
            gi1:"56",
            name1:"月饼",
            food2:require("@/assets/44.jpeg"),
            gi2:"70",
            name2:"饼干",
        },
        {
            food1:require("@/assets/45.jpeg"),
            gi1:"90",
            name1:"蛋挞",
            food2:require("@/assets/46.jpeg"),
            gi2:"21",
            name2:"坚果",
        },
        {
            food1:require("@/assets/47.jpeg"),
            gi1:"36",
            name1:"苹果",
            food2:require("@/assets/48.jpeg"),
            gi2:"36",
            name2:"梨",
        },
        {
            food1:require("@/assets/49.jpeg"),
            gi1:"40",
            name1:"草莓",
            food2:require("@/assets/50.jpeg"),
            gi2:"43",
            name2:"葡萄",
        },
        {
            food1:require("@/assets/51.jpeg"),
            gi1:"43",
            name1:"橙子",
            food2:require("@/assets/52.jpeg"),
            gi2:"52",
            name2:"香蕉",
        },
        {
            food1:require("@/assets/53.jpeg"),
            gi1:"47",
            name1:"胡萝卜",
            food2:require("@/assets/54.jpeg"),
            gi2:"75",
            name2:"南瓜",
        },
        {
            food1:require("@/assets/55.jpeg"),
            gi1:"27.6",
            name1:"牛奶",
            food2:require("@/assets/56.jpeg"),
            gi2:"61",
            name2:"冰淇淋",
        },
        {
            food1:require("@/assets/57.jpeg"),
            gi1:"<15",
            name1:"芹菜",
            food2:require("@/assets/58.jpeg"),
            gi2:"<15",
            name2:"黄瓜",
        },
        {
            food1:require("@/assets/59.jpeg"),
            gi1:"<15",
            name1:"西红柿",
            food2:require("@/assets/60.jpeg"),
            gi2:"<15",
            name2:"菠菜",
        },
        ],
    }
  },
  methods:{
    backTop(){
      document.querySelector("#father").scrollIntoView(true);
    },
  },
  mounted(){
    if (localStorage.getItem('userId') && localStorage.getItem('jwt')){
        this.user.jwt = localStorage.getItem('jwt');
        this.user.id = localStorage.getItem('userId');
        this.$root.getAvatar(this.user.id, this.user.jwt);
    }

    let week = ['周日食谱','周一食谱','周二食谱','周三食谱','周四食谱','周五食谱','周六食谱'];
    this.date = new Date().getDay();
    this.dateLabel = week[this.date];
  },
});
</script>

<style scoped>
* {
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
}

.recipe{
    width:600px;
    margin:100px auto;
    font-size:20px;
}

.recommend {
    padding: 0;
    margin: -30px 0;
}

#father{
    position:absolute;
    top:150px;
    width:100%;
    padding: 0;
}

.menu{
    font-size:24px;
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