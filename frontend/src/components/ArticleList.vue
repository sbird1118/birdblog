<template>
    <div v-for="article in info.results" v-bind:key="article.url" id="articles">
        <div class="grid" :style="gridStyle(article)">
            <div class="image-container">
                <img :src="imageIfExists(article)" alt="" class="image">
            </div>
            <div>
                <!-- 文章标签 -->
                <div>
                    <span
                    v-if="article.category !== null"
                    class="category"
                    >
                        {{article.category.name}}
                    </span>
                    <span 
                        v-for="tag in article.tags" 
                        v-bind:key="tag" 
                        class="tag"
                    >
                        {{ tag }}
                    </span>

                </div>
                <div class="a-title-container">
                    <!-- 文章标题 -->
                    <router-link
                        :to="{ name: 'ArticleDetail', params: { id: article.id }}"
                        class="article-title"
                    >
                        {{ article.title }}
                    </router-link>
                    <!-- 调用 vue-router 不再需要常规的 <a> 标签了，而是 <router-link> 。
                    :to 属性指定了跳转位置，注意看动态参数 id 是如何传递的。
                    在 Vue 中，属性前面的冒号 : 表示此属性被”绑定“了。”绑定“的对象可以是某个动态的参数
                    （比如这里的 id 值），也可以是 Vue 所管理的 data，也可以是 methods。
                    总之，看到冒号就要明白这个属性后面跟着个变量或者表达式，没有冒号就是普通的字符串。
                    冒号 : 实际上是 v-bind: 的缩写。 -->
                </div>

                <div>{{ formatted_time(article.create_time) }}</div>
            </div>
        </div>
    </div>

    <!-- 翻页 -->
    <div id="paginator">
        <span v-if="is_page_exists('previous')">
            <router-link :to="get_path('previous')">
                上一页
            </router-link>
        </span>
        <span class="current-page">
            {{ get_page_param('current') }}
        </span>
        <span v-if="is_page_exists('next')">
            <router-link :to="get_path('next')">
                下一页
            </router-link>
        </span>
        <!-- is_page_exists(...) 用于确认需要跳转的页面是否存在，如果不存在那就不渲染对应的跳转标签。
            它的唯一参数用于确定页面的方向（当前页、上一页或下一页？）。
            get_page_param(...) 用于获取页码，它的参数作用也类似，基本上就是个标记。
            router-link 通过 query 传递参数，看来还是挺方便的 -->
    </div>
</template>

<script>
    // import axios from 'axios'
    import { ref } from 'vue'
    import { useRoute } from 'vue-router'
    import getArticleData from '@/composables/getArticleData'
    import pagination from '@/composables/pagination'
    import articleGrid from '@/composables/articleGrid'
    import formattedTime from '@/composables/formattedTime'
    export default {
        // 组合式 APi 入口
        setup() {
            const info = ref('');
            // 创建路由
            const route = useRoute();

            // 获取文章列表数据的方法
            // const get_article_data = function () {
            //     let url = '/api/blog';
            //     let params = new URLSearchParams();
            //     params.appendIfExists('page', route.query.page);
            //     params.appendIfExists('search', route.query.search);

            //     const paramsString = params.toString();
            //     if (paramsString.charAt(0) !== '') {
            //         url += '/?' + paramsString
            //     }
            //     axios
            //         .get(url)
            //         .then(response => (info.value = response.data))
            // };
            // onMounted(get_article_data);
            // watch(route, get_article_data);
            const {
                is_page_exists,
                get_page_param,
                get_path
            } = pagination(info, route);
            getArticleData(info, route);

            // 调整页面外观
            const {
                imageIfExists,
                gridStyle
            } = articleGrid();

            // 日期格式化
            const formatted_time = formattedTime;
            // 需要注入到 Vue 实例的数据、方法等
            return {
                info,
                is_page_exists,
                get_page_param,
                get_path,
                imageIfExists,
                gridStyle,
                formatted_time
            }
        },

        name: 'App',
        // data: function () {
        //     return {
        //         info: ''
        //     }
        // },

        // mounted() {
        //     this.get_article_data()
        // },

        methods: {
            // imageIfExists(article) {
            //     if (article.avatar) {
            //         return article.avatar.content
            //     }
            // },
            // gridStyle(article) {
            //     if (article.avatar) {
            //         return {
            //             display: 'grid',
            //             gridTemplateColumns: '1fr 4fr'
            //         }
            //     }
            // },
            // formatted_time: function (iso_date_string) {
            //     const date = new Date(iso_date_string);
            //     return date.toLocaleDateString()
            // },
            // // 判断页面是否存在
            // is_page_exists(direction) {
            //     if (direction === 'next') {
            //         return this.info.next !== null
            //     }
            //     return this.info.previous !== null
            // },
            // // 获取页码
            // get_page_param: function (direction) {
            //     try {
            //         let url_string;
            //         switch (direction) {
            //             case 'next':
            //                 url_string = this.info.next;
            //                 break;
            //             case 'previous':
            //                 url_string = this.info.previous;
            //                 break;
            //             default:
            //                 return this.$route.query.page
            //         }

            //         const url = new URL(url_string);
            //         return url.searchParams.get('page')
            //     }
            //     catch (err) {
            //         return
            //     }
            // },
            // get_path: function (direction) {
            //         let url = '';

            //         try {
            //             switch (direction) {
            //                 case 'next':
            //                     if (this.info.next !== undefined) {
            //                         url += (new URL(this.info.next)).search
            //                     }
            //                     break;
            //                 case 'previous':
            //                     if (this.info.previous !== undefined) {
            //                         url += (new URL(this.info.previous)).search
            //                     }
            //                     break;
            //             }
            //         }
            //         catch { return url }

            //         return url
            //     },

            // 获取文章列表数据
            // get_article_data: function () {
            //         let url = '/api/blog';

            //         let params = new URLSearchParams();
            //         // 注意 appendIfExists 方法是原生没有的
            //         // 原生只有 append 方法，但此方法不能判断值是否存在
            //         params.appendIfExists('page', this.$route.query.page);
            //         params.appendIfExists('search', this.$route.query.search);

            //         const paramsString = params.toString();
            //         if (paramsString.charAt(0) !== '') {
            //             url += '/?' + paramsString
            //         }

            //         axios
            //             .get(url)
            //             .then(response => (this.info = response.data))
                
            //     }
            // },
            // watch: {
            //     // 监听路由是否有变化
            //     $route() {
            //         this.get_article_data()
            //     }
            // }
            }
    }
</script>
<!-- "scoped" 使样式仅在当前组件生效 -->
<style scoped>
    .image {
        width: 180px;
        border-radius: 10px;
        box-shadow: darkslategrey 0 0 12px;
    }
    .image-container {
        width: 200px;
    }
    .grid {
        padding-bottom: 10px;
    }
    .category {
    padding: 5px 10px 5px 10px;
    margin: 5px 5px 5px 0;
    font-family: Georgia, Arial, sans-serif;
    font-size: small;
    background-color: darkred;
    color: whitesmoke;
    border-radius: 15px;
  }

    #articles {
        padding: 10px;
    }

    .article-title {
        font-size: large;
        font-weight: bolder;
        color: black;
        text-decoration: none;
        padding: 5px 0 5px 0;
    }

    .tag {
        padding: 2px 5px 2px 5px;
        margin: 5px 5px 5px 0;
        font-family: Georgia, Arial, sans-serif;
        font-size: small;
        background-color: #4e4e4e;
        color: whitesmoke;
        border-radius: 5px;
    }

    #paginator {
        text-align: center;
        padding-top: 50px;
    }

    a {
        color: black;
    }

    .current-page {
        font-size: x-large;
        font-weight: bold;
        padding-left: 10px;
        padding-right: 10px;
    }
</style>