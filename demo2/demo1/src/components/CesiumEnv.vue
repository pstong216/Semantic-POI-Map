<template>
    <div id="cesiumContainer"></div>
  </template>
  
  <script lang="ts">
  import { assertOptionalCallExpression } from '@babel/types';
import * as _ from 'lodash';
  import { defineComponent,  computed, watch, onMounted, ref, watchEffect } from 'vue';
  import { useStore } from 'vuex';
  
  export default defineComponent({

    props: {
      cesiumMode: {
        type: String,
        required: true,
      },
      basemap: {
      type: String,
      required: true,
    },
    heatmap: {
        type: String,
        required: true,
      },
      geoJsonPromise: null,
    },
    setup() {
    const store = useStore();  

    // 使用计算属性从 Vuex store 中获取 geoJsonData
    const geoJsonData = computed(() => store.state.geoJsonData?.poiData);


    // 监视 geoJsonData 的变化，当它变化时，将新的数据加载到视图中


    return {
      geoJsonData,
    };
  },
    mounted() {
      setTimeout(() => {
        const script = document.createElement('script');
        script.src = '/Cesium/Cesium.js';
        script.onload = this.initializeCesium;
        document.body.appendChild(script);
      }, 0);
      
      
    },
    
    data() {
  return {
    majorAxisIncrement: 0,
    minorAxisIncrement: 0,
    isDragging: false
  };
  },

    methods: {
      initializeCesium() {
        
        if (typeof window.Cesium === 'undefined') {
          console.error('Failed to load Cesium library.');
          return;
        }

  
        window.Cesium.Ion.defaultAccessToken =
          'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI1NzFkYmQ1Yy02ZGM0LTRlODAtYTdmMy00YjI3YzY2M2FiYjEiLCJpZCI6MTMxODA5LCJpYXQiOjE2ODA0OTIyMjN9.SBxcWeFQohgZ_qxFyF3MqIqxd9zU6WJ9OsuBpzVKvsE';
  
        const viewer = new window.Cesium.Viewer('cesiumContainer', {
          animation: false,
          baseLayerPicker: false,
          fullscreenButton: false,
          geocoder: false,
          homeButton: false,
          sceneModePicker: false,
          timeline: false,
          navigationHelpButton: false,
        });
  
        viewer._cesiumWidget._creditContainer.style.display = 'none';

        const provider = new window.Cesium.IonImageryProvider({ assetId: 4 });
        const imageryLayers = viewer.imageryLayers;
        const layer = imageryLayers.addImageryProvider(provider);
        // 获取 InfoBox 容器元素
        const infoBoxContainer = viewer.infoBox.container;
        const infoBox = viewer.infoBox;


        // 设置样式属性
        infoBoxContainer.style.color = 'white';
        // infoBoxContainer.style.bottom = '50%';
        infoBoxContainer.style.position = 'fixed';
        infoBoxContainer.style.left = '50%';
        infoBoxContainer.style.bottom = '6%';
        infoBoxContainer.style.transform = 'translateX(-80%)';
        infoBoxContainer.style.width = '1000px';
        infoBoxContainer.style.height = '200px';
        infoBoxContainer.style.borderRadius = '1px';
        infoBox.frame.setAttribute('style', 'background-color: lightgrey;');



  
        const terrainProvider = new window.Cesium.CesiumTerrainProvider({
          url: window.Cesium.IonResource.fromAssetId(1),
          requestWaterMask: true,
          requestVertexNormals: true,
        });
  
        viewer.terrainProvider = terrainProvider;
        if (viewer && viewer.imageryLayers) {
        let layer = null;
        if (this.basemap === 'basemap1') {
          viewer.imageryLayers.removeAll();
          layer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          viewer.imageryLayers.removeAll();
          layer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
      }
      
      var heatprovider = null;
      if(this.heatmap === 'Base') {
        heatprovider = null;
        viewer.imageryLayers.removeAll();
        var baselayer = null;
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
      } else if (this.heatmap === 'Comfort') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Comfort',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Convenience') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Convenience',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Economic_Vitality') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Economic_Vitality',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Elder_Friendly') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Elder_Friendly',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Livability') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Livability',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Mobility') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Mobility',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } else if (this.heatmap === 'Romance') {
        viewer.imageryLayers.removeAll();
        if (this.basemap === 'basemap1') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 4,
            })
          );
        } else if (this.basemap === 'basemap2') {
          // viewer.imageryLayers.removeAll();
          baselayer = viewer.imageryLayers.addImageryProvider(
            new window.Cesium.IonImageryProvider({
              assetId: 3,
            })
          );
        }
        heatprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:Romance',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(heatprovider);
      } 


      var borderprovider = new window.Cesium.WebMapServiceImageryProvider({
          url: 'http://localhost:8080/geoserver/ne/wms',
          layers: 'ne:hangzhou',
          parameters: {
            transparent: true,
            format: 'image/png',
            service: 'WMS',
          },
        });
        viewer.imageryLayers.addImageryProvider(borderprovider);

        // 根据 cesiumMode 的值设置场景模式
        if (this.cesiumMode === '2D') {
          viewer.scene.mode = window.Cesium.SceneMode.SCENE2D;
        } else if (this.cesiumMode === '3D') {
          viewer.scene.mode = window.Cesium.SceneMode.SCENE3D;
        }

        viewer.camera.flyTo({
        destination: window.Cesium.Cartesian3.fromDegrees(120.2, 30.3,5000)
       });

       

       // 创建一个圆
    let circle = viewer.entities.add({
      position: window.Cesium.Cartesian3.fromDegrees(120.2, 30.3, 0),
      name: 'circle at Hangzhou',
      ellipse: {
        semiMinorAxis: 300.0,
        semiMajorAxis: 270.0,
        material: new window.Cesium.Color(0.5, 0.5, 0.5, 0.4), // 中间透明
        outline: true, // 显示边框
        outlineColor: window.Cesium.Color.GREY, // 边框颜色为红色
        outlineWidth: 2.0, // 边框粗细
        description: undefined, // 这样设置可以防止点击实体时弹出信息框
      }
    });

    // 创建一个handler来处理鼠标和触摸事件
    let handler = new window.Cesium.ScreenSpaceEventHandler(viewer.canvas);

      // 开始拖动
    handler.setInputAction((click: any) => {
    let pickedObject = viewer.scene.pick(click.position);
  //viewer.scene.screenSpaceCameraController.enableRotate = false;
  //viewer.scene.screenSpaceCameraController.enableTranslate = false;
  //viewer.scene.screenSpaceCameraController.enableZoom = false;
  //let isDragging = false; // 添加标志变量
    if (window.Cesium.defined(pickedObject) && pickedObject.id === circle) {
      viewer.selectedEntity = null; // 这将阻止实体被选中，因此infobox不会显示
      viewer.scene.screenSpaceCameraController.enableTranslate = false;
      viewer.scene.screenSpaceCameraController.enableRotate = false;
      let startCartesian = viewer.camera.pickEllipsoid(
      click.position,
      viewer.scene.globe.ellipsoid
      );
    //这里先把鼠标点击圆时的鼠标位置和圆的位置记下
    let pos = circle.position.getValue(window.Cesium.JulianDate.now());
    let cartographic = window.Cesium.Cartographic.fromCartesian(pos);
    let x = cartographic.longitude
    let y = cartographic.latitude

    // 移动,throttle是节流函数
    handler.setInputAction(_.throttle((movement: any) => {
      viewer.dataSources.removeAll();
      let endCartesian = viewer.camera.pickEllipsoid(
        movement.endPosition,
        viewer.scene.globe.ellipsoid
      );

      if (startCartesian && endCartesian) {
        let startCartographic = window.Cesium.Cartographic.fromCartesian(startCartesian);
        let endCartographic = window.Cesium.Cartographic.fromCartesian(endCartesian);

        let deltaLon = endCartographic.longitude - startCartographic.longitude;
        let deltaLat = endCartographic.latitude - startCartographic.latitude;
        
        let pos = circle.position.getValue(window.Cesium.JulianDate.now());
        let cartographic = window.Cesium.Cartographic.fromCartesian(pos);

        cartographic.longitude = x + deltaLon;
        cartographic.latitude = y + deltaLat;

        circle.ellipse.semiMinorAxis = this.$store.state.radius
        circle.ellipse.semiMajorAxis = 0.9*this.$store.state.radius

        circle.position = new window.Cesium.ConstantPositionProperty(
          window.Cesium.Cartesian3.fromRadians(
            cartographic.longitude,
            cartographic.latitude,
            cartographic.height
          )
        );
      }
    },200), window.Cesium.ScreenSpaceEventType.MOUSE_MOVE);
  }
}, window.Cesium.ScreenSpaceEventType.LEFT_DOWN);

// 停止拖动
handler.setInputAction(() => {
  handler.removeInputAction(window.Cesium.ScreenSpaceEventType.MOUSE_MOVE);
  // 执行你的后端请求
  let position = circle.position.getValue(window.Cesium.JulianDate.now());
  let cartographicPosition = window.Cesium.Cartographic.fromCartesian(position);
  let center_lon = window.Cesium.Math.toDegrees(cartographicPosition.longitude);
  let center_lat = window.Cesium.Math.toDegrees(cartographicPosition.latitude);
  let radius = this.$store.state.radius;
  let head_class = this.$store.state.head_class
          
        // Dispatch the action to fetch the data
    
        this.$store.dispatch('fetchGeoJsonData', {
            center_lon,
            center_lat,
            radius,
            head_class
        }).then(() => {
            // Now that we have the data, create a new data source
            var dataSource = new window.Cesium.GeoJsonDataSource();

            // Use the freshly updated data
            var geoJsonData = this.$store.state.geoJsonData?.poiData;

            // If geoJsonData is not null or undefined, load it into the data source
            if (geoJsonData) {
                //console.log(geoJsonData);
                var geoJsonPromise = dataSource.load(geoJsonData);

                // Add the data source to the viewer
                viewer.dataSources.add(dataSource);

                // 处理加载完成的GeoJSON数据
                geoJsonPromise.then(function() {
                // 获取加载的实体集合
                var entities = dataSource.entities.values;

                // 设置每个实体的显示样式
                for (var i = 0; i < entities.length; i++) {
                    var entity = entities[i];
                    //console.log(entity.properties.head_class.getValue())
                    entity.billboard = undefined;
                    entity.height = 0
                     entity.point = {
                        pixelSize: 5,
                        outline: false
                        //color: window.Cesium.Color.RED
                     };
                     switch (entity.properties.head_class.getValue()) {
                  case '餐饮服务':
                      entity.point.color = window.Cesium.Color.RED;
                      break;
                  case '风景名胜':
                      entity.point.color = window.Cesium.Color.GREEN;
                      break;
                  case '公共设施':
                      entity.point.color = window.Cesium.Color.BLUE;
                      break;
                  case '购物服务':
                      entity.point.color = window.Cesium.Color.YELLOW;
                      break;
                  case '交通设施服务':
                      entity.point.color = window.Cesium.Color.ORANGE;
                      break;
                  case '金融保险服务':
                      entity.point.color = window.Cesium.Color.PURPLE;
                      break;
                  case '科教文化服务':
                      entity.point.color = window.Cesium.Color.LIME;
                      break;
                  case '生活服务':
                      entity.point.color = window.Cesium.Color.TURQUOISE;
                      break;
                  case '体育休闲服务':
                      entity.point.color = window.Cesium.Color.PINK;
                      break;
                  case '医疗保健服务':
                      entity.point.color = window.Cesium.Color.AQUA;
                      break;
                  case '政府机构及社会团体':
                      entity.point.color = window.Cesium.Color.DARKGOLDENROD;
                      break;
                  case '住宿服务':
                      entity.point.color = window.Cesium.Color.GOLD;
                      break;
                  default:
                      entity.point.color = window.Cesium.Color.WHITE;
                      break;
        }
                 // 如果GeoJSON数据包含其他属性，您也可以在这里设置它们
                }

                // 调整相机视图以显示所有实体
                //viewer.zoomTo(dataSource);
                })
            } 
        })
        
  // 启用地球的旋转
  viewer.scene.screenSpaceCameraController.enableRotate = true;
  viewer.scene.screenSpaceCameraController.enableTranslate = true;
  //viewer.scene.screenSpaceCameraController.enableZoom = true;
}, window.Cesium.ScreenSpaceEventType.LEFT_UP);
       
    },
    
    },
  })
  
    // watch: {
    //   cesiumMode(newValue) {
    //     // 当 cesiumMode 的值发生变化时重新设置场景模式
    //     this.initializeCesium();
    //   },
      
    // },


  //console.log(1)
  </script>

  
  <style scoped>
  #cesiumContainer {
    position: relative;
    top: 30px;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: auto;
  }
  </style>
  