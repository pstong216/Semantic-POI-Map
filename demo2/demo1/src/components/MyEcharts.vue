<!-- <template>
    <div ref="chartRef" style="width: 600px;height:400px; z-index:100;"></div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts';

const chartRef = ref(null);

onMounted(() => {
  if (chartRef.value) {
    const chartInstance = echarts.init(chartRef.value);

    const option = {
      title: {
          text: 'ECharts 示例'
      },
      tooltip: {},
      legend: {
          data:['销量']
      },
      xAxis: {
          data: ["衬衫","羊毛衫","雪纺衫","裤子","高跟鞋","袜子"]
      },
      yAxis: {},
      series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
      }]
    };

    chartInstance.setOption(option);
  }
});
</script>

<style scoped>
  
</style> -->
<template>
    <div style="position:absolute;;right:0px;top:0px; align-items: center;z-index: 100;">
      <el-popover placement="right" :width="700" trigger="click">
        <template #reference>
        <el-icon  size="30px"><Histogram /></el-icon>
          <el-button style="margin-right: 16px;z-index: 100;">bar charts</el-button>
        </template>
        <template #default>
          <div ref="chartRef1" style="width: 700px;height:600px;backgroundColor:white; z-index:100;"></div>
        </template>
      </el-popover>
      <el-popover placement="right" :width="700" trigger="click">
        <template #reference>
            <el-icon size="30px"><PieChart /></el-icon>
          <el-button style="margin-right: 16px;z-index: 100;">pie charts</el-button>
        </template>
        <template #default>
          <div ref="chartRef2" style="width: 700px;height:600px;backgroundColor:white; z-index:100;"></div>
        </template>
      </el-popover>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted, watch } from 'vue';
  import * as echarts from 'echarts';
  import { useStore } from 'vuex';
  
  const chartRef1 = ref(null);
  const chartRef2 = ref(null);
  const store = useStore(); 
  const option1 = ref(); // 声明为响应式的ref对象 
  const option2 = ref(); // 声明为响应式的ref对象 
  
  onMounted(() => {
    if (chartRef1.value) {
      const chartInstance1 = echarts.init(chartRef1.value);
  
      option1.value = {
        title: {
            text: 'POI COUNT',
            left: 'center', // 将图例水平居中
        },
        tooltip: {
        formatter: '{a}: {c}' // 显示柱的名称（类别）和数量
        },
        legend: {
            data:['food&catering','attractions','public infrastructure','retail&shopping','travel','Financial&insurance services','Education','life services','sports','healthcare','government&civil society','residential'],
            bottom: 0,
            left: 'center', // 将图例水平居中
            width: '60%', // 设置图例区域宽度 
        },
        xAxis: {
          type: 'category', // 设置为类别类型
          axisLabel: {
        show: false // 隐藏 x 轴标签
        },
            //data: ["food&catering","attractions","public infrastructure","retail&shopping","travel","Financial&insurance services","Education","life services","sports","healthcare","government&civil society","residential"]
        },
        yAxis: {},
        grid: {
      containLabel: true,
      bottom: '20%' // 调整图例与 x 轴之间的距离
      },
        series: [{
            name: 'food&catering',
            type: 'bar',
            data: [0],
        },{
            name: 'attractions',
            type: 'bar',
            data: [0]
        },{
            name: 'public infrastructure',
            type: 'bar',
            data: [0]
        },{
            name: 'retail&shopping',
            type: 'bar',
            data: [0]
        },{
            name: 'travel',
            type: 'bar',
            data: [0]
        },{
            name: 'Financial&insurance services',
            type: 'bar',
            data: [0]
        },{
            name: 'Education',
            type: 'bar',
            data: [0]
        },{
            name: 'life services',
            type: 'bar',
            data: [0]
        },{
            name: 'sports',
            type: 'bar',
            data: [0]
        },{
            name: 'healthcare',
            type: 'bar',
            data: [0]
        },{
            name: 'government&civil society',
            type: 'bar',
            data: [0]
        },{
            name: 'residential',
            type: 'bar',
            data: [0]
        },
  
      ]
      
      };
      
    
      chartInstance1.setOption(option1.value);
    }
    if (chartRef2.value) {
      const chartInstance2 = echarts.init(chartRef2.value);
  
      option2.value = {
    title: {
      text: 'POI COUNT',
      left: 'center',
    },
    tooltip: {
      formatter: '{a}: {c}' // 显示饼块的名称和数量
    },
    legend: {
      data: ['food&catering', 'attractions', 'public infrastructure', 'retail&shopping', 'travel', 'Financial&insurance services', 'Education', 'life services', 'sports', 'healthcare', 'government&civil society', 'residential'],
      bottom: 0,
      left: 'center',
      width: '60%',
    },
    series: [
      {
        name: 'COUNT',
        type: 'pie',
        radius: '50%', // 设置饼图半径
        center: ['50%', '45%'], // 设置饼图中心位置
        data: [
          { value: 0, name: 'food&catering' },
          { value: 0, name: 'attractions' },
          { value: 0, name: 'public infrastructure' },
          { value: 0, name: 'retail&shopping' },
          { value: 0, name: 'travel' },
          { value: 0, name: 'Financial&insurance services' },
          { value: 0, name: 'Education' },
          { value: 0, name: 'life services' },
          { value: 0, name: 'sports' },
          { value: 0, name: 'healthcare' },
          { value: 0, name: 'government&civil society' },
          { value: 0, name: 'residential' }
        ]
      }
    ]
  };   
      chartInstance2.setOption(option2.value);
    }
  });
  watch(
    () => store.state.geoJsonData,
    (newGeoJsonData, oldGeoJsonData) => {
      if (newGeoJsonData && newGeoJsonData.class_counts) {
        //console.log(newGeoJsonData.class_counts['交通设施服务']);
        if(option1.value){
          option1.value.series[0].data = [newGeoJsonData.class_counts['餐饮服务']]
          option1.value.series[1].data = [newGeoJsonData.class_counts['风景名胜']]
          option1.value.series[2].data = [newGeoJsonData.class_counts['公共设施']]
          option1.value.series[3].data = [newGeoJsonData.class_counts['购物服务']]
          option1.value.series[4].data = [newGeoJsonData.class_counts['交通设施服务']]
          option1.value.series[5].data = [newGeoJsonData.class_counts['金融保险服务']]
          option1.value.series[6].data = [newGeoJsonData.class_counts['科教文化服务']]
          option1.value.series[7].data = [newGeoJsonData.class_counts['生活服务']]
          option1.value.series[8].data = [newGeoJsonData.class_counts['体育休闲服务']]
          option1.value.series[9].data = [newGeoJsonData.class_counts['医疗保健服务']]
          option1.value.series[10].data = [newGeoJsonData.class_counts['政府机构及社会团体']]
          option1.value.series[11].data = [newGeoJsonData.class_counts['住宿服务']]
  
          //console.log(option.value)
          if(chartRef1.value){
          const chartInstance = echarts.init(chartRef1.value);
          chartInstance.setOption(option1.value);
          }
        }
        if(option2.value){
          option2.value.series[0].data[0].value = [newGeoJsonData.class_counts['餐饮服务']]
          option2.value.series[0].data[1].value = [newGeoJsonData.class_counts['风景名胜']]
          option2.value.series[0].data[2].value = [newGeoJsonData.class_counts['公共设施']]
          option2.value.series[0].data[3].value = [newGeoJsonData.class_counts['购物服务']]
          option2.value.series[0].data[4].value = [newGeoJsonData.class_counts['交通设施服务']]
          option2.value.series[0].data[5].value = [newGeoJsonData.class_counts['金融保险服务']]
          option2.value.series[0].data[6].value = [newGeoJsonData.class_counts['科教文化服务']]
          option2.value.series[0].data[7].value = [newGeoJsonData.class_counts['生活服务']]
          option2.value.series[0].data[8].value = [newGeoJsonData.class_counts['体育休闲服务']]
          option2.value.series[0].data[9].value = [newGeoJsonData.class_counts['医疗保健服务']]
          option2.value.series[0].data[10].value = [newGeoJsonData.class_counts['政府机构及社会团体']]
          option2.value.series[0].data[11].value = [newGeoJsonData.class_counts['住宿服务']]
  
          //console.log(option.value)
          if(chartRef2.value){
          const chartInstance = echarts.init(chartRef2.value);
          chartInstance.setOption(option2.value);
          }
        }
      }
      // newGeoJsonData 是 geoJsonData 的新值
      // oldGeoJsonData 是 geoJsonData 的旧值
    })
  
  </script>
  <style>

  </style>