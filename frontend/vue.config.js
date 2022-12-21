const {defineConfig} = require('@vue/cli-service')
module.exports = {
    chainWebpack: config => {
        config
            .plugin('html')
            .tap(args => {
                args[0].title = '0768顾长生的个人博客'
                return args
            })
    }
}
module.exports = defineConfig({
    transpileDependencies: true
})
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: `http://127.0.0.1:8000/api`,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
};
