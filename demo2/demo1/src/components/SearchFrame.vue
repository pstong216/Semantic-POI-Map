<template>
  <!-- 搜索框 -->
  <div class="demo-input-suffix">
    <el-row>
      <el-input v-model="input1" class="w-50 m-2" placeholder="Type something">
        <template #prefix>
          <el-icon class="el-input__icon">
            <search />
          </el-icon>
        </template>
      </el-input>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
// 获取input的值
const input1 = ref('')

</script>
<style>
.demo-input-suffix {
  width: 40%;
  position: absolute;
  top: 15%;
  left: 30%;
  z-index: 1;
}
</style>
