import Vue from 'vue'
import App from './App'

import store from './store'
import 'store/font.less'

Vue.config.devtools = true
Vue.config.productionTip = false

Vue.prototype.$store = store

App.mpType = 'app'

const app = new Vue({
    store,
    ...App
})
app.$mount()
