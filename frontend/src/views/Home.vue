<template>
  <BlogHeader/>
  <ArticleList/>
  <BlogFooter/>
</template>

<script>
import BlogHeader from '@/components/BlogHeader.vue'
import BlogFooter from '@/components/BlogFooter.vue'
import ArticleList from '@/components/ArticleList.vue'

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'Home',
  components: {BlogHeader, BlogFooter, ArticleList}
}
</script>

