<template>
  <div id="app">
    <div class="content">
      <BtnSample @mode-change="handleModeChange" @change-basemap="changeBasemap" @heat-map="selectHeatLayer"></BtnSample>
      <SearchFrame></SearchFrame>
      <POIList></POIList>
      <MeasureScore></MeasureScore>
      <MyEcharts></MyEcharts>
    </div>
    <!-- 使用条件渲染来保持只有一个 CesiumEnv 组件实例存在 -->
    <CesiumEnv v-if="showCesiumEnv" :basemap="basemap" :cesium-mode="cesiumMode" :heatmap="heatmap"></CesiumEnv>
  </div>
</template>



<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}

// .content {
//   position:absolute; 
//   z-index: 1; /* 设置层叠顺序高于Cesium图 */
//   top:0;
//   left: 0;
//   width: 100%;
//   height: 100%;
// }

// #cesiumContainer {
//   position: relative; 
//   top: 0;
//   left: 0;
//   width: 100%;
//   height: 100%;
//   z-index: 0; /* 设置层叠顺序为最低，确保其他组件在其上方 */

// }

// .cesium-container {
//   pointer-events: auto; /* 启用 Cesium 图中的鼠标事件 */
// }
</style>


<script lang="ts">
import { defineComponent } from 'vue';
import SearchFrame from './components/SearchFrame.vue';
import BtnSample from './components/BtnSample.vue';
import POIList from './components/POIList.vue';
import MeasureScore from './components/MeasureScore.vue';
import CesiumEnv from './components/CesiumEnv.vue';
import MyEcharts from './components/MyEcharts.vue'

export default defineComponent({
  name: 'App',
  components: {
    SearchFrame,
    BtnSample,
    POIList,
    MeasureScore,
    CesiumEnv,
    MyEcharts
  },
  data() {
    return {
      cesiumMode: '2D', // 默认地图模式为2D
      showCesiumEnv: true, // 控制是否显示 CesiumEnv 组件
      basemap: 'basemap1', // 默认底图为 basemap1
      heatmap: 'Base' // 默认热力图图层为 base
    };
  },
  methods: {
    handleModeChange(mode: string) {
      this.showCesiumEnv = false; // 隐藏旧的 CesiumEnv 组件实例
      setTimeout(() => {
        this.cesiumMode = mode; // 更新地图模式
        this.showCesiumEnv = true; // 显示新的 CesiumEnv 组件实例
      }, 0);
    },
    changeBasemap(basemap: string) {

      this.showCesiumEnv = false; // 隐藏旧的 CesiumEnv 组件实例
      setTimeout(() => {
        this.basemap = basemap; // 更新底图
        this.showCesiumEnv = true; // 显示新的 CesiumEnv 组件实例
      }, 0);
    },
    selectHeatLayer(heatmap: string) {
    this.showCesiumEnv = false; // 隐藏旧的 CesiumEnv 组件实例
    this.$nextTick(() => {
      this.heatmap = heatmap; // 更新热力图图层
      this.showCesiumEnv = true; // 显示新的 CesiumEnv 组件实例
    });
  }
  },
});
</script>