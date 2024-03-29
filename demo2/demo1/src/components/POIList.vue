<template>
  <div class="frame">
    <!-- poi数据半径的选择 -->
    <div class="head" style="text-align:left">
      <a>Choose your circle</a>
    </div>
    <div class="tip">Please set the radius for the circle</div>
    <div class="resizable-circle">
      <div class="circle-dashed">
        <div class="icon">
          <el-icon size="20">
            <iconClass />
          </el-icon>
          <a>{{ time }}min</a>
        </div>
      </div>
    </div>
    <div class="slider-container">
      <el-slider v-model="slidervalue" :format-tooltip="formatTooltip" class="slider"></el-slider>
    </div>
    <div class="description" style="padding-top:40px;line-height:25px;">
      <span>Radius:</span>
      <label>{{ (slidervalue / 10).toFixed(1) + "km" }}</label>
      <tr></tr>
      <span>Area:</span>
      <label>{{ (slidervalue / 10 * slidervalue / 10 * 3.14).toFixed(1) + "km²" }}</label>
      <tr></tr>
      This is a distance of {{ time }}-minutes of {{ trafficstyle }}
    </div>
    <el-divider />
    <el-divider style="top:30%;border-width:5px;" />
    <!-- poi数据的展示列表 -->
    <div class="show">
      <div style="
                   font-weight: bold; 
                    font-family: Arial, Helvetica, sans-serif; 
                    color: black;
                    text-align: left; 
                    font-size:20px;
                    margin-left:10px;
                    margin-top:20px">
        POI LIST</div>
      <div class="selection">
        <a>Category:</a>
        <el-select class="select" v-model="value" placeholder="Select" clearable>
          <el-option v-for="item in categorys" :key="item.value" :label="item.label" :value="item.value">
            <div style="height:20px;width:20px;float:left">
              <component :is="item.icon" size="10"> </component>
            </div>
            <a style="
                                color: var(--el-text-color-secondary);
                                font-size: 13px;
                              ">{{ item.label }}</a>
          </el-option>
        </el-select>
      </div>
      <div class="list">
        <el-card class="box-card" >
          <el-scrollbar height="350px" >
               <div id="totaldiv">
                <el-empty :image-size="200" />
               </div> 
          </el-scrollbar>

        </el-card>
      </div>
    </div>
  </div>
</template>
<script lang="ts" setup>
import {
  Bicycle, Van, Avatar
} from '@element-plus/icons-vue'

import { ref, computed,  watch } from 'vue'
import { useStore } from 'vuex'
import { debounce } from 'lodash';

// Vuex Store
const store = useStore();

// 滑块上显示数据
const slidervalue = ref(30)
slidervalue.value = store.state.radius / 10
const formatTooltip = (val: number) => {
  return val / 10 + "km"
}
//分钟的显示
const time = computed(() => {
  if (slidervalue.value < 20) {
    return slidervalue.value.toFixed(1);
  } else if (slidervalue.value < 40) {
    return (slidervalue.value / 2).toFixed(1);
  } else { return (slidervalue.value / 3).toFixed(1); }
});
//运动方式的显示
const trafficstyle = computed(() => {
  if (slidervalue.value < 20) {
    return "walk or jogging";
  } else if (slidervalue.value < 40) {
    return "bike ride";
  } else { return "car drive"; }
});

const iconClass = computed(() => {
  if (slidervalue.value < 20) {
    return Avatar;
  } else if (slidervalue.value < 40) {
    return Bicycle;
  } else { return Van; }
});

//下拉列表的内容 暂列五类
const value = ref('')
const categorys = [
  {
    value: 'all',
    label: 'all',
    icon: "Grid"
  },
  {
    value: '餐饮服务',
    label: 'food&catering',
    icon: "KnifeFork"
  },
  {
    value: '风景名胜',
    label: 'attractions',
    icon: "Sunrise"
  },
  {
    value: '公共设施',
    label: 'public infrastructure',
    icon: "place"
  },
  {
    value: '购物服务',
    label: 'retail&shopping',
    icon: "ShoppingCartFull"
  },
  {
    value: '交通设施服务',
    label: 'traffic',
    icon: "Ship"
  },
  {
    value: '金融保险服务',
    label: 'Financial&insurance services',
    icon: "CreditCard"
  },
  {
    value: '科教文化服务',
    label: 'Education',
    icon: "Notebook"
  },
  {
    value: '生活服务',
    label: 'life services',
    icon: "Film"
  },
  {
    value: '体育休闲服务',
    label: 'sports',
    icon: "Basketball"

  },
  {
    value: '医疗保健服务',
    label: 'healthcare',
    icon: "NoSmoking"
  },
  {
    value: '政府机构及社会团体',
    label: 'government&civil society',
    icon: "OfficeBuilding"
  },
  {
    value: '住宿服务',
    label: 'residential',
    icon: "Key"
  },

]

// 监听 geoJsonData 的变化
// watchEffect(() => {
//   const geoJsonData = store.state.geoJsonData;
//   // 在这里根据新的 geoJsonData 值执行操作
//   if(geoJsonData){
//     console.log(geoJsonData.poiData)
//   }
// });


const debouncedFetch = debounce((newSliderValue) => {
  // 计算新的半径
  const radius = newSliderValue * 10;

  store.commit('setRadius', radius)

}, 300); // 300 ms 的防抖时间

watch(slidervalue, debouncedFetch);

watch(value, (newValue) => {
  //console.log(newValue)
  if (newValue) {  // 判断新值是否存在
    store.commit('setHeadclass', newValue)
  }
})

watch(
  () => store.state.geoJsonData,
  (newGeoJsonData, oldGeoJsonData) => {
    // 当 geoJsonData 变化时，这个函数将会被执行
    // newGeoJsonData 是 geoJsonData 的新值
    // oldGeoJsonData 是 geoJsonData 的旧值
let myDiv = document.getElementById('totaldiv')
while (myDiv&&myDiv.firstChild) {
  myDiv.removeChild(myDiv.firstChild)
}

    if (newGeoJsonData && newGeoJsonData.poiData
    ) {
      // var names = { "names": [] };
      for (let i = 0; i < newGeoJsonData.poiData.features.length && newGeoJsonData.poiData.features[i].properties.name != null; i++) {
        // console.log(newGeoJsonData.poiData.features[i].properties.name);
        let newli = document.createElement('li');
        let newa = document.createElement('h');
        let newh = document.createElement('h');
        newh.setAttribute("style","font-weight:bold;font-color:black;font-size:large;");
        newa.setAttribute("style","color:grey;font-size:small;");
        newa.innerHTML=newGeoJsonData.poiData.features[i].properties.name;
        if(newGeoJsonData.poiData.features[i].properties.head_class=="餐饮服务")
        {
          newh.innerHTML="food&catering";
          newli.setAttribute("style","color:red;font-size: 30px;float:left;margin-right:30px;");
        }
       else if(newGeoJsonData.poiData.features[i].properties.head_class=="风景名胜")
        {
          newh.innerHTML="attractions";
          newli.setAttribute("style","color:green;font-size: 30px;float:left;margin-right:30px;");
        }

        else if(newGeoJsonData.poiData.features[i].properties.head_class=="公共设施")
        {
          newh.innerHTML="public infrastructure";
          newli.setAttribute("style","color:blue;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="购物服务")
        {
          newh.innerHTML="retail&shopping";
          newli.setAttribute("style","color:yellow;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="交通设施服务")
        {
          newh.innerHTML="traffic";
          newli.setAttribute("style","color:orange;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="金融保险服务")
        {
          newh.innerHTML="Financial&insurance services";
          newli.setAttribute("style","color:purple;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="住宿服务")
        {
          newh.innerHTML="residential";
          newli.setAttribute("style","color:gold;font-size: 30px;float:left;margin-right:30px;");
        }else if(newGeoJsonData.poiData.features[i].properties.head_class=="生活服务")
        {
          newh.innerHTML="life services";
          newli.setAttribute("style","color:turquoise;font-size: 30px;float:left;margin-right:30px;");
        }else if(newGeoJsonData.poiData.features[i].properties.head_class=="体育休闲服务")
        {
          newh.innerHTML="sports";
          newli.setAttribute("style","color:pink;font-size: 30px;float:left;margin-right:30px;");
        }else if(newGeoJsonData.poiData.features[i].properties.head_class=="医疗保健服务")
        {
          newh.innerHTML="healthcare";
          newli.setAttribute("style","color:aqua;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="政府机构及社会团体")
        {
          newh.innerHTML="government&civil society";
          newli.setAttribute("style","color:darkgoldenrod;font-size: 30px;float:left;margin-right:30px;");
        }
        else if(newGeoJsonData.poiData.features[i].properties.head_class=="科教文化服务")
        {
          newh.innerHTML="education";
          newli.setAttribute("style","color:lime;font-size: 30px;float:left;margin-right:30px;text-align: center;");
          
        }
 


        
        const divtotal=document.getElementById("totaldiv")
        
        if(divtotal){
          divtotal.setAttribute("style","float:left");
          divtotal.appendChild(newli)
          divtotal.appendChild(newh)
          divtotal.appendChild(document.createElement('br'))
          divtotal.appendChild(newa)
          divtotal.appendChild(document.createElement('br'))
        } 
        
      }

           
    } else {
      console.log('not found');
    }
  },
  { immediate: true } // 配置 immediate 为 true 会立即以表达式的当前值触发回调
);

</script>
<style scoped>
/* 整个大框架面板*/
.frame {
  top: 4%;
  height: 96%;
  width: 22%;
  background-color: hsl(0, 0%, 94%);
  position: absolute;
  right: 0px;
  margin: 0px;
  z-index: 1;
}

/* 图标的设置 */
.icon {
  position: absolute;
  top: 42%;
  left: 16%;
  font-weight: bold;
  font-size: 130%;
  display: flex;
  flex-direction: row;

}

.selection a {
  font-family: Arial, Helvetica, sans-serif;
  color: grey;
  text-align: left;
}

.head a {
  font-weight: bold;
  font-family: Arial, Helvetica, sans-serif;
  color: black;
  text-align: left;
  font-size: 150%;
  margin-left: 2%;
  margin-top: 4%;
}

a {
  word-wrap: break-word;
}


/* 运动的描述,包括显示的radius和area等 */
.description {
  text-align: left;
  position: absolute;
  top: 10%;
  left: 50%;

}

/* 虚线圆和中心的xxmin和图标 */
.resizable-circle {
  position: absolute;
  top: 4%;
  left: 4%;
  height: 15%;
  width: 37%;
}

/* 虚线圆 */
.circle-dashed {
  position: absolute;
  top: 50%;
  left: 0%;
  height: 100%;
  width: 100%;
  border-radius: 50%;
  border-style: dashed;
  border-width: 5px;
}

/* 滑块 */
.slider {
  border-radius: 5px;
  outline: none;
  opacity: 0.7;
  -webkit-transition: 0.2s;
  transition: opacity .2s;
  --el-slider-main-bg-color: black;
  --el-slider-runway-bg-color: white;
  --el-slider-border-radius: 3px;
  --el-slider-height: 6px;
}

.slider-container .slider {
  margin-top: 0;
  margin-left: 12px;
}

.slider-container {
  display: flex;
  align-items: center;
  position: absolute;
  top: 30%;
  left: 2%;
  width: 96%;
  font-size: 14px;
  color: var(--el-text-color-secondary);
  line-height: 44px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}



.item {
  margin-bottom: 18px;
}

.box-card {
  width: 100%;
}

.demo-pagination-block+.demo-pagination-block {
  margin-top: 10px;
  position: absolute;
  margin-left: 0px;
}

.demo-pagination-block {
  margin-bottom: 16px;
}

.show {
  position: absolute;
  top: 40%;
  left: 0%;
  height: 60%;
  width: 100%;
}

.selection {
  margin-top: 20px;
}

.list {
  height: 60%;
  width: 90%;
  position: absolute;
  top: 20%;
  left: 5%;
}

.tip {
  text-align: left;
  font-size: medium;
  margin: 2%;
}

.select {
  width: 72%
}
.scrollbar-demo-item {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  margin: 10px;
  text-align: center;
  border-radius: 4px;
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

</style>



