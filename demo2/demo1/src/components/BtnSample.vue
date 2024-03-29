<template>
  <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
    <el-sub-menu index="1">
      <template #title>
        <el-icon size="20">
          <Grid />
        </el-icon>
        heatmap
      </template>
      <el-menu-item index="1-0" @click="selectHeatLayer('Base')">Base</el-menu-item>
      <el-menu-item index="1-1" @click="selectHeatLayer('Comfort')">Comfort</el-menu-item>
      <el-menu-item index="1-2" @click="selectHeatLayer('Convenience')">Convenience</el-menu-item>
      <el-menu-item index="1-3" @click="selectHeatLayer('Economic_Vitality')">Economic Vitality</el-menu-item>
      <el-menu-item index="1-4" @click="selectHeatLayer('Elder_Friendly')">Elder Friendly</el-menu-item>
      <el-menu-item index="1-5" @click="selectHeatLayer('Livability')">Livability</el-menu-item>
      <el-menu-item index="1-6" @click="selectHeatLayer('Mobility')">Mobility</el-menu-item>
      <el-menu-item index="1-7" @click="selectHeatLayer('Romance')">Romance</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="3">
      <template #title>
        <el-icon size="20">
          <Picture />
        </el-icon>basemap</template>
      <el-menu-item index="3-1" @click="changeBasemap('basemap1')">basemap1</el-menu-item>
      <el-menu-item index="3-2" @click="changeBasemap('basemap2')">basemap2</el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="4">
      <template #title>
        <el-icon size="20">
          <Switch />
        </el-icon>
        dimension
      </template>
      <el-menu-item index="4-1">2D</el-menu-item>
      <el-menu-item index="4-2">3D</el-menu-item>
    </el-sub-menu>
  </el-menu>
  <div class="h-6" />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import {
  Grid, Picture, Switch, DataLine
} from '@element-plus/icons-vue'

export default defineComponent({
  name: 'BtnSample',
  data() {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    handleSelect(key: string) {
      if (key === '4-1') {
        this.$emit('mode-change', '2D') // 触发事件，将地图模式设置为2D
      } else if (key === '4-2') {
        this.$emit('mode-change', '3D') // 触发事件，将地图模式设置为3D
      }
    },
    changeBasemap(basemap: string) {
      this.$emit('change-basemap', basemap); // 触发底图更换事件，传递底图标识符
    },
    selectHeatLayer(heatmap: string) {
      this.$emit('heat-map', heatmap)
    }
  }
})
</script>

<style>
.el-menu-demo {
  position: absolute;
  top: 0;
  height: 30px;
  z-index: 1;
}
</style>