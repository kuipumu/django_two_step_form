const path = require('path');
const webpack = require("webpack");
const TerserJSPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const FaviconsWebpackPlugin = require('favicons-webpack-plugin')

module.exports = {

  entry: {
    main: [
      './assets/src/js/main.js',
      './assets/src/scss/styles.scss'
    ],
  },

  plugins: [
    new MiniCssExtractPlugin({
      filename: 'css/[name].css',
      chunkFilename: 'css/[id].css',
    }),
    new FaviconsWebpackPlugin({
      logo: './assets/src/img/icons/logo.png',
      prefix: 'img/icons/'
    })
  ],

  optimization: {
    minimizer: [
      new TerserJSPlugin({}),
      new OptimizeCSSAssetsPlugin({})
    ],
  },

  module: {
    rules: [ {
      test: /\.scss$/,
      use: [
        {
          loader: MiniCssExtractPlugin.loader,
          options: {
            hmr: process.env.NODE_ENV === 'development',
            reloadAll: true
          },
        },
        {
          loader: 'css-loader',
          options: {
            url: false, sourceMap: true
          }
        },
        {
          loader: 'sass-loader',
          options: {
            sourceMap: true
          }
        },
      ],
    },
    {
      test: /\.(jpg|png)$/,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: './img/[name].[ext]',
          },
        },
      ]
    },
    {
      test: /\.(woff2|otf)$/,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: './fonts/[name].[ext]',
          },
        },
      ]
    },
    ]
  },

  output: {
    filename: "js/[name].js",
    path: path.resolve(__dirname, "assets/dist"),
    publicPath: "assets/",
  },

}