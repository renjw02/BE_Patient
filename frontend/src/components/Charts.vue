<template>
  <div class="echarts-box">
    <div id="myEcharts" :style="{ width: '900px', height: '300px' }"></div>
  </div>
</template>

<script>
import { defineComponent,} from 'vue';
import * as echarts from "echarts";
import axios from 'axios';

export default defineComponent({
    name: "pgChart",
    data(){
        return {
            jwt: "",
            fpg_list: [],
            p2hpg_list: []
            
        }
    },
    methods: {
        
    },
    async mounted(){
        this.jwt = localStorage.getItem('jwt');
        await axios.get("/pg/api/getpgall", {
            headers: {'Authorization': this.jwt},
        }).then((res) => {
            console.log(res);
            this.fpg_list = res.data.fpg_list
            this.p2hpg_list = res.data.p2hpg_list
        }).catch((error) => {
            console.log(error)
        })


        let chart = echarts.init(document.getElementById("myEcharts"), "light");
        // 把配置和数据放这里
        chart.setOption({
            title: {
                text: '血糖视图'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['餐前血糖fpg', '餐后两小时血糖p2hpg']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'time',
                boundaryGap: false,
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '餐前血糖fpg',
                    type: 'line',
                    label: {
                        show: true,
                    },
                    data: this.fpg_list
                },
                {
                    name: '餐后两小时血糖p2hpg',
                    type: 'line',
                    label: {
                        show: true,
                    },
                    data: this.p2hpg_list
                },
                {
                    name: 'p2hpg1',
                    type: 'line',
                    markLine : {
                        symbol:"none",               
                        label:{
                            position:"middle",         
                            formatter: "餐后2小时血糖低线"
                        },
                        data : [{
                            silent:false,             
                            lineStyle:{               
                                type:"solid",
                                width: '2',
                                color:"green"
                            },
                            yAxis: "5.0"     //警戒线在y轴的坐标
                        }]
                    }
                },
                {
                    name: 'p2hpg2',
                    type: 'line',
                    markLine : {
                        symbol:"none",               
                        label:{
                            position:"middle",         
                            formatter: "餐后2小时血糖高线"
                        },
                        data : [{
                            silent:false,             
                            lineStyle:{               
                                type:"solid",
                                width: '2',
                                color:"red"
                            },
                            yAxis: "8.9"     //警戒线在y轴的坐标
                        }]
                    }
                },
                {
                    name: 'fpg1',
                    type: 'line',
                    markLine : {
                        symbol:"none",               
                        label:{
                            position:"middle",         
                            formatter: "餐前血糖低线"
                        },
                        data : [{
                            silent:false,             
                            lineStyle:{               
                                type:"solid",
                                width: '2',
                                color:"green"
                            },
                            yAxis: "3.9"     //警戒线在y轴的坐标
                        }]
                    }
                },
                {
                    name: 'fpg2',
                    type: 'line',
                    markLine : {
                        symbol:"none",               
                        label:{
                            position:"middle",         
                            formatter: "餐前血糖高线"
                        },
                        data : [{
                            silent:false,             
                            lineStyle:{               
                                type:"solid",
                                width: '2',
                                color:"red"
                            },
                            yAxis: "7.2"     //警戒线在y轴的坐标
                        }]
                    }
                }
            ],
            dataZoom: [
                {
                type: 'inside'
                }
            ]
        });
        window.onresize = function() {
            //自适应大小
            chart.resize();
        };
        
        
    }
})
</script>


