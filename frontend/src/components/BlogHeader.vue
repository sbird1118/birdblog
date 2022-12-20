<template>
    <div id="header">
        <div class="grid">
            <div></div>
            <h1>0768顾长生</h1>
            <SearchButton/>
        </div>
        <hr>
       
        <div class="login">
            <div v-if="hasLogin">
                <div class="dropdown">
                    <button class="dropbtn">欢迎, {{username}}!</button>
                    <div class="dropdown-content">
                        <router-link :to="{ name: 'UserCenter', params: { username: username }}">用户中心</router-link>
                        <router-link 
                        :to="{ name: 'ArticleCreate' }" 
                        v-if="isSuperuser"
                        >
                            发表文章
                        </router-link>
                    </div>
                </div>
            </div>
            <div v-else>
                <router-link to="/login" class="login-link">登录</router-link>
            </div>
        </div>


    </div>
</template>
<script>
    // import axios from 'axios'
    import SearchButton from '@/components/SearchButton.vue'
    import authorization from '@/utils/authorization'

    export default {
        name: 'BlogHeader',
        components: {SearchButton},
        data: function () {
            return {
                username: '',
                hasLogin: false,
                isSuperuser: JSON.parse(localStorage.getItem('isSuperuser.myblog')),
            }
        },

        methods: {
            refresh() {
                this.username = localStorage.getItem('username.myblog');
            }
        },

        mounted() {
            // const that = this;
            // const storage = localStorage;
            // // 过期时间
            // const expiredTime = Number(storage.getItem('expiredTime.myblog'));
            // // 当前时间
            // const current = (new Date()).getTime();
            // // 刷新令牌
            // const refreshToken = storage.getItem('refresh.myblog');
            // // 用户名
            // that.username = storage.getItem('username.myblog');

            // // 初始 token 未过期
            // if (expiredTime > current) {
            //     that.hasLogin = true;
            // }
            // // 初始 token 过期
            // // 如果有刷新令牌则申请新的token
            // else if (refreshToken !== null) {
            //     axios
            //         .post('/api/token/refresh/', {
            //             refresh: refreshToken,
            //         })
            //         .then(function (response) {
            //             const nextExpiredTime = Date.parse(response.headers.date) + 60000;

            //             storage.setItem('access.myblog', response.data.access);
            //             storage.setItem('expiredTime.myblog', nextExpiredTime);
            //             storage.removeItem('refresh.myblog');

            //             that.hasLogin = true;
            //         })
            //         .catch(function () {
            //             // .clear() 清空当前域名下所有的值
            //             // 慎用
            //             storage.clear();
            //             that.hasLogin = false;
            //         })
            // }
            // // 无任何有效 token
            // else {
            //     storage.clear();
            //     that.hasLogin = false;
            // }
            // 千言万语汇成此句
            authorization().then((data) => [this.hasLogin, this.username] = data);

        }
}
</script>
<style scoped>
/* 样式来源: https://www.runoob.com/css/css-dropdowns.html* /
    /* 下拉按钮样式 */
    .dropbtn {
        background-color: mediumslateblue;
        color: white;
        padding: 8px 8px 30px 8px ;
        font-size: 16px;
        border: none;
        cursor: pointer;
        height: 16px;
        border-radius: 5px;
    }
    /* 容器 <div> - 需要定位下拉内容 */
    .dropdown {
        position: relative;
        display: inline-block;
    }
    /* 下拉内容 (默认隐藏) */
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 120px;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        text-align: center;
    }
    /* 下拉菜单的链接 */
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }
    /* 鼠标移上去后修改下拉菜单链接颜色 */
    .dropdown-content a:hover {
        background-color: #f1f1f1
    }
    /* 在鼠标移上去后显示下拉菜单 */
    .dropdown:hover .dropdown-content {
        display: block;
    }
    /* 当下拉内容显示后修改下拉按钮的背景颜色 */
    .dropdown:hover .dropbtn {
        background-color: darkslateblue;
    }
</style>
<style scoped>
    #header {
        text-align: center;
        margin-top: 20px;
    }
    .grid {
        display: grid;
        grid-template-columns: 1fr 4fr 1fr;
    }

    .login-link {
        color: black;
    }

    .login {
        text-align: right;
        padding-right: 5px;
    }
</style>