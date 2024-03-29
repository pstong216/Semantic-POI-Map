<template>
  <div class="show2">
    <el-radio-group v-model="score" label="sizecontrol" size="large" text-color="white" fill="black">
      <el-radio-button v-model="score" label="1">relevance score</el-radio-button>
      <el-radio-button v-model="score" label="2">diversity score</el-radio-button>
    </el-radio-group>
    <!-- 空白页显示 -->
    <el-empty v-if="score == 0" description="description" />

    <div class="scorelist">
      <!-- measurescore类型选择 -->
      <div style="float:left; position:absolute;left:5%">
        <el-radio-group v-model="radio" v-if="score == 1" type="vertical">
          <div class="measure type" style="display: inline-flex;
        flex-direction: column;
        padding-top: 20%;
        align-items: flex-start;">
            <el-radio :label="0" value="Comfort">Comfort</el-radio>
            <el-radio :label="1" value="Convenience">Convenience</el-radio>
            <el-radio :label="2" value="Economic_Vitality">Economic Vitality</el-radio>
            <el-radio :label="3" value="Elder_Friendly">Elder Friendly</el-radio>
            <el-radio :label="4" value="Livability">Livability</el-radio>
            <el-radio :label="5" value="Mobility">Mobility</el-radio>
            <el-radio :label="6" value="Romance">Romance</el-radio>
          </div>
        </el-radio-group>
      </div>
      <!-- 色轮1 -->
      <div class="demo-progress1">
        <el-progress v-if="score == 1" type="dashboard" :percentage="selectedRelevanceScore" :color="colors" :stroke-width="20" >
          <template #default="{ percentage }">
        <span class="percentage-value">{{ percentage }}</span>
      </template>
        </el-progress>
      </div>
      <!-- 色轮2 -->
      <div class="demo-progress2">
        <el-progress v-if="score == 2" size="large" type="dashboard" :percentage="diversity_score" :color="colors" :stroke-width="20" >
          <template #default="{ percentage }">
        <span class="percentage-value">{{ percentage }}</span>
      </template>
        </el-progress>
      </div>
    </div>
    <!-- 文字描述 -->
    <div class="description">
      <div v-if="score == 1" style="position:absolute;
            top:35%;line-height:30px">&emsp;&emsp;This score indicates how the score for the urban performance measure is derived.</div>
      <div v-if="score == 2" style="position:absolute;line-height:40px;
            top:30%;">&emsp;&emsp;This score indicates the diversity of transportation site POIs in your selected circle
        range.<br>&emsp;&emsp;The higher the score is,the more mixed and diverse the POI categories are.
      </div>
    </div>
    <!-- diversity下的poidensity -->
    <div class="barshow" v-if="score == 1">
      <div style="text-align:left">POI DENSITY</div>
      <div v-for="item in poibar" :key="item.value" :label="item.label" :value="item.value" :color="item.color">
        <div style="
                                            float: left;
                                            color: var(--el-text-color-secondary);
                                            font-size: 13px;
                                          ">{{ item.label }}</div>
        <br>
        <el-progress :percentage="item.percentage * 5" :stroke-width="10" :color="item.color" :show-text="false" striped
          striped-flow />
      </div>
    </div>
    <!-- diversity下的count -->
    <div class="releshow2" v-if="score == 2">
      <div>COUNT</div>
      <div v-for="item in poibar" :key="item.value" :label="item.label" :value="item.value" :color="item.color"
        :count="item.count">
        <div style="
                                            float: left;
                                            color: var(--el-text-color-secondary);
                                            font-size: 13px;
                                          ">{{ item.label }}</div>
        <div style="
                                            float: right;
                                            color: var(--el-text-color-secondary);
                                            font-size: 13px;
                                          ">{{ item.count }}</div>
        <br>
        <el-progress :percentage="item.count * 2" :stroke-width="10" :color="item.color" :show-text="false" striped
          striped-flow />
      </div>
    </div>
    <!-- measurescore下的count -->
    <div class="releshow1" v-if="score == 1">
      <div>COUNT</div>
      <div v-for="item in poibar" :key="item.value" :label="item.label" :value="item.value" :color="item.color"
        :count="item.count">
        <div style="
                                            float: right;
                                            color: var(--el-text-color-secondary);
                                            font-size: 13px;
                                          ">{{ item.count }}</div>
        <br>
        <el-progress style="transform: rotateY(180deg);" :percentage="item.count" :stroke-width="10" :color="item.color"
          :show-text="false" striped striped-flow />
      </div>
    </div>
  </div>
</template>
  
<script lang="ts" setup>

import { ref, computed, watch, reactive } from 'vue'
import { useStore } from 'vuex'

const score = ref(0)
const radio = ref(0)
// const selectedValue = computed(() => {
//   if (score.value === 1) {
//     if (radio.value === 3) {
//       return 'Comfort';
//     } else if (radio.value === 6) {
//       return 'Convenience';
//     } else if (radio.value === 9) {
//       return 'Economic_Vitality';
//     } else if (radio.value === 12) {
//       return 'Elder_Friendliess';
//     } else if (radio.value === 15) {
//       return 'Livability';
//     } else if (radio.value === 18) {
//       return 'Mobility';
//     } else if (radio.value === 21) {
//       return 'Romance';
//     }
//   }
//   return null;
// })

// const percentage = ref(0)
const diversity_score = ref(0)
const selectedRelevanceScore = ref(0);
const colors = [
  { color: '#CCFFFF', percentage: 20 },
  { color: '#66B2FF', percentage: 40 },
  { color: '#0080ff', percentage: 60 },
  { color: '#004c99', percentage: 80 },
  { color: '#001933', percentage: 100 },
]
const poibar = reactive([
  {
    value: '餐饮服务',
    label: 'food&catering',
    color: 'RED',
    percentage: 0,
    count: 0,
  },
  {
    value: '风景名胜',
    label: 'attractions',
    color: 'GREEN',
    percentage: 0,
    count: 0,
  },
  {
    value: '公共设施',
    label: 'public infrastructure',
    color: 'BLUE',
    percentage: 0,
    count: 0,
  },
  {
    value: '购物服务',
    label: 'retail&shopping',
    color: 'YELLOW',
    percentage: 0,
    count: 0,
  },
  {
    value: '交通设施服务',
    label: 'travel',
    color: 'ORANGE',
    percentage: 0,
    count: 0,
  },
  {
    value: '金融保险服务',
    label: 'Financial&insurance services',
    color: 'PURPLE',
    percentage: 0,
    count: 0,
  },
  {
    value: '科教文化服务',
    label: 'Education',
    color: 'LIME',
    percentage: 0,
    count: 0,
  },
  {
    value: '生活服务',
    label: 'life services',
    color: 'TURQUOISE',
    percentage: 0,
    count: 0,
  },
  {
    value: '体育休闲服务',
    label: 'sports',
    color: 'PINK',
    percentage: 0,
    count: 0,
  },
  {
    value: '医疗保健服务',
    label: 'healthcare',
    color: 'AQUA',
    percentage: 0,
    count: 0,
  },
  {
    value: '政府机构及社会团体',
    label: 'government&civil society',
    color: 'darkgoldenrod',
    percentage: 0,
    count: 0,
  },
  {
    value: '住宿服务',
    label: 'residential',
    color: 'GOLD',
    percentage: 0,
    count: 0,
  }
]);
const relevanceScores = ref([
      { label: 0, value: 'Comfort', relevance_score: 0 },
      { label: 1, value: 'Convenience', relevance_score: 0 },
      { label: 2, value: 'Economic_Vitality', relevance_score: 0 },
      { label: 3, value: 'Elder_Friendly', relevance_score:0 },
      { label: 4, value: 'Livability', relevance_score: 0 },
      { label: 5, value: 'Mobility', relevance_score: 0 },
      { label: 6, value: 'Romance', relevance_score: 0 }
    ]);

// Vuex Store
const store = useStore();


watch(
  () => store.state.geoJsonData,
  (newGeoJsonData, oldGeoJsonData) => {
    if (newGeoJsonData && newGeoJsonData.class_counts && newGeoJsonData.totalNumber) {
      const geoData = newGeoJsonData.class_counts;
      const totalNumber = newGeoJsonData.totalNumber;
      // console.log(geoData);
      // console.log(totalNumber);
      poibar.forEach((item) => {
        if (geoData[item.value]) {
          item.count = geoData[item.value];
          // console.log(item.count)
          item.percentage = Math.round((geoData[item.value] / totalNumber) * 100);
        } else {
          item.count = 0;
          item.percentage = 0;
        }
      });
      if (newGeoJsonData.relevance_score) {
        const relevancescores = newGeoJsonData.relevance_score;
        relevancescores.forEach((score: number, index: number) => {
          if (relevancescores[index].relevance_score) {
            relevanceScores.value[index].relevance_score = relevancescores[index].relevance_score.toFixed(2);
          }
        });
        const selectedScore = relevanceScores.value.find((item: { label: number; }) => item.label === radio.value);
      if (selectedScore) {
        selectedRelevanceScore.value = selectedScore.relevance_score;
      }
        console.log(relevanceScores);
      }
      diversity_score.value = newGeoJsonData.diversity_score.toFixed(2);
      console.log(newGeoJsonData.relevance_score)
      // relevance_score.value = newGeoJsonData.relevance_score.toFixed(2);
      console.log(newGeoJsonData);
      watch(radio, (newValue) => {
      // 根据选中的值更新 selectedRelevanceScore
      const selectedScore = relevanceScores.value.find((item: { label: number; }) => item.label === newValue);
      if (selectedScore) {
        selectedRelevanceScore.value = selectedScore.relevance_score;
      }
    });
    }

    // 当 geoJsonData 变化时，这个函数将会被执行
    // newGeoJsonData 是 geoJsonData 的新值
    // oldGeoJsonData 是 geoJsonData 的旧值

  },
  { immediate: true } // 配置 immediate 为 true 会立即以表达式的当前值触发回调
);


</script>
<style scoped>
.demo-progress1 .el-progress--line {
  margin-bottom: 15px;
  width: 400px;
}

.demo-progress1 .el-progress--circle {
  margin-right: 15px;
}

.demo-progress1 {
  position: absolute;
  top: 15%;
  left: 55%;

}

.show2 {
  top: 4%;
  height: 96%;
  width: 22%;
  background-color: hsl(0, 0%, 94%);
  position: absolute;
  left: 0px;
  margin: 0px;
  z-index: 1;
}

el-radio-button {
  font-size: 16px;
  color: #333;
  background-color: #fff;
  border: 1px solid #ccc;
}

.barshow {
  width: 45%;
  height: 50%;
  position: absolute;
  top: 50%;
  left: 5%;
}

.releshow1 {
  text-align: right;
  width: 45%;
  height: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
}

.releshow2 {
  text-align: left;
  width: 90%;
  height: 50%;
  position: absolute;
  top: 50%;
  left: 5%;
}

::v-deep .el-radio {
  display: block;
  line-height: 23px;
  white-space: normal;
  margin-left: 0px;
}

.description {
  text-align: left;
  margin-left: 10px;
}

.demo-progress2 {
  position: absolute;
  top: 15%;
  left: 35%;
}

.measure type {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
}
</style>
  