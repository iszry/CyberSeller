import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import axios from 'axios';

import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
import './assets/css/theme-green/index.css'; // 浅绿色主题
import './assets/css/icon.css';
import ECharts from 'vue-echarts'
import htmlToPdf from '@/htmlToPdf';
import JsPDF from 'jspdf';
import html2canvas from 'html2canvas';
// 使用 Vue.use() 方法就会调用工具方法中的install方法
Vue.use(htmlToPdf);


//使用

Vue.component('v-chart', ECharts)
Vue.config.productionTip = false;

/**
 * ElementUI配置并生效，全局使用
 */
Vue.use(ElementUI, {
  size: 'small'
});



/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
