// import './assets/main.css'

import {createApp} from 'vue'
import App from './App.vue'
import {library} from '@fortawesome/fontawesome-svg-core';
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

// import { faUser } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios'
import VueAxios from 'vue-axios'
import {fas} from '@fortawesome/free-solid-svg-icons';
import {far} from '@fortawesome/free-regular-svg-icons';
import {fab} from '@fortawesome/free-brands-svg-icons';
import VueClipBoard from 'vue-clipboard2'
import fontawesome from '@fortawesome/fontawesome'
// import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
import solid from '@fortawesome/fontawesome-free-solid'
import regular from '@fortawesome/fontawesome-free-regular'
import brands from '@fortawesome/fontawesome-free-brands'
import hljs from "highlight.js";
// import "highlight.js/styles/a11y-light.css";
import showdown from "showdown";


const app = createApp(App);
app.config.productionTip = false
app.use(VueClipBoard)

app.use(showdown);
// 代码高亮
app.directive("highlight", function (el) {
    let blocks = el.querySelectorAll("pre code");
    blocks.forEach((block) => {
        hljs.highlightBlock(block);
    })
})

//use：将第三方模块 注入到Vue实例对象中的方法
app.use(VueAxios, axios)
// app.use(fetchEventSource, fetchEventSource)
app.config.productionTip = false
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');

// app.component('font-awesome-icon', FontAwesomeIcon)
fontawesome.library.add(solid)
fontawesome.library.add(regular)
fontawesome.library.add(brands)


library.add(fas, far, fab)