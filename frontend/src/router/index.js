import {createWebHistory, createRouter} from "vue-router";
import Home from "@/views/Home.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";
import Login from "@/views/Login.vue"
import UserCenter from "@/views/UserCenter.vue"
import ArticleCreate from "@/views/ArticleCreate.vue"
import ArticleEdit from "@/views/ArticleEdit.vue"
const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
    },
    {
        path: "/article/:id",
        name: "ArticleDetail",
        component: ArticleDetail
    },
    {
        path: "/login",
        name: "Login",
        component: Login
    },
    {
        path: "/user/:username",
        name: "UserCenter",
        component: UserCenter
    },
    {
        path: "/article/create",
        name: "ArticleCreate",
        component: ArticleCreate
    },
    {
        path: "/article/edit/:id",
        name: "ArticleEdit",
        component: ArticleEdit
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
/*列表 routes 定义了所有需要挂载到路由中的路径，成员为路径 url 、路径名和路径的 vue 对象。
详情页面的动态路由采用冒号 :id 的形式来定义。
接着就用 createRouter() 创建 router。参数里的 history 定义具体的路由形式，
createWebHashHistory() 为哈希模式（具体路径在 # 符号后面）；
createWebHistory() 为 HTML5 模式（路径中没有丑陋的 # 符号），此为推荐模式，但是部署时需要额外的配置。 */