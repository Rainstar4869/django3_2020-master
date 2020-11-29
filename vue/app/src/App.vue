<template>
	<div id="app">
		<img alt="Vue logo" src="./assets/logo.png">
		<HelloWorld msg="Welcome to HU"/>
		<!--<input type="file" @change="onFileChange" />-->
		<el-upload
				class="upload-demo"
				action="http://localhost/store/api/newproducts/"
				:on-preview="handlePreview"
				:on-remove="handleRemove"
				:headers="{'Authorization':accessToken}"
				:data="{'name':'lionhu'}"
				:file-list="fileList"
				list-type="picture">
			<el-button size="small" type="primary">点击上传</el-button>
			<div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
		</el-upload>
	</div>
</template>

<script>
    import * as API from './API';
    import {Upload, Button} from 'element-ui';
    import HelloWorld from './components/HelloWorld.vue';

    export default {
        name: 'App',
        components: {
            HelloWorld,
            'el-upload': Upload,
            'el-button': Button
        },
        computed: {
            accessToken() {
                return sessionStorage.getItem('accessToken') ? sessionStorage.getItem('accessToken') : "";
            }
        },
        data() {
            return {
                fileList: [],
                uploadimage: null,
                headers: {
                    'content-type': 'multipart/form-data',
                    'Authorization': this.access_token
                }
            };
        },
        methods: {
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePreview(file) {
                console.log(file);
            },
            submitUpload() {
                console.log(this.$refs.upload);
                this.$refs.upload.submit();
            },
            handleAvatarSuccess(res, file) {
                console.log(res)
                console.log(file)
                // this.imageUrl = URL.createObjectURL(file.raw);
                // if(res.result=='OK'){
                // this.sync_lastest_product(res.product);
                // this.imageUrl=''
                // }
            },
            beforeAvatarUpload(file) {
                const isJPG = file.type === 'image/jpeg';
                const isLt2M = file.size / 1024 / 1024 < 2;

                if (!isJPG) {
                    this.$message.error('上传头像图片只能是 JPG 格式!');
                }
                if (!isLt2M) {
                    this.$message.error('上传头像图片大小不能超过 2MB!');
                }
                return isJPG && isLt2M;
            },


            onFileChange(e) {
                const files = e.target.files || e.dataTransfer.files;
                this.img_name = files[0];
                const uploadParams = new FormData();

                uploadParams.append('name', "huhaiguang");
                uploadParams.append('file', this.img_name);

                API.fileUpload('/store/api/newproducts/', uploadParams).then(response => {
                    console.log(response)
                    // if (response.payload.status === 200) {
                    //     this.fileName = '';
                    //     this.previewSrc = '';
                    //     this.comment = '';
                    //     this.$refs.fileInput.lazyValue = '';
                    // }
                });


            },
        },
        mounted() {
            const params = new FormData();
            params.append('email', "huhaiguang@me.com");
            params.append('username', "admin");
            params.append('password', "lionhu");
            API.post('/apiauth/login/', params).then(response => {
                console.log(response.payload);
                if (response.payload.status === 200) {
                    sessionStorage.removeItem("accessToken");
                    sessionStorage.setItem('accessToken', `Bearer ${response.payload.data.tokens.access}`);
                    console.log(sessionStorage.getItem("accessToken"));
                }
            });

            API.get('/store/api/newproducts/')
                .then(response => {
                    console.log(response);
                    const files=response.payload.data;
                    var jsonData = [];
                    files.forEach(function (file) {
                        jsonData.push({'name':file.name,'url':"http://localhost:8000"+file.file});
                    });
                    console.log(jsonData);
                    this.fileList=jsonData;
                });


            // window.axios.post("/apiauth/login/", {
            //   "email": "huhaiguang@me.com",
            //   "username": "admin",
            //   "password": "lionhu"
            // }).then((res) => {
            //     console.log(res.data);
            // }).catch(function (error) {
            //   console.log(error)
            // });
        }
    }
</script>

<style>
	#app {
		font-family: Avenir, Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: #2c3e50;
		margin-top: 60px;
	}
</style>
