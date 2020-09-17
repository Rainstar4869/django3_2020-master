var path = require('path');
var webpack = require('webpack');
var VueLoaderPlugin = require('vue-loader/lib/plugin');
var BundleTracker = require('webpack-bundle-tracker');
const HtmlWebpackPlugin = require('html-webpack-plugin')


var ManifestPlugin = require('webpack-manifest-plugin');
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const SpeedMeasurePlugin = require("speed-measure-webpack-plugin");

// const smp = new SpeedMeasurePlugin();
var env = process.env.NODE_ENV;

module.exports ={
  entry:{
    main:['babel-polyfill', './vueapp/vue_django/src/main.js'],
  },
  devtool: '#eval-source-map',
  output: {
    filename: "[name].js",
    // filename: "[name]-[hash].js",
    // chunkFilename: '[name].bundle.js',
    path: path.resolve('./staticfiles/bundles/'),
    // publicPath: 'http://localhost:8080/static/',
  },
  watch: true,
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000,
    ignored: /node_modules/
  },
  module: {
        rules: [
	        {
    			    test: /\.vue$/,
    			    loader: 'vue-loader',
    			    options: {
    			        loaders: {
    			            'scss': [
    			                'vue-style-loader',
    			                'css-loader',
    			                'sass-loader'
    			            ],
    			            'sass': [
    			                'vue-style-loader',
    			                'css-loader',
    			                'sass-loader?indentedSyntax'
    			            ]
    			        }
    			    }
    			},
	        {
    			    test: /\.js$/,
    			    loader: 'babel-loader',
    			    exclude: /node_modules/,
              options:{
                plugins:['syntax-dynamic-import']
              },
    			},
          {
              test: /\.css$/,
              use: [
                  'vue-style-loader',
                  'css-loader'
              ],
          },
          {
              test: /\.scss$/,
              use: [
                  'vue-style-loader',
                  'css-loader',
                  'sass-loader'
              ],
          },
          {
              test: /\.sass$/,
              use: [
                  'vue-style-loader',
                  'css-loader',
                  'sass-loader?indentedSyntax'
              ],
          },
          {
            test: /\.(otf|eot|svg|ttf|woff|woff2)(\?.+)?$/,
            loader: 'url-loader'
          },
         {
           test: /\.(png|svg|jpg|gif)$/,
           use: [
             'file-loader',
           ],
         },
        ]
    },
  plugins:[
  	new VueLoaderPlugin(),
    new ManifestPlugin(),
    // new BundleAnalyzerPlugin({
    //   analyzerPort:18888
    // }),
  	new BundleTracker({filename: './webpack-stats.json'}),
    new CleanWebpackPlugin(),

  ],
  devServer: {
    	open:true,//自动打开站点首页
        port:8080,//把默认端口号8080修改成9000
        inline:true,//浏览器页面自动刷新
  },
  resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
  },
  optimization: {
        splitChunks: {
          name: 'vendor',
          chunks: 'initial',
         }
     }
};