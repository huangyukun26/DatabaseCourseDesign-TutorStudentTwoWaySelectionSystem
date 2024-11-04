const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.(png|jpe?g|gif)$/i,
          use: [
            {
              loader: 'file-loader',
              options: {
                // 这里可以添加file-loader的配置选项
                name: '[name].[ext]', // 保留原始文件结构
                esModule: false, // 确保图片可以正确显示
              },
            },
          ],
        },
      ],
    },
  },
})
