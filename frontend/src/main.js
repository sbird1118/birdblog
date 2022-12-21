import router from './router'
import {createApp} from 'vue'
import App from './App.vue'

URLSearchParams.prototype.appendIfExists = function (key, value) {
    if (value !== null && value !== undefined) {
        this.append(key, value)
    }
};

createApp(App).mount('#app');

createApp(App).use(router).mount('#app');