const MODE = "development";
var webpack = require('webpack');
// ソースマップの利用有無(productionのときはソースマップを利用しない)
const enabledSourceMap = MODE === "development";
const {VueLoaderPlugin} = require("vue-loader");
const CopyWebpackPlugin = require('copy-webpack-plugin'); // installed via npm
var ManifestPlugin = require('webpack-manifest-plugin');
const {CleanWebpackPlugin} = require("clean-webpack-plugin");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');

// プラグイン
// js最適化
const TerserPlugin = require('terser-webpack-plugin');


// const CopyPatterns = [
//     {from: './dist/js', to: "../../../lionhu"}];

module.exports = {
    // エントリーポイント(メインのjsファイル)
    entry: {
        main: ['babel-polyfill', './src/main.js'],
        auth: ['babel-polyfill', './src/auth.js']
    },
    // ファイルの出力設定
    output: {
        // 出力先(絶対パスでの指定必須)
        path: path.resolve(__dirname, 'dist/js'),
        // 出力ファイル名
        filename: "[name].js",
    },
    mode: MODE,
    // ソースマップ有効
    devtool: 'source-map',
    // ローダーの設定
    module: {
        rules: [
            {
                test: /\.css$/,
                // use: ["vue-style-loader", "css-loader"]
                use:[
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
                test: /\.vue$/,
                loader: "vue-loader"
            },
                // ローダーの対象 // 拡張子 .js の場合
            {
                test: /\.js$/,
                // ローダーの処理対象から外すディレクトリ
                exclude: /node_modules/,
                // Babel を利用する
                loader: "babel-loader",
                // Babel のオプションを指定する
                options: {
                    presets: [
                        // プリセットを指定することで、ES2019 を ES5 に変換
                        "@babel/preset-env"
                    ]
                }
            },
                // 対象となるファイルの拡張子
            {
                test: /\.(gif|png|jpe?g|svg|eot|wof|woff|woff2|ttf)$/i,
                use: [
                    {
                        //画像をData URI（Base64）に変換するローダー
                        loader: 'url-loader',
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
        ]
    },
    // import 文で .ts ファイルを解決するため
    resolve: {
        // Webpackで利用するときの設定
        alias: {
            vue$: "vue/dist/vue.esm.js"
        },
        extensions: ["*", ".js", ".vue", ".json"]
    },
    plugins: [
        new webpack.ProgressPlugin(),
        // Vueを読み込めるようにするため
        new VueLoaderPlugin(),
        // new CopyWebpackPlugin(CopyPatterns),
        new MiniCssExtractPlugin({filename: 'css/vue_style.css'}),
        new ManifestPlugin(),
        new CleanWebpackPlugin(),
    ],
    // mode:puroductionでビルドした場合のファイル圧縮
    optimization: {
        minimizer: [
            // jsファイルの最適化
            new TerserPlugin({
                // すべてのコメント削除
                extractComments: 'all',
                // console.logの出力除去
                terserOptions: {
                    compress: {drop_console: true}
                },
            }),
        ],
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
    },
    // js, css, html更新時自動的にブラウザをリロード
    devServer: {
        // サーバーの起点ディレクトリ
        // contentBase: "dist",
        // バンドルされるファイルの監視 // パスがサーバー起点と異なる場合に設定
        // publicPath: '/dist/',
        publicPath: '/dist/js/',
        //コンテンツの変更監視をする
        watchContentBase: true,
        // 実行時(サーバー起動時)ブラウザ自動起動
        open: true,
        // 自動で指定したページを開く
        openPage: "index.html",
        //　同一network内からのアクセス可能に
        host: "0.0.0.0"
    }
};