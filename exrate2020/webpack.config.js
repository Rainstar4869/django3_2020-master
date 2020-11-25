var path = require('path');
var webpack = require('webpack');
var VueLoaderPlugin = require('vue-loader/lib/plugin');
var BundleTracker = require('webpack-bundle-tracker');
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin'); // installed via npm
var ManifestPlugin = require('webpack-manifest-plugin');
const {CleanWebpackPlugin} = require("clean-webpack-plugin");
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// const SpeedMeasurePlugin = require("speed-measure-webpack-plugin");

// const smp = new SpeedMeasurePlugin();
var env = process.env.NODE_ENV;

const CopyPatterns = [
    {from: './vueapp/vue_django/src/assets', to: "./assets"}]


module.exports = {
    entry: {
        main: ['babel-polyfill', './vueapp/vue_django/src/main.js'],
        auth: ['babel-polyfill', './vueapp/vue_django/src/auth.js'],
    },
    devtool: '#eval-source-map',
    output: {
        filename: "[name].js",
        path: path.resolve('./staticfiles/bundles/'),
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
                test: /.(js|jsx)$/,
                include: [path.resolve(__dirname, 'src/js')],
                loader: 'babel-loader'
            },
            {
                test: /.js$/,
                include: [path.resolve(__dirname, 'src/js')],
                loader: 'eslint-loader'
            },
            {
                test: /.css$/,
                // include: [path.resolve(__dirname, 'src/styles')],
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        options: {
                            publicPath: '../'
                        }
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ]
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
                test: /.(gif|png|jpg)$/,
                include: [path.resolve(__dirname, 'src/images')],
                use: [
                    {
                        loader: 'url-loader',
                        // ↓ 追加
                        options: {
                            limit: 30720,
                            name: '[name].[ext]',
                            outputPath: './images/'
                        }
                        // ↑ 追加
                    }
                ]
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: [
                    'file-loader',
                ],
            },
        ]
    },
    plugins: [
        new webpack.ProgressPlugin(),
        new VueLoaderPlugin(),
        new ManifestPlugin(),
        new CopyWebpackPlugin({patterns: CopyPatterns}),
        new MiniCssExtractPlugin({filename: 'css/style.[chunkhash].css'}),
        new BundleTracker({
            path: __dirname,
            filename: './assets/webpack-stats.json',
        }),
        new CleanWebpackPlugin(),

    ],
    devServer: {
        open: true,//自动打开站点首页
        port: 8080,//把默认端口号8080修改成9000
        inline: true,//浏览器页面自动刷新
    },
    resolve: {
        alias: {
            'vue$': 'vue/dist/vue.esm.js'
        }
    },
    optimization: {
        // splitChunks: {
        //   name: 'vendor',
        //   chunks: 'initial',
        //  }
        minimizer: [new TerserPlugin()],
        splitChunks: {
            cacheGroups: {
                vendors: {
                    priority: -10,
                    test: /[\\/]node_modules[\\/]/
                }
            },
            minChunks: 1,
            minSize: 30000,
            name: 'vendor',
            chunks: 'initial',
        }
    }
};